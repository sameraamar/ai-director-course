from pathlib import Path
import importlib
import sys
import tempfile
import unittest
from unittest.mock import patch


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

gemini_service = importlib.import_module("ai_director_backend.services.gemini_service")


class GeminiServiceTests(unittest.TestCase):
    def test_build_gemini_prompt_includes_question_and_sources(self) -> None:
        prompt = gemini_service.build_gemini_prompt(
            question="How do I create a storyboard?",
            chunks=[
                {
                    "path": "course/day-1-storyboard.md",
                    "section_heading": "Day 1 — The Director's Blueprint",
                    "text": "## Fast Track\nCreate a 5-shot storyboard with subject, action, and lighting intent.",
                }
            ],
        )

        self.assertIn("How do I create a storyboard?", prompt)
        self.assertIn("course/day-1-storyboard.md", prompt)
        self.assertIn("Day 1 — The Director's Blueprint", prompt)
        self.assertIn("5-shot storyboard", prompt)
        self.assertIn("using ONLY the retrieved repository context", prompt)

    def test_build_scoped_gemini_prompt_includes_scope_and_question(self) -> None:
        prompt = gemini_service.build_scoped_gemini_prompt("How do camera lenses affect perspective?")

        self.assertIn("PROJECT SCOPE", prompt)
        self.assertIn("lens basics", prompt)
        self.assertIn("How do camera lenses affect perspective?", prompt)
        self.assertIn(gemini_service.SCOPED_AI_OUT_OF_SCOPE_SENTINEL, prompt)

    def test_extract_gemini_text_reads_first_candidate_text(self) -> None:
        payload = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Use the Day 1 blueprint to break the idea into five shots.",
                            }
                        ]
                    }
                }
            ]
        }

        self.assertEqual(
            "Use the Day 1 blueprint to break the idea into five shots.",
            gemini_service.extract_gemini_text(payload),
        )

    def test_is_retryable_gemini_status_identifies_transient_status_codes(self) -> None:
        self.assertTrue(gemini_service.is_retryable_gemini_status(429))
        self.assertTrue(gemini_service.is_retryable_gemini_status(503))
        self.assertFalse(gemini_service.is_retryable_gemini_status(400))
        self.assertFalse(gemini_service.is_retryable_gemini_status(None))

    def test_load_local_env_file_overrides_stale_environment_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("AI_DIRECTOR_GEMINI_MODEL=gemini-2.5-flash\n", encoding="utf-8")

            with patch.dict(gemini_service.os.environ, {"AI_DIRECTOR_GEMINI_MODEL": "gemini-2.0-flash-lite"}, clear=False):
                gemini_service.load_local_env_file(env_path)
                self.assertEqual("gemini-2.5-flash", gemini_service.os.environ["AI_DIRECTOR_GEMINI_MODEL"])

    def test_verbose_ai_logging_enabled_reads_env_flag(self) -> None:
        with patch.dict(gemini_service.os.environ, {"AI_DIRECTOR_VERBOSE_LOGGING": "true"}, clear=False):
            self.assertTrue(gemini_service.verbose_ai_logging_enabled())

        with patch.dict(gemini_service.os.environ, {"AI_DIRECTOR_VERBOSE_LOGGING": "false"}, clear=False):
            self.assertFalse(gemini_service.verbose_ai_logging_enabled())


if __name__ == "__main__":
    unittest.main()
