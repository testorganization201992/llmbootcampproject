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
from memory import MemoryManager


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
    async def invoke_with_memory(chain: Any, user_input: str, memory_manager: MemoryManager) -> Any:
        """Invoke chain with semantic and conversation memory"""
        # Get comprehensive context from memory manager
        context = await memory_manager.get_unified_context(user_input, conversation_limit=5, semantic_limit=3)
        
        # Convert context to LangChain message format
        formatted_history = []
        for ctx in context:
            if ctx["role"] == "user":
                formatted_history.append(("human", ctx["content"]))
            elif ctx["role"] == "assistant":
                formatted_history.append(("assistant", ctx["content"]))
            elif ctx["role"] == "system" and ctx["type"] == "semantic":
                # Add semantic memories as system context
                formatted_history.append(("system", f"Relevant context: {ctx['content']}"))
        
        return chain.invoke({
            "input": user_input,
            "chat_history": formatted_history
        })
    
    @staticmethod
    async def create_memory_manager(session_id: str, api_key: str) -> MemoryManager:
        """Create a memory manager instance"""
        return MemoryManager(
            session_id=session_id,
            api_key=api_key,
            enable_semantic=True,
            enable_conversation=True
        )
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration for basic chatbot"""
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        }


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
    def save_file(file, folder: str = "tmp") -> str:
        """Save uploaded file to specified folder"""
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getvalue())
        return file_path
    
    @staticmethod
    def build_vectorstore(files, api_key: str = None) -> FAISS:
        """Build vector store from uploaded PDF files"""
        docs: List[Document] = []
        
        for file in files:
            path = RAGHelper.save_file(file)
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        
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