import streamlit as st

st.set_page_config(
    page_title="LLM Bootcamp Project",
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Custom CSS for sleek home page
st.markdown("""
<style>
/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Feature cards */
.feature-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    border-left: 4px solid;
    backdrop-filter: blur(10px);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.basic-card { border-left-color: #FF6B6B; }
.agent-card { border-left-color: #4ECDC4; }
.rag-card { border-left-color: #45B7D1; }

/* Tech stack */
.tech-stack {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1>🤖 LLM Bootcamp Project</h1>
    <h3>Advanced Chatbot Implementations</h3>
    <p style="font-size: 1.2em; opacity: 0.9;">
        Powered by OpenAI & LangChain with sleek Streamlit interfaces
    </p>
</div>
""", unsafe_allow_html=True)

# Features Overview - Staggered Card Layout
col1, col2 = st.columns([1, 1])

with col1:
    # Basic Chatbot - Full width
    st.markdown("""
    <div class="feature-card basic-card" style="margin-bottom: 2rem;">
        <h3>💬 Basic Chatbot</h3>
        <p>Stateless conversations with no memory between messages. Perfect for quick questions and independent interactions.</p>
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div>
                <strong>Features:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>Multiple OpenAI models</li>
                    <li>Real-time streaming</li>
                </ul>
            </div>
            <div>
                <strong>Specs:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>No conversation memory</li>
                    <li>Configurable temperature</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Document Chat - Offset
    st.markdown("""
    <div class="feature-card rag-card" style="margin-top: 2rem;">
        <h3>📄 Document Chat</h3>
        <p>RAG-powered chatbot that can understand and answer questions about your uploaded PDF documents.</p>
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div>
                <strong>Capabilities:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>PDF document processing</li>
                    <li>FAISS vector search</li>
                </ul>
            </div>
            <div>
                <strong>AI:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>Agentic RAG pipeline</li>
                    <li>Context-aware responses</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Agent Chatbot - Centered with offset
    st.markdown("""
    <div class="feature-card agent-card" style="margin-top: 1rem; margin-bottom: 3rem;">
        <h3>🌐 Agent Chatbot</h3>
        <p>Internet-enabled chatbot with web search capabilities using Tavily integration for real-time information.</p>
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div>
                <strong>Integration:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>Web search integration</li>
                    <li>LangGraph workflows</li>
                </ul>
            </div>
            <div>
                <strong>Intelligence:</strong>
                <ul style="margin: 0.5rem 0;">
                    <li>Real-time data access</li>
                    <li>Agent-based reasoning</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats/Metrics section
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 1.5rem; text-align: center; margin-top: 1rem;">
        <h4>⚡ Performance Metrics</h4>
        <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
            <div>
                <h2 style="color: #FF6B6B; margin: 0;">3</h2>
                <p style="margin: 0; opacity: 0.8;">Chatbot Types</p>
            </div>
            <div>
                <h2 style="color: #4ECDC4; margin: 0;">6+</h2>
                <p style="margin: 0; opacity: 0.8;">AI Models</p>
            </div>
            <div>
                <h2 style="color: #45B7D1; margin: 0;">∞</h2>
                <p style="margin: 0; opacity: 0.8;">Possibilities</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tech Stack
st.markdown("""
<div class="tech-stack">
    <h3>🛠️ Technology Stack</h3>
    <p>
        <strong>LangChain</strong> • <strong>OpenAI GPT Models</strong> • <strong>LangGraph</strong> • 
        <strong>Streamlit</strong> • <strong>FAISS</strong> • <strong>Tavily Search</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# Getting Started
st.markdown("""
<div style="text-align: center; margin: 3rem 0;">
    <h3>🚀 Get Started</h3>
    <p style="font-size: 1.1em;">
        Navigate to any chatbot page using the sidebar to start exploring different AI conversation patterns.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    **Available Chatbots:**
    - 💬 **Basic Chatbot** - Clean, minimalist interface with advanced controls
    - 🌐 **Agent Chatbot** - Web-enabled with search capabilities
    - 📄 **Document Chat** - PDF Q&A with RAG technology
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Tips")
    st.markdown("""
    - **Basic Chatbot** - Clean design with full parameter control
    - **Agent Chatbot** - Current events and web information
    - **Document Chat** - Upload and chat with your PDF files
    """)
    
    st.markdown("---")
    st.success("✅ All systems operational")
