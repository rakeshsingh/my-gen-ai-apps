# from strands.tools.mcp.mcp_client import MCPClient
from helpers.agent_handler import get_agent
import streamlit as st


# ---- Streamlit UI ---- #
st.title("📚 My Local Agent")

# ---- Steamlit Sidebar ---- #
st.sidebar.header("Settings")
MODEL = st.sidebar.selectbox("Choose Ollama Model", ["llama3.2","deepseek-r1:8b", "gemma3:4b"], index=0)
MAX_HISTORY = st.sidebar.number_input("Max History", 1, 10, 2)
CONTEXT_SIZE = st.sidebar.number_input("Context Size", 1024, 16384, 8192, step=1024)
MAX_ITERATIONS = 4

# ---- Session State Setup ---- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Trim Chat Memory ---- #
def trim_memory():
    while len(st.session_state.chat_history) > MAX_HISTORY * 4:
        st.session_state.chat_history.pop(0)  # Remove oldest messages

# ---- Display Chat History ---- #
# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---- Handle User Input ---- #
if query := st.chat_input("Say something"):
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    # Use the MCP server in a context manager
    # with streamable_http_mcp_client:
    #     # Get the tools from the MCP server
    #     tools = streamable_http_mcp_client.list_tools_sync()
        # Create an agent with the MCP tools
        agent = get_agent()
        response = agent(query)
        answer = response.__str__()
        print(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
        trim_memory()   

