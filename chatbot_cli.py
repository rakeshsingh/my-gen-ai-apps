import os
import uuid
from helpers import indexer, session_handler, config_handler, llm_handler
from langchain_core.runnables.history import RunnableWithMessageHistory


EMBEDDING_MODEL = config_handler.get_embedding_model()
PERSISTENT_DIRECTORY = config_handler.get_db_path()
MODEL_PROVIDER = "ollama"  # Default model provider
MODEL = "llama3.2"

session_id = str(uuid.uuid4())
retriever = indexer.setup_retriever(persistent_directory=PERSISTENT_DIRECTORY, embedding_model=EMBEDDING_MODEL)
chat_history = session_handler.get_session_history(session_id)

while True:
    question = input("\n Enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    # ---- LangChain Components ---- #
    rag_chain = llm_handler.setup_chain_chatbot(model=MODEL, retriever=retriever)
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda _: chat_history,
        input_messages_key="input",
        history_messages_key="history",
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