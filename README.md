# My GenAI Apps 
A guide on how to build GenAI chatbots, and agents on your local device, using Ollama, and langchain.

## Overview

This project, contains codes written by me as part of a learning excercise to learn more about Generative AI concepts, and large language models.
This project is a quick utilization of several tools and libraries built by the opensource community. Thank you Ollama, Langchain, and Streamlit. As they say, ``If I have seen further it is by standing on the shoulders of Giants``.


PS: The skeleton of this project was taken from [https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain]. Thanks @isurulkh for your great introduction.

## Example Gen-AI ChatBots, and Agents
1. [chatbot_cli.py](chatbot_cli.py) - A basic gen-ai powered chatbot using ollama, and langchain, that reads data from your local directory, and answers questions based on it.
2. [chatbot_ui.py](chatbot_ui.py) - A simple gen-ai chatbot built using ollama, and langchain, with an ui built using streamlit. 
3. [chatbot_ui_rag.py](chatbot_ui_rag.py) - A simple gen-ai chatbot using ollama, langchain, and ui using streamlit. Enhanced further by a RAG workflow powered by Chroma DB. 
4. [agent_ui_rag.py](agent_ui_rag.py) - A simple Agent built using ollama, langchain, and ui using streamlit. Enhanced further by a RAG workflow powered by Chroma DB, and a set of custom and langchain provided tools 

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
4. Modify the dev.ini configurations, and update the **DATA_FOLDER** variable to map to a directory on your local machine that contains the files that you want your gen-ai agent to read from. The current codebase reads only markdown (*.md) files.
5. Index the files by running 
   ```bash
   python -m helpers.indexer
   ```
6. Run a sample chatbot or agent
   ```bash
   streamlit run chatbot_ui_rag.py
   streamlit run agent_ui_rag.py
   ```

## Contact
For any questions or suggestions, please open an issue in the repository.
