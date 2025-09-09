# Exercise 2: Chatbot Agent - Multi-Source Research System

## Objective
Extend the basic agent with multiple research tools including web search, Wikipedia, and academic papers.

## Prerequisites
- OpenAI API key
- Tavily API key

---

## Implementation

### Step 1: Install Dependencies
Add to `requirements.txt`:
```
wikipedia>=1.4.0
arxiv==2.2.0
```

Run: `pip install wikipedia>=1.4.0 arxiv==2.2.0`

### Step 2: Add Multi-Tool Agent
**File:** `project_code/langchain_helpers.py`  
**Location:** Inside `AgentChatbotHelper` class, add new method after `setup_agent()`

```python
@staticmethod
def setup_agent_with_research_tools(openai_api_key: str, tavily_api_key: str) -> Any:
    """Setup agent with Tavily web search, Wikipedia, and Arxiv research tools"""
    from langchain_tavily import TavilySearch
    from langgraph.prebuilt import create_react_agent
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
    from langchain.agents import Tool
    
    # Web search for current information
    tavily_search = TavilySearch(
        max_results=5,
        topic="general", 
        tavily_api_key=tavily_api_key,
    )
    
    # Wikipedia for encyclopedic knowledge
    wiki_tool = Tool(
        name="wikipedia",
        func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
        description="Search Wikipedia for comprehensive information on topics, people, events.",
    )
    
    # Arxiv for academic research papers
    arxiv_tool = Tool(
        name="arxiv", 
        func=ArxivAPIWrapper().run,
        description="Find academic research papers and scientific publications.",
    )
    
    tools = [tavily_search, wiki_tool, arxiv_tool]
    
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, api_key=openai_api_key)
    return create_react_agent(llm, tools)
```

### Step 3: Update UI Integration
**File:** `project_code/pages/2_Chatbot_Agent.py`  
**Location:** Replace the `setup_agent()` method in `ChatbotTools` class

```python
def setup_agent(self) -> Any:
    """Setup the web search-enabled agent with research tools."""
    openai_key = st.session_state.get("agent_openai_key", "")
    tavily_key = st.session_state.get("agent_tavily_key", "")
    return AgentChatbotHelper.setup_agent_with_research_tools(openai_key, tavily_key)
```

**Location:** Update subtitle in `render_page_header()` call (around line 135)
```python
"AI agent with web search, Wikipedia, and research paper capabilities"
```

---

## Usage

1. Run `streamlit run Home.py`
2. Navigate to Chatbot Agent page
3. Enter both OpenAI and Tavily API keys
4. Try queries that utilize different tools:
   - **Web search**: "What's happening with AI in 2025?"
   - **Wikipedia**: "Tell me about Marie Curie's discoveries"
   - **Research**: "Find recent papers about large language models"

## Key Learning Points

- **Tool composition** enables multi-source information gathering
- **ReAct agents** automatically select appropriate tools based on queries
- **Tool descriptions** guide the agent's decision-making process
- **Streaming responses** show the agent's reasoning process in real-time