import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore


def index_files(config_handler):
    """     
    Indexes files from the data folder and returns the indexed chunks.
    """
    
    #load
    data_folder = config_handler.get_data_folder()
    if not data_folder:
        raise ValueError("Data folder path is not set in the configuration.")
    print(f"Loading documents from {data_folder}")
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"The specified data folder does not exist: {data_folder}")
    loader = DirectoryLoader(data_folder, glob="**/*.md", recursive=True)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {data_folder}")
    
    
    #split
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=80,
                                                   length_function=len,
                                                   is_separator_regex=False)
    chunks = splitter.split_documents(docs)
    print(f"Split documents into {len(chunks)} chunks.")
    #print(f"First chunk: {chunks[0].page_content[:100]}...")  # Print first 100 characters of the first chunk for debugging
    
    #embed
    embeddings_model = config_handler.get_embedding_model()
    if not embeddings_model:
        raise ValueError("Embedding model name is not set in the configuration.")
    embeddings = OllamaEmbeddings(model=embeddings_model)
    vector_store = InMemoryVectorStore(embeddings)
    print("Embedding documents...")
    #storing documents 
    document_ids = vector_store.add_documents(documents=chunks)
    print(f"Stored {len(document_ids)} document IDs in the vector store.")
    print(document_ids[:3])
    
    return vector_store