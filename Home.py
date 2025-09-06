import streamlit as st
import os
import glob

st.set_page_config(
    page_title="LLM Bootcamp Project",
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state="expanded"
)


# Enhanced visual styling for home page
st.markdown("""
<style>
    /* Enhanced card styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a883);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: 600;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 212, 170, 0.3);
        font-size: 1.1rem;
        height: 80px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.4);
        background: linear-gradient(135deg, #00e6c0, #00cc99);
    }
    
    /* Enhanced main title */
    .main-title {
        background: linear-gradient(135deg, #00d4aa, #ffffff, #00d4aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 0 0 40px rgba(0, 212, 170, 0.5);
    }
    
    /* Feature list styling */
    .feature-list {
        background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 170, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
    }
</style>

<div style="text-align: center; margin: 3rem 0;">
    <h1 class="main-title" style="font-size: 4rem; margin-bottom: 1rem;">
        🤖 LLM Bootcamp Project
    </h1>
    <p style="font-size: 1.5rem; color: #a0a0a0; margin-bottom: 2rem;">
        Explore advanced AI chatbot capabilities with multiple specialized agents
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Available AI Assistants:")

# Automatically discover pages
pages_dir = "pages"
if os.path.exists(pages_dir):
    page_files = glob.glob(f"{pages_dir}/*.py")
    page_files.sort()
    
    def extract_page_info(file_path):
        """Extract title and description from file docstring or comments"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for docstring at top of file
            if '"""' in content:
                start = content.find('"""')
                end = content.find('"""', start + 3)
                if start != -1 and end != -1:
                    docstring = content[start+3:end].strip()
                    lines = docstring.split('\n')
                    title = lines[0].strip() if lines else ""
                    description = lines[1].strip() if len(lines) > 1 else ""
                    return title, description
        except:
            pass
        
        # Fallback: generate from filename
        base_name = os.path.basename(file_path)
        clean_name = base_name.replace('.py', '').replace('_', ' ')
        # Remove leading numbers like "1_"
        if clean_name[0].isdigit() and '_' in clean_name:
            clean_name = clean_name.split('_', 1)[1]
        title = clean_name.title()
        return title, "AI assistant page"
    
    def get_page_info(filename):
        """Get specific page info based on filename"""
        filename_lower = filename.lower()
        
        if '1_basic' in filename_lower:
            return "💬", "Basic AI Chat", "Simple AI conversation"
        elif '2_chatbot_agent' in filename_lower:
            return "🔍", "Search Enabled Chat", "AI with internet search capabilities"
        elif '3_chat_with_your_data' in filename_lower:
            return "📚", "RAG", "Retrieval-Augmented Generation with documents"
        elif '4_mcp_agent' in filename_lower:
            return "🔧", "MCP Chatbot", "Model Context Protocol integration"
        else:
            # Fallback for any other files
            clean_name = filename.replace('.py', '').replace('_', ' ').title()
            return "🤖", clean_name, "AI assistant page"
    
    # Create columns based on number of pages
    num_pages = len(page_files)
    cols = st.columns(num_pages)
    
    for i, page_file in enumerate(page_files):
        page_name = os.path.basename(page_file)
        
        with cols[i]:
            # Get page info based on filename
            icon, title, description = get_page_info(page_name)
            button_text = f"{icon} {title}"
            
            if st.button(button_text, key=page_name, use_container_width=True):
                st.switch_page(page_file)

    # Enhanced feature list
    st.markdown("""
    <div class="feature-list">
        <h3 style="color: #00d4aa; margin-bottom: 1.5rem; text-align: center;">✨ Available Features</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for page_file in page_files:
        page_name = os.path.basename(page_file)
        icon, title, description = get_page_info(page_name)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            border-left: 4px solid #00d4aa;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        ">
            <strong style="color: #00d4aa;">{icon} {title}</strong> - <span style="color: #cccccc;">{description}</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("Pages directory not found!")
    st.markdown("Available pages will be automatically discovered when the pages/ directory exists.")
