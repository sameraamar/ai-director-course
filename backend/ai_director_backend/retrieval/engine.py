from __future__ import annotations

from collections import defaultdict
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from typing import Any

from ai_director_backend.ingestion.pipeline import build_ingestion_index, enumerate_markdown_files, write_ingestion_index

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
INDEX_PATH = Path(__file__).resolve().parents[2] / ".artifacts" / "ingestion" / "index.json"
REPO_ROOT = Path(__file__).resolve().parents[3]
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "be",
    "by",
    "do",
    "for",
    "from",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "know",
    "me",
    "my",
    "name",
    "of",
    "on",
    "or",
    "should",
    "that",
    "the",
    "to",
    "what",
    "when",
    "with",
    "you",
    "your",
}
TABLE_SEPARATOR_PATTERN = re.compile(r"^\|\s*[-: ]+\|")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
PERSONAL_QUERY_PATTERNS = [
    re.compile(r"\bmy name\b"),
    re.compile(r"\bwho am i\b"),
    re.compile(r"\bdo you know (me|my name)\b"),
    re.compile(r"\bdo you remember (me|my name)\b"),
    re.compile(r"\bwhat is my name\b"),
]
WORKFLOW_KEYWORDS = {
    "Storyboarding / Planning": {"storyboard", "storyboarding", "planning", "plan", "blueprint", "shots", "shot"},
    "Image Generation": {"image", "images", "frame", "frames", "prompt", "prompts", "cref", "sref"},
    "Image-to-Video": {"video", "motion", "camera", "pan", "dolly", "tilt", "animation", "image-to-video"},
    "Voice / Dialogue": {"voice", "dialogue", "dialog", "narration", "voiceover", "speech"},
    "Lip Sync": {"lip", "lipsync", "lip-sync", "mouth", "sync"},
    "Music": {"music", "track", "soundtrack", "score"},
    "Sound Effects / Foley": {"foley", "sound", "effects", "sfx", "whoosh", "ambient", "ambience"},
    "Editing / Finishing": {"edit", "editing", "editor", "capcut", "timeline", "finish", "finishing", "cut"},
    "Upscaling": {"upscale", "upscaling", "resolution", "4k", "sharpen"},
}
COURSE_DOMAIN_KEYWORDS = set().union(*WORKFLOW_KEYWORDS.values()) | {
    "course",
    "day",
    "days",
    "lesson",
    "lessons",
    "learner",
    "learners",
    "sprint",
    "tool",
    "tools",
    "vault",
    "clip",
    "clips",
}


def tokenize(text: str) -> list[str]:
    return [token for token in TOKEN_PATTERN.findall(text.lower()) if token not in STOP_WORDS]


def build_bigrams(tokens: list[str]) -> set[tuple[str, str]]:
    return {(tokens[index], tokens[index + 1]) for index in range(len(tokens) - 1)}


def extract_day_number(text: str) -> str | None:
    match = re.search(r"\bday\s+([1-7])\b", text.lower())
    if match:
        return match.group(1)
    return None


def normalize_for_personal_detection(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def has_identity_like_token(tokens: set[str]) -> bool:
    identity_targets = {"name", "remember", "know", "identity", "samer"}
    for token in tokens:
        for target in identity_targets:
            if SequenceMatcher(a=token, b=target).ratio() >= 0.74:
                return True
    return False


def is_personal_question(question: str) -> bool:
    normalized = question.strip().lower()
    if any(pattern.search(normalized) for pattern in PERSONAL_QUERY_PATTERNS):
        return True

    punctuation_normalized = normalize_for_personal_detection(normalized)
    if any(pattern.search(punctuation_normalized) for pattern in PERSONAL_QUERY_PATTERNS):
        return True

    tokens = set(tokenize(punctuation_normalized))
    if has_identity_like_token(tokens) and not tokens & COURSE_DOMAIN_KEYWORDS:
        return True

    return False


def ensure_index(index_path: Path = INDEX_PATH) -> Path:
    if index_path.exists() and not index_is_stale(index_path):
        return index_path
    index = build_ingestion_index(REPO_ROOT)
    return write_ingestion_index(index, index_path)


def index_is_stale(index_path: Path, repo_root: Path = REPO_ROOT) -> bool:
    if not index_path.exists():
        return True

    index_mtime = index_path.stat().st_mtime
    for markdown_file in enumerate_markdown_files(repo_root):
        if markdown_file.stat().st_mtime > index_mtime:
            return True

    return False


def load_index(index_path: Path = INDEX_PATH) -> dict[str, Any]:
    path = ensure_index(index_path)
    return json.loads(path.read_text(encoding="utf-8"))


def build_chunk_lookup(index_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {chunk["chunk_id"]: chunk for chunk in index_data["chunks"]}


def score_chunk(chunk: dict[str, Any], query_tokens: list[str], user_mode: str) -> tuple[int, int]:
    chunk_tokens = set(tokenize(chunk["text"]))
    overlap = sum(1 for token in query_tokens if token in chunk_tokens)
    if overlap == 0:
        return 0, 0

    score = overlap * 10
    category = chunk.get("source_category", "unknown")
    heading_tokens = tokenize(chunk.get("section_heading", ""))
    title_tokens = tokenize(chunk.get("title", ""))
    path_tokens = tokenize(chunk.get("path", ""))
    query_bigrams = build_bigrams(query_tokens)
    heading_bigrams = build_bigrams(heading_tokens)
    title_bigrams = build_bigrams(title_tokens)

    if user_mode == "learner" and category == "course":
        score += 5
    if user_mode == "maintainer" and category in {"design", "tasks", "docs"}:
        score += 5
    if any(token in heading_tokens for token in query_tokens):
        score += 3
    if any(token in title_tokens for token in query_tokens):
        score += 2

    bigram_overlap = len(query_bigrams & (heading_bigrams | title_bigrams))
    score += bigram_overlap * 8

    query_day = extract_day_number(" ".join(query_tokens))
    if query_day and (f"day-{query_day}" in chunk.get("path", "") or query_day in heading_tokens or query_day in title_tokens or query_day in path_tokens):
        score += 20

    return score, overlap


def retrieve_chunks(question: str, user_mode: str, top_k: int = 4) -> list[dict[str, Any]]:
    if is_personal_question(question):
        return []

    query_tokens = tokenize(question)
    if not query_tokens:
        return []

    index_data = load_index()
    chunk_lookup = build_chunk_lookup(index_data)
    candidate_ids: set[str] = set()
    for token in query_tokens:
        candidate_ids.update(index_data.get("term_index", {}).get(token, []))

    if not candidate_ids:
        return []

    minimum_overlap = 1 if len(query_tokens) <= 2 else 2
    scored: list[tuple[int, dict[str, Any]]] = []
    for chunk_id in candidate_ids:
        chunk = chunk_lookup.get(chunk_id)
        if not chunk:
            continue
        score, overlap = score_chunk(chunk, query_tokens, user_mode)
        if score > 0 and overlap >= minimum_overlap:
            scored.append((score, chunk))

    if not scored:
        return []

    grouped: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for score, chunk in scored:
        grouped[chunk["path"]].append((score, chunk))

    diversified: list[tuple[int, dict[str, Any]]] = []
    for path, items in grouped.items():
        best = sorted(items, key=lambda item: (-item[0], item[1]["ordinal_within_file"]))[0]
        diversified.append(best)

    ranked = sorted(diversified, key=lambda item: (-item[0], item[1]["path"], item[1]["ordinal_within_file"]))
    return [chunk for _, chunk in ranked[:top_k]]


def summarize_chunk(chunk: dict[str, Any], max_words: int = 45) -> str:
    lines = [line.strip() for line in chunk["text"].splitlines() if line.strip() and not line.strip().startswith("#")]
    text = " ".join(lines)
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip(".,;:") + "..."


def is_tool_question(question: str) -> bool:
    tokens = set(tokenize(question))
    return any(token in tokens for token in {"tool", "tools", "use", "using", "editor", "editing", "software"})


def detect_workflow_area(question: str) -> str | None:
    tokens = set(tokenize(question))
    if {"edit", "video"} <= tokens or {"editing", "video"} <= tokens or {"editor", "video"} <= tokens:
        return "Editing / Finishing"

    best_area: str | None = None
    best_score = 0
    for area, keywords in WORKFLOW_KEYWORDS.items():
        score = len(tokens & keywords)
        if score > best_score:
            best_area = area
            best_score = score
    return best_area


def parse_tool_vault_rows(chunks: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for chunk in chunks:
        if chunk.get("path") != "course/tool-vault.md":
            continue
        for line in chunk.get("text", "").splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            if TABLE_SEPARATOR_PATTERN.match(stripped):
                continue
            columns = [column.strip() for column in stripped.strip("|").split("|")]
            if len(columns) != 4 or columns[0] == "Workflow Area":
                continue
            rows.append(
                {
                    "workflow_area": columns[0],
                    "free": columns[1],
                    "paid": columns[2],
                    "notes": columns[3],
                }
            )
    return rows


def synthesize_tool_answer(question: str, chunks: list[dict[str, Any]]) -> str | None:
    rows = parse_tool_vault_rows(chunks)
    if not rows:
        return None

    workflow_area = detect_workflow_area(question)
    row = None
    if workflow_area:
        row = next((item for item in rows if item["workflow_area"] == workflow_area), None)

    if row is None:
        return None

    free_tool = row["free"]
    paid_tool = row["paid"]
    notes = row["notes"]

    if free_tool == "To Be Discovered" and paid_tool == "To Be Discovered":
        return (
            f"For {row['workflow_area'].lower()}, the current Tool Vault does not name a specific recommended tool yet. "
            f"Both the starter-friendly and pro-oriented recommendations are still marked as To Be Discovered. "
            f"The current guidance is to choose tools that fit this stage well: {notes}"
        )

    return (
        f"For {row['workflow_area'].lower()}, the Tool Vault currently points to {free_tool} for a free or starter-friendly option "
        f"and {paid_tool} for a paid or pro-oriented option. {notes}"
    )


def clean_chunk_text(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("```"):
            continue
        if stripped.startswith("|"):
            continue
        if stripped.startswith("- "):
            cleaned_lines.append(stripped[2:])
            continue
        cleaned_lines.append(stripped)
    return " ".join(cleaned_lines)


def extract_supporting_points(chunks: list[dict[str, Any]], max_points: int = 3) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        cleaned = clean_chunk_text(chunk.get("text", ""))
        if not cleaned:
            continue
        sentences = SENTENCE_SPLIT_PATTERN.split(cleaned)
        for sentence in sentences:
            normalized = sentence.strip()
            if len(normalized) < 25:
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            points.append(normalized)
            if len(points) >= max_points:
                return points
    return points


def synthesize_general_answer(question: str, chunks: list[dict[str, Any]]) -> str:
    workflow_area = detect_workflow_area(question)
    points = extract_supporting_points(chunks)
    if not points:
        return "I found relevant repository context, but it still needs a clearer documented explanation for this question."

    intro = "Based on the course repository, here is the clearest guidance right now:"
    if workflow_area:
        intro = f"Based on the course repository, here is the clearest guidance for {workflow_area.lower()}:"

    lead = points[0]
    if len(points) == 1:
        return f"{intro} {lead}"

    remainder = " ".join(points[1:])
    return f"{intro} {lead} {remainder}"


def build_out_of_scope_response() -> dict[str, Any]:
    return {
        "answer": (
            "I could not find enough support for that in the current repository. "
            "The question may be outside the current 7-day sprint scope or not documented yet."
        ),
        "grounded": False,
        "status": "out_of_scope",
        "answer_source": "out_of_scope",
        "citations": [],
    }


def build_personal_question_response() -> dict[str, Any]:
    return {
        "answer": (
            "I do not store or know personal identity details like your name. "
            "I can only answer from the repository's documented course and project content."
        ),
        "grounded": False,
        "status": "out_of_scope",
        "answer_source": "out_of_scope",
        "citations": [],
    }


def build_scoped_ai_response(answer: str) -> dict[str, Any]:
    return {
        "answer": answer,
        "grounded": False,
        "status": "scoped_ai",
        "answer_source": "gemini_scoped",
        "citations": [],
    }


def build_citations(chunks: list[dict[str, Any]]) -> list[str]:
    return [f"{chunk['path']}#{chunk['section_heading']}" for chunk in chunks]


def build_local_grounded_answer(question: str, chunks: list[dict[str, Any]]) -> str:
    citations = [f"{chunk['path']}#{chunk['section_heading']}" for chunk in chunks]
    answer = None
    if is_tool_question(question):
        answer = synthesize_tool_answer(question, chunks)

    if answer is None:
        answer = synthesize_general_answer(question, chunks)

    return answer


def build_grounded_response_from_chunks(question: str, chunks: list[dict[str, Any]], answer: str | None = None) -> dict[str, Any]:
    final_answer = answer or build_local_grounded_answer(question, chunks)
    citations = build_citations(chunks)

    return {
        "answer": final_answer,
        "grounded": True,
        "status": "grounded",
        "answer_source": "gemini_grounded" if answer else "local_grounded",
        "citations": citations,
    }


def build_grounded_answer(question: str, user_mode: str) -> dict[str, Any]:
    if is_personal_question(question):
        return build_personal_question_response()

    chunks = retrieve_chunks(question=question, user_mode=user_mode)
    if not chunks:
        return build_out_of_scope_response()

    return build_grounded_response_from_chunks(question=question, chunks=chunks)
