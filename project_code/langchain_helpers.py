"""
LangChain Helper Functions
Centralized AI/ML functionality for the LLM Bootcamp Project
"""

import os
from typing import List, Dict, Any, TypedDict, Literal, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END


class BasicChatbotHelper:
    """Helper class for basic chatbot functionality"""
    
    @staticmethod
    def build_chain(config: Dict[str, Any], api_key: str = None) -> Any:
        """Build the LangChain chain for basic chatbot"""
        llm_kwargs = {
            "model": config["model"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "top_p": config.get("top_p", 1.0),
            "frequency_penalty": config.get("frequency_penalty", 0.0),
            "presence_penalty": config.get("presence_penalty", 0.0),
            "streaming": False
        }
        
        if api_key:
            llm_kwargs["api_key"] = api_key
            
        llm = ChatOpenAI(**llm_kwargs)
        
        # Dynamic system prompt based on response style
        system_prompts = {
            "Professional": "You are a professional AI assistant. Provide formal, detailed, and well-structured responses suitable for business contexts.",
            "Casual": "You are a friendly and casual AI assistant. Use conversational language and be approachable in your responses.",
            "Creative": "You are a creative AI assistant. Provide imaginative, engaging responses with varied perspectives and creative insights.",
            "Technical": "You are a technical AI assistant. Provide precise, detailed explanations with technical accuracy and clarity.",
            "Balanced": config.get("system_prompt", "You are a helpful AI assistant. Provide clear, concise, and friendly responses.")
        }
        
        system_message = system_prompts.get(config.get("response_style", "Balanced"), system_prompts["Balanced"])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ])
        
        return prompt | llm
    
    @staticmethod
    def invoke_with_memory(chain: Any, user_input: str, chat_history: List[Dict[str, str]]) -> Any:
        """Invoke chain with conversation memory"""
        # Convert chat history to LangChain message format
        formatted_history = []
        for msg in chat_history[:-1]:  # Exclude the current user message
            if msg["role"] == "user":
                formatted_history.append(("human", msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(("assistant", msg["content"]))
        
        return chain.invoke({
            "input": user_input,
            "chat_history": formatted_history
        })
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration for basic chatbot"""
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    
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


class AgentChatbotHelper:
    """Helper class for agent chatbot with web search functionality"""
    
    @staticmethod
    def setup_agent(openai_api_key: str, tavily_api_key: str) -> Any:
        """Setup the agent with Tavily search capabilities"""
        from langchain_tavily import TavilySearch
        from langgraph.prebuilt import create_react_agent
        
        # Tavily tool
        tavily_search = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=tavily_api_key,
        )
        
        tools = [tavily_search]
        
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, api_key=openai_api_key)
        agent = create_react_agent(llm, tools)
        return agent
    
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
    
    @staticmethod
    async def process_agent_response(agent: Any, user_query: str) -> str:
        """Process agent response with streaming support"""
        acc = ""
        # Stream state updates (chunked by reasoning/tool steps)
        for update in agent.stream({"messages": user_query}):
            msgs = update.get("messages", [])
            for m in msgs:
                content = getattr(m, "content", "")
                if not content and isinstance(getattr(m, "content", None), list):
                    content = "".join(
                        c.get("text", "")
                        for c in m.content
                        if isinstance(c, dict) and c.get("type") == "text"
                    )
                if content:
                    acc += content

        # Fallback if nothing streamed
        if not acc:
            resp = agent.invoke({"messages": user_query})
            acc = (
                resp["messages"][-1].content
                if isinstance(resp, dict) and resp.get("messages")
                else str(resp)
            )
        
        return acc


class RAGHelper:
    """Helper class for RAG (Retrieval-Augmented Generation) functionality"""
    
    # RAG State type definition
    class RAGState(TypedDict):
        question: str
        mode: Literal["summary", "fact"]
        documents: List[Document]
        generation: str
    
    @staticmethod
    def save_file(file, folder: str = "tmp") -> tuple[str, str]:
        """Save file and return path + extension"""
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        extension = os.path.splitext(file.name)[1].lower()
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path, extension
    
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
                import streamlit as st
                st.warning(f"Can't read {extension} files yet!")
                continue
                
            try:
                docs.extend(loader.load())
            except Exception as e:
                import streamlit as st
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
    
    @staticmethod
    def build_simple_agentic_rag(retriever, llm: ChatOpenAI):
        """Build simple agentic RAG graph"""
        
        # Node: classify mode (summary vs fact)
        SUMMARY_HINTS = ("summarize", "summary", "overview", "key points", "bullet", "synthesize")
        FACT_HINTS = ("when", "date", "who", "where", "amount", "total", "price", "figure", "specific", "exact")
        
        def classify_mode(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            q = state["question"].lower()
            if any(w in q for w in SUMMARY_HINTS) and not any(w in q for w in FACT_HINTS):
                mode: Literal["summary", "fact"] = "summary"
            elif any(w in q for w in FACT_HINTS):
                mode = "fact"
            else:
                # default to fact unless they asked to summarize
                mode = "summary" if "summary" in q or "summarize" in q else "fact"
            return {**state, "mode": mode}
        
        # Node: retrieve
        def retrieve(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            q = state["question"]
            k = 8 if state["mode"] == "summary" else 3
            docs = retriever.invoke(q)
            return {**state, "documents": docs[:k]}
        
        # Node: generate
        gen_prompt_summary = ChatPromptTemplate.from_messages([
            ("system",
             "You are a helpful assistant. Create a concise, faithful summary ONLY using the provided context. "
             "Prefer bullet points if helpful. Do not use outside knowledge."),
            ("human",
             "Question:\n{question}\n\n"
             "Context (multiple document chunks):\n{context}\n\n"
             "Write a grounded summary:")
        ])
        
        gen_prompt_fact = ChatPromptTemplate.from_messages([
            ("system",
             "You are a helpful assistant. Answer precisely and ONLY using the provided context. "
             "If the context is insufficient, say so."),
            ("human",
             "Question:\n{question}\n\n"
             "Context:\n{context}\n\n"
             "Answer:")
        ])
        
        def generate(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            ctx = "\n\n---\n\n".join(d.page_content for d in state.get("documents", []))
            if not ctx.strip():
                return {**state, "generation": "I couldn't find enough information in the documents to answer that."}
            
            if state["mode"] == "summary":
                answer = llm.invoke(gen_prompt_summary.format_messages(
                    question=state["question"], context=ctx
                )).content
            else:
                answer = llm.invoke(gen_prompt_fact.format_messages(
                    question=state["question"], context=ctx
                )).content
            return {**state, "generation": answer}
        
        # Build graph
        graph = StateGraph(RAGHelper.RAGState)
        graph.add_node("classify_mode", classify_mode)
        graph.add_node("retrieve", retrieve)
        graph.add_node("generate", generate)
        
        graph.set_entry_point("classify_mode")
        graph.add_edge("classify_mode", "retrieve")
        graph.add_edge("retrieve", "generate")
        graph.add_edge("generate", END)
        
        return graph.compile()
    
    @staticmethod
    def setup_rag_system(uploaded_files, api_key: str = None) -> Any:
        """Setup complete RAG system from uploaded files"""
        vectordb = RAGHelper.build_vectorstore(uploaded_files, api_key)
        retriever = vectordb.as_retriever()
        
        llm_kwargs = {"model": "gpt-4o-mini", "temperature": 0, "streaming": False}
        if api_key:
            llm_kwargs["api_key"] = api_key
            
        llm = ChatOpenAI(**llm_kwargs)
        return RAGHelper.build_simple_agentic_rag(retriever, llm)


class MCPHelper:
    """Helper class for Model Context Protocol functionality"""
    
    @staticmethod
    async def get_agent(openai_api_key: str, mcp_server_url: str):
        """Get MCP agent instance"""
        from agent_service import get_agent
        return await get_agent(openai_api_key, mcp_server_url)
    
    @staticmethod
    async def process_mcp_query(agent: Any, messages: List[Dict[str, str]]) -> str:
        """Process MCP query through the agent"""
        try:
            response_text = await agent.invoke(messages)
            return response_text
        except Exception as e:
            return f"❌ MCP Agent Error: {str(e)}"


class ValidationHelper:
    """Helper class for input validation"""
    
    @staticmethod
    def validate_openai_key(api_key: str) -> bool:
        """Validate OpenAI API key format"""
        return api_key and api_key.startswith("sk-")
    
    @staticmethod
    def validate_tavily_key(api_key: str) -> bool:
        """Validate Tavily API key format"""
        return api_key and api_key.startswith("tvly-")
    
    @staticmethod
    def validate_mcp_url(url: str) -> bool:
        """Validate MCP server URL format"""
        return url and (url.startswith("http://") or url.startswith("https://"))