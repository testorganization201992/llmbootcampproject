# Code Architecture

## System Overview

The LLM Bootcamp project implements a chatbot architecture with 4 applications and separation of concerns.

```mermaid
graph TD
    A[Home.py] --> B[Basic Chatbot]
    A --> C[Agent Chatbot]
    A --> D[Document Chat]
    A --> E[MCP Agent]
    
    B --> F[ui_components.py]
    C --> F
    D --> F
    E --> F
    
    B --> G[langchain_helpers.py]
    C --> G
    D --> G
    E --> G
    
    E --> H[agent_service.py]
    E --> I[server.py]
```

## Core Components

### 1. UI Layer (`ui_components.py`)

**ChatbotUI Class:**
- Chat interface components
- Avatar management with SVG emoji rendering
- Page setup and styling systems

**APIKeyUI Class:**
- API key input forms with validation
- Credential management

### 2. Business Logic (`langchain_helpers.py`)

**Helper Classes:**
- `BasicChatbotHelper`: Conversation AI with memory
- `AgentChatbotHelper`: Web search integration via Tavily
- `RAGHelper`: PDF document processing with FAISS
- `MCPHelper`: Model Context Protocol integration
- `ValidationHelper`: Input validation

### 3. MCP Integration

**agent_service.py:**
- MCPAgent class for MCP client connections
- Multi-server configuration support
- Async agent processing

**server.py:**
- FastMCP server implementation
- LangMem prompt optimization tools
- Stdio transport support

## Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant P as Page
    participant H as Helper
    participant L as LangChain
    participant A as API
    
    U->>P: Input message
    P->>H: Process with helper
    H->>L: Build/invoke chain
    L->>A: API call (OpenAI/Tavily)
    A->>L: Response
    L->>H: Formatted response
    H->>P: Final output
    P->>U: Display message
```

## Memory Architecture

### Session State Management
Each chatbot maintains isolated state:
- `basic_messages`: Basic chatbot conversations
- `agent_messages`: Agent chatbot with search
- `rag_messages`: Document chat conversations
- `mcp_messages`: MCP agent conversations

### Processing Flow
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: User input
    Processing --> Response: Generate with helper
    Response --> Idle: Update session state
    Processing --> Error: API failure
    Error --> Idle: Show error message
```

## MCP Architecture

### Client-Server Model
```mermaid
graph LR
    A[MCP Agent Page] --> B[agent_service.py]
    B --> C[MultiServerMCPClient]
    C --> D[Local server.py<br/>stdio transport]
    C --> E[Remote MCP Server<br/>HTTP transport]
    
    D --> F[LangMem Tools]
    E --> G[External Tools]
```

### Tools Integration
- **Local**: Prompt optimization via LangMem
- **Remote**: External MCP server tools
- **Transport**: Stdio for local, HTTP for remote

## File Organization

```
project_code/
├── Home.py                 # Main app entry
├── pages/                  # Individual chatbot pages
│   ├── 1_Basic_Chatbot.py
│   ├── 2_Chatbot_Agent.py
│   ├── 3_Chat_with_your_Data.py
│   └── 4_MCP_Agent.py
├── ui_components.py        # UI layer
├── langchain_helpers.py    # Business logic
├── agent_service.py        # MCP client
├── server.py              # MCP server
└── requirements.txt        # Dependencies
```

## Key Design Patterns

### Separation of Concerns
- **UI**: Streamlit components, styling, user interaction
- **Business Logic**: LangChain integration, API calls
- **Validation**: Input checking, error handling

### Factory Pattern
- Helper classes create configured LangChain objects
- UI components generate consistent interfaces

### Configuration Management
- API keys injected at runtime
- Model parameters configurable per chatbot
- Environment-based settings

## Technology Integration

### LangChain Components
- **ChatOpenAI**: GPT model integration
- **LangGraph**: Agent workflows with memory
- **FAISS**: Vector storage for documents
- **Tavily**: Web search integration

### Streamlit Features
- Session state for conversation persistence
- File upload for document processing
- UI updates with `st.rerun()`

### MCP Implementation
- **FastMCP**: Server framework
- **LangMem**: Prompt optimization
- **Multi-transport**: Stdio and HTTP support

This architecture provides:
- **Modularity**: Independent components
- **Scalability**: Interfaces for adding features
- **Maintainability**: Separation of concerns
- **Testability**: Isolated business logic