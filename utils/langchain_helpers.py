"""LangChain Helper Functions.

Centralized AI/ML functionality for the LLM Bootcamp Project.
Provides helper classes for different types of chatbot functionality.
"""

import os
import asyncio
from typing import List, Dict, Any, TypedDict, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END


class BasicChatbotHelper:
    """Helper class for basic conversational chatbot functionality."""
    
    @staticmethod
    def build_chain(config: Dict[str, Any], api_key: str = None) -> Any:
        """Build a LangChain chain for basic chatbot functionality."""
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
        
        # Configure response style with predefined system prompts
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
        """Invoke the chain with conversation memory support."""
        # Convert chat history to LangChain message format
        formatted_history = []
        for msg in chat_history[:-1]:  # Exclude the latest user message to avoid duplication
            if msg["role"] == "user":
                formatted_history.append(("human", msg["content"]))
            elif msg["role"] == "assistant":
                formatted_history.append(("ai", msg["content"]))
        
        return chain.invoke({
            "input": user_input,
            "chat_history": formatted_history
        })
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration for basic chatbot."""
        return {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 2000
        }


class AgentChatbotHelper:
    """Helper class for agent chatbot with real-time web search functionality."""
    
    @staticmethod
    def setup_agent(openai_api_key: str, tavily_api_key: str) -> Any:
        """Setup an AI agent with Tavily web search capabilities."""
        from langchain_tavily import TavilySearch
        from langgraph.prebuilt import create_react_agent
        
        # Configure Tavily search tool with optimal settings
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
        """Process agent response with streaming support."""
        accumulated_response = ""
        
        # Stream state updates (includes reasoning and tool execution steps)
        for update in agent.stream({"messages": user_query}):
            if "messages" in update and update["messages"]:
                last_message = update["messages"][-1]
                if hasattr(last_message, 'content') and last_message.content:
                    accumulated_response = last_message.content

        # Fallback to direct invocation if streaming failed
        if not accumulated_response:
            result = await agent.ainvoke({"messages": [{"role": "user", "content": user_query}]})
            if "messages" in result and result["messages"]:
                accumulated_response = result["messages"][-1].content
        
        return accumulated_response


class RAGHelper:
    """Helper class for RAG (Retrieval-Augmented Generation) functionality."""
    
    # Type definition for RAG workflow state management
    class RAGState(TypedDict):
        question: str
        mode: Literal["summary", "fact"]
        documents: List[Document]
        generation: str
    
    @staticmethod
    def save_file(file, folder: str = "tmp") -> str:
        """Save uploaded file to local storage."""
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path
    
    @staticmethod
    def build_vectorstore(files, api_key: str = None) -> FAISS:
        """Build FAISS vector store from uploaded PDF files."""
        documents: List[Document] = []
        
        # Process each uploaded PDF file
        for file in files:
            file_path = RAGHelper.save_file(file)
            loader = PyPDFLoader(file_path)
            file_documents = loader.load()
            documents.extend(file_documents)
        
        # Split documents into manageable chunks for processing
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, 
            chunk_overlap=200
        )
        document_chunks = text_splitter.split_documents(documents)
        
        embeddings_kwargs = {}
        if api_key:
            embeddings_kwargs["api_key"] = api_key
            
        # Create embeddings and build vector store
        embeddings = OpenAIEmbeddings(**embeddings_kwargs)
        vector_store = FAISS.from_documents(document_chunks, embeddings)
        
        return vector_store
    
    @staticmethod
    def build_simple_agentic_rag(retriever, llm: ChatOpenAI):
        """Build an intelligent agentic RAG workflow."""
        
        # Classification node: determine if query needs summary or specific facts
        SUMMARY_HINTS = ("summarize", "summary", "overview", "key points", "bullet", "synthesize")
        FACT_HINTS = ("when", "date", "who", "where", "amount", "total", "price", "figure", "specific", "exact")
        
        def classify_mode(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            question_lower = state["question"].lower()
            if any(hint in question_lower for hint in SUMMARY_HINTS):
                state["mode"] = "summary"
            elif any(hint in question_lower for hint in FACT_HINTS):
                state["mode"] = "fact"
            else:
                state["mode"] = "fact"  # Default to fact-finding
            return state
        
        # Retrieval node: fetch relevant documents based on query type
        def retrieve(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            if state["mode"] == "summary":
                docs = retriever.invoke(state["question"], k=8)  # More docs for summary
            else:
                docs = retriever.invoke(state["question"], k=4)  # Fewer docs for specific facts
            state["documents"] = docs
            return state
        
        # Generation node: create appropriate response based on mode and context
        def generate(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
            context = "\n\n".join([doc.page_content for doc in state["documents"]])
            
            if state["mode"] == "summary":
                prompt = f"""Based on the following documents, provide a comprehensive summary that addresses: {state["question"]}

Context from documents:
{context}

Provide a well-structured summary with key points and insights from the documents."""
            else:
                prompt = f"""Based on the following documents, answer this specific question: {state["question"]}

Context from documents:
{context}

Provide a direct, factual answer based on the information in the documents. If the information is not available, say so clearly."""
            
            response = llm.invoke(prompt)
            state["generation"] = response.content
            return state
        
        # Build the workflow graph
        workflow = StateGraph(RAGHelper.RAGState)
        workflow.add_node("classify", classify_mode)
        workflow.add_node("retrieve", retrieve)
        workflow.add_node("generate", generate)
        
        workflow.set_entry_point("classify")
        workflow.add_edge("classify", "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    @staticmethod
    def setup_rag_system(uploaded_files, api_key: str = None) -> Any:
        """Setup complete RAG system with uploaded documents."""
        # Build vector store from uploaded files
        vectorstore = RAGHelper.build_vectorstore(uploaded_files, api_key)
        retriever = vectorstore.as_retriever()
        
        # Initialize LLM
        llm_kwargs = {"model": "gpt-4o-mini", "temperature": 0.3}
        if api_key:
            llm_kwargs["api_key"] = api_key
        llm = ChatOpenAI(**llm_kwargs)
        
        # Build and return the agentic RAG workflow
        return RAGHelper.build_simple_agentic_rag(retriever, llm)
