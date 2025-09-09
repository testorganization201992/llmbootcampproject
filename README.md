# LLM Bootcamp Project

A comprehensive chatbot application demonstrating advanced AI features with custom personalities, multi-tool agents, document processing capabilities, and Model Context Protocol integration.

## 🚀 Quick Start

Navigate to the `project_code/` directory for the complete Streamlit application:

```bash
cd project_code/
pip install -r requirements.txt
streamlit run Home.py
```

## 📁 Project Structure

```
├── project_code/          # Complete Streamlit application
│   ├── .streamlit/        # Streamlit configuration
│   ├── assets/            # Static assets (logos, images)
│   ├── pages/             # Individual chatbot pages
│   ├── tmp/               # Temporary files for document processing
│   ├── Home.py            # Main application entry point
│   ├── server.py          # MCP server for prompt optimization
│   ├── requirements.txt   # Python dependencies
│   ├── ui_components.py   # Reusable UI components
│   ├── langchain_helpers.py # LangChain integration helpers
│   └── agent_service.py   # MCP agent service
├── Exercises/             # Hands-on coding exercises
│   ├── 1_Basic_Chatbot.md
│   ├── 2_Chatbot_Agent.md
│   ├── 3_Chat_with_your_Data.md
│   └── 4_MCP_Prompt_Optimizer.md
├── User_Guide/            # User guides for each chatbot
│   ├── 1_Basic_Chatbot.md
│   ├── 2_Chatbot_Agent.md
│   ├── 3_Chat_with_your_Data.md
│   └── 4_MCP_Agent.md
├── docs/                  # Technical documentation
│   ├── Code_Architecture.md # Technical implementation details
│   └── streamlit_conversion_guide.md
└── README.md              # This file
```

## Project Overview

### Implemented Applications:
1. **Basic Chatbot** - Conversational AI with memory
2. **Agent Chatbot** - Web search integration 
3. **Document Chat** - RAG with PDF support
4. **MCP Agent** - Model Context Protocol integration

### Exercise Projects:
- **Exercise 4: MCP Prompt Optimizer** - Build prompt optimization using LangMem

### Technical Features:
- LangGraph conversation memory
- Tavily web search integration
- FAISS vector storage for documents
- Model Context Protocol server
- Modular UI components

## 📚 Documentation & Learning

### For Users:
- **[User Guides](User_Guide/)** - How to use each chatbot interface
- **[Project Code README](project_code/README.md)** - Deployment instructions

### For Developers:
- **[Exercises](Exercises/)** - Step-by-step coding exercises
- **[Code Architecture](docs/Code_Architecture.md)** - Technical implementation details

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom UI components
- **AI/ML**: OpenAI GPT models, LangChain, LangGraph
- **Search**: Tavily API for real-time web search
- **Document Processing**: FAISS vectorstore, PDF parser
- **Memory**: LangMem for prompt optimization
- **Protocols**: Model Context Protocol (MCP) with FastMCP
- **Architecture**: Modular design with clean separation of concerns

## 🎓 Educational Use

Perfect for:
- Learning AI application development
- Understanding LangChain and LangGraph patterns
- Exploring Model Context Protocol
- Building production-ready chatbot systems
- Hands-on experience with RAG and agent architectures

## 🚀 Getting Started

1. **Clone the repository**
2. **Navigate to project_code/** 
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Configure API keys** (OpenAI, Tavily)
5. **Run the app**: `streamlit run Home.py`
6. **Explore the 4 different chatbot implementations**
7. **Try the exercises** to build your own versions!