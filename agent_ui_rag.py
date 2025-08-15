from helpers.llm_handler import setup_agent
from helpers.indexer import setup_retriever
from langchain_core.messages import AIMessage, HumanMessage
from helpers.tools import tools 
from helpers import config_handler
import streamlit as st


# ---- Streamlit UI ---- #
st.title("📚 My Local Chatbot")
st.set_page_config(layout="wide")

# ---- Steamlit Sidebar ---- #
st.sidebar.header("Settings")
MODEL = st.sidebar.selectbox("Choose Ollama Model", ["llama3.2","deepseek-r1:8b", "gemma3:4b"], index=0)

MAX_HISTORY = st.sidebar.number_input("Max History", 1, 10, 2)
CONTEXT_SIZE = st.sidebar.number_input("Context Size", 1024, 16384, 8192, step=1024)
MODEL_PROVIDER = "ollama"  # Default model provider
MAX_ITERATIONS = 4
EMBEDDING_MODEL = config_handler.get_embedding_model()
PERSISTENT_DIRECTORY = config_handler.get_db_path()

# ---- Session State Setup ---- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- LangChain Components ---- #
retriever = setup_retriever(persistent_directory=PERSISTENT_DIRECTORY, embedding_model=EMBEDDING_MODEL)
agent = setup_agent(MODEL_PROVIDER, MODEL)

# ---- Display Chat History ---- #
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# ---- Trim Chat Memory ---- #
def trim_memory():
    while len(st.session_state.chat_history) > MAX_HISTORY * 2:
        st.session_state.chat_history.pop(0)  # Remove oldest messages

# ---- Handle User Input ---- #
if query := st.chat_input("Say something"):
    st.session_state.chat_history.append(HumanMessage(content=query))
    
    with st.chat_message("Human"):
        st.write(query)
        trim_memory()

    with st.chat_message("AI"):
        # Retrieve relevant documents & run QA
        print(query)
        retrieved_docs = retriever.invoke(query)
        print(retrieved_docs)
        response = agent.invoke(
            {"messages":[
                    {
                    "role": "user",
                    "content": query, 
                    "history": st.session_state.chat_history, 
                    "context": retrieved_docs, 
                    "tools": tools, 
                    "agent_scratchpad": ""
                    }]
            }
            )       
        print("Result from agent:")
        print(response["messages"][-1].content) # Output the final answer

        # Display the full response
        st.write(response["messages"][-1].content)
        st.session_state.chat_history.append(AIMessage(response["messages"][-1].content))
        trim_memory()
