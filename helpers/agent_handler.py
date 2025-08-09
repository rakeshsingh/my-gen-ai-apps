from strands import Agent, tool
from strands_tools import calculator, current_time, python_repl
from strands.models.ollama import OllamaModel


# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool
 # Create an Ollama model instance
ollama_model = OllamaModel(
        host="http://localhost:11434",  # Ollama server address
        model_id="llama3.2",  # Specify which model to use
    )
tools =[calculator, current_time, python_repl]
agent = Agent(model=ollama_model, tools=tools)

# Ask the agent a question that uses the available tools
message = """
I have 4 requests:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
4. Output a script that does what we just spoke about!
   Use your python tools to confirm that the script works before outputting it
"""
agent(message)