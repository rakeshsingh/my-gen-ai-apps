import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock, mock_open
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from helpers import indexer
from langchain.schema.document import Document


class TestIndexer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_documents = [
            Document(page_content="Test content 1", metadata={"source": "test1.md"}),
            Document(page_content="Test content 2", metadata={"source": "test2.md"})
        ]
        self.test_chunks = [
            Document(page_content="Chunk 1", metadata={"source": "test1.md"}),
            Document(page_content="Chunk 2", metadata={"source": "test1.md"}),
            Document(page_content="Chunk 3", metadata={"source": "test2.md"})
        ]
        self.test_persistent_directory = "/test/db/path"
        self.test_embedding_model = "test_embedding_model"

    @patch('helpers.indexer.Chroma')
    @patch('helpers.indexer.OllamaEmbeddings')
    def test_setup_vector_store_success(self, mock_embeddings_class, mock_chroma_class):
        """Test successful vector store setup."""
        mock_embeddings = MagicMock()
        mock_embeddings_class.return_value = mock_embeddings
        mock_vectorstore = MagicMock()
        mock_chroma_class.return_value = mock_vectorstore
        
        result = indexer.setup_vector_store(self.test_persistent_directory, self.test_embedding_model)
        
        mock_embeddings_class.assert_called_once_with(model=self.test_embedding_model)
        mock_chroma_class.assert_called_once_with(
            persist_directory=self.test_persistent_directory,
            embedding_function=mock_embeddings
        )
        self.assertEqual(result, mock_vectorstore)

    @patch('helpers.indexer.setup_vector_store')
    def test_setup_retriever_default_search_type(self, mock_setup_vector_store):
        """Test retriever setup with default search type."""
        mock_vector_store = MagicMock()
        mock_retriever = MagicMock()
        mock_vector_store.as_retriever.return_value = mock_retriever
        mock_setup_vector_store.return_value = mock_vector_store
        
        result = indexer.setup_retriever(self.test_persistent_directory, self.test_embedding_model)
        
        mock_setup_vector_store.assert_called_once_with(
            self.test_persistent_directory, 
            self.test_embedding_model
        )
        mock_vector_store.as_retriever.assert_called_once_with(search_type="similarity")
        self.assertEqual(result, mock_retriever)

    @patch('helpers.indexer.setup_vector_store')
    def test_setup_retriever_custom_search_type(self, mock_setup_vector_store):
        """Test retriever setup with custom search type."""
        mock_vector_store = MagicMock()
        mock_retriever = MagicMock()
        mock_vector_store.as_retriever.return_value = mock_retriever
        mock_setup_vector_store.return_value = mock_vector_store
        
        result = indexer.setup_retriever(
            self.test_persistent_directory, 
            self.test_embedding_model, 
            search_type="mmr"
        )
        
        mock_vector_store.as_retriever.assert_called_once_with(search_type="mmr")
        self.assertEqual(result, mock_retriever)

    @patch('helpers.indexer.setup_vector_store')
    @patch('helpers.indexer.RecursiveCharacterTextSplitter')
    @patch('helpers.indexer.DirectoryLoader')
    def test_index_files_success(self, mock_loader_class, mock_splitter_class, mock_setup_vector_store):
        """Test successful file indexing."""
        # Setup mocks
        mock_loader = MagicMock()
        mock_loader.load.return_value = self.test_documents
        mock_loader_class.return_value = mock_loader
        
        mock_splitter = MagicMock()
        mock_splitter.split_documents.return_value = self.test_chunks
        mock_splitter_class.return_value = mock_splitter
        
        mock_vector_store = MagicMock()
        mock_vector_store.add_documents.return_value = ["doc1", "doc2", "doc3"]
        mock_setup_vector_store.return_value = mock_vector_store
        
        mock_config_handler = MagicMock()
        
        with patch('helpers.indexer.DATA_FOLDER', '/test/data'), \
             patch('helpers.indexer.PERSISTENT_DIRECTORY', '/test/db'), \
             patch('helpers.indexer.EMBEDDING_MODEL', 'test_model'):
            
            result = indexer.index_files(mock_config_handler)
        
        # Verify all components were called correctly
        mock_loader_class.assert_called_once_with('/test/data', glob="**/*.md", recursive=True)
        mock_loader.load.assert_called_once()
        
        mock_splitter_class.assert_called_once_with(
            chunk_size=1000,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False
        )
        mock_splitter.split_documents.assert_called_once_with(self.test_documents)
        
        mock_setup_vector_store.assert_called_once_with(
            persistent_directory='/test/db',
            embedding_model='test_model'
        )
        mock_vector_store.add_documents.assert_called_once_with(documents=self.test_chunks)
        
        self.assertEqual(result, mock_vector_store)

    @patch('helpers.indexer.DirectoryLoader')
    def test_index_files_no_documents(self, mock_loader_class):
        """Test file indexing when no documents are found."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = []
        mock_loader_class.return_value = mock_loader
        
        with patch('helpers.indexer.RecursiveCharacterTextSplitter') as mock_splitter_class:
            mock_splitter = MagicMock()
            mock_splitter.split_documents.return_value = []
            mock_splitter_class.return_value = mock_splitter
            
            with patch('helpers.indexer.setup_vector_store') as mock_setup_vector_store:
                mock_vector_store = MagicMock()
                mock_vector_store.add_documents.return_value = []
                mock_setup_vector_store.return_value = mock_vector_store
                
                mock_config_handler = MagicMock()
                
                with patch('helpers.indexer.DATA_FOLDER', '/test/data'), \
                     patch('helpers.indexer.PERSISTENT_DIRECTORY', '/test/db'), \
                     patch('helpers.indexer.EMBEDDING_MODEL', 'test_model'):
                    
                    result = indexer.index_files(mock_config_handler)
                
                # Should still work with empty document list
                mock_vector_store.add_documents.assert_called_once_with(documents=[])
                self.assertEqual(result, mock_vector_store)

    @patch('helpers.indexer.RecursiveCharacterTextSplitter')
    @patch('helpers.indexer.DirectoryLoader')
    def test_index_files_chunking_process(self, mock_loader_class, mock_splitter_class):
        """Test the document chunking process in file indexing."""
        mock_loader = MagicMock()
        mock_loader.load.return_value = self.test_documents
        mock_loader_class.return_value = mock_loader
        
        mock_splitter = MagicMock()
        mock_splitter.split_documents.return_value = self.test_chunks
        mock_splitter_class.return_value = mock_splitter
        
        with patch('helpers.indexer.setup_vector_store') as mock_setup_vector_store:
            mock_vector_store = MagicMock()
            mock_vector_store.add_documents.return_value = ["doc1", "doc2", "doc3"]
            mock_setup_vector_store.return_value = mock_vector_store
            
            mock_config_handler = MagicMock()
            
            with patch('helpers.indexer.DATA_FOLDER', '/test/data'), \
                 patch('helpers.indexer.PERSISTENT_DIRECTORY', '/test/db'), \
                 patch('helpers.indexer.EMBEDDING_MODEL', 'test_model'):
                
                indexer.index_files(mock_config_handler)
            
            # Verify splitter configuration
            mock_splitter_class.assert_called_once_with(
                chunk_size=1000,
                chunk_overlap=80,
                length_function=len,
                is_separator_regex=False
            )
            
            # Verify documents were split
            mock_splitter.split_documents.assert_called_once_with(self.test_documents)

    @patch('helpers.indexer.OllamaEmbeddings')
    def test_setup_vector_store_embedding_configuration(self, mock_embeddings_class):
        """Test vector store setup with embedding configuration."""
        mock_embeddings = MagicMock()
        mock_embeddings_class.return_value = mock_embeddings
        
        with patch('helpers.indexer.Chroma') as mock_chroma_class:
            mock_vectorstore = MagicMock()
            mock_chroma_class.return_value = mock_vectorstore
            
            indexer.setup_vector_store(self.test_persistent_directory, self.test_embedding_model)
            
            # Verify embeddings were configured with correct model
            mock_embeddings_class.assert_called_once_with(model=self.test_embedding_model)
            
            # Verify Chroma was initialized with correct parameters
            mock_chroma_class.assert_called_once_with(
                persist_directory=self.test_persistent_directory,
                embedding_function=mock_embeddings
            )

    @patch('helpers.indexer.setup_vector_store')
    def test_setup_retriever_vector_store_integration(self, mock_setup_vector_store):
        """Test retriever setup integration with vector store."""
        mock_vector_store = MagicMock()
        mock_retriever = MagicMock()
        mock_vector_store.as_retriever.return_value = mock_retriever
        mock_setup_vector_store.return_value = mock_vector_store
        
        result = indexer.setup_retriever(
            self.test_persistent_directory, 
            self.test_embedding_model,
            search_type="similarity_score_threshold"
        )
        
        # Verify vector store setup was called
        mock_setup_vector_store.assert_called_once_with(
            self.test_persistent_directory, 
            self.test_embedding_model
        )
        
        # Verify retriever was configured with custom search type
        mock_vector_store.as_retriever.assert_called_once_with(
            search_type="similarity_score_threshold"
        )
        
        self.assertEqual(result, mock_retriever)


if __name__ == '__main__':
    unittest.main()
