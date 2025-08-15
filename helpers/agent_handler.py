from strands import Agent
from strands_tools import calculator, current_time, python_repl
from strands.models.ollama import OllamaModel


# Create an agent with tools from the strands-tools example tools package
def get_agent():
    # Create an Ollama model instance
    ollama_model = OllamaModel(
        host="http://localhost:11434",  # Ollama server address
        model_id="llama3.2",  # Specify which model to use
    )
    #collect tools 
    tools = [calculator, current_time, python_repl]
    #setup system prompt
    system_prompt = """
    You are a helpful assistant. You can use the tools available to you to help answer the user's question.
    """
    # Create an agent with the MCP tools
    agent = Agent(model=ollama_model, tools=tools, system_prompt=system_prompt)
    return agent
