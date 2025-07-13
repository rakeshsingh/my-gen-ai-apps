from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from helpers.tools import tools  # Assuming you have a tools module with custom tools defined
# from langchain_core.messages import AIMessage, HumanMessage
import requests
import json
from typing import Optional

# Initialize the language model
llm =  ChatOllama(
        model='llama3.2', 
        temperature=0.8, 
        num_predict=256, 
        keep_alive=-1,
        streaming=True, 
        max_tokens=1024, 
        return_source_documents=True  
        )

# List of available tools
tools = tools

# Create the agent prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that can use various tools to answer questions.
    
    You have access to the following tools:
    - get_weather: Get weather information for a location
    - calculate_math: Perform mathematical calculations
    - search: Search for information on the web
    
    When using tools, make sure to:
    1. Choose the most appropriate tool for the question
    2. Provide clear and helpful responses
    3. If you can't find the exact information, explain what you found instead
    
    Always be helpful and provide detailed explanations when possible."""),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# Create the agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Create the AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Set to True to see the agent's reasoning process
    handle_parsing_errors=True,
    max_iterations=5  # Prevent infinite loops
)

# Example usage
def main():
    print("LangChain AgentExecutor Example")
    print("=" * 40)
    
    # Example queries
    queries = [
        "What's the weather like in New York?",
        "Calculate 15 * 24 + 100",
        "Tell me about Python programming",
        "Search for the latest news on AI",
        "Who is the president of the United States?",
        "What's 2 + 2 and what's the weather in London?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 20)
        
        try:
            # Execute the query
            response = agent_executor.invoke({"input": query})
            print(f"Response: {response['output']}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 40)

# Interactive mode
def interactive_mode():
    print("\nInteractive Mode - Type 'quit' to exit")
    print("=" * 40)
    
    while True:
        user_input = input("\nEnter your question: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            response = agent_executor.invoke({"input": user_input})
            print(f"\nAgent: {response['output']}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Run example queries
    main()
    
    # Uncomment the line below to run in interactive mode
    # interactive_mode()
