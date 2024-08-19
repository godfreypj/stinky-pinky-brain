import unittest
from unittest.mock import patch
from services.load_prompt import load_prompt

class TestLoadPrompt(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_successful_prompt_loading(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['prompt.txt', 'other_file.txt']

        with patch('builtins.open', unittest.mock.mock_open(read_data='This is the prompt content\n')) as mock_file:
            result = load_prompt("Some training data")

        mock_file.assert_called_once_with('data/prompt.txt', 'r')
        self.assertFalse(result['is_error'])
        self.assertIn('This is the prompt content', result['prompt'])
        self.assertIn('Some training data', result['prompt'])
        self.assertIn('"word1": "[Word]"', result['prompt'])

    @patch('os.path.exists')
    def test_data_folder_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = load_prompt("Some training data")
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: 'data' folder not found. Please provide training data in a 'data' folder.")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_prompt_file_not_found(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['other_file.txt']
        result = load_prompt("Some training data")
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: No prompt found. Please provide a 'prompt.txt' file in the 'data' folder.")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_empty_prompt(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['prompt.txt']

        with patch('builtins.open', unittest.mock.mock_open(read_data=' \n ')) as mock_file:
            result = load_prompt("Some training data")

        mock_file.assert_called_once_with('data/prompt.txt', 'r')
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: Prompt is empty. Please provide a non-empty 'prompt.txt' file in the 'data' folder.")

if __name__ == '__main__':
    unittest.main()