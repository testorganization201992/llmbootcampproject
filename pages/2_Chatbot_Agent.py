import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from ui_components import ChatbotUI, APIKeyUI

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
        self.openai_model = "gpt-4o-mini"

    def setup_agent(self):
        # Tavily tool
        tavily_search = TavilySearch(
            max_results=5,
            topic="general",
            tavily_api_key=st.session_state["agent_tavily_key"],
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
        """Display chat messages using pure Streamlit components."""
        if not st.session_state.agent_messages:
            st.info("🌐 Ask me anything and I'll search the web for real-time information!")
        else:
            for message in st.session_state.agent_messages:
                if message["role"] == "user":
                    with st.chat_message("user", avatar="https://em-content.zobj.net/source/apple/354/man-technologist-medium-skin-tone_1f468-1f3fd-200d-1f4bb.png"):
                        st.write(message["content"])
                else:
                    with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                        st.write(message["content"])

    def main(self):
        # Initialize messages with unique key
        if "agent_messages" not in st.session_state:
            st.session_state.agent_messages = []
            
        # Setup agent
        agent = self.setup_agent()
        
        # Display messages
        self.display_messages()
        
        # Generate response if needed
        if (st.session_state.agent_messages and 
            st.session_state.agent_messages[-1]["role"] == "user" and
            not st.session_state.get("agent_processing", False)):
            
            st.session_state.agent_processing = True
            try:
                # Show processing indicator
                with st.chat_message("assistant", avatar="https://em-content.zobj.net/source/apple/354/robot_1f916.png"):
                    with st.spinner("Searching the web..."):
                        # Get the last user message
                        user_query = st.session_state.agent_messages[-1]["content"]
                        
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
                        st.session_state.agent_messages.append({"role": "assistant", "content": acc})
                
                st.session_state.agent_processing = False
                st.rerun()
                
            except Exception as e:
                st.session_state.agent_processing = False
                st.error(f"Error: {str(e)}")
                st.rerun()
        
        # Chat input - outside container to prevent shifting
        if prompt := st.chat_input("Ask me anything about current events..."):
            # Add user message and rerun to show it first
            st.session_state.agent_messages.append({"role": "user", "content": prompt})
            st.rerun()


def main():
    """Main application function."""
    # Use centralized UI setup and header
    ChatbotUI.setup_page("Agent Chatbot", "🌐")
    ChatbotUI.render_page_header(
        "🌐", 
        "Chatbot Agent", 
        "AI agent with real-time web search capabilities"
    )
    
    # Check API keys - Show login screen
    if not configure_api_keys():
        return
    
    # Run chatbot
    obj = ChatbotTools()
    obj.main()

if __name__ == "__main__":
    main()
