import os
import uuid
from helpers import indexer, session_handler, config_handler
from helpers.retriever import retrieve_docs
from helpers.chain_handler import setup_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOllama

session_id = str(uuid.uuid4())
vector_store = indexer.index_files(config_handler)  # Index files and store them in the vector store
chat_history = session_handler.get_session_history(session_id)

while True:
    question = input("\n Enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
        
    retriever = retrieve_docs(question, vector_store, similar_docs_count = 5, see_content=False)
    rag_chain = setup_chain("llama3.2", retriever)
    
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda _: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    
    answer = ""
    for chunk in conversational_rag_chain.stream(
        {"input": question},
        config={
            "configurable": {"session_id": session_id}
        },
    ):
        if 'answer' in chunk:
            print(chunk['answer'], end="", flush=True)
            answer += chunk['answer']
            
    chat_history.add_user_message(question)
    chat_history.add_ai_message(answer)
    session_handler.save_session_history(session_id)