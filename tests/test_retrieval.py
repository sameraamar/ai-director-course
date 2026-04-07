from pathlib import Path
import importlib
import sys
import unittest


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

engine = importlib.import_module("ai_director_backend.retrieval.engine")


class RetrievalEngineTests(unittest.TestCase):
    def test_retrieve_chunks_finds_course_content_for_learner(self) -> None:
        chunks = engine.retrieve_chunks("How do I make a 5-shot storyboard?", user_mode="learner")

        self.assertTrue(chunks)
        self.assertTrue(any(chunk["path"] == "course/day-1-storyboard.md" for chunk in chunks))

    def test_build_grounded_answer_returns_citations(self) -> None:
        result = engine.build_grounded_answer("How do I create image prompts?", user_mode="learner")

        self.assertTrue(result["grounded"])
        self.assertEqual("grounded", result["status"])
        self.assertTrue(result["citations"])
        self.assertIn("course repository", result["answer"])
        self.assertNotIn("| Workflow Area |", result["answer"])

    def test_retrieve_chunks_prioritizes_specific_day_formula_question(self) -> None:
        chunks = engine.retrieve_chunks("What is the 3-line script formula for Day 4?", user_mode="learner")

        self.assertTrue(chunks)
        self.assertEqual("course/day-4-audio.md", chunks[0]["path"])
        self.assertIn("3-Line Script Formula", chunks[0]["section_heading"])

    def test_build_grounded_answer_synthesizes_tool_vault_question(self) -> None:
        result = engine.build_grounded_answer("What tool should I use for video editing?", user_mode="learner")

        self.assertTrue(result["grounded"])
        self.assertEqual("grounded", result["status"])
        self.assertTrue(any("course/tool-vault.md" in citation for citation in result["citations"]))
        self.assertIn("editing / finishing", result["answer"].lower())
        self.assertNotIn("| Workflow Area |", result["answer"])
        self.assertTrue(
            "capcut" in result["answer"].lower() or "premiere pro" in result["answer"].lower() or "davinci resolve" in result["answer"].lower()
        )

    def test_build_grounded_answer_handles_out_of_scope_question(self) -> None:
        result = engine.build_grounded_answer("Explain quantum gravity", user_mode="learner")

        self.assertFalse(result["grounded"])
        self.assertEqual("out_of_scope", result["status"])
        self.assertEqual([], result["citations"])

    def test_build_grounded_answer_declines_personal_identity_question(self) -> None:
        result = engine.build_grounded_answer("Do you know that my name is Samer?", user_mode="learner")

        self.assertFalse(result["grounded"])
        self.assertEqual("out_of_scope", result["status"])
        self.assertEqual([], result["citations"])
        self.assertIn("do not store or know personal identity details", result["answer"].lower())

    def test_build_grounded_answer_declines_personal_identity_question_with_typo(self) -> None:
        result = engine.build_grounded_answer("what is my na,e?", user_mode="learner")

        self.assertFalse(result["grounded"])
        self.assertEqual("out_of_scope", result["status"])
        self.assertEqual([], result["citations"])
        self.assertIn("do not store or know personal identity details", result["answer"].lower())


if __name__ == "__main__":
    unittest.main()
