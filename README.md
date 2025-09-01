# My Generative AI Apps 🤖

Build powerful AI chatbots and agents locally using **Ollama**, **LangChain**, and **Streamlit**.

## 🎯 What You'll Build

This repository contains complete implementations of AI chatbots and agents that run entirely on your local machine. Perfect for learning generative AI concepts hands-on.

**Key Technologies:**
- 🦙 **Ollama** - Local LLM runtime
- 🔗 **LangChain** - AI application framework  
- 🎨 **Streamlit** - Web UI framework
- 📊 **Chroma DB** - Vector database for RAG

> *"If I have seen further, it is by standing on the shoulders of Giants"*

**Credits:** Initial project structure inspired by [@isurulkh's RAG App](https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain)

## 🚀 Available Applications

### 💬 ChatBots
| Application | Description | Features |
|-------------|-------------|----------|
| [chatbot_cli.py](chatbot_cli.py) | Command-line chatbot | Basic Q&A using local documents |
| [chatbot_ui.py](chatbot_ui.py) | Web-based chatbot | Simple Streamlit interface |
| [chatbot_ui_rag.py](chatbot_ui_rag.py) | RAG-enhanced chatbot | Advanced context retrieval with Chroma DB |

### 🤖 Agents
| Application | Description | Features |
|-------------|-------------|----------|
| [agent_cli.py](agent_cli.py) | Command-line agent | Tool integration capabilities |
| [agent_ui_rag.py](agent_ui_rag.py) | RAG-enhanced agent | Custom tools + RAG workflow |
| [agent_ui_mcp.py](agent_ui_mcp.py) | MCP-enabled agent | Weather tools via Model Context Protocol |


## 📁 Project Structure

### Helper Modules (`helpers/` directory)
- [indexer.py](helpers/indexer.py) - Document indexing utility for creating vector embeddings from markdown files
- [llm_handler.py](helpers/llm_handler.py) - LangChain workflow management and chain creation utilities
- [tools.py](helpers/tools.py) - Custom tools and utilities for agent functionality
- [session_handler.py](helpers/session_handler.py) - Session management for maintaining conversation state
- [config_handler.py](helpers/config_handler.py) - Configuration file parser and handler
- [agent_handler.py](helpers/agent_handler.py) - Agent workflow management and execution utilities
- [simple_mcp_server.py](helpers/simple_mcp_server.py) - Simple Model Context Protocol server implementation

### Configuration Files (`config/` directory)
- [dev.ini](config/dev.ini) - Main configuration file containing settings for data folders, models, and other parameters

## 🛠️ Quick Start

### Prerequisites

- Python 3.12 or higher
- Ollama Installation with llama3.2 installed

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rakeshsingh/my-gen-ai-apps/
   ```

2. **Setup the development environment and install the required packages:**
   ```bash
   python3 -m venv ~/.venv/my-gen-ai-apps
   source ~/.venv/my-gen-ai-apps/bin/activate
   cd my-gen-ai-apps
   pip install -r requirements.txt
   ```

3. **Download and install Ollama:**
   - Visit [https://ollama.ai](https://ollama.ai) to download Ollama for your operating system
   - Install the required LLM model:
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   ollama pull gemma3:4b
   ```

4. **Configure the application:**
   - Copy and modify the configuration file in `config/dev.ini`
   - Update the **DATA_FOLDER** variable to point to a directory containing your markdown files
   - Adjust other settings like model names, chunk sizes, etc. as needed

5. **Index your documents:**
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
  python agent_cli.py
  ```

## Contact
For any questions or suggestions, please open an issue in the repository.
