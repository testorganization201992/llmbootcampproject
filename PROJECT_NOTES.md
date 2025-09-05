# Claude Code Reference

## Project Overview
LLM Bootcamp Project - Advanced chatbot implementations using OpenAI & LangChain with Streamlit UI.

## Key Commands
```bash
# Run application
streamlit run Home.py

# Install dependencies
pip install -r requirements.txt

# Update packages
pip install --upgrade package_name
```

## Project Architecture
```
├── Home.py                 # Main entry point with project overview
├── pages/
│   ├── 1_Basic_Chatbot.py     # Enterprise-grade stateless chatbot
│   ├── 2_Chatbot_Agent.py     # Web-enabled chatbot with Tavily search
│   └── 3_Chat_with_your_Data.py # RAG chatbot for document Q&A
├── utils.py                # Shared utilities (API keys, chat history)
├── streaming.py            # Real-time response streaming handler
└── requirements.txt        # Python dependencies
```

## Key Components

### utils.py
- `configure_openai_api_key()`: API key setup with sidebar UI
- `enable_chat_history()`: Decorator for chat history management
- `display_msg()`: Message display utility

### streaming.py
- `StreamHandler`: Callback handler for real-time LLM responses

### Basic Chatbot (pages/1_Basic_Chatbot.py)
**Enterprise-grade implementation with:**
- `AdvancedBasicChatbot` class with full configuration
- Response caching with TTL
- Retry logic with exponential backoff
- Input validation and sanitization
- Real-time metrics tracking
- Configurable models (GPT-4o, GPT-4-turbo, etc.)
- Advanced error handling with specific guidance

### Agent Chatbot (pages/2_Chatbot_Agent.py)
- Uses LangGraph for agent workflow
- Tavily search integration for web access
- Streaming responses with state updates

### Document Chat (pages/3_Chat_with_your_Data.py)
- Simple Agentic RAG with LangGraph
- PDF document processing with PyPDF
- FAISS vector store for embeddings
- Query classification (summary vs fact-based)
- Configurable retrieval parameters

## Configuration Patterns
All chatbots follow this pattern:
1. Page config with `st.set_page_config()`
2. API key configuration via `utils.configure_openai_api_key()`
3. Session state management for persistence
4. Error handling with user-friendly messages

## Common Issues & Solutions
- **API Key**: Ensure OpenAI API key is set in sidebar
- **Dependencies**: Run `pip install -r requirements.txt` if imports fail
- **Tavily**: Agent chatbot requires Tavily API key for web search
- **Memory**: Basic chatbot is stateless by design (no memory)

## Development Notes
- All chatbots use `@utils.enable_chat_history` decorator
- Streaming is handled via `StreamHandler` callback
- Error messages include helpful troubleshooting tips
- Configuration is validated in dataclasses (`ChatbotConfig`)
- Metrics are tracked in `ChatMetrics` dataclass

## LangGraph LLM Integration

**Supported Providers:**
- **OpenAI** (primary): gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
- **Anthropic**: Claude models
- **Azure OpenAI**: Enterprise OpenAI models
- **Google Gemini**: Gemini Pro/Flash
- **AWS Bedrock**: Various foundation models

**Model Configuration Options:**
- `temperature`: 0.0-2.0 (creativity vs consistency)
- `max_tokens`: Response length limit
- `timeout`: Request timeout in seconds
- `streaming`: Enable/disable real-time responses
- `disable_streaming`: LangGraph-specific streaming control
- **Tool calling support**: Essential for agent workflows
- **Model fallbacks**: Reliability improvement

**LangGraph Best Practices:**
- **Agent Use**: Choose models with strong reasoning and tool calling
- **RAG Applications**: Models with good semantic understanding
- **Multi-Agent Systems**: Models with complementary strengths
- **Streaming**: Enable for enhanced user experience
- **Evaluation**: Use LangSmith for performance testing

**Current Project Usage:**
- **Basic Chatbot**: Configurable OpenAI models with advanced features
- **Agent Chatbot**: GPT-4o-mini with Tavily search tool integration
- **Document Chat**: GPT-4o-mini for RAG with FAISS retrieval

## Package Versions (Latest)
- langchain-core: 0.3.75
- langchain-openai: 0.3.32
- langchain-community: 0.3.29
- langgraph: 0.6.6 (supports gpt-4o, gpt-4o-mini)
- tiktoken: 0.11.0
- faiss-cpu: 1.12.0