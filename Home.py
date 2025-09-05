import streamlit as st
import os
import glob

st.set_page_config(
    page_title="LLM Bootcamp Project",
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state="expanded"
)

# Force light theme
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    .stApp > div {
        background-color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">🤖 LLM Bootcamp Project</h1>
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

    st.markdown("---")
    
    # Auto-generate descriptions
    st.markdown("**Available Features:**")
    for page_file in page_files:
        page_name = os.path.basename(page_file)
        icon, title, description = get_page_info(page_name)
        st.markdown(f"- **{title}** - {description}")

else:
    st.error("Pages directory not found!")
    st.markdown("Available pages will be automatically discovered when the pages/ directory exists.")
