# AI Chatbot Platform

An enterprise-grade conversational AI platform featuring intelligent agents, document processing, web search integration, and adaptive prompt optimization through Model Context Protocol.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation & Setup

```bash
# Clone and navigate to the project
git clone <repository>
cd agenticai-project/

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

1. **Get Required API Keys**
   - **OpenAI API Key** (Required): Visit https://platform.openai.com/api-keys
   - **Tavily API Key** (For Search Agent): Visit https://tavily.com/ for free account

2. **Create Environment File**
   ```bash
   # Create .env file in project root
   OPENAI_API_KEY=sk-proj-your-actual-openai-key
   TAVILY_API_KEY=tvly-your-actual-tavily-key
   MCP_SERVER_URL=http://localhost:8000
   ```

3. **Start MCP Server** (Optional - for Prompt Optimization)
   ```bash
   # In one terminal
   python server.py
   ```

4. **Launch Application**
   ```bash
   # In another terminal
   streamlit run Home.py
   ```

🎉 **Access**: Open http://localhost:8501 in your browser

## 📁 System Architecture

```
agenticai-project/
├── .streamlit/            # Streamlit configuration
├── assets/                # Static resources (logos, images)
├── config/                # Application configuration
│   ├── __init__.py
│   └── app_config.py      # App settings and page config
├── pages/                 # Streamlit page modules
│   ├── 1_Basic_Chatbot.py
│   ├── 2_Chatbot_Agent.py
│   ├── 3_Chat_with_your_Data.py
│   └── 4_MCP_Agent.py
├── services/              # Business logic and external services
│   ├── __init__.py
│   └── agent_service.py   # Agent orchestration layer
├── ui_components/         # Reusable UI components
│   ├── __init__.py
│   └── home_ui.py         # Home page UI components
├── utils/                 # Utility functions and helpers
│   ├── __init__.py
│   ├── langchain_helpers.py # AI integration utilities
│   └── page_utils.py      # Page discovery and navigation
├── tmp/                   # Temporary file processing
├── Exercises/             # Implementation tutorials
├── User_Guide/            # Documentation and guides
├── Home.py                # Main application entry point
├── server.py              # MCP optimization server
├── healthcheck.py         # Health monitoring
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Platform Capabilities

### Project Organization
The codebase follows a modular, service-oriented architecture with clear separation of concerns:
- **`config/`** - Centralized application configuration and settings
- **`services/`** - Business logic and external service integrations
- **`utils/`** - Reusable utility functions and AI helpers
- **`ui_components/`** - Modular Streamlit UI components for consistent interface design
- **`pages/`** - Individual application modules with specific AI capabilities

### Built-in Applications
1. **Basic Chatbot** - Dialogue system with context memory and customizable personalities *(Requires: OpenAI API key)*
2. **Agent Chatbot** - Web-enabled research and real-time information retrieval *(Requires: OpenAI + Tavily API keys)*
3. **Document Chat** - PDF document analysis and question-answering with RAG *(Requires: OpenAI API key)*
4. **MCP Agent** - Model Context Protocol integration with tool access *(Requires: OpenAI API key + MCP server)*

### Exercise Implementations
1. **Basic Chatbot** - Conversational AI with customizable personalities and response styles
2. **Chatbot Agent** - Web search integration using Tavily API for real-time information
3. **Chat with your Data** - Multi-format document processing (PDF, MD, HTML) with agentic RAG
4. **MCP Prompt Optimizer** - Feedback-driven prompt optimization using LangMem with persistent storage

### Key Technologies
- **Conversation Memory**: LangGraph state management
- **Web Intelligence**: Tavily search integration
- **Document Processing**: FAISS vector storage with multi-format support
- **Protocol Integration**: Model Context Protocol server architecture
- **Optimization**: LangMem-powered prompt enhancement
- **Interface**: Modular Streamlit components

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom component library
- **AI/ML**: OpenAI GPT-4, LangChain orchestration, LangGraph workflows
- **Search**: Tavily API for real-time information retrieval
- **Document Processing**: FAISS vectorstore, multi-format parsing (PDF, MD, HTML)
- **Optimization**: LangMem adaptive prompt tuning
- **Protocols**: Model Context Protocol (MCP) with FastMCP framework
- **Architecture**: Service-oriented design with clean abstractions

## 📚 Documentation

### Operations
- **[User Guides](User_Guide/)** - Application operation procedures and component guides
- **[Architecture Overview](User_Guide/Code_Architecture.md)** - System design specifications
- **[Streamlit Conversion Guide](User_Guide/streamlit_conversion_guide.md)** - Migration documentation

### Development
- **[Implementation Guides](Exercises/)** - Step-by-step component development tutorials
- **[Basic Chatbot Tutorial](Exercises/1_Basic_Chatbot.md)** - Build a simple conversational AI
- **[Agent Integration Guide](Exercises/2_Chatbot_Agent.md)** - Add web search capabilities
- **[RAG Implementation](Exercises/3_Chat_with_your_Data.md)** - Document processing and retrieval
- **[MCP Integration](Exercises/4_MCP_Prompt_Optimizer.md)** - Model Context Protocol setup

## Deployment

### System Setup
```bash
git clone <repository>
cd agenticai-project/
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-proj-your-actual-openai-key
TAVILY_API_KEY=tvly-your-actual-tavily-key  # Optional, for web search
MCP_SERVER_URL=http://localhost:8000        # Optional, for MCP features
```

### Launch
```bash
# Start MCP server (optional, for prompt optimization)
python server.py

# In another terminal, start the main application
streamlit run Home.py
```

### Access
- Navigate to http://localhost:8501
- Explore 4 different AI interfaces
- Configure agents for specific use cases
- Upload documents for analysis

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "API key not found" | Check `.env` file exists in project root |
| "MCP Server offline" | Run `python server.py` in separate terminal |
| "Invalid API key" | Verify API keys are correct and active |
| Import errors | Run `pip install -r requirements.txt` |

## 🔒 Security Notes
- Never commit your `.env` file to git
- Keep API keys private and rotate regularly
- Use environment variables for production deployments