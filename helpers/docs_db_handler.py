import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
# SPLIT THE DOCS INTO CHUNKS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

def load_docs(data_folder):
    print(f"Loading documents from {data_folder}")
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"The specified data folder does not exist: {data_folder}")
    loader = DirectoryLoader(data_folder, glob="**/*.md", recursive=True)
    docs = loader.load()
    print(f"Loaded {len(docs)} documents from {data_folder}")
    return docs


def split_docs(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                   chunk_overlap=80,
                                                   length_function=len,
                                                   is_separator_regex=False)
    return text_splitter.split_documents(docs)

def init_db(chunks, embeddings_model, folder_path, embeddings):
    """
    Initialize FAISS with given chunks and embedding model, save it to the folder path, or load from the folder if it exists.
    """
    faiss_path = os.path.join(folder_path, "index.faiss")
    if os.path.exists(faiss_path):
        vectorstore = FAISS.load_local(folder_path, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings_model)
        os.makedirs(folder_path, exist_ok=True)
        vectorstore.save_local(folder_path)
    return vectorstore

def add_db_docs(vectorstore, data_path, db_path, embeddings_model):
    """
    Load documents from the folder, check if they exist in the vectorstore, and add them if they don't.
    """
    documents = load_docs(data_path)
    #chunks = split_docs(documents)
    for document in documents:
        content = document.page_content
        embedding = embeddings_model.embed_query(content)
        result = vectorstore.similarity_search_by_vector(embedding, k=3)
        if not result:
            print("This content does not exist in vector database. Adding the content.")
            chunks = split_docs(content)
            vectorstore.add_texts(chunks)
    vectorstore.save_local(db_path)
    
    
if __name__ == "__main__":
    import config_handler
    print('came here')
    data_folder = config_handler.get_data_folder()
    # data_folder = '/Users/raksingh/personal/github/my-ollama-rag-app/data/'
    print(data_folder)
    load_docs(data_folder)
    