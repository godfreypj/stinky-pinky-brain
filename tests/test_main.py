import unittest
from unittest.mock import patch
import google.generativeai as genai
from main import app
from collections import namedtuple


class TestGenerateApi(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test for Missing API_KEY
    def test_missing_api_key(self):
        with patch("main.API_KEY", "TODO"):
            response = self.app.get("/api/generate")
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn("error", data)
            self.assertIn("get an API key", data["error"])

    # Test for Missing SP_CONTROL
    def test_missing_sp_control(self):
        with patch("main.SP_CONTROL", "TODO"):
            response = self.app.get("/api/generate")
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn("error", data)
            self.assertIn("Stinky Pinky Control", data["error"])

    # Test for Error in load_training_data
    @patch("main.load_training_data")
    def test_error_in_load_training_data(self, mock_load_training_data):
        mock_load_training_data.return_value = "Error: Some training data error"
        response = self.app.get("/api/generate")
        self.assertEqual(response.status_code, 500)

    # Test for Error in load_prompt
    @patch("main.load_prompt")
    def test_error_in_load_prompt(self, mock_load_prompt):
        mock_load_prompt.return_value = "Error: Some prompt error"
        response = self.app.get("/api/generate")
        self.assertEqual(response.status_code, 500)

    # Test for Error in format_response (Empty AI Response)
    @patch("google.generativeai.GenerativeModel.generate_content")
    def test_error_in_format_response_empty(self, mock_generate_content):
        mock_generate_content.return_value = ""  # Simulate empty response
        response = self.app.get("/api/generate")
        self.assertEqual(response.status_code, 404)

    # Test for Successful Response
    @patch("google.generativeai.GenerativeModel.generate_content")
    @patch("main.load_training_data")
    @patch("main.load_prompt")
    def test_successful_response(
        self, mock_load_prompt, mock_load_training_data, mock_generate_content
    ):
        mock_load_prompt.return_value = "Some prompt"
        mock_load_training_data.return_value = "Some training data"

        # Create a namedtuple to represent the objects returned by generate_content
        MockContentChunk = namedtuple("MockContentChunk", ["text"])

        mock_generate_content.return_value = iter(
            [
                MockContentChunk(
                    text='{"word1": "cat", "clue1": "Fluffy pet", "word2": "hat", "clue2": "Headwear"}'
                )
            ]
        )
        response = self.app.get("/api/generate")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")


if __name__ == "__main__":
    unittest.main()
