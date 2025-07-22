from strands import Agent
from strands_tools import calculator
from strands.models.ollama import OllamaModel


# Ollama
ollama_model = OllamaModel(
  host="http://localhost:11434",
  model_id="llama3.2"
)
agent = Agent(model=ollama_model, tools=[calculator])
agent("Tell me about Agentic AI")
agent("What is the square root of 1764")


