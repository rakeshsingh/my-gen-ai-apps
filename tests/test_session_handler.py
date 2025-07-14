import unittest
import tempfile
import os
import json
from unittest.mock import patch, mock_open, MagicMock
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import session_handler
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory


class TestSessionHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_session_id = "test_session_123"
        self.test_messages = [
            {"role": "human", "content": "Hello, how are you?"},
            {"role": "ai", "content": "I'm doing well, thank you!"},
            {"role": "human", "content": "What's the weather like?"},
            {"role": "ai", "content": "I don't have access to current weather data."}
        ]
        
        # Clear the store before each test
        session_handler.store.clear()

    def test_get_session_history_new_session(self):
        """Test getting session history for a new session."""
        with patch('os.path.exists', return_value=False):
            history = session_handler.get_session_history(self.test_session_id)
            
            self.assertIsInstance(history, ChatMessageHistory)
            self.assertEqual(len(history.messages), 0)
            self.assertIn(self.test_session_id, session_handler.store)

    def test_get_session_history_existing_session_in_store(self):
        """Test getting session history for an existing session already in store."""
        # Pre-populate the store
        existing_history = ChatMessageHistory()
        existing_history.add_user_message("Previous message")
        session_handler.store[self.test_session_id] = existing_history
        
        history = session_handler.get_session_history(self.test_session_id)
        
        self.assertEqual(history, existing_history)
        self.assertEqual(len(history.messages), 1)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('json.load')
    def test_get_session_history_load_from_file(self, mock_json_load, mock_exists, mock_file):
        """Test loading session history from file."""
        mock_exists.return_value = True
        mock_json_load.return_value = self.test_messages
        
        history = session_handler.get_session_history(self.test_session_id)
        
        self.assertIsInstance(history, ChatMessageHistory)
        self.assertEqual(len(history.messages), 4)
        
        # Verify the messages were loaded correctly
        messages = history.messages
        self.assertIsInstance(messages[0], HumanMessage)
        self.assertEqual(messages[0].content, "Hello, how are you?")
        self.assertIsInstance(messages[1], AIMessage)
        self.assertEqual(messages[1].content, "I'm doing well, thank you!")

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('json.load')
    def test_get_session_history_file_load_error(self, mock_json_load, mock_exists, mock_file):
        """Test handling of file load errors."""
        mock_exists.return_value = True
        mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        
        # Should handle the error gracefully and create new history
        with self.assertRaises(json.JSONDecodeError):
            session_handler.get_session_history(self.test_session_id)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_session_history_success(self, mock_json_dump, mock_file):
        """Test successful session history saving."""
        # Create a history with messages
        history = ChatMessageHistory()
        history.add_user_message("Hello")
        history.add_ai_message("Hi there!")
        session_handler.store[self.test_session_id] = history
        
        session_handler.save_session_history(self.test_session_id)
        
        # Verify file operations
        expected_filename = f"{self.test_session_id}.json"
        mock_file.assert_called_once()
        
        # Verify JSON dump was called with correct data
        mock_json_dump.assert_called_once()
        saved_data = mock_json_dump.call_args[0][0]
        
        self.assertEqual(len(saved_data), 2)
        self.assertEqual(saved_data[0]["role"], "human")
        self.assertEqual(saved_data[0]["content"], "Hello")
        self.assertEqual(saved_data[1]["role"], "ai")
        self.assertEqual(saved_data[1]["content"], "Hi there!")

    def test_save_session_history_nonexistent_session(self):
        """Test saving history for a session that doesn't exist in store."""
        # Should not raise an error, just do nothing
        session_handler.save_session_history("nonexistent_session")
        
        # No assertions needed, just verify it doesn't crash

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_session_history_empty_history(self, mock_json_dump, mock_file):
        """Test saving empty session history."""
        # Create empty history
        history = ChatMessageHistory()
        session_handler.store[self.test_session_id] = history
        
        session_handler.save_session_history(self.test_session_id)
        
        # Verify empty list was saved
        mock_json_dump.assert_called_once()
        saved_data = mock_json_dump.call_args[0][0]
        self.assertEqual(saved_data, [])

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_session_history_mixed_messages(self, mock_json_dump, mock_file):
        """Test saving session history with mixed message types."""
        history = ChatMessageHistory()
        history.add_user_message("User message 1")
        history.add_ai_message("AI response 1")
        history.add_user_message("User message 2")
        history.add_ai_message("AI response 2")
        session_handler.store[self.test_session_id] = history
        
        session_handler.save_session_history(self.test_session_id)
        
        mock_json_dump.assert_called_once()
        saved_data = mock_json_dump.call_args[0][0]
        
        self.assertEqual(len(saved_data), 4)
        self.assertEqual(saved_data[0]["role"], "human")
        self.assertEqual(saved_data[1]["role"], "ai")
        self.assertEqual(saved_data[2]["role"], "human")
        self.assertEqual(saved_data[3]["role"], "ai")

    @patch('os.makedirs')
    @patch('os.path.dirname')
    @patch('os.path.abspath')
    def test_history_directory_creation(self, mock_abspath, mock_dirname, mock_makedirs):
        """Test that history directory is created properly."""
        mock_abspath.return_value = "/test/path/session_handler.py"
        mock_dirname.return_value = "/test/path"
        
        # Reload the module to trigger directory creation
        import importlib
        importlib.reload(session_handler)
        
        mock_makedirs.assert_called_with("/test/path/sessions", exist_ok=True)

    def test_store_persistence_across_calls(self):
        """Test that the store persists across multiple function calls."""
        # First call - create new session
        with patch('os.path.exists', return_value=False):
            history1 = session_handler.get_session_history(self.test_session_id)
            history1.add_user_message("Test message")
        
        # Second call - should return the same session
        history2 = session_handler.get_session_history(self.test_session_id)
        
        self.assertEqual(history1, history2)
        self.assertEqual(len(history2.messages), 1)
        self.assertEqual(history2.messages[0].content, "Test message")


if __name__ == '__main__':
    unittest.main()
