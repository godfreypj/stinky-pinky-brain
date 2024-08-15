import unittest
import os
from unittest.mock import patch, Mock
from utils.load_config import load_config

class TestLoadConfig(unittest.TestCase):

    @patch.dict(os.environ, {'GEMINI_KEY': 'test_key', 'MODEL': 'test_model', 
                             'SP_CONTROL': 'test_control', 'PROJECT_ID': 'local'})
    def test_successful_config_loading_local(self):
        """Test successful loading from .env in local environment"""
        result = load_config()
        self.assertIsInstance(result, dict)  # Check if it's a dictionary
        self.assertEqual(result['GEMINI_KEY'], 'test_key')
        self.assertEqual(result['MODEL'], 'test_model')
        self.assertEqual(result['SP_CONTROL'], 'test_control')
        self.assertEqual(result['PROJECT_ID'], 'local')

    @patch.dict(os.environ, {'MODEL': 'test_model', 'SP_CONTROL': 'test_control', 'PROJECT_ID': 'test_project'})
    @patch('google.cloud.secretmanager_v1.SecretManagerServiceClient')
    def test_successful_config_loading_non_local(self, mock_client):
        """Test successful loading from Secret Manager in non-local environment"""
        mock_instance = mock_client.return_value
        mock_response = Mock()
        mock_response.payload.data.decode.return_value = 'secret_key_from_manager'
        mock_instance.access_secret_version.return_value = mock_response

        result = load_config()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['GEMINI_KEY'], 'secret_key_from_manager')
        self.assertEqual(result['MODEL'], 'test_model')
        self.assertEqual(result['SP_CONTROL'], 'test_control')
        self.assertEqual(result['PROJECT_ID'], 'test_project')

    @patch.dict(os.environ, {}, clear=True)  # Clear all environment variables
    def test_missing_env_variables(self):
        """Test error handling when required env variables are missing"""
        result = load_config()
        self.assertIsInstance(result, Exception)
        self.assertEqual(str(result), "Missing required configuration values")

    @patch.dict(os.environ, {'MODEL': 'test_model', 'SP_CONTROL': 'test_control', 'PROJECT_ID': 'test_project'})
    @patch('google.cloud.secretmanager_v1.SecretManagerServiceClient')
    def test_secret_manager_access_error(self, mock_client):
        """Test error handling when there's an issue accessing Secret Manager"""
        mock_instance = mock_client.return_value
        mock_instance.access_secret_version.side_effect = Exception("Secret Manager error")

        result = load_config()
        self.assertIsInstance(result, Exception)
        self.assertEqual(str(result), "Secret Manager error")

if __name__ == '__main__':
    unittest.main()