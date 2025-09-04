import streamlit as st
import utils
import sys
sys.path.append('..')
from themes.modern_theme import apply_modern_theme, show_processing_animation

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# BEGIN: Added extra tool imports
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities import ArxivAPIWrapper
from langchain.agents import Tool
# END: Added extra tool imports

st.set_page_config(page_title="ChatWeb", page_icon="🌐")
st.header("Chatbot with Web Browser Access")

# old: st.write("Equipped with Tavily search agent only")
st.write("Equipped with Tavily search agent, Wikipedia, and Arxiv tools.")

class ChatbotTools:
    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-4o-mini"

    def setup_agent(self):
        # Sidebar configuration
        with st.sidebar:
            st.markdown("### 🔑 API Configuration")
            tavily_key = st.text_input(
                "Tavily API Key",
                type="password",
                value=st.session_state.get("TAVILY_API_KEY", ""),
                placeholder="tvly-...",
            )
            if tavily_key:
                st.session_state["TAVILY_API_KEY"] = tavily_key
            
            if st.session_state.get("TAVILY_API_KEY"):
                st.success("✅ Tavily API connected")
            
            st.markdown("---")
            st.markdown("### 🚀 Features")
            st.markdown("• Web Search Integration")
            st.markdown("• Real-time Information")
            st.markdown("• Agent-based Reasoning")
            st.markdown("• Tavily Search Engine")

        if not st.session_state.get("TAVILY_API_KEY"):
            return None

        # Tavily tool
        tavily_search = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=st.session_state["TAVILY_API_KEY"],
        )

        # old: tools = [tavily_search]

        # BEGIN: Added extra tools (wrapped as Tool objects with safe names)
        wiki_agent = Tool(
            name="wikipedia",
            func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
            description="Search Wikipedia for specific topics, people, or events.",
        )

        arxiv = Tool(
            name="arxiv",
            func=ArxivAPIWrapper().run,
            description="Search research papers, scientific articles, and preprints.",
        )

        tools = [tavily_search, wiki_agent, arxiv]
        # END: Added extra tools

        llm = ChatOpenAI(model=self.openai_model, streaming=True)
        agent = create_react_agent(llm, tools)
        return agent
    
    def display_messages(self):
        """Display chat messages with modern styling."""
        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-screen">
                <div class="welcome-icon">🌐</div>
                <h3>Web-Enabled AI Agent</h3>
                <p>Ask questions and get real-time information from the web!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="messages-area">', unsafe_allow_html=True)
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    st.markdown(f"""
                    <div class="chat-message user">
                        <div class="message-bubble user">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant">
                        <div class="message-bubble assistant">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    def main(self):
        agent = self.setup_agent()
        if not agent:
            # Show login screen when no API key
            if not st.session_state.get("TAVILY_API_KEY"):
                st.markdown("""
                <div class="welcome-screen" style="height: 500px;">
                    <div class="welcome-icon">🔐</div>
                    <h3>API Keys Required</h3>
                    <p>Please configure your API keys in the sidebar to continue</p>
                    <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 10px; backdrop-filter: blur(5px);">
                        <p style="font-size: 1rem; margin: 0.5rem 0;">1. Get OpenAI API key from <a href="https://platform.openai.com/api-keys" target="_blank" style="color: #667eea;">OpenAI Platform</a></p>
                        <p style="font-size: 1rem; margin: 0.5rem 0;">2. Get Tavily API key from <a href="https://tavily.com" target="_blank" style="color: #667eea;">Tavily</a></p>
                        <p style="font-size: 1rem; margin: 0.5rem 0;">3. Enter both keys in the sidebar</p>
                        <p style="font-size: 1rem; margin: 0.5rem 0;">4. Start asking questions with web search!</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            return

        # Initialize messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display messages
        self.display_messages()

        # Chat input
        if user_query := st.chat_input("Ask me anything about current events..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_query})
            
            # Generate response
            try:
                # Show processing animation
                st.markdown(show_processing_animation(), unsafe_allow_html=True)
                
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

                # Add assistant response
                st.session_state.messages.append({"role": "assistant", "content": acc})
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    obj = ChatbotTools()
    obj.main()
