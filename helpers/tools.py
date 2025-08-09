from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain.tools.retriever import create_retriever_tool
from helpers import config_handler, indexer
from strands_tools import calculator, current_time, python_repl

EMBEDDING_MODEL = config_handler.get_embedding_model()
PERSISTENT_DIRECTORY = config_handler.get_db_path()


# Define custom tools

#------------------ setup a custom search tool -----------------------#
search = DuckDuckGoSearchRun()
search_tool = search.as_tool(name="search_web", description="Search for information on the web using DuckDuckGo. This tool should be used only when the other tools are not giving any information")  

#------------------ setup a wiikipedia tool -----------------------#
wikipedia_api_wrapper = WikipediaAPIWrapper(
    lang="en",  # Specify English Wikipedia
    top_k_results=1  # Get only the top result
)
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api_wrapper)
wikipedia_tool = wikipedia.as_tool(name="wikidata", description="Search for information on Wikidata when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query.This tool should be used only when the other tools are not giving any information")

#---------- setup a math expression evaluator  tool ------------------#
@tool
def math_tool(expression: str) -> str:
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

#---------- setup local retriever tool ------------------#
retriever = indexer.setup_retriever(persistent_directory=PERSISTENT_DIRECTORY, embedding_model=EMBEDDING_MODEL)
retriever_tool = create_retriever_tool(
    retriever,
    "local search",
    "Search for information about myself and my team members. For any questions about me, my team, and my workplace you must use this tool!",
)

# Define the tools
tools = [math_tool, wikipedia_tool, search_tool, retriever_tool, calculator, current_time, python_repl]