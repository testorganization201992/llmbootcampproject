# LLM Bootcamp Project - Let's Build Some Cool Stuff! 🚀

> 📚 **Quick heads up:** If you want the deep technical details, check out [Code_Architecture.md](./Code_Architecture.md) - but you can totally jump right into these assignments!

---

# Assignment 1: Build Custom AI Personalities! 

## What We're Building
You're going to create 3 new AI personality types for the chatbot and add a cool selector so users can switch between them on the fly. By the end, you'll have a chatbot that can be creative, analytical, or conversational - whatever the user wants!

## What You Need
- Python with Streamlit 
- OpenAI API key
- Basic Python skills

---

## Part 1: Create Your AI Personalities

### Task 1.1: Add New Configuration Methods
Jump into `langchain_helpers.py` and add these three new methods to the `BasicChatbotHelper` class:

```python
@staticmethod
def get_creative_config() -> Dict[str, Any]:
    """Configuration optimized for creative and imaginative responses"""
    return {
        "model": "gpt-4o-mini",
        "temperature": 1.2,              # High creativity
        "max_tokens": 3000,              # Extended response length
        "top_p": 0.9,                    # Diverse token selection
        "frequency_penalty": 0.3,        # Reduce repetition
        "presence_penalty": 0.6,         # Encourage topic diversity
        "response_style": "Creative"
    }

@staticmethod
def get_analytical_config() -> Dict[str, Any]:
    """Configuration for precise, analytical responses"""
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.1,              # Highly focused
        "max_tokens": 2500,              # Comprehensive but controlled
        "top_p": 0.95,                   # Precise token selection
        "frequency_penalty": 0.0,        # Allow technical repetition
        "presence_penalty": 0.0,         # Stay on topic
        "response_style": "Technical"
    }

@staticmethod
def get_conversational_config() -> Dict[str, Any]:
    """Configuration for natural, friendly conversations"""
    return {
        "model": "gpt-4o-mini", 
        "temperature": 0.8,              # Balanced creativity
        "max_tokens": 2000,              # Natural response length
        "top_p": 0.85,                   # Varied but focused
        "frequency_penalty": 0.2,        # Slight repetition reduction
        "presence_penalty": 0.3,         # Moderate topic variation
        "response_style": "Casual"
    }
```

### Task 1.2: Build the Personality Selector
Now let's add a cool UI selector! In `pages/1_Basic_Chatbot.py`, replace the boring static config (around line 72) with this dynamic selector:

```python
# Create personality selector in sidebar
st.sidebar.markdown("### 🎭 Choose AI Personality")
config_type = st.sidebar.selectbox(
    "Pick your AI's vibe:",
    ["Default", "Creative", "Analytical", "Conversational"],
    key="basic_config_type"
)

# Map personalities to configs
config_map = {
    "Default": BasicChatbotHelper.get_default_config(),
    "Creative": BasicChatbotHelper.get_creative_config(),
    "Analytical": BasicChatbotHelper.get_analytical_config(), 
    "Conversational": BasicChatbotHelper.get_conversational_config()
}

config = config_map[config_type]

# Show what's under the hood
with st.sidebar.expander("🔧 Current Settings"):
    st.json(config)
```

---

## Part 2: Test Your Personalities

### Task 2.1: Run Your Creation
1. Fire up the app: `streamlit run Home.py`
2. Go to Basic Chatbot
3. Enter your API key
4. Check out that shiny new personality selector in the sidebar!

### Task 2.2: Personality Battle Test
Ask the same question in each mode and see how different they are:

**The Question:** "Explain artificial intelligence"

Try each personality:
- **Default**: Should be balanced and informative
- **Creative**: Expect wild analogies and creative explanations  
- **Analytical**: Very technical and structured
- **Conversational**: Like chatting with a friend

### Task 2.3: Specialized Tests
Now hit each personality with their "dream question":

- **Creative**: "Write a story about a robot learning to paint"
- **Analytical**: "Compare neural networks vs decision trees - pros and cons"
- **Conversational**: "What's your favorite programming language and why?"

Document the differences - they should be pretty dramatic!

---

## Part 3: Test the Memory System

### Task 3.1: Memory Experiments
Let's make sure the chatbot actually remembers your conversation! Try these tests:

**🧠 Context Test:**
1. Say: "My name is [YourName] and I work in [your field]"
2. Chat about something else for a bit
3. Then ask: "What do you know about my job?"
4. It should remember what you told it earlier!

**🔗 Reference Test:**
1. Ask: "Tell me about machine learning"
2. Then ask: "What are the main challenges with it?"
3. Notice how it knows "it" refers to machine learning from your previous question

**🎯 Multi-topic Test:**
1. Discuss 3 different topics (like Python, cooking, and movies)
2. Go back to the first topic with: "Going back to what we discussed about Python..."
3. The AI should remember the earlier Python conversation

**🔄 Session Boundary Test:**
1. Have a conversation, then refresh the page
2. Your conversation should still be there (same browser session)
3. Open a new tab/browser - this should start fresh (different session)

### Task 3.2: Understanding How Memory Works
The chatbot uses Streamlit's session state to remember your conversations:

1. **Each message is stored** with a role ("user" or "assistant") and content
2. **Full history is sent** to the AI with each new message
3. **Unique prefixes** keep different chatbot pages separate (`basic_`, `agent_`, `rag_`)
4. **Processing flags** prevent duplicate responses when you send messages

Try having conversations on different chatbot pages - they should each remember their own separate conversations!

---

## Part 4: Add Smart Memory with LangGraph (Advanced)

Want to make your chatbot smarter about remembering things? Let's add a simple LangGraph workflow that can extract user info and create conversation summaries!

### Task 4.1: Create the Smart Memory System
Add this new method to `BasicChatbotHelper` in `langchain_helpers.py`:

```python
@staticmethod
def build_smart_memory_chain(config: Dict[str, Any], api_key: str = None) -> Any:
    """Build LangGraph chain that extracts user info and summarizes conversations"""
    from langgraph.graph import StateGraph, END
    from typing_extensions import TypedDict
    
    # Define what our smart memory remembers
    class SmartMemoryState(TypedDict):
        messages: list
        user_info: dict  # Store user name, job, interests, etc.
        conversation_summary: str
        current_input: str
        response: str
    
    # Configure the LLM
    llm_kwargs = {
        "model": config["model"],
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"],
        "streaming": False
    }
    
    if api_key:
        llm_kwargs["api_key"] = api_key
        
    llm = ChatOpenAI(**llm_kwargs)
    
    # Node 1: Generate response with memory context
    def generate_response(state: SmartMemoryState):
        # Build context from memory
        context_parts = []
        
        # Add user info if we have any
        if state.get("user_info"):
            user_context = ", ".join([f"{k}: {v}" for k, v in state["user_info"].items()])
            context_parts.append(f"What I know about you: {user_context}")
        
        # Add conversation summary if available
        if state.get("conversation_summary"):
            context_parts.append(f"Our conversation so far: {state['conversation_summary']}")
        
        # Build the prompt
        system_prompt = f"""You are a helpful AI assistant with memory. 
        
        {'. '.join(context_parts) if context_parts else 'This is the start of our conversation.'}
        
        Respond naturally and reference previous context when relevant."""
        
        # Get recent messages for context (last 5 to keep it manageable)
        recent_messages = state["messages"][-5:] if state["messages"] else []
        
        messages_for_llm = [("system", system_prompt)]
        for msg in recent_messages:
            role = "human" if msg["role"] == "user" else "assistant"
            messages_for_llm.append((role, msg["content"]))
        
        # Add current input
        messages_for_llm.append(("human", state["current_input"]))
        
        response = llm.invoke(messages_for_llm)
        return {"response": response.content}
    
    # Node 2: Extract user information
    def extract_user_info(state: SmartMemoryState):
        current_info = state.get("user_info", {})
        user_input = state["current_input"].lower()
        
        # Simple patterns to extract info
        if "my name is" in user_input:
            parts = user_input.split("my name is")
            if len(parts) > 1:
                name = parts[1].split()[0].strip(".,!?").title()
                current_info["name"] = name
        
        if any(phrase in user_input for phrase in ["i work", "i'm a", "my job"]):
            for phrase in ["i work as", "i work in", "i'm a", "i am a", "my job is"]:
                if phrase in user_input:
                    parts = user_input.split(phrase)
                    if len(parts) > 1:
                        job = parts[1].split(".")[0].split(",")[0].strip()
                        current_info["job"] = job
                    break
        
        if any(phrase in user_input for phrase in ["i like", "i love", "i enjoy"]):
            for phrase in ["i like", "i love", "i enjoy"]:
                if phrase in user_input:
                    parts = user_input.split(phrase)
                    if len(parts) > 1:
                        interest = parts[1].split(".")[0].split(",")[0].strip()
                        current_info["interests"] = current_info.get("interests", [])
                        if interest not in current_info["interests"]:
                            current_info["interests"].append(interest)
                    break
        
        return {"user_info": current_info}
    
    # Node 3: Update conversation summary (every 10 messages)
    def update_summary(state: SmartMemoryState):
        messages = state["messages"]
        
        # Only update summary every 10 messages to save API calls
        if len(messages) % 10 == 0 and len(messages) > 0:
            # Get recent conversation
            recent_conversation = []
            for msg in messages[-10:]:
                role = "You" if msg["role"] == "user" else "Assistant"
                recent_conversation.append(f"{role}: {msg['content'][:100]}...")
            
            summary_prompt = f"""Briefly summarize this conversation in 2-3 sentences, focusing on main topics discussed:

{chr(10).join(recent_conversation)}

Current summary: {state.get('conversation_summary', 'None')}

New summary:"""
            
            try:
                summary_response = llm.invoke([("human", summary_prompt)])
                return {"conversation_summary": summary_response.content}
            except:
                # If summary fails, keep the old one
                pass
        
        return {"conversation_summary": state.get("conversation_summary", "")}
    
    # Build the graph
    graph = StateGraph(SmartMemoryState)
    
    # Add our nodes
    graph.add_node("generate", generate_response)
    graph.add_node("extract_info", extract_user_info)
    graph.add_node("summarize", update_summary)
    
    # Set up the flow: generate -> extract -> summarize -> end
    graph.set_entry_point("generate")
    graph.add_edge("generate", "extract_info")
    graph.add_edge("extract_info", "summarize")
    graph.add_edge("summarize", END)
    
    return graph.compile()
```

### Task 4.2: Add Memory Toggle to the UI
In `pages/1_Basic_Chatbot.py`, add this after the personality selector:

```python
# Add smart memory toggle
use_smart_memory = st.sidebar.checkbox(
    "🧠 Enable Smart Memory", 
    help="AI will remember things about you and summarize conversations"
)

if use_smart_memory:
    # Initialize smart memory state
    if "smart_memory_state" not in st.session_state:
        st.session_state.smart_memory_state = {
            "messages": [],
            "user_info": {},
            "conversation_summary": ""
        }
    
    # Build smart memory chain if needed
    if api_key and ("smart_memory_chain" not in st.session_state or 
                   st.session_state.get("smart_memory_config") != config_type):
        st.session_state.smart_memory_chain = BasicChatbotHelper.build_smart_memory_chain(config, api_key)
        st.session_state.smart_memory_config = config_type
    
    # Show what the AI remembers about you
    with st.sidebar.expander("🧠 What I Remember"):
        memory_state = st.session_state.smart_memory_state
        
        if memory_state["user_info"]:
            st.write("**About You:**")
            for key, value in memory_state["user_info"].items():
                st.write(f"• {key.title()}: {value}")
        else:
            st.write("I don't know much about you yet!")
        
        if memory_state["conversation_summary"]:
            st.write("**Our Conversation:**")
            st.write(memory_state["conversation_summary"])
```

### Task 4.3: Update Message Processing for Smart Memory
Add this to handle smart memory responses (in the same file):

```python
# Smart Memory Processing (add this where you handle responses)
if use_smart_memory and "smart_memory_chain" in st.session_state:
    if (st.session_state.basic_messages and 
        st.session_state.basic_messages[-1]["role"] == "user" and
        not st.session_state.get("basic_processing", False)):
        
        st.session_state.basic_processing = True
        try:
            with st.chat_message("assistant", avatar="🧠"):
                with st.spinner("Thinking and remembering..."):
                    user_input = st.session_state.basic_messages[-1]["content"]
                    
                    # Prepare state for LangGraph
                    current_state = st.session_state.smart_memory_state.copy()
                    current_state["current_input"] = user_input
                    
                    # Run through the smart memory graph
                    result = st.session_state.smart_memory_chain.invoke(current_state)
                    
                    # Get the response
                    response_content = result["response"]
                    
                    # Update our memory state
                    st.session_state.smart_memory_state["messages"] = current_state["messages"] + [
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": response_content}
                    ]
                    st.session_state.smart_memory_state["user_info"] = result.get("user_info", {})
                    st.session_state.smart_memory_state["conversation_summary"] = result.get("conversation_summary", "")
                    
                    # Add to display
                    st.session_state.basic_messages.append({
                        "role": "assistant", 
                        "content": response_content
                    })
            
            st.session_state.basic_processing = False
            st.rerun()
            
        except Exception as e:
            st.session_state.basic_processing = False
            st.error(f"Smart Memory Error: {str(e)}")
            st.rerun()

else:
    # Your existing regular processing code goes here
    # (the code you already have for basic responses)
```

### Task 4.4: Test Your Smart Memory System

**🧠 Smart Memory Tests:**

1. **Turn on Smart Memory** with the checkbox

2. **Personal Info Test:**
   - Say: "Hi! My name is Sarah and I work as a teacher"
   - Ask: "What do you remember about me?"
   - Check the sidebar - it should show your name and job!

3. **Interest Tracking:**
   - Say: "I really love cooking and playing guitar"
   - Later ask: "What are my hobbies?"
   - The sidebar should show your interests

4. **Context Memory:**
   - Discuss a topic like "machine learning"
   - Later reference it: "What did we talk about earlier?"
   - The AI should remember the previous topic

5. **Summary Test:**
   - Have a conversation with 10+ messages
   - Check sidebar for conversation summary
   - Ask: "Can you summarize our chat?"

### Task 4.5: Compare Memory Types

Try both modes and see the difference:

**Simple Memory (checkbox off):**
- ✅ Just remembers the chat history
- ✅ Fast and straightforward

**Smart Memory (checkbox on):**
- ✅ Extracts and remembers personal info
- ✅ Creates conversation summaries
- ✅ Uses memory context in responses
- ✅ Shows you what it remembers in the sidebar

The smart memory makes conversations feel much more natural and personal!

---

## Part 5: Make It Look Good

### Task 5.1: Customize the UI
Time to make it yours! In `ui_components.py`, find the `apply_enhanced_styling()` method and:

1. **Change the accent color** from green to your favorite color (try `#2196F3` for blue)
2. **Modify the background gradient** - make it your vibe
3. **Play with font sizes** - make headers bigger or smaller

### Task 5.2: Test Your Style Changes
Refresh the app and see your changes! Try different screen sizes to make sure it still looks good.

---

## What You Should Have Now
✅ 3 new AI personalities that act totally different  
✅ A slick personality selector in the sidebar  
✅ Custom styling that makes it look like yours  
✅ Proof that different AI settings create completely different experiences  

---

# Assignment 2: Build a Super Smart Research Agent! 

## What We're Building
We're going to take the basic agent and turn it into a research powerhouse! It'll be able to search the web, grab info from Wikipedia, AND find the latest research papers. Basically, we're building an AI research assistant that's way smarter than just ChatGPT.

## What You Need
- Finished Assignment 1 
- OpenAI API key
- Tavily API key (grab one - it's free!)

---

## Part 1: Set Up the Tools

### Task 1.1: Install the New Stuff
Add these to your `requirements.txt`:
```
wikipedia>=1.4.0
arxiv==2.2.0
```

Then install them: `pip install wikipedia>=1.4.0 arxiv==2.2.0`

### Task 1.2: Build the Super Agent
Time to upgrade! Add this monster method to `AgentChatbotHelper` in `langchain_helpers.py`:

```python
@staticmethod
def setup_agent_with_research_tools(openai_api_key: str, tavily_api_key: str) -> Any:
    """Setup agent with Tavily, Wikipedia, and Arxiv tools"""
    from langchain_tavily import TavilySearch
    from langgraph.prebuilt import create_react_agent
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
    from langchain.agents import Tool
    
    # Web search (for current stuff)
    tavily_search = TavilySearch(
        max_results=5,
        topic="general", 
        tavily_api_key=tavily_api_key,
    )
    
    # Wikipedia (for general knowledge)
    wiki_tool = Tool(
        name="wikipedia",
        func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
        description="Search Wikipedia for topics, people, events, etc.",
    )
    
    # Arxiv (for research papers)
    arxiv_tool = Tool(
        name="arxiv", 
        func=ArxivAPIWrapper().run,
        description="Find research papers and scientific articles.",
    )
    
    tools = [tavily_search, wiki_tool, arxiv_tool]
    
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, api_key=openai_api_key)
    return create_react_agent(llm, tools)
```

### Task 1.3: Hook It Up to the UI
Now let's make the agent page use our new super agent! In `pages/2_Chatbot_Agent.py`:

1. Find the `setup_agent` method in the `ChatbotTools` class
2. Replace it with this:

```python
def setup_agent(self):
    openai_key = st.session_state.get("agent_openai_key", "")
    tavily_key = st.session_state.get("agent_tavily_key", "")
    # Use our awesome new agent!
    return AgentChatbotHelper.setup_agent_with_research_tools(openai_key, tavily_key)
```

3. Update the page subtitle to brag about your new powers:
   ```python
   "AI agent with web search, Wikipedia, and research paper capabilities"
   ```

---

## Part 2: Test Your Research Beast

### Task 2.1: Fire It Up
1. Run: `streamlit run Home.py`
2. Go to Chatbot Agent page
3. Enter both API keys
4. Ask: "What tools do you have?" (it should list all 3!)

### Task 2.2: Tool Test Time
Let's see what each tool can do:

**🌐 Web Search Test:**
"What's happening with AI in 2024?"
*Should get you recent news and developments*

**📚 Wikipedia Test:** 
"Tell me about Marie Curie's discoveries"
*Should get biographical info from Wikipedia*

**🔬 Research Paper Test:**
"Find recent papers about large language models"
*Should find actual research papers with authors and abstracts*

**🚀 Combo Test:**
"Compare recent research on quantum computing with what Wikipedia says about quantum physics"
*Watch it use multiple tools and combine the info!*

### Task 2.3: Break It (On Purpose)
Try to break your agent:
- Ask about something that doesn't exist
- Give it weird, confusing questions
- See how gracefully it handles failures

---

## Part 3: Make It Even Better

### Task 3.1: Optimize the Tools
Let's make them work better. Update your tool definitions to be more focused:

```python
# Better Wikipedia tool
wiki_tool = Tool(
    name="wikipedia",
    func=lambda query: WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
    ).run(query),
    description="Search Wikipedia for topics, people, events. Gets concise summaries.",
)

# Better Arxiv tool  
arxiv_tool = Tool(
    name="arxiv",
    func=lambda query: ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=2000).run(query),
    description="Find recent academic papers, especially AI and computer science research.",
)
```

### Task 2.4: Speed Test
Time some queries and see which tools are fastest/slowest. Document what you find!

---

## What You Should Have Now
✅ An agent that can search 3 different sources  
✅ Tool that picks the right source for each question  
✅ Combo queries that use multiple tools together  
✅ Error handling when things go wrong  
✅ Speed optimized tools that work better

---

# Assignment 3: Build a Smart Document Chat System!

## What We're Building  
We're creating a system that can read your documents (PDFs, Word docs, text files) and then chat about them intelligently. Upload a research paper, ask questions about it, get summaries - it's like having a research assistant that actually read everything!

## What You Need
- Finished Assignment 2
- OpenAI API key  
- Some test documents (PDFs work great)

---

## Part 1: Add Multi-Format Support

### Task 1.1: Install Document Readers
Add this to `requirements.txt`:
```
python-docx>=0.8.11
```

Run: `pip install python-docx>=0.8.11`

### Task 1.2: Upgrade the File Handler
Replace the `save_file` method in `RAGHelper` with this smarter version:

```python
@staticmethod
def save_file(file, folder: str = "tmp") -> tuple[str, str]:
    """Save file and return path + extension"""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.name)
    extension = os.path.splitext(file.name)[1].lower()
    with open(file_path, "wb") as f:
        f.write(file.getvalue())
    return file_path, extension
```

### Task 1.3: Build the Multi-Format Document Processor
Replace the `build_vectorstore` method with this beast that can handle multiple file types:

```python
@staticmethod
def build_vectorstore(files, api_key: str = None) -> FAISS:
    """Build vector store from multiple file types"""
    from langchain_community.document_loaders import TextLoader
    try:
        from langchain_community.document_loaders import Docx2txtLoader
    except ImportError:
        Docx2txtLoader = None
        
    docs = []
    
    for file in files:
        file_path, extension = RAGHelper.save_file(file)
        
        # Pick the right loader for each file type
        if extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif extension == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        elif extension == '.docx' and Docx2txtLoader:
            loader = Docx2txtLoader(file_path)
        else:
            st.warning(f"Can't read {extension} files yet!")
            continue
            
        try:
            docs.extend(loader.load())
        except Exception as e:
            st.error(f"Couldn't load {file.name}: {str(e)}")
            continue
    
    if not docs:
        raise ValueError("No documents loaded!")
        
    # Chunk the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    
    # Create embeddings and vector store
    embeddings_kwargs = {}
    if api_key:
        embeddings_kwargs["api_key"] = api_key
        
    embeddings = OpenAIEmbeddings(**embeddings_kwargs)
    vectordb = FAISS.from_documents(chunks, embeddings)
    
    return vectordb
```

### Task 1.4: Update the File Uploader
In `pages/3_Chat_with_your_Data.py`, find the file uploader and make it accept more types:

```python
uploaded_files = st.file_uploader(
    "📎 Drop your docs here",
    accept_multiple_files=True,
    type=['pdf', 'txt', 'docx'],  # Now accepts all 3 types!
    help="Upload PDFs, text files, or Word docs"
)
```

---

## Part 2: Test With Real Documents

### Task 2.1: Get It Running
1. Fire up: `streamlit run Home.py`
2. Go to "Chat with your Data"  
3. Enter your API key
4. Upload a test document (try a PDF first)

### Task 2.2: Test Different Query Types

**📊 Summary Questions:**
- "Summarize this document"
- "What are the main points?"
- "Give me the key takeaways"

**🔍 Specific Questions:**
- "What dates are mentioned?"
- "Who wrote this?" 
- "What's the methodology?"

**🤔 Analysis Questions:**
- "What are the pros and cons discussed?"
- "What are the implications?"
- "How does this relate to [topic]?"

### Task 2.3: Multi-Format Test
Try uploading:
1. A PDF file
2. A .txt file  
3. A .docx file
4. All three at once!

See how well it handles each format.

---

## Part 3: Make It Smarter

### Task 3.1: Tune the Document Chunking
Try different chunk sizes for different types of questions:

```python
# For detailed analysis (bigger chunks)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)

# For quick facts (smaller chunks)  
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
```

Test both and see which works better for your documents!

### Task 3.2: Improve the Query Classification
Make the system smarter about what type of answer to give. Update the classification logic:

```python
def classify_mode(state):
    q = state["question"].lower()
    
    # More patterns to detect what the user wants
    summary_words = ["summarize", "overview", "main points", "key themes", "compare", "analyze"]
    fact_words = ["when", "who", "where", "how much", "what date", "specific", "exact"]
    
    summary_score = sum(1 for word in summary_words if word in q)
    fact_score = sum(1 for word in fact_words if word in q)
    
    mode = "summary" if summary_score > fact_score else "fact"
    return {**state, "mode": mode}
```

### Task 3.3: Add a Debug Mode
Want to see what's happening under the hood? Add this debug function:

```python
def show_chunks(vectorstore, query, k=5):
    """Show which chunks the system found"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    st.write(f"Found {len(docs)} relevant chunks:")
    for i, doc in enumerate(docs):
        st.write(f"**Chunk {i+1}:**")
        st.write(doc.page_content[:200] + "...")
        st.write("---")
```

Add this to your sidebar to debug what chunks are being used!

---

## Part 4: Speed It Up and Fix Bugs

### Task 4.1: Performance Testing
Time different operations:
- Document upload and processing
- Different query types  
- Different file formats
- Multiple documents vs single documents

Document what's fast and what's slow!

### Task 4.2: Break It and Fix It
Try to break your system:
- Upload corrupted files
- Ask questions about stuff not in the docs
- Upload huge documents
- Ask really weird questions

Then figure out how to handle these cases gracefully.

### Task 4.3: Make Error Messages Helpful
Instead of cryptic errors, give users helpful messages:
- "That file format isn't supported yet"
- "I couldn't find information about that in your documents"  
- "Try uploading a smaller document"

---

## What You Should Have Now
✅ A system that reads PDFs, Word docs, and text files  
✅ Smart query classification (summary vs facts)  
✅ Multi-document support  
✅ Debugging tools to see what's happening  
✅ Performance testing and optimization  
✅ Error handling that doesn't confuse users

---

## 🎉 Bonus Challenge: Combine Everything!

If you've finished all three assignments, try this ultimate challenge:

**Build a unified chatbot dashboard** that lets users:
1. Switch between all the personality types from Assignment 1
2. Use the research agent from Assignment 2  
3. Chat with their documents from Assignment 3
4. All with consistent, awesome UI styling

This would be like building your own personal AI assistant that can do everything!
