# import unittest
# from unittest.mock import patch, Mock
# from main import app  # Use the actual filename 'main'

# class TestMainApp(unittest.TestCase):

#     def setUp(self):
#         self.app = app.test_client()

#     @patch('main.load_config')
#     def test_load_config_failure(self, mock_load_config):
#         """Test scenario where load_config fails."""
#         mock_load_config.side_effect = Exception("Config loading failed")
#         with self.assertRaises(RuntimeError):
#             self.app.get('/api/generate') 

#     @patch('main.load_training_data')
#     @patch('main.load_prompt')
#     @patch('main.genai.GenerativeModel')
#     def test_generate_api_success(self, mock_model, mock_load_prompt, mock_load_training_data):
#         """Test successful API call to /api/generate."""
#         mock_load_training_data.return_value = {'is_error': False, 'training_data': 'some_training_data'}
#         mock_load_prompt.return_value = {'is_error': False, 'prompt': 'generated_prompt'}

#         mock_model_instance = mock_model.return_value
#         mock_model_instance.generate_content.return_value = [Mock(text='{"word1": "cat", "clue1": "Meow", "word2": "hat", "clue2": "On your head"}')]

#         response = self.app.get('/api/generate')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.content_type, 'application/json')
#         self.assertEqual(response.json, {'text': {'word1': 'cat', 'clue1': 'Meow', 'word2': 'hat', 'clue2': 'On your head'}})

#     @patch('main.load_training_data')
#     def test_generate_api_training_data_error(self, mock_load_training_data):
#         """Test when load_training_data returns an error."""
#         mock_load_training_data.return_value = {'is_error': True, 'error_message': 'Training data error'}

#         response = self.app.get('/api/generate')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {'error': 'Training data error'})

#     @patch('main.load_training_data')
#     @patch('main.load_prompt')
#     def test_generate_api_load_prompt_error(self, mock_load_prompt, mock_load_training_data):
#         """Test when load_prompt returns an error."""
#         mock_load_training_data.return_value = {'is_error': False, 'training_data': 'some_training_data'}
#         mock_load_prompt.return_value = {'is_error': True, 'error_message': 'Prompt loading error'}

#         response = self.app.get('/api/generate')
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json, {'error': 'Prompt loading error'})

#     @patch('main.load_training_data')
#     @patch('main.load_prompt')
#     @patch('main.genai.GenerativeModel')
#     def test_generate_api_format_response_error(self, mock_model, mock_load_prompt, mock_load_training_data):
#         """Test when format_response returns an error."""
#         mock_load_training_data.return_value = {'is_error': False, 'training_data': 'some_training_data'}
#         mock_load_prompt.return_value = {'is_error': False, 'prompt': 'generated_prompt'}

#         mock_model_instance = mock_model.return_value
#         mock_model_instance.generate_content.return_value = [Mock(text='invalid_json_response')] 

#         response = self.app.get('/api/generate')
#         self.assertEqual(response.status_code, 404)  # Assuming format_response returns 404 on error
#         self.assertEqual(response.json.get('error'), 'No AI Response found! Check main.py') 

#     @patch('main.load_training_data')
#     @patch('main.load_prompt')
#     @patch('main.genai.GenerativeModel')
#     def test_generate_api_gemini_model_error(self, mock_model, mock_load_prompt, mock_load_training_data):
#         """Test when genai.GenerativeModel raises an exception."""
#         mock_load_training_data.return_value = {'is_error': False, 'training_data': 'some_training_data'}
#         mock_load_prompt.return_value = {'is_error': False, 'prompt': 'generated_prompt'}

#         mock_model_instance = mock_model.return_value
#         mock_model_instance.generate_content.side_effect = Exception('Gemini API error')

#         response = self.app.get('/api/generate')
#         self.assertEqual(response.status_code, 500) 
#         self.assertEqual(response.json.get('error'), 'Gemini API error') 

#     def test_serve_static(self):
#         """Test serving a static file from the 'web' directory."""
#         # Assuming you have an 'index.html' file in your 'web' directory
#         response = self.app.get('/index.html')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('text/html', response.content_type) 

# if __name__ == '__main__':
#     unittest.main()