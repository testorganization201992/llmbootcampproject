"""
UI Components and Styling Module
Centralized UI styling and components for the LLM Bootcamp Project
"""

import streamlit as st

class ChatbotUI:
    """Centralized UI components and styling for chatbot pages"""
    
    # Avatar URLs
    USER_AVATAR = "https://em-content.zobj.net/source/apple/354/man-technologist-medium-skin-tone_1f468-1f3fd-200d-1f4bb.png"
    BOT_AVATAR = "https://em-content.zobj.net/source/apple/354/robot_1f916.png"
    
    @staticmethod
    def apply_enhanced_styling():
        """Apply enhanced dark theme styling to the page"""
        st.markdown("""
        <style>
            /* Enhanced chat styling */
            .stChatMessage {
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 15px;
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border: 1px solid rgba(0, 212, 170, 0.1);
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            }
            
            /* Enhanced buttons */
            .stButton > button {
                background: linear-gradient(135deg, #00d4aa, #00a883);
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: 600;
                padding: 0.75rem 2rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 212, 170, 0.4);
                background: linear-gradient(135deg, #00e6c0, #00cc99);
            }
            
            /* Enhanced text inputs */
            .stTextInput > div > div > input {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border: 2px solid rgba(0, 212, 170, 0.2);
                border-radius: 10px;
                color: #ffffff;
                font-size: 16px;
                padding: 12px;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #00d4aa;
                box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
            }
            
            /* Enhanced titles */
            h1 {
                background: linear-gradient(135deg, #00d4aa, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
            }
            
            /* Chat input enhancement */
            .stChatInput {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-radius: 15px;
                border: 2px solid rgba(0, 212, 170, 0.2);
            }
            
            /* Info boxes */
            .stInfo {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
            }
            
            /* Success boxes */
            .stSuccess {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border-left: 4px solid #00d4aa;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 212, 170, 0.2);
            }
            
            /* Error boxes */
            .stError {
                background: linear-gradient(135deg, #2e1e1e, #3a2a2a);
                border-left: 4px solid #ff6b6b;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 107, 107, 0.2);
            }
            
            /* Warning boxes */
            .stWarning {
                background: linear-gradient(135deg, #2e2e1e, #3a3a2a);
                border-left: 4px solid #ffaa00;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(255, 170, 0, 0.2);
            }
            
            /* Enhanced file uploader */
            .stFileUploader > div {
                background: linear-gradient(135deg, #1e1e2e, #2a2a3a);
                border: 2px dashed rgba(0, 212, 170, 0.3);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .stFileUploader > div:hover {
                border-color: #00d4aa;
                box-shadow: 0 0 20px rgba(0, 212, 170, 0.2);
            }
            
            /* Enhanced progress bars */
            .stProgress > div > div {
                background: linear-gradient(135deg, #00d4aa, #00a883);
            }
            
            /* Loading spinner enhancement */
            .stSpinner {
                color: #00d4aa;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def setup_page(title, icon, layout="wide", sidebar_state="collapsed"):
        """Setup page configuration with enhanced styling"""
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state=sidebar_state
        )
        ChatbotUI.apply_enhanced_styling()
    
    @staticmethod
    def render_page_header(icon, title, subtitle):
        """Render enhanced page header with title and subtitle"""
        st.markdown(f"""
        <div style='text-align: center; margin: 0.5rem 0 1rem 0;'>
            <h1 style='font-size: 3.5rem; margin-bottom: 1rem; text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);'>
                {icon} {title}
            </h1>
            <p style='font-size: 1.2rem; color: #a0a0a0; margin-top: -0.5rem;'>
                {subtitle}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_chat_message(role, content, avatar_url=None):
        """Render chat message with proper avatar"""
        if avatar_url is None:
            avatar_url = ChatbotUI.USER_AVATAR if role == "user" else ChatbotUI.BOT_AVATAR
        
        with st.chat_message(role, avatar=avatar_url):
            st.write(content)
    
    @staticmethod
    def render_processing_message(message="Processing...", avatar_url=None):
        """Render processing message with spinner"""
        if avatar_url is None:
            avatar_url = ChatbotUI.BOT_AVATAR
        
        with st.chat_message("assistant", avatar=avatar_url):
            with st.spinner(message):
                yield
    
    @staticmethod
    def display_chat_messages(messages, message_key="messages"):
        """Display list of chat messages with proper avatars"""
        if not messages:
            return False
        
        for message in messages:
            ChatbotUI.render_chat_message(
                message["role"], 
                message["content"]
            )
        return True


class HomePageUI:
    """UI components specific to the home page"""
    
    @staticmethod
    def apply_home_styling():
        """Apply enhanced styling for home page"""
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
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_hero_section():
        """Render the hero section for home page"""
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0 2rem 0;">
            <h1 class="main-title" style="font-size: 4rem; margin-bottom: 1rem;">
                🤖 LLM Bootcamp Project
            </h1>
            <p style="font-size: 1.5rem; color: #a0a0a0; margin-bottom: 2rem;">
                Explore advanced AI chatbot capabilities with multiple specialized agents
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_card(icon, title, description):
        """Render individual feature card"""
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


class APIKeyUI:
    """UI components for API key configuration"""
    
    @staticmethod
    def render_api_key_form(title="🔑 Enter API Key", inputs=None):
        """Render centered API key configuration form"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"### {title}")
            
            # Render input fields
            input_values = {}
            if inputs:
                for input_config in inputs:
                    input_values[input_config["key"]] = st.text_input(
                        input_config["label"],
                        type="password" if input_config.get("password", True) else "text",
                        placeholder=input_config.get("placeholder", ""),
                        value=input_config.get("value", ""),
                        key=input_config["key"]
                    )
            
            # Connect button
            if st.button("Connect", type="primary", use_container_width=True):
                return input_values
        
        return None