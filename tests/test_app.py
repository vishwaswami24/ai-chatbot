from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import httpx

from app import DEFAULT_MAX_TOKENS, DEFAULT_MODEL, DEFAULT_TEMPERATURE, DEFAULT_TIMEOUT_SECONDS, create_app


class ChatbotAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "WTF_CSRF_ENABLED": False,
                "COHERE_API_KEY": "test-key",
                "COHERE_MODEL": DEFAULT_MODEL,
                "COHERE_MAX_TOKENS": DEFAULT_MAX_TOKENS,
                "COHERE_TEMPERATURE": DEFAULT_TEMPERATURE,
                "COHERE_TIMEOUT_SECONDS": DEFAULT_TIMEOUT_SECONDS,
            }
        )
        self.client = self.app.test_client()

    def test_home_page_renders(self) -> None:
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Chatbot", response.data)

    def test_missing_api_key_shows_helpful_message(self) -> None:
        self.app.config["COHERE_API_KEY"] = ""

        response = self.client.post("/", data={"text": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add your Cohere API key in local_settings.py", response.data)

    def test_whitespace_only_prompt_is_rejected(self) -> None:
        response = self.client.post("/", data={"text": "   "})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please enter a prompt.", response.data)

    def test_successful_prompt_renders_model_output(self) -> None:
        mock_client = Mock()
        mock_client.chat.return_value = SimpleNamespace(text="Hello from the model")

        with patch("app.Client", return_value=mock_client) as client_cls:
            response = self.client.post("/", data={"text": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello from the model", response.data)
        client_cls.assert_called_once_with("test-key", timeout=DEFAULT_TIMEOUT_SECONDS)
        mock_client.chat.assert_called_once_with(
            message="Hello",
            model=DEFAULT_MODEL,
            max_tokens=DEFAULT_MAX_TOKENS,
            temperature=DEFAULT_TEMPERATURE,
        )

    def test_timeout_returns_friendly_error(self) -> None:
        mock_client = Mock()
        mock_client.chat.side_effect = httpx.TimeoutException("slow")

        with patch("app.Client", return_value=mock_client):
            response = self.client.post("/", data={"text": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The chatbot took too long to respond.", response.data)

    def test_api_failure_returns_friendly_error(self) -> None:
        mock_client = Mock()
        mock_client.chat.side_effect = RuntimeError("boom")

        with patch("app.Client", return_value=mock_client):
            response = self.client.post("/", data={"text": "Hello"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"The chatbot could not reach Cohere just now.", response.data)


if __name__ == "__main__":
    unittest.main()
