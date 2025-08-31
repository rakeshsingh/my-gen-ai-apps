from strands import Agent
from strands_tools import calculator, current_time, python_repl
from strands.tools.mcp.mcp_client import MCPClient
from strands.models.ollama import OllamaModel
from mcp.client.streamable_http import streamablehttp_client


def create_streamable_http_transport():
    return streamablehttp_client("http://localhost:8000/mcp/")

# Create an agent with tools from the strands-tools example tools package
def get_agent():
    # Create an Ollama model instance
    ollama_model = OllamaModel(
        host="http://localhost:11434",  # Ollama server address
        model_id="llama3.2",  # Specify which model to use
    )
    #collect tools 
    builtin_tools = [calculator, current_time, python_repl]
    streamable_http_mcp_client = MCPClient(create_streamable_http_transport)
    with streamable_http_mcp_client:
        # Get the tools from the MCP server
        mcp_tools = streamable_http_mcp_client.list_tools_sync()
    tools = builtin_tools + mcp_tools
    #setup system prompt
    system_prompt = """
    You are a helpful assistant. You can use the tools available to you to help answer the user's question.
    """
    # Create an agent with the MCP tools
    agent = Agent(model=ollama_model, tools=tools, system_prompt=system_prompt)
    return agent
