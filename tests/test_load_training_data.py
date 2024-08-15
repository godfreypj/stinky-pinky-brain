import unittest
from unittest.mock import patch
from utils.load_training_data import load_training_data

class TestLoadTrainingData(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_successful_data_loading(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'other_file.jpg']

        # Mock the open function with side_effect to provide different read_data for each file
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            mock_file.side_effect = [
                unittest.mock.mock_open(read_data='Training data from file1\n').return_value,
                unittest.mock.mock_open(read_data='Training data from file2\n').return_value
            ]

            result = load_training_data() 

        self.assertEqual(mock_file.call_count, 2)
        mock_file.assert_any_call('data/file1.txt', 'r')
        mock_file.assert_any_call('data/file2.txt', 'r')

    @patch('os.path.exists')
    def test_data_folder_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = load_training_data()
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: 'data' folder not found. Please provide training data in a 'data' folder.")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_no_txt_files_found(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['other_file.jpg']
        result = load_training_data()
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: No .txt files found in 'data' folder. Please provide training data.")

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_empty_training_data(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['empty.txt']
        with patch('builtins.open', unittest.mock.mock_open(read_data='')) as mock_file:
            result = load_training_data()
        
        mock_file.assert_called_once_with('data/empty.txt', 'r')
        self.assertTrue(result['is_error'])
        self.assertEqual(result['error_message'], "Error: Training data is empty. Please provide valid training data.")

if __name__ == '__main__':
    unittest.main()