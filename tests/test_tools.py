import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import tools


class TestTools(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def test_math_tool_valid_expression(self):
        """Test math tool with valid mathematical expression."""
        result = tools.math_tool("2 + 3 * 4")
        self.assertEqual(result, "The result of 2 + 3 * 4 is 14")

    def test_math_tool_simple_addition(self):
        """Test math tool with simple addition."""
        result = tools.math_tool("5 + 3")
        self.assertEqual(result, "The result of 5 + 3 is 8")

    def test_math_tool_division(self):
        """Test math tool with division."""
        result = tools.math_tool("10 / 2")
        self.assertEqual(result, "The result of 10 / 2 is 5.0")

    def test_math_tool_parentheses(self):
        """Test math tool with parentheses."""
        result = tools.math_tool("(2 + 3) * 4")
        self.assertEqual(result, "The result of (2 + 3) * 4 is 20")

    def test_math_tool_decimal_numbers(self):
        """Test math tool with decimal numbers."""
        result = tools.math_tool("3.5 + 2.1")
        self.assertEqual(result, "The result of 3.5 + 2.1 is 5.6")

    def test_math_tool_invalid_characters(self):
        """Test math tool with invalid characters."""
        result = tools.math_tool("2 + 3 * abc")
        self.assertEqual(result, "Error: Invalid characters in expression")

    def test_math_tool_invalid_expression(self):
        """Test math tool with invalid mathematical expression."""
        result = tools.math_tool("2 + + 3")
        self.assertIn("Error calculating", result)

    def test_math_tool_division_by_zero(self):
        """Test math tool with division by zero."""
        result = tools.math_tool("5 / 0")
        self.assertIn("Error calculating", result)

    def test_math_tool_empty_expression(self):
        """Test math tool with empty expression."""
        result = tools.math_tool("")
        self.assertEqual(result, "The result of  is ")

    def test_math_tool_spaces_only(self):
        """Test math tool with spaces only."""
        result = tools.math_tool("   ")
        self.assertEqual(result, "The result of    is ")

    def test_math_tool_complex_expression(self):
        """Test math tool with complex expression."""
        result = tools.math_tool("((2 + 3) * 4) - (10 / 2)")
        self.assertEqual(result, "The result of ((2 + 3) * 4) - (10 / 2) is 15.0")

    @patch('helpers.config_handler.get_embedding_model')
    @patch('helpers.config_handler.get_db_path')
    def test_tools_initialization(self, mock_get_db_path, mock_get_embedding_model):
        """Test that tools are properly initialized."""
        mock_get_embedding_model.return_value = "test_embedding_model"
        mock_get_db_path.return_value = "/test/db/path"
        
        # Import tools module to trigger initialization
        import importlib
        importlib.reload(tools)
        
        # Verify that the tools list contains expected tools
        self.assertIsInstance(tools.tools, list)
        self.assertEqual(len(tools.tools), 3)  # math_tool, search_tool, retriever_tool

    @patch('helpers.tools.DuckDuckGoSearchRun')
    def test_search_tool_initialization(self, mock_search_class):
        """Test search tool initialization."""
        mock_search_instance = MagicMock()
        mock_search_tool = MagicMock()
        mock_search_instance.as_tool.return_value = mock_search_tool
        mock_search_class.return_value = mock_search_instance
        
        # Reload the module to test initialization
        import importlib
        importlib.reload(tools)
        
        mock_search_instance.as_tool.assert_called_once_with(
            name="search_web",
            description="Search for information on the web using DuckDuckGo. This tool should be used only when the other tools are not giving any information"
        )

    @patch('helpers.tools.create_retriever_tool')
    @patch('helpers.indexer.setup_retriever')
    @patch('helpers.config_handler.get_embedding_model')
    @patch('helpers.config_handler.get_db_path')
    def test_retriever_tool_initialization(self, mock_get_db_path, mock_get_embedding_model,
                                          mock_setup_retriever, mock_create_retriever_tool):
        """Test retriever tool initialization."""
        mock_get_embedding_model.return_value = "test_embedding_model"
        mock_get_db_path.return_value = "/test/db/path"
        mock_retriever = MagicMock()
        mock_setup_retriever.return_value = mock_retriever
        mock_retriever_tool = MagicMock()
        mock_create_retriever_tool.return_value = mock_retriever_tool
        
        # Reload the module to test initialization
        import importlib
        importlib.reload(tools)
        
        mock_setup_retriever.assert_called_once_with(
            persistent_directory="/test/db/path",
            embedding_model="test_embedding_model"
        )
        mock_create_retriever_tool.assert_called_once_with(
            mock_retriever,
            "local search",
            "Search for information about myself and my team members. For any questions about me, my team, and my workplace you must use this tool!"
        )


if __name__ == '__main__':
    unittest.main()
