## Overview

This project, contains codes written by me as part of a learning excercise to learn more about Generative AI concepts, and large language models. 

The skeleton of this repository was taken from [https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain]. Thanks @isurulkh for your great introduction.

## Example Gen-AI Bots/Agents
1.  Build a basic gen-ai chat model using ollama, and langchain, that reads data from your local directory, and answers questions based on it [[agent_cli.py]]
    - modify the dev.ini configurations, and update the **DATA_FOLDER** variable to map to a directory on your local machine that contains the files that you want your gen-ai agent to read from
2. Build a basic gen-ai chat bot, and a ui using ollama, langchain, and streamlit. [agent_chat_ui.py](agent_chat_ui.py)
3. Build a basic gen-ai chat bot using ollama, langchain, and ui using streamlit. Enhance it further by a RAG workflow powered by Chroma DB. [agent_chat_ui_rag.py](agent_chat_ui_rag.py)


## Getting Started

### Prerequisites

- Python 3.12 or higher
- Required Python packages (see `requirements.txt`)
- Ollama Installation with llama3.2 installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/isurulkh/RAG-App-using-Ollama-and-LangChain.git
   cd RAG-App-using-Ollama-and-LangChai
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Ollama and install LLM using Ollama:
   ```bash
   ollama pull llama3.2
   ```

### Usage
1. agent_cli.py - 
2. agent_chat_ui.py - 
3. agent_chat_ui_rag.py - 


## Contact

For any questions or suggestions, please open an issue in the repository.
