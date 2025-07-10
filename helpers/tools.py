from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
@tool
def sum(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a + b

search = DuckDuckGoSearchRun()

# Define the tools
tools = [multiply, sum, search]