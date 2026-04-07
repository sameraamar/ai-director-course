from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SourceDocument:
    path: str
    source_category: str
    title: str
    raw_text: str
    content_hash: str


@dataclass(slots=True)
class DocumentChunk:
    chunk_id: str
    path: str
    title: str
    section_heading: str
    source_category: str
    text: str
    content_hash: str
    ordinal_within_file: int
    word_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class IngestionIndex:
    root_path: str
    generated_at: str
    chunk_count: int
    source_count: int
    chunks: list[DocumentChunk]
    term_index: dict[str, list[str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "root_path": self.root_path,
            "generated_at": self.generated_at,
            "chunk_count": self.chunk_count,
            "source_count": self.source_count,
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "term_index": self.term_index,
        }


def resolve_repo_root(start_path: Path) -> Path:
    return start_path.resolve()
