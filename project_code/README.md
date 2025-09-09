# LLM Bootcamp Project - Streamlit Application

A comprehensive chatbot application demonstrating advanced AI features with custom personalities, multi-tool agents, and document processing capabilities.

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run Home.py
```

### Streamlit Cloud Deployment
1. Upload this entire `project_code` folder to your GitHub repository
2. Connect your GitHub repo to Streamlit Cloud
3. Set `Home.py` as your main file
4. Deploy!

## 📁 Project Structure

```
project_code/
├── Home.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── langchain_helpers.py       # AI/ML helper functions
├── ui_components.py          # Streamlit UI components
├── .streamlit/               # Theme configuration (dark theme)
│   └── config.toml          # Custom styling settings
└── pages/
    ├── 1_Basic_Chatbot.py    # Assignment 1: Custom AI personalities
    ├── 2_Chatbot_Agent.py    # Assignment 2: Multi-tool research agent  
    ├── 3_Chat_with_your_Data.py  # Assignment 3: RAG document chat
    └── 4_MCP_Agent.py        # Bonus: Model Context Protocol
```

## 🎯 Features

### Assignment 1: Custom AI Personalities 🎭
- **4 AI Personalities**: Default, Creative, Analytical, Conversational
- **Smart Memory**: LangGraph-powered memory that extracts user info
- **Dynamic UI**: Personality selector and memory status panel
- **Real-time Config**: See AI settings change in the sidebar

### Assignment 2: Multi-Tool Research Agent 🌐  
- **Web Search**: Real-time internet search via Tavily
- **Wikipedia**: Encyclopedic knowledge lookup
- **Arxiv Papers**: Academic research paper search
- **Intelligent Routing**: AI decides which tool(s) to use

### Assignment 3: Document Chat System 📄
- **Multi-Format**: PDF, TXT, DOCX support
- **RAG Pipeline**: Advanced retrieval-augmented generation
- **Smart Chunking**: Optimized document processing
- **Query Classification**: Summary vs fact-based responses

## 🔧 Setup Instructions

### Required API Keys
You'll need these API keys to use all features:

1. **OpenAI API Key** (Required for all features)
   - Get it from: https://platform.openai.com/api-keys
   - Format: `sk-proj-...`

2. **Tavily API Key** (Required for Agent search)
   - Get it from: https://tavily.com
   - Format: `tvly-...`

### Environment Variables (Optional)
You can set these as Streamlit secrets or environment variables:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-proj-..."
TAVILY_API_KEY = "tvly-..."
```

## 🎓 Educational Value

This project demonstrates:
- **Modular Architecture**: Clean separation of concerns
- **LangChain Integration**: Professional AI application development
- **LangGraph Workflows**: Advanced state management and memory
- **Streamlit UI/UX**: Modern, responsive web interfaces
- **Multi-Modal AI**: Text, search, and document processing
- **Production Patterns**: Error handling, validation, testing

## 🧪 Testing Features

### Test Assignment 1 (Basic Chatbot)
1. Go to "Basic AI Chat"
2. Try different personalities (Creative, Analytical, etc.)
3. Enable "Smart Memory" and tell it about yourself
4. Ask follow-up questions to test memory

### Test Assignment 2 (Agent)  
1. Go to "Search Enabled Chat"
2. Ask: "What's happening with AI in 2024?" (web search)
3. Ask: "Tell me about Einstein" (Wikipedia)
4. Ask: "Find papers about transformers" (Arxiv)

### Test Assignment 3 (RAG)
1. Go to "RAG" 
2. Upload a PDF, TXT, or DOCX file
3. Ask summary questions: "Summarize this document"
4. Ask specific questions: "What dates are mentioned?"

## 📦 Dependencies

All required packages are listed in `requirements.txt`:
- Core: `streamlit`, `langchain-*`, `langgraph`
- AI: `langchain-openai`, `langchain-anthropic` 
- Tools: `tavily-python`, `wikipedia`, `arxiv`
- Documents: `pypdf`, `python-docx`, `faiss-cpu`

## 🚨 Troubleshooting

**Import Errors**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

**API Key Errors**: Double-check your API key format and validity

**File Upload Issues**: Try smaller files first, check file format support

**Memory Issues**: Restart the app if smart memory seems stuck

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

## 🤝 Contributing

This is an educational project! Feel free to:
- Add new AI personalities
- Implement additional tools for the agent
- Support more document formats
- Improve the UI/UX
- Add new chatbot types

## 📄 License

Educational use - perfect for learning AI application development!

---

**Happy Learning! 🎓🚀**