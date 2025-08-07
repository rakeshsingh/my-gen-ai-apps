import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader, CSVLoader, PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from . import config_handler

EMBEDDING_MODEL = config_handler.get_embedding_model()
PERSISTENT_DIRECTORY = config_handler.get_db_path()
DATA_FOLDER = config_handler.get_data_folder()


loader_mapping = {
        ".txt": TextLoader,
        ".md": UnstructuredMarkdownLoader,
        # ".csv": CSVLoader,
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
    }


def setup_vector_store(persistent_directory, embedding_model):
    """     
    Configure a vectore store to persist local data.
    """
    print(persistent_directory)
    print(embedding_model)
    embeddings = OllamaEmbeddings(model=embedding_model)
    # Initialize Chroma vector store
    vectorstore = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
    return vectorstore


def setup_retriever(persistent_directory, embedding_model, search_type="similarity"):
    vector_store = setup_vector_store(persistent_directory, embedding_model)
    return vector_store.as_retriever(search_type=search_type)


def load_multiple_file_types(directory_path):
    """Load multiple file types using loader mapping"""    
    # Define loader mapping for different file extensions
    
    all_documents = []
    
    # Walk through directory and load files based on extension
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            if file_ext in loader_mapping:
                try:
                    print(f"Working on {file_path}")
                    loader_class = loader_mapping[file_ext]
                    loader = loader_class(file_path)
                    documents = loader.load()
                    all_documents.extend(documents)
                    print(f"Loaded {len(documents)} documents from {file}")
                except Exception as e:
                    print(f"Error loading {file}: {str(e)}")
    
    return all_documents


def index_files():
    """     
    Indexes files from the data folder and returns the indexed chunks.
    """
    
    #load
    # loader = DirectoryLoader(DATA_FOLDER, glob=["**/*.md","**/*.txt","**/*.pdf","**/*.docx"], recursive=True)
    # docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=80,
                                                   length_function=len,
                                                   is_separator_regex=False)
    #------- embed ----------
    # moved the embedding logic to setup_vector_store function
    vector_store = setup_vector_store(persistent_directory=PERSISTENT_DIRECTORY, embedding_model=EMBEDDING_MODEL)
    # docs = load_multiple_file_types(DATA_FOLDER)
    
    # Walk through directory and load files based on extension
    for root, dirs, files in os.walk(DATA_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            if file_ext in loader_mapping:
                try:
                    print(f"Working on {file_path}")
                    #load 
                    loader_class = loader_mapping[file_ext]
                    loader = loader_class(file_path)
                    documents = loader.load()
                    # all_documents.extend(documents)
                    print(f"Loaded {len(documents)} documents from {file}")
                    #split
                    chunks = splitter.split_documents(documents)
                    print(f"Split documents into {len(chunks)} chunks.")
                    #store
                    document_ids = vector_store.add_documents(documents=chunks)
                    print(f"Stored {len(document_ids)} document IDs in the vector store.")
                    print(document_ids[:3])
                except Exception as e:
                    print(f"Error loading {file}: {str(e)}")
    #print(f"First chunk: {chunks[0].page_content[:100]}...")  # Print first 100 characters of the first chunk for debugging
    return vector_store

if __name__ == "__main__":
    index_files()  # Call the function to index files and store them in the vector store
   
    