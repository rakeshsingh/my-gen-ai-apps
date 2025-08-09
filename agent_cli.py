from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from helpers.tools import tools

# Define the LLM
llm = ChatOllama(model="llama3.2", temperature=0.8, max_tokens=1000)

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# Example usage
result = agent_executor.invoke({"input": "What is 5 * 7?", "history": []})
print(result)

