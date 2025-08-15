from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from helpers.agent_handler import get_agent
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st


def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

streamable_http_mcp_client = MCPClient(create_streamable_http_transport)

# ---- Streamlit UI ---- #
st.title("📚 My Local Chatbot")
st.set_page_config(layout="wide")

# ---- Steamlit Sidebar ---- #
st.sidebar.header("Settings")
MODEL = st.sidebar.selectbox("Choose Ollama Model", ["llama3.2","deepseek-r1:8b", "gemma3:4b"], index=0)
MAX_HISTORY = st.sidebar.number_input("Max History", 1, 10, 2)
CONTEXT_SIZE = st.sidebar.number_input("Context Size", 1024, 16384, 8192, step=1024)
MAX_ITERATIONS = 4

# ---- Session State Setup ---- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        
# Use the MCP server in a context manager
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()
    # Create an agent with the MCP tools
    agent = get_agent()
    # Let the agent handle the tool selection and parameter extraction
    response = agent("What is 125 plus 375?")
    print(response)
    response = agent("If I have 1000 and spend 246, how much do I have left?")
    print(response)
    response = agent("What is 24 multiplied by 7 divided by 3?")
    print(response)
