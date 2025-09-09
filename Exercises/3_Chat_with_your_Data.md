# Exercise 3: Chat with your Data - Agentic Multi-Format Document Processing

## Objective
Build an agentic RAG system that can process multiple document formats and intelligently decide how to answer questions.

## Prerequisites
- OpenAI API key
- Test documents (PDF, MD, HTML)

---

## Implementation

### Step 1: Install Dependencies
Add to `requirements.txt`:
```
beautifulsoup4>=4.9.0
```

Run: `pip install beautifulsoup4>=4.9.0`

### Step 2: Enhance File Processing
**File:** `project_code/langchain_helpers.py`  
**Location:** Replace `save_file()` method in `RAGHelper` class

```python
@staticmethod
def save_file(file, folder: str = "tmp") -> tuple[str, str]:
    """Save uploaded file and return path with extension for format detection"""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file.name)
    extension = os.path.splitext(file.name)[1].lower()
    with open(file_path, "wb") as f:
        f.write(file.getvalue())
    return file_path, extension
```

### Step 3: Add Multi-Format Document Loader
**File:** `project_code/langchain_helpers.py`  
**Location:** Replace `build_vectorstore()` method in `RAGHelper` class

```python
@staticmethod
def build_vectorstore(files, api_key: str = None) -> FAISS:
    """Build vector store supporting PDF, MD, and HTML formats"""
    from langchain_community.document_loaders import TextLoader, UnstructuredHTMLLoader
    try:
        from langchain_community.document_loaders import UnstructuredMarkdownLoader
    except ImportError:
        UnstructuredMarkdownLoader = None
        
    documents: List[Document] = []
    
    for file in files:
        file_path, extension = RAGHelper.save_file(file)
        
        # Format-specific loader selection
        if extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif extension == '.md' and UnstructuredMarkdownLoader:
            loader = UnstructuredMarkdownLoader(file_path)
        elif extension == '.html':
            loader = UnstructuredHTMLLoader(file_path)
        else:
            st.warning(f"Unsupported file format: {extension}")
            continue
            
        try:
            documents.extend(loader.load())
        except Exception as e:
            st.error(f"Failed to process {file.name}: {str(e)}")
            continue
    
    if not documents:
        raise ValueError("No documents successfully loaded")
        
    # Split documents into manageable chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=200
    )
    document_chunks = text_splitter.split_documents(documents)
    
    # Create embeddings and build vector store
    embeddings_kwargs = {}
    if api_key:
        embeddings_kwargs["api_key"] = api_key
        
    embeddings = OpenAIEmbeddings(**embeddings_kwargs)
    vector_store = FAISS.from_documents(document_chunks, embeddings)
    
    return vector_store
```

### Step 4: Replace Simple RAG with Agentic RAG
**File:** `project_code/langchain_helpers.py`  
**Location:** Replace `build_simple_agentic_rag()` method in `RAGHelper` class

```python
@staticmethod
def build_advanced_agentic_rag(retriever, llm: ChatOpenAI):
    """Build an advanced agentic RAG workflow with intelligent decision making"""
    
    # Enhanced classification with more sophisticated patterns
    SUMMARY_HINTS = (
        "summarize", "summary", "overview", "key points", "bullet", "synthesize",
        "main ideas", "outline", "gist", "essence", "highlights"
    )
    FACT_HINTS = (
        "when", "date", "who", "where", "amount", "total", "price", "figure", 
        "specific", "exact", "how many", "which", "what time", "name"
    )
    ANALYSIS_HINTS = (
        "analyze", "compare", "contrast", "evaluate", "assess", "pros and cons",
        "advantages", "disadvantages", "implications", "impact", "significance"
    )
    
    def intelligent_classify_mode(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
        """Advanced classification with analysis mode"""
        query_lower = state["question"].lower()
        
        # Count different types of hints
        summary_score = sum(1 for hint in SUMMARY_HINTS if hint in query_lower)
        fact_score = sum(1 for hint in FACT_HINTS if hint in query_lower)
        analysis_score = sum(1 for hint in ANALYSIS_HINTS if hint in query_lower)
        
        # Intelligent mode selection
        if analysis_score > 0:
            mode: Literal["summary", "fact", "analysis"] = "analysis"
        elif summary_score > fact_score:
            mode = "summary"
        else:
            mode = "fact"
            
        return {**state, "mode": mode}
    
    def adaptive_retrieve(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
        """Retrieve different amounts of context based on query type"""
        question = state["question"]
        mode = state["mode"]
        
        # Adjust retrieval based on mode
        if mode == "analysis":
            k = 8  # More context for analysis
        elif mode == "summary":
            k = 6  # Moderate context for summaries
        else:
            k = 3  # Focused context for facts
            
        retrieved_docs = retriever.invoke(question)
        return {**state, "documents": retrieved_docs[:k]}
    
    def intelligent_generate(state: RAGHelper.RAGState) -> RAGHelper.RAGState:
        """Generate responses with mode-specific prompts"""
        document_context = "\n\n---\n\n".join(
            doc.page_content for doc in state.get("documents", [])
        )
        
        if not document_context.strip():
            return {
                **state, 
                "generation": "I couldn't find enough information in the documents to answer that."
            }
        
        # Mode-specific prompts
        if state["mode"] == "analysis":
            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are an analytical assistant. Provide a thorough analysis using the provided context. "
                 "Include multiple perspectives, implications, and detailed reasoning."),
                ("human",
                 "Question: {question}\n\nContext: {context}\n\nAnalyze this thoroughly:")
            ])
        elif state["mode"] == "summary":
            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are a summarization expert. Create a comprehensive summary using the provided context. "
                 "Organize information logically and highlight key points."),
                ("human",
                 "Question: {question}\n\nContext: {context}\n\nSummarize:")
            ])
        else:  # fact mode
            prompt = ChatPromptTemplate.from_messages([
                ("system",
                 "You are a factual information assistant. Answer precisely using only the provided context. "
                 "If the answer isn't in the context, say so."),
                ("human",
                 "Question: {question}\n\nContext: {context}\n\nAnswer:")
            ])
        
        response = llm.invoke(prompt.format_messages(
            question=state["question"], 
            context=document_context
        ))
        
        return {**state, "generation": response.content}
    
    # Build enhanced graph
    graph = StateGraph(RAGHelper.RAGState)
    
    # Add intelligent nodes
    graph.add_node("classify", intelligent_classify_mode)
    graph.add_node("retrieve", adaptive_retrieve)
    graph.add_node("generate", intelligent_generate)
    
    # Set up enhanced flow
    graph.set_entry_point("classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    
    return graph.compile()
```

### Step 5: Update RAG State for Analysis Mode
**File:** `project_code/langchain_helpers.py`  
**Location:** Update `RAGState` class in `RAGHelper`

```python
class RAGState(TypedDict):
    question: str
    mode: Literal["summary", "fact", "analysis"]
    documents: List[Document]
    generation: str
```

### Step 6: Update Setup Method
**File:** `project_code/langchain_helpers.py`  
**Location:** Replace `setup_rag_system()` method in `RAGHelper` class

```python
@staticmethod
def setup_rag_system(uploaded_files, api_key: str = None) -> Any:
    """Setup complete agentic RAG system from uploaded files"""
    # Build vector store and configure retriever
    vector_store = RAGHelper.build_vectorstore(uploaded_files, api_key)
    retriever = vector_store.as_retriever()
    
    # Configure language model for generation
    llm_config = {
        "model": "gpt-4o-mini", 
        "temperature": 0,
        "streaming": False
    }
    if api_key:
        llm_config["api_key"] = api_key
        
    llm = ChatOpenAI(**llm_config)
    return RAGHelper.build_advanced_agentic_rag(retriever, llm)
```

### Step 7: Update File Upload Interface
**File:** `project_code/pages/3_Chat_with_your_Data.py`  
**Location:** Replace file uploader section (around line 160)

```python
uploaded_files = st.file_uploader(
    label="**Upload files to chat with your documents**",
    type=["pdf", "md", "html"],
    accept_multiple_files=True,
    help="Supports PDF, Markdown, and HTML document formats"
)
```

---

## Usage

1. Run `streamlit run Home.py`
2. Navigate to "Chat with your Data" page
3. Enter OpenAI API key
4. Upload documents (PDF, MD, or HTML)
5. Wait for processing to complete
6. Try different query types to see agentic behavior:
   - **Summary**: "Summarize the main points in this document"
   - **Facts**: "What specific dates are mentioned?"
   - **Analysis**: "Analyze the pros and cons discussed in the document"

## Key Learning Points

- **Agentic RAG** makes intelligent decisions about how to process queries
- **Mode classification** determines the appropriate response strategy
- **Adaptive retrieval** adjusts context amount based on query type
- **Specialized prompts** optimize responses for different information needs