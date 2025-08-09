# My Generative AI Apps 
A step by step guide on how to build Generative AI chatbots, and agents on your local device, using Ollama, Langchain, and Streamlit.

## Overview
This project, contains codes written by me as part of an exercise to learn more about Generative AI, and the Large Language model concepts. This project is a quick utilization of several tools and libraries built by the Opensource community. Thank you Ollama, Langchain, and Streamlit. As they say, ``If I have seen further it is by standing on the shoulders of Giants``.

PS: The skeleton of this project was taken from [https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain]. Thanks @isurulkh for your great introduction.

## Example Gen-AI ChatBots, and Agents

### ChatBots
1. [chatbot_cli.py](chatbot_cli.py) - A basic gen-ai powered chatbot using ollama, and langchain, that reads data from your local directory, and answers questions based on it.
2. [chatbot_ui.py](chatbot_ui.py) - A simple gen-ai chatbot built using ollama, and langchain, with an ui built using streamlit. 
3. [chatbot_ui_rag.py](chatbot_ui_rag.py) - A simple gen-ai chatbot using ollama, langchain, and ui using streamlit. Enhanced further by a RAG workflow powered by Chroma DB.

### Agents
4. [agent_cli.py](agent_cli.py) - A command-line agent implementation using LangChain with tool integration capabilities.
5. [agent_ui_rag.py](agent_ui_rag.py) - A simple Agent built using ollama, langchain, and ui using streamlit. Enhanced further by a RAG workflow powered by Chroma DB, and a set of custom and langchain provided tools.
6. [agent_ui_mcp.py](agent_ui_mcp.py) - An agent with Model Context Protocol (MCP) integration for enhanced context handling.

## Helper Modules and Configuration

### Helper Modules (`helpers/` directory)
- [indexer.py](helpers/indexer.py) - Document indexing utility for creating vector embeddings from markdown files
- [docs_db_handler.py](helpers/docs_db_handler.py) - Database handler for document storage and retrieval using Chroma DB
- [llm_handler.py](helpers/llm_handler.py) - LangChain workflow management and chain creation utilities
- [tools.py](helpers/tools.py) - Custom tools and utilities for agent functionality
- [session_handler.py](helpers/session_handler.py) - Session management for maintaining conversation state
- [config_handler.py](helpers/config_handler.py) - Configuration file parser and handler
- [simple_mcp_server.py](helpers/simple_mcp_server.py) - Simple Model Context Protocol server implementation

### Configuration Files (`config/` directory)
- [dev.ini](config/dev.ini) - Main configuration file containing settings for data folders, models, and other parameters

## How to use this project

### Prerequisites

- Python 3.12 or higher
- Required Python packages (see `requirements.txt`)
- Ollama Installation with llama3.2 installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rakeshsingh/my-ollama-rag-app
   cd my-gen-ai-apps
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download and install Ollama:
   - Visit [https://ollama.ai](https://ollama.ai) to download Ollama for your operating system
   - Install the required LLM model:
   ```bash
   ollama pull llama3.2
   ```

4. Configure the application:
   - Copy and modify the configuration file in `config/dev.ini`
   - Update the **DATA_FOLDER** variable to point to a directory containing your markdown files
   - Adjust other settings like model names, chunk sizes, etc. as needed

5. Index your documents:
   ```bash
   python -m helpers.indexer
   ```
   This will create vector embeddings of your markdown files and store them in the Chroma database.

### Running the Applications

#### ChatBots
- **Command-line chatbot:**
  ```bash
  python chatbot_cli.py
  ```

- **Web-based chatbots:**
  ```bash
  # Basic UI chatbot
  streamlit run chatbot_ui.py
  
  # RAG-enhanced chatbot
  streamlit run chatbot_ui_rag.py
  ```

#### Agents
- **Web-based agents:**
  ```bash
  # RAG-enhanced agent with tools
  streamlit run agent_ui_rag.py
  
  # MCP-enabled agent
  streamlit run agent_ui_mcp.py
  ```

- **Command-line agents:**
  ```bash
  # LangChain-based CLI agent
  python agent_cli_langchain.py
  
  ```

## Contact
For any questions or suggestions, please open an issue in the repository.
