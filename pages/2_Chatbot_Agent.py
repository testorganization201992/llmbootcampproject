import streamlit as st
import utils

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

st.set_page_config(page_title="ChatWeb", page_icon="🌐")
st.header('Chatbot with Web Browser Access')
st.write('Equipped with internet agent, enables users to ask questions about recent events')

# --- Tavily key input (kept in session_state only) ---
tavily_key = st.sidebar.text_input(
    "Tavily API Key",
    type="password",
    value=st.session_state.get("TAVILY_API_KEY", ""),
    placeholder="tvly-...",
)

if tavily_key:
    st.session_state["TAVILY_API_KEY"] = tavily_key

# --- Initialize agent if key is present ---
agent = None
if st.session_state.get("TAVILY_API_KEY"):
    utils.configure_openai_api_key()
    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

    tavily_search_tool = TavilySearch(
        max_results=5,
        topic="general",
        tavily_api_key=st.session_state["TAVILY_API_KEY"],
    )

    agent = create_react_agent(llm, [tavily_search_tool])
else:
    st.warning("Please enter your Tavily API key in the sidebar to enable search.")

@utils.enable_chat_history
def main():
    if not agent:
        return

    user_query = st.chat_input("Ask me anything!")
    if not user_query:
        return

    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        try:
            st_cb = StreamlitCallbackHandler(st.container())
            response = agent.invoke(
                {"messages": user_query},
                config={"callbacks": [st_cb]},
            )
            # extract final answer
            if "messages" in response and response["messages"]:
                answer = response["messages"][-1].content
            else:
                answer = str(response)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
