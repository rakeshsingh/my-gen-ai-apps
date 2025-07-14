import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
import configparser
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import config_handler


class TestConfigHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_config_content = """
[General]
DATA_FOLDER = /test/data/folder
DB_PATH = /test/db/path
EMBEDDING_MODEL = test_embedding_model
MODEL = test_model
"""
        self.empty_config_content = ""
        self.incomplete_config_content = """
[General]
DATA_FOLDER = /test/data/folder
"""

    def test_read_config_success(self):
        """Test successful configuration reading."""
        with patch('builtins.open', mock_open(read_data=self.test_config_content)):
            with patch('configparser.ConfigParser.read') as mock_read:
                mock_config = configparser.ConfigParser()
                mock_config.read_string(self.test_config_content)
                with patch('configparser.ConfigParser.sections', return_value=['General']):
                    # Should not raise an exception
                    config_handler.read_config('test_config.ini')

    def test_read_config_empty_file(self):
        """Test reading empty configuration file."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.sections', return_value=[]):
                with self.assertRaises(ValueError) as context:
                    config_handler.read_config('empty_config.ini')
                self.assertIn("Configuration file is empty or not found", str(context.exception))

    def test_get_data_folder_success(self):
        """Test successful data folder retrieval."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'DATA_FOLDER': '/test/data/folder'}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    result = config_handler.get_data_folder('test_config.ini')
                    self.assertEqual(result, '/test/data/folder')

    def test_get_data_folder_missing_section(self):
        """Test data folder retrieval with missing General section."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__contains__', return_value=False):
                with self.assertRaises(ValueError) as context:
                    config_handler.get_data_folder('test_config.ini')
                self.assertIn("DATA_FOLDER not found in the configuration file", str(context.exception))

    def test_get_data_folder_empty_value(self):
        """Test data folder retrieval with empty value."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'DATA_FOLDER': ''}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    with self.assertRaises(ValueError) as context:
                        config_handler.get_data_folder('test_config.ini')
                    self.assertIn("DATA_FOLDER is empty in the configuration file", str(context.exception))

    def test_get_db_path_success(self):
        """Test successful database path retrieval."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'DB_PATH': '/test/db/path'}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    result = config_handler.get_db_path('test_config.ini')
                    self.assertEqual(result, '/test/db/path')

    def test_get_db_path_missing_key(self):
        """Test database path retrieval with missing DB_PATH key."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__contains__', return_value=False):
                with self.assertRaises(ValueError) as context:
                    config_handler.get_db_path('test_config.ini')
                self.assertIn("DB_PATH not found in the configuration file", str(context.exception))

    def test_get_embedding_model_success(self):
        """Test successful embedding model retrieval."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'EMBEDDING_MODEL': 'test_embedding_model'}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    result = config_handler.get_embedding_model('test_config.ini')
                    self.assertEqual(result, 'test_embedding_model')

    def test_get_embedding_model_empty_value(self):
        """Test embedding model retrieval with empty value."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'EMBEDDING_MODEL': ''}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    with self.assertRaises(ValueError) as context:
                        config_handler.get_embedding_model('test_config.ini')
                    self.assertIn("EMBEDDING_MODEL is empty in the configuration file", str(context.exception))

    def test_get_model_success(self):
        """Test successful model retrieval."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__getitem__') as mock_getitem:
                mock_section = {'MODEL': 'test_model'}
                mock_getitem.return_value = mock_section
                with patch('configparser.ConfigParser.__contains__', return_value=True):
                    result = config_handler.get_model('test_config.ini')
                    self.assertEqual(result, 'test_model')

    def test_get_model_missing_key(self):
        """Test model retrieval with missing MODEL key."""
        with patch('configparser.ConfigParser.read'):
            with patch('configparser.ConfigParser.__contains__', return_value=False):
                with self.assertRaises(ValueError) as context:
                    config_handler.get_model('test_config.ini')
                self.assertIn("MODEL not found in the configuration file", str(context.exception))


if __name__ == '__main__':
    unittest.main()
