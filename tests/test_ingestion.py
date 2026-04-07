from pathlib import Path
import importlib
import os
import sys
import tempfile
import time
import unittest


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

pipeline = importlib.import_module("ai_director_backend.ingestion.pipeline")
engine = importlib.import_module("ai_director_backend.retrieval.engine")


class IngestionPipelineTests(unittest.TestCase):
    def test_chunk_source_document_preserves_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            docs_root = repo_root / "docs"
            docs_root.mkdir(parents=True)
            source_path = docs_root / "example.md"
            source_path.write_text(
                "# Example Title\n\nIntro text.\n\n## Section A\n\nAlpha beta gamma.\n\n## Section B\n\nDelta epsilon zeta.\n",
                encoding="utf-8",
            )

            document = pipeline.load_source_document(repo_root, source_path)
            chunks = pipeline.chunk_source_document(document)

            self.assertEqual("Example Title", document.title)
            self.assertEqual(["Example Title", "Section A", "Section B"], [chunk.section_heading for chunk in chunks])
            self.assertTrue(all(chunk.path == "docs/example.md" for chunk in chunks))

    def test_build_ingestion_index_reads_repo_markdown(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]

        index = pipeline.build_ingestion_index(repo_root)

        self.assertGreater(index.source_count, 0)
        self.assertGreater(index.chunk_count, 0)
        self.assertEqual(repo_root.name, index.root_path)
        self.assertTrue(any(chunk.path == "course/day-1-storyboard.md" for chunk in index.chunks))
        self.assertIn("course", {chunk.source_category for chunk in index.chunks})
        self.assertIn("design", {chunk.source_category for chunk in index.chunks})
        self.assertIn("storyboard", index.term_index)

    def test_ingest_repository_writes_index_file(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "index.json"
            written_path = pipeline.ingest_repository(repo_root, output_path)

            self.assertEqual(output_path, written_path)
            self.assertTrue(output_path.exists())
            content = output_path.read_text(encoding="utf-8")
            self.assertIn('"chunk_count"', content)
            self.assertIn('"term_index"', content)

    def test_index_is_stale_when_markdown_changes_after_index_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            course_root = repo_root / "course"
            docs_root = repo_root / "docs"
            course_root.mkdir(parents=True)
            docs_root.mkdir(parents=True)

            markdown_path = course_root / "lesson.md"
            markdown_path.write_text("# Lesson\n\nOriginal content.\n", encoding="utf-8")

            index_path = repo_root / "backend" / ".artifacts" / "ingestion" / "index.json"
            pipeline.ingest_repository(repo_root, index_path)

            self.assertFalse(engine.index_is_stale(index_path, repo_root))

            time.sleep(1.1)
            markdown_path.write_text("# Lesson\n\nUpdated content with new details.\n", encoding="utf-8")
            os.utime(markdown_path, None)

            self.assertTrue(engine.index_is_stale(index_path, repo_root))


if __name__ == "__main__":
    unittest.main()
