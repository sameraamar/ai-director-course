from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable

from ai_director_backend.ingestion.models import DocumentChunk, IngestionIndex, SourceDocument

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
MAX_WORDS_PER_CHUNK = 700
CHUNK_OVERLAP_WORDS = 75
INCLUDED_ROOTS = ("course", "docs")
EXCLUDED_PARTS = {".venv", "__pycache__", ".git", ".pytest_cache", "node_modules", "dist", "build"}


def enumerate_markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for root_name in INCLUDED_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if any(part in EXCLUDED_PARTS for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def detect_source_category(relative_path: Path) -> str:
    parts = relative_path.parts
    if not parts:
        return "unknown"
    if parts[0] == "course":
        return "course"
    if parts[0] != "docs":
        return "unknown"
    if len(parts) == 1:
        return "docs"
    if parts[1] == "design":
        return "design"
    if parts[1] == "research":
        return "research"
    if parts[1] == "templates":
        return "templates"
    if parts[1] == "tasks.md":
        return "tasks"
    if parts[1] == "START_HERE.md":
        return "docs"
    return parts[1].replace(".md", "")


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    normalized = "\n".join(lines).strip()
    return f"{normalized}\n" if normalized else ""


def compute_content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def derive_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def load_source_document(repo_root: Path, file_path: Path) -> SourceDocument:
    relative_path = file_path.relative_to(repo_root)
    raw_text = normalize_text(file_path.read_text(encoding="utf-8"))
    return SourceDocument(
        path=relative_path.as_posix(),
        source_category=detect_source_category(relative_path),
        title=derive_title(file_path, raw_text),
        raw_text=raw_text,
        content_hash=compute_content_hash(raw_text),
    )


def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading = "Introduction"
    current_lines: list[str] = []

    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            if current_lines:
                section_text = "\n".join(current_lines).strip()
                if section_text:
                    sections.append((current_heading, section_text))
            current_heading = match.group(2).strip()
            current_lines = [line]
            continue
        current_lines.append(line)

    if current_lines:
        section_text = "\n".join(current_lines).strip()
        if section_text:
            sections.append((current_heading, section_text))
    return sections


def split_oversized_section(section_text: str, max_words: int = MAX_WORDS_PER_CHUNK) -> list[str]:
    words = section_text.split()
    if len(words) <= max_words:
        return [section_text]

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + max_words, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(end - CHUNK_OVERLAP_WORDS, start + 1)
    return chunks


def chunk_source_document(document: SourceDocument) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    ordinal = 1
    for section_heading, section_text in split_markdown_sections(document.raw_text):
        for piece in split_oversized_section(section_text):
            chunk_hash = compute_content_hash(f"{document.path}:{section_heading}:{piece}")
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_hash[:16],
                    path=document.path,
                    title=document.title,
                    section_heading=section_heading,
                    source_category=document.source_category,
                    text=piece,
                    content_hash=chunk_hash,
                    ordinal_within_file=ordinal,
                    word_count=len(piece.split()),
                )
            )
            ordinal += 1
    return chunks


def tokenize(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(text.lower()))


def build_term_index(chunks: Iterable[DocumentChunk]) -> dict[str, list[str]]:
    postings: dict[str, list[str]] = defaultdict(list)
    for chunk in chunks:
        for token in sorted(tokenize(chunk.text)):
            postings[token].append(chunk.chunk_id)
    return dict(sorted(postings.items()))


def build_ingestion_index(repo_root: Path) -> IngestionIndex:
    files = enumerate_markdown_files(repo_root)
    sources = [load_source_document(repo_root, file_path) for file_path in files]
    chunks = [chunk for source in sources for chunk in chunk_source_document(source)]
    term_index = build_term_index(chunks)
    return IngestionIndex(
        root_path=str(repo_root.resolve()),
        generated_at=datetime.now(UTC).isoformat(),
        chunk_count=len(chunks),
        source_count=len(sources),
        chunks=chunks,
        term_index=term_index,
    )


def write_ingestion_index(index: IngestionIndex, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(index.to_dict(), indent=2), encoding="utf-8")
    return output_path


def ingest_repository(repo_root: Path, output_path: Path | None = None) -> Path:
    output = output_path or repo_root / "backend" / ".artifacts" / "ingestion" / "index.json"
    index = build_ingestion_index(repo_root)
    return write_ingestion_index(index, output)


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parents[3]
    written_path = ingest_repository(repository_root)
    print(f"Wrote ingestion index to {written_path}")
