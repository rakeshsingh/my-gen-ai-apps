"""
Configuration file for Strands MCP Agent
"""

import os
from typing import Dict, Any

# Model Configuration
DEFAULT_MODEL = "llama3.2"
AVAILABLE_MODELS = [
    "llama3.2",
    "llama2", 
    "mistral",
    "codellama",
    "phi3",
    "gemma"
]

# MCP Tools Configuration
MCP_TOOLS_CONFIG = {
    "weather_tool": {
        "name": "get_weather",
        "description": "Get current weather information for any location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state/country (e.g., 'New York, NY' or 'London, UK')"
                },
                "units": {
                    "type": "string",
                    "description": "Temperature units: 'celsius' or 'fahrenheit'",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "fahrenheit"
                }
            },
            "required": ["location"]
        }
    },
    "calculator_tool": {
        "name": "calculate",
        "description": "Perform mathematical calculations and expressions",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (supports +, -, *, /, **, parentheses)"
                }
            },
            "required": ["expression"]
        }
    },
    "file_search_tool": {
        "name": "search_files",
        "description": "Search for files and directories in the current directory",
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "File pattern to search for (supports wildcards like *.py, *.txt)"
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Whether to search recursively in subdirectories",
                    "default": False
                }
            },
            "required": ["pattern"]
        }
    },
    "text_analysis_tool": {
        "name": "analyze_text",
        "description": "Analyze text for various metrics like word count, readability, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to analyze"
                },
                "analysis_type": {
                    "type": "string",
                    "description": "Type of analysis to perform",
                    "enum": ["word_count", "character_count", "readability", "sentiment"],
                    "default": "word_count"
                }
            },
            "required": ["text"]
        }
    }
}

# Agent System Message
SYSTEM_MESSAGE = """You are a helpful AI assistant with access to various tools through MCP (Model Context Protocol).

Available tools:
- **get_weather**: Get current weather information for any location worldwide
- **calculate**: Perform mathematical calculations and solve expressions
- **search_files**: Search for files and directories using patterns
- **analyze_text**: Analyze text for various metrics and properties

Guidelines:
1. When users ask questions that can be answered using these tools, use them appropriately
2. Always explain what you're doing when using tools
3. Provide clear, helpful responses based on tool results
4. If a tool fails, explain the issue and suggest alternatives
5. Be conversational and friendly while being informative

Remember to use tools when they can help answer the user's question more accurately or provide real-time information."""

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "Strands MCP Agent Chatbot",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Example prompts for users
EXAMPLE_PROMPTS = [
    {
        "title": "🌤️ Weather Check",
        "prompt": "What's the weather like in San Francisco?",
        "description": "Get current weather information"
    },
    {
        "title": "🧮 Math Calculation", 
        "prompt": "Calculate the compound interest for $1000 at 5% for 3 years: 1000 * (1.05 ** 3)",
        "description": "Perform complex calculations"
    },
    {
        "title": "📁 File Search",
        "prompt": "Find all Python files in the current directory",
        "description": "Search for specific file types"
    },
    {
        "title": "📊 Text Analysis",
        "prompt": "Analyze this text for word count: 'The quick brown fox jumps over the lazy dog'",
        "description": "Get text statistics and analysis"
    },
    {
        "title": "🔍 Advanced Search",
        "prompt": "Search for all markdown files recursively",
        "description": "Recursive file searching"
    }
]

# Environment variables
def get_env_config() -> Dict[str, Any]:
    """Get configuration from environment variables"""
    return {
        "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }
