import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from . import config_handler

EMBEDDING_MODEL = config_handler.get_embedding_model()
PERSISTENT_DIRECTORY = config_handler.get_db_path()
DATA_FOLDER = config_handler.get_data_folder()

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


def index_files(config_handler):
    """     
    Indexes files from the data folder and returns the indexed chunks.
    """
    
    #load
    loader = DirectoryLoader(DATA_FOLDER, glob="**/*.md", recursive=True)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {DATA_FOLDER}")
    
    #split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=80,
                                                   length_function=len,
                                                   is_separator_regex=False)
    chunks = splitter.split_documents(docs)
    print(f"Split documents into {len(chunks)} chunks.")
    #print(f"First chunk: {chunks[0].page_content[:100]}...")  # Print first 100 characters of the first chunk for debugging
    
    #------- embed ----------
    # moved the embedding logic to setup_vector_store function
    vector_store = setup_vector_store(persistent_directory=PERSISTENT_DIRECTORY, embedding_model=EMBEDDING_MODEL)

    #store
    document_ids = vector_store.add_documents(documents=chunks)
    print(f"Stored {len(document_ids)} document IDs in the vector store.")
    print(document_ids[:3])
    
    return vector_store

if __name__ == "__main__":
    index_files(config_handler)  # Call the function to index files and store them in the vector store
   
    