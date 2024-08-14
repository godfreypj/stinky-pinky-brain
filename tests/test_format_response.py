import unittest
import os
import json
from utils.format_response import format_response

class TestFormatResponse(unittest.TestCase):

    def test_format_response_with_valid_json(self):
        ai_response = "```json\n{\"word1\": \"stinky\", \"clue1\": \"smelly\", \"word2\": \"pinky\", \"clue2\": \"finger\"}```"
        expected_result = {"is_error": False, "data": {"word1": "stinky", "clue1": "smelly", "word2": "pinky", "clue2": "finger"}}
        actual_result = format_response(ai_response)
        self.assertEqual(actual_result, expected_result)

    def test_format_response_with_empty_response(self):
        ai_response = ""
        expected_result = {"is_error": True, "error_message": "No AI Response found! Check main.py"}
        actual_result = format_response(ai_response)
        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()