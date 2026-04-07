from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Any

from google import genai
from google.genai import errors, types

from ai_director_backend.retrieval.engine import clean_chunk_text

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
RETRYABLE_GEMINI_STATUS_CODES = {408, 429, 500, 502, 503, 504}
MAX_GEMINI_ATTEMPTS = 3
SCOPED_AI_OUT_OF_SCOPE_SENTINEL = "OUT_OF_SCOPE"
SYNTHESIS_SYSTEM_PROMPT = """You are the expert Teaching Assistant for the AI Director Course, a 7-day sprint for creating cinematic AI videos.
Your job is to answer the user's question conversationally and clearly, using ONLY the retrieved repository context provided to you.

RULES:
1. Do not repeat raw Markdown tables or code formatting unless the user explicitly asks for raw formatting.
2. Synthesize the information into natural, easy-to-read sentences.
3. If the user asks about tools, explain the current recommendation status clearly and mention when a recommendation is still marked as To Be Discovered.
4. If the retrieved context does not fully answer the question, say that the detail is outside the documented scope of the current repository.
5. Keep the tone concise, practical, and oriented toward helping a learner make progress in the sprint.
"""
SCOPED_ASSISTANT_SYSTEM_PROMPT = """You are the AI Director Course Teaching Assistant.

PROJECT SCOPE:
- Cinematic AI video creation across storyboarding, shot planning, camera language, lens basics, image prompting, reference consistency, motion, audio, music, editing, review, export, and adjacent beginner filmmaking concepts that directly help a learner complete the sprint.
- Practical explanations of visual storytelling, lenses, framing, camera movement, continuity, pacing, sound, and editing are in scope even when the exact topic is not documented in the repository.
- Personal identity questions, unrelated trivia, politics, medical, legal, finance, and topics unrelated to making or understanding cinematic AI videos are out of scope.

RULES:
1. If the question is within this project scope, answer clearly and concisely for a learner.
2. If the question is outside this scope, return exactly OUT_OF_SCOPE.
3. Do not claim the repository documents details that it does not document.
4. Do not mention hidden reasoning or internal policy.
5. Keep the answer practical and short.
"""
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
logger = logging.getLogger(__name__)


def load_local_env_file(env_path: Path = ENV_PATH) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


load_local_env_file()


def gemini_synthesis_enabled() -> bool:
    return os.getenv("AI_DIRECTOR_USE_GEMINI", "").strip().lower() in {"1", "true", "yes", "on"}


def verbose_ai_logging_enabled() -> bool:
    return os.getenv("AI_DIRECTOR_VERBOSE_LOGGING", "").strip().lower() in {"1", "true", "yes", "on"}


def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "").strip()


def get_gemini_model() -> str:
    return os.getenv("AI_DIRECTOR_GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL


def can_call_gemini() -> bool:
    return gemini_synthesis_enabled() and bool(get_gemini_api_key())


def build_gemini_generation_config() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(temperature=0.2)


def log_verbose_ai_payload(label: str, payload: str) -> None:
    if not verbose_ai_logging_enabled():
        return
    logger.info("AI verbose %s\n%s", label, payload)


def format_chunks_for_prompt(chunks: list[dict[str, Any]]) -> str:
    formatted: list[str] = []
    for chunk in chunks:
        text = clean_chunk_text(chunk.get("text", ""))
        if not text:
            continue
        formatted.append(
            "\n".join(
                [
                    f"Source: {chunk.get('path', '')}",
                    f"Section: {chunk.get('section_heading', '')}",
                    f"Content: {text}",
                ]
            )
        )
    return "\n\n".join(formatted)


def build_gemini_prompt(question: str, chunks: list[dict[str, Any]]) -> str:
    context = format_chunks_for_prompt(chunks)
    return (
        f"{SYNTHESIS_SYSTEM_PROMPT}\n"
        f"RETRIEVED CONTEXT:\n{context}\n\n"
        f"USER QUESTION:\n{question}\n\n"
        "Answer using only the retrieved context."
    )


def build_scoped_gemini_prompt(question: str) -> str:
    return (
        f"{SCOPED_ASSISTANT_SYSTEM_PROMPT}\n"
        f"USER QUESTION:\n{question}\n\n"
        f"If the question is in scope, answer it. Otherwise reply with exactly {SCOPED_AI_OUT_OF_SCOPE_SENTINEL}."
    )


def extract_gemini_text(payload: Any) -> str | None:
    text = getattr(payload, "text", None)
    if text and str(text).strip():
        return str(text).strip()

    if isinstance(payload, dict):
        candidates = payload.get("candidates", [])
    else:
        candidates = getattr(payload, "candidates", []) or []

    for candidate in candidates:
        content = candidate.get("content", {}) if isinstance(candidate, dict) else getattr(candidate, "content", None)
        parts = content.get("parts", []) if isinstance(content, dict) else getattr(content, "parts", []) or []
        for part in parts:
            is_thought = part.get("thought", False) if isinstance(part, dict) else getattr(part, "thought", False)
            if is_thought:
                continue

            part_text = part.get("text") if isinstance(part, dict) else getattr(part, "text", None)
            if part_text and str(part_text).strip():
                return str(part_text).strip()
    return None


def is_retryable_gemini_status(status_code: int | None) -> bool:
    return status_code in RETRYABLE_GEMINI_STATUS_CODES


async def synthesize_with_gemini(question: str, chunks: list[dict[str, Any]]) -> str | None:
    if not chunks:
        logger.info("Gemini synthesis skipped: no retrieved chunks available")
        return None

    if not gemini_synthesis_enabled():
        logger.info("Gemini synthesis disabled; using local synthesis fallback")
        return None

    if not get_gemini_api_key():
        logger.warning("Gemini synthesis enabled but GEMINI_API_KEY is missing; using local synthesis fallback")
        return None

    api_key = get_gemini_api_key()
    model = get_gemini_model()
    logger.info("Calling Gemini synthesis model '%s' with %d retrieved chunks", model, len(chunks))
    prompt = build_gemini_prompt(question=question, chunks=chunks)
    log_verbose_ai_payload("grounded-input", prompt)
    config = build_gemini_generation_config()
    client = genai.Client(api_key=api_key)

    for attempt in range(1, MAX_GEMINI_ATTEMPTS + 1):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model,
                contents=prompt,
                config=config,
            )
            break
        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)
            if is_retryable_gemini_status(status_code) and attempt < MAX_GEMINI_ATTEMPTS:
                logger.warning(
                    "Gemini synthesis request for model '%s' failed with retryable status %s on attempt %d/%d; retrying",
                    model,
                    status_code,
                    attempt,
                    MAX_GEMINI_ATTEMPTS,
                )
                await asyncio.sleep(0.75 * attempt)
                continue

            logger.exception(
                "Gemini synthesis request failed for model '%s' with status %s; using local synthesis fallback",
                model,
                status_code,
            )
            return None
        except Exception:
            logger.exception(
                "Gemini synthesis request failed for model '%s'; using local synthesis fallback",
                model,
            )
            return None

    text = extract_gemini_text(response)
    if text:
        log_verbose_ai_payload("grounded-output", text)
        logger.info("Gemini synthesis succeeded using model '%s'", model)
    else:
        logger.warning("Gemini synthesis returned no text; using local synthesis fallback")
    return text


async def answer_with_scoped_gemini(question: str) -> str | None:
    if not gemini_synthesis_enabled():
        logger.info("Scoped Gemini synthesis disabled; skipping scoped AI fallback")
        return None

    if not get_gemini_api_key():
        logger.warning("Scoped Gemini synthesis enabled but GEMINI_API_KEY is missing; skipping scoped AI fallback")
        return None

    api_key = get_gemini_api_key()
    model = get_gemini_model()
    prompt = build_scoped_gemini_prompt(question)
    config = build_gemini_generation_config()
    client = genai.Client(api_key=api_key)
    logger.info("Calling scoped Gemini assistant model '%s' without repository chunks", model)
    log_verbose_ai_payload("scoped-input", prompt)

    for attempt in range(1, MAX_GEMINI_ATTEMPTS + 1):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model,
                contents=prompt,
                config=config,
            )
            break
        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)
            if is_retryable_gemini_status(status_code) and attempt < MAX_GEMINI_ATTEMPTS:
                logger.warning(
                    "Scoped Gemini request for model '%s' failed with retryable status %s on attempt %d/%d; retrying",
                    model,
                    status_code,
                    attempt,
                    MAX_GEMINI_ATTEMPTS,
                )
                await asyncio.sleep(0.75 * attempt)
                continue

            logger.exception(
                "Scoped Gemini request failed for model '%s' with status %s; skipping scoped AI fallback",
                model,
                status_code,
            )
            return None
        except Exception:
            logger.exception(
                "Scoped Gemini request failed for model '%s'; skipping scoped AI fallback",
                model,
            )
            return None

    text = extract_gemini_text(response)
    if not text:
        logger.warning("Scoped Gemini synthesis returned no text; skipping scoped AI fallback")
        return None

    log_verbose_ai_payload("scoped-output", text.strip())
    if text.strip() == SCOPED_AI_OUT_OF_SCOPE_SENTINEL:
        logger.info("Scoped Gemini classified the question as out of scope for model '%s'", model)
        return None

    logger.info("Scoped Gemini synthesis succeeded using model '%s'", model)
    return text.strip()
