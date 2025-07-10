# Guide and tutorial to build Generative AI bots, and agents on your local device

## Overview

This project, contains codes written by me as part of a learning excercise to learn more about Generative AI concepts, and large language models. 

The skeleton of this repository was taken from [https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain]. Thanks @isurulkh for your great introduction.

## Example Gen-AI ChatBots, and Agents
1.  A basic gen-ai powered chatbot using ollama, and langchain, that reads data from your local directory, and answers questions based on it [chatbot_cli.py](chatbot_cli.py)
    - modify the dev.ini configurations, and update the **DATA_FOLDER** variable to map to a directory on your local machine that contains the files that you want your gen-ai agent to read from
2. Build a basic gen-ai chatbot, and a ui using ollama, langchain, and streamlit. [chatbot_ui.py](chatbot_ui.py)
3. Build a basic gen-ai chatbot using ollama, langchain, and ui using streamlit. Enhance it further by a RAG workflow powered by Chroma DB. [chatbot_ui_rag.py](chatbot_ui_rag.py)
4. A simple Agent built using ollama, langchain, and ui using streamlit. Enhanced further by a RAG workflow powered by Chroma DB, and a set of custom and langchain provided tools [agent_ui_rag.py](agent_ui_rag.py)

## How to use this project
### Prerequisites

- Python 3.12 or higher
- Required Python packages (see `requirements.txt`)
- Ollama Installation with llama3.2 installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rakeshsingh/my-ollama-rag-app
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Ollama and install LLM using Ollama:
   ```bash
   ollama pull llama3.2
   ```
4. run a sample chatbot or agent
   ```bash
   streamlit run chatbot_ui_rag.py
   ```

### Additional usage, and configuration details for each chatbot or an agent
1. [chatbot_cli.py](chatbot_cli.py)
    - modify the dev.ini configurations, and update the **DATA_FOLDER** variable to map to a directory on your local machine that contains the files that you want your gen-ai agent to read from
2.  [chatbot_ui.py](chatbot_ui.py)
   - streamlit run agent_chat_ui.py
3. [chatbot_ui_rag.py](chatbot_ui_rag.py)
   - streamlit run agent_chat_ui_rag.py


## Contact
For any questions or suggestions, please open an issue in the repository.
