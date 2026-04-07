from pathlib import Path
import importlib
import os
import sys
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


BACKEND_ROOT = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

app = importlib.import_module("ai_director_backend.app").app


class BackendApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.env_patcher = patch.dict(os.environ, {"AI_DIRECTOR_USE_GEMINI": "false"}, clear=False)
        cls.env_patcher.start()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.env_patcher.stop()

    def test_health_endpoint_returns_expected_status(self) -> None:
        response = self.client.get("/api/health")

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "service": "ai-director-backend",
                "status": "ok",
                "phase": "grounded-retrieval",
            },
            response.json(),
        )

    def test_chat_endpoint_returns_grounded_course_answer(self) -> None:
        response = self.client.post(
            "/api/chat",
            json={"question": "How do I create a 5-shot storyboard?", "user_mode": "learner"},
        )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("How do I create a 5-shot storyboard?", payload["question"])
        self.assertEqual("grounded", payload["status"])
        self.assertTrue(payload["grounded"])
        self.assertEqual("local_grounded", payload["answer_source"])
        self.assertTrue(payload["citations"])
        self.assertIn("course repository", payload["answer"])
        self.assertTrue(any("course/day-1-storyboard.md" in citation for citation in payload["citations"]))

    def test_chat_endpoint_synthesizes_tool_vault_answer(self) -> None:
        response = self.client.post(
            "/api/chat",
            json={"question": "What tool should I use for video editing?", "user_mode": "learner"},
        )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("grounded", payload["status"])
        self.assertEqual("local_grounded", payload["answer_source"])
        self.assertTrue(any("course/tool-vault.md" in citation for citation in payload["citations"]))
        self.assertNotIn("| Workflow Area |", payload["answer"])
        self.assertTrue(
            "capcut" in payload["answer"].lower() or "premiere pro" in payload["answer"].lower() or "davinci resolve" in payload["answer"].lower()
        )

    def test_chat_endpoint_declines_out_of_scope_question(self) -> None:
        response = self.client.post(
            "/api/chat",
            json={"question": "What is the capital of France?", "user_mode": "learner"},
        )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("out_of_scope", payload["status"])
        self.assertEqual("out_of_scope", payload["answer_source"])
        self.assertFalse(payload["grounded"])
        self.assertEqual([], payload["citations"])
        self.assertIn("outside the current 7-day sprint scope", payload["answer"])

    def test_chat_endpoint_declines_personal_identity_question(self) -> None:
        response = self.client.post(
            "/api/chat",
            json={"question": "Do you know that my name is Samer?", "user_mode": "learner"},
        )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("out_of_scope", payload["status"])
        self.assertEqual("out_of_scope", payload["answer_source"])
        self.assertFalse(payload["grounded"])
        self.assertEqual([], payload["citations"])

    def test_chat_endpoint_declines_personal_identity_question_with_typo(self) -> None:
        response = self.client.post(
            "/api/chat",
            json={"question": "what is my na,e?", "user_mode": "learner"},
        )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("out_of_scope", payload["status"])
        self.assertEqual("out_of_scope", payload["answer_source"])
        self.assertFalse(payload["grounded"])
        self.assertEqual([], payload["citations"])
        self.assertIn("do not store or know personal identity details", payload["answer"].lower())

    def test_chat_endpoint_uses_scoped_gemini_for_in_scope_general_question(self) -> None:
        with patch.dict(os.environ, {"AI_DIRECTOR_USE_GEMINI": "true"}, clear=False):
            with patch("ai_director_backend.services.chat_service.can_call_gemini", return_value=True):
                with patch(
                    "ai_director_backend.services.chat_service.answer_with_scoped_gemini",
                    new=AsyncMock(return_value="A wider lens captures more of the scene and exaggerates perspective compared with a longer lens."),
                ):
                    response = self.client.post(
                        "/api/chat",
                        json={"question": "How do camera lenses work?", "user_mode": "learner"},
                    )

        self.assertEqual(200, response.status_code)
        payload = response.json()
        self.assertEqual("scoped_ai", payload["status"])
        self.assertEqual("gemini_scoped", payload["answer_source"])
        self.assertFalse(payload["grounded"])
        self.assertEqual([], payload["citations"])
        self.assertIn("lens", payload["answer"].lower())


if __name__ == "__main__":
    unittest.main()
