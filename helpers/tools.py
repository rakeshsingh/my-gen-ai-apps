from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search_tool = search.as_tool(name="search_web", description="Search for information on the web using DuckDuckGo. This tool should be used only when the other tools are not giving any information")  

# Define custom tools
@tool
def calculate_math(expression: str) -> str:
    """Evaluate a mathematical expressions to calculate its result. This tool must be used to evaluate a mathematical calculation question from user."""
    try:
        # Only allow basic mathematical operations for safety
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# retriever_tool = create_retriever_tool(
#     retriever,
#     "local search",
#     "Search for information about myself and my team members. For any questions about me, my team, and my workplace you must use this tool!",
# )

# Define the tools
tools = [calculate_math, search_tool]