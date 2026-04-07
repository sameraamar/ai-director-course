from pathlib import Path
import unittest


class ProjectScaffoldTests(unittest.TestCase):
    def test_expected_bootstrap_files_exist(self) -> None:
        root = Path(__file__).resolve().parents[1]
        expected_paths = [
            "README.md",
            ".env.template",
            ".github/copilot-instructions.md",
            "docs/START_HERE.md",
            "docs/tasks.md",
            "docs/design/design.md",
            "docs/design/backend/retrieval-architecture.md",
            "docs/design/backend/package-layout.md",
            "docs/design/chat-widget/website-chat-widget.md",
            "docs/research/research-notes.md",
            "docs/templates/TASK-COMPLETION-TEMPLATE.md",
            "docs/templates/TASK-KICKOFF-TEMPLATE.md",
            "backend/requirements.txt",
            "backend/ai_director_backend/__init__.py",
            "backend/ai_director_backend/app.py",
            "backend/ai_director_backend/models.py",
            "backend/ai_director_backend/ingestion/__init__.py",
            "backend/ai_director_backend/ingestion/models.py",
            "backend/ai_director_backend/ingestion/pipeline.py",
            "backend/ai_director_backend/retrieval/__init__.py",
            "backend/ai_director_backend/retrieval/engine.py",
            "backend/ai_director_backend/api/__init__.py",
            "backend/ai_director_backend/api/routes.py",
            "backend/ai_director_backend/services/__init__.py",
            "backend/ai_director_backend/services/chat_service.py",
            "backend/ai_director_backend/services/gemini_service.py",
            "overrides/main.html",
            "course/assets/stylesheets/chat-widget.css",
            "course/assets/javascripts/chat-widget.js",
            "mkdocs.yml",
            ".vscode/tasks.json",
            "course/index.md",
            "course/tool-vault.md",
            "course/day-1-storyboard.md",
            "course/day-2-images.md",
            "course/day-3-video.md",
            "course/day-4-audio.md",
            "course/day-5-music.md",
            "course/day-6-editing.md",
            "course/day-7-final.md",
        ]

        missing = [path for path in expected_paths if not (root / path).exists()]
        self.assertEqual([], missing, f"Missing scaffold files: {missing}")

    def test_course_pages_include_required_sections(self) -> None:
        root = Path(__file__).resolve().parents[1]
        required_by_file = {
            "course/day-1-storyboard.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-2-images.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-3-video.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-4-audio.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-5-music.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-6-editing.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Checkpoint"],
            "course/day-7-final.md": ["## Outcome for Today", "## Fast Track", "## Deep Dive", "## Finish Line"],
            "course/tool-vault.md": ["## Tool Categories", "## Update Checklist", "## Maintenance Workflow"],
        }

        for relative_path, required_sections in required_by_file.items():
            content = (root / relative_path).read_text(encoding="utf-8")
            for section in required_sections:
                self.assertIn(section, content, f"Expected '{section}' in {relative_path}")

    def test_backend_retrieval_design_includes_core_sections(self) -> None:
        root = Path(__file__).resolve().parents[1]
        content = (root / "docs/design/backend/retrieval-architecture.md").read_text(encoding="utf-8")

        required_sections = [
            "# Chunking Strategy",
            "# Embedding Strategy",
            "# Vector Store Decision",
            "# Retrieval Flow",
            "# Grounded Answer Rules",
            "# Ingestion Workflow",
        ]

        for section in required_sections:
            self.assertIn(section, content, f"Expected '{section}' in backend retrieval design")

    def test_backend_package_layout_design_includes_core_sections(self) -> None:
        root = Path(__file__).resolve().parents[1]
        content = (root / "docs/design/backend/package-layout.md").read_text(encoding="utf-8")

        required_sections = [
            "# Package Layout Decision",
            "# Module Responsibilities",
            "# Test Conventions",
            "# Packaging Guidance",
        ]

        for section in required_sections:
            self.assertIn(section, content, f"Expected '{section}' in backend package layout design")

    def test_retrieval_test_file_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "tests/test_retrieval.py").exists())

    def test_chat_widget_design_file_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "docs/design/chat-widget/website-chat-widget.md").exists())

    def test_gemini_service_file_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "backend/ai_director_backend/services/gemini_service.py").exists())

    def test_gemini_service_test_file_exists(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertTrue((root / "tests/test_gemini_service.py").exists())

    def test_mkdocs_widget_assets_are_configured(self) -> None:
        root = Path(__file__).resolve().parents[1]
        content = (root / "mkdocs.yml").read_text(encoding="utf-8")

        self.assertIn("custom_dir: overrides", content)
        self.assertIn("assets/stylesheets/chat-widget.css", content)
        self.assertIn("assets/javascripts/chat-widget.js", content)
        self.assertIn("chat_widget:", content)


if __name__ == "__main__":
    unittest.main()
