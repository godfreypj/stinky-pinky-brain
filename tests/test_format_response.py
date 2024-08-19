import unittest
from services.format_response import format_response

class TestFormatResponse(unittest.TestCase):

    def test_successful_response_parsing(self):
        ai_response = '{"word1": "stinky", "clue1": "smelly", "word2": "pinky", "clue2": "finger"}'
        result = format_response(ai_response)

        self.assertFalse(result['is_error'])
        self.assertEqual(result['formatted_response'], {
            "word1": "stinky",
            "clue1": "smelly",
            "word2": "pinky",
            "clue2": "finger"
        })

    def test_no_ai_response(self):
        ai_response = ""
        result = format_response(ai_response)

        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: No AI Response found! Check main.py")

    def test_empty_ai_response(self):
        ai_response = "   \n  "
        result = format_response(ai_response)

        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: No AI Response found! Check main.py")

    def test_invalid_json(self):
        ai_response = '`json\n{"word1": "stinky", "clue1": "smelly"`'  # Missing closing brace
        result = format_response(ai_response)

        self.assertTrue(result['is_error'])
        self.assertIn("Error parsing AI response:", result['error_message'])

if __name__ == '__main__':
    unittest.main()