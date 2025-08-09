import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import llm_handler


class TestLLMHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_docs = [
            MagicMock(page_content="Document 1 content"),
            MagicMock(page_content="Document 2 content"),
            MagicMock(page_content="Document 3 content")
        ]
        self.test_model = "llama3.2"
        self.test_retriever = MagicMock()

    def test_format_docs(self):
        """Test document formatting function."""
        result = llm_handler.format_docs(self.test_docs)
        expected = "Document 1 content\n\nDocument 2 content\n\nDocument 3 content"
        self.assertEqual(result, expected)

    def test_format_docs_empty_list(self):
        """Test document formatting with empty list."""
        result = llm_handler.format_docs([])
        self.assertEqual(result, "")

    def test_format_docs_single_doc(self):
        """Test document formatting with single document."""
        single_doc = [MagicMock(page_content="Single document content")]
        result = llm_handler.format_docs(single_doc)
        self.assertEqual(result, "Single document content")

    @patch('helpers.llm_handler.create_react_agent')
    @patch('helpers.llm_handler.InMemorySaver')
    @patch('helpers.llm_handler.ChatPromptTemplate')
    @patch('helpers.llm_handler.init_chat_model')
    @patch('helpers.tools.tools')
    def test_setup_agent(self, mock_tools, mock_init_chat_model, mock_prompt_template, 
                        mock_memory_saver, mock_create_react_agent):
        """Test agent setup."""
        mock_model = MagicMock()
        mock_init_chat_model.return_value = mock_model
        mock_prompt = MagicMock()
        mock_prompt_template.from_messages.return_value = mock_prompt
        mock_memory = MagicMock()
        mock_memory_saver.return_value = mock_memory
        mock_agent = MagicMock()
        mock_create_react_agent.return_value = mock_agent
        mock_tools.return_value = []
        
        result = llm_handler.setup_agent("ollama", "llama3.2")
        
        mock_init_chat_model.assert_called_once_with("ollama:llama3.2")
        mock_create_react_agent.assert_called_once_with(
            model=mock_model, 
            tools=mock_tools, 
            prompt=mock_prompt
        )
        self.assertEqual(result, mock_agent)

    @patch('helpers.llm_handler.create_retrieval_chain')
    @patch('helpers.llm_handler.create_stuff_documents_chain')
    @patch('helpers.llm_handler.ChatPromptTemplate')
    @patch('helpers.llm_handler.ChatOllama')
    def test_setup_chain(self, mock_chat_ollama, mock_prompt_template, 
                        mock_create_stuff_chain, mock_create_retrieval_chain):
        """Test chain setup."""
        mock_llm = MagicMock()
        mock_chat_ollama.return_value = mock_llm
        mock_prompt = MagicMock()
        mock_prompt_template.from_template.return_value = mock_prompt
        mock_qa_chain = MagicMock()
        mock_create_stuff_chain.return_value = mock_qa_chain
        mock_rag_chain = MagicMock()
        mock_create_retrieval_chain.return_value = mock_rag_chain
        
        result = llm_handler.setup_chain(self.test_model, self.test_retriever)
        
        mock_chat_ollama.assert_called_once_with(
            model=self.test_model,
            temperature=0.8,
            num_predict=256,
            keep_alive=-1,
            streaming=True,
            max_tokens=8192,
            return_source_documents=True
        )
        mock_create_stuff_chain.assert_called_once_with(mock_llm, mock_prompt)
        mock_create_retrieval_chain.assert_called_once_with(self.test_retriever, mock_qa_chain)
        self.assertEqual(result, mock_rag_chain)

    @patch('helpers.llm_handler.create_retrieval_chain')
    @patch('helpers.llm_handler.create_stuff_documents_chain')
    @patch('helpers.llm_handler.create_history_aware_retriever')
    @patch('helpers.llm_handler.ChatPromptTemplate')
    @patch('helpers.llm_handler.ChatOllama')
    def test_setup_chain_chatbot(self, mock_chat_ollama, mock_prompt_template,
                                mock_create_history_retriever, mock_create_stuff_chain,
                                mock_create_retrieval_chain):
        """Test chatbot chain setup."""
        mock_llm = MagicMock()
        mock_chat_ollama.return_value = mock_llm
        mock_contextualize_prompt = MagicMock()
        mock_qa_prompt = MagicMock()
        mock_prompt_template.from_messages.side_effect = [mock_contextualize_prompt, mock_qa_prompt]
        mock_history_retriever = MagicMock()
        mock_create_history_retriever.return_value = mock_history_retriever
        mock_qa_chain = MagicMock()
        mock_create_stuff_chain.return_value = mock_qa_chain
        mock_rag_chain = MagicMock()
        mock_create_retrieval_chain.return_value = mock_rag_chain
        
        result = llm_handler.setup_chain_chatbot(self.test_model, self.test_retriever)
        
        mock_chat_ollama.assert_called_once_with(
            model=self.test_model,
            temperature=0.8,
            num_predict=256,
            keep_alive=-1
        )
        self.assertEqual(mock_prompt_template.from_messages.call_count, 2)
        mock_create_history_retriever.assert_called_once_with(
            mock_llm, self.test_retriever, mock_contextualize_prompt
        )
        mock_create_stuff_chain.assert_called_once_with(mock_llm, mock_qa_prompt)
        mock_create_retrieval_chain.assert_called_once_with(mock_history_retriever, mock_qa_chain)
        self.assertEqual(result, mock_rag_chain)

    @patch('helpers.llm_handler.ChatOllama')
    def test_setup_chain_custom_context_size(self, mock_chat_ollama):
        """Test chain setup with custom context size."""
        mock_llm = MagicMock()
        mock_chat_ollama.return_value = mock_llm
        
        with patch('helpers.llm_handler.ChatPromptTemplate'), \
             patch('helpers.llm_handler.create_stuff_documents_chain'), \
             patch('helpers.llm_handler.create_retrieval_chain'):
            
            llm_handler.setup_chain(self.test_model, self.test_retriever, context_size=4096)
            
            mock_chat_ollama.assert_called_once_with(
                model=self.test_model,
                temperature=0.8,
                num_predict=256,
                keep_alive=-1,
                streaming=True,
                max_tokens=4096,
                return_source_documents=True
            )


if __name__ == '__main__':
    unittest.main()
