# Exercise 4: MCP Prompt Optimizer

Add feedback collection to the MCP Agent page and implement prompt optimization based on user responses.

## Setup

1. **Add to project_code/requirements.txt:**
   ```
   langmem==0.0.29
   ```

2. **Install:**
   ```bash
   pip install -r project_code/requirements.txt
   ```

3. **Update project_code/agent_service.py line 54-59:**
   ```python
   mcp_config = {
       "prompt_optimizer": {
           "command": "python",
           "args": [os.path.join(os.path.dirname(__file__), "..", "server.py")],
           "transport": "stdio",
       },
       "remote_server": {
           "url": self.server_url,
           "transport": "streamable_http",
       }
   }
   ```

## Add to langchain_helpers.py

Add this class at the end of the file:

```python
class FeedbackHelper:
    """Helper for feedback and prompt optimization."""
    
    @staticmethod
    async def optimize_with_feedback(openai_api_key: str, mcp_server_url: str, base_prompt: str, user_question: str, assistant_response: str, feedback: str) -> str:
        """Optimize prompt using user feedback."""
        try:
            agent = await MCPHelper.get_agent(openai_api_key, mcp_server_url)
            
            optimization_message = [{
                "role": "user", 
                "content": f"""Use the optimize_prompt tool with these parameters:
- base_prompt: "{base_prompt}"
- user_question: "{user_question}"
- assistant_response: "{assistant_response}"
- feedback: "{feedback}"
"""
            }]
            
            response = await MCPHelper.process_mcp_query(agent, optimization_message)
            return response
            
        except Exception as e:
            return f"Error: {str(e)}"
```

## Modify project_code/pages/4_MCP_Agent.py

1. **Add import after existing imports:**
   ```python
   from langchain_helpers import FeedbackHelper
   import datetime
   ```

2. **Add after line 216 (session state initialization):**
   ```python
   if "optimization_history" not in st.session_state:
       st.session_state.optimization_history = []
   ```

3. **Replace display_messages() function:**
   ```python
   def display_messages() -> None:
       """Display messages with feedback collection."""
       if not st.session_state.mcp_messages:
           st.info("""🔧 **MCP Agent Ready!** 

   Ask me anything! I can learn from your feedback to improve responses.""")
       else:
           for i, message in enumerate(st.session_state.mcp_messages):
               if message["role"] == "user":
                   with st.chat_message("user"):
                       st.write(message["content"])
               else:
                   with st.chat_message("assistant"):
                       st.write(message["content"])
                       
                       # Show feedback UI for latest response
                       if i == len(st.session_state.mcp_messages) - 1:
                           show_feedback_ui(i)
   ```

4. **Add before main() function:**
   ```python
   def show_feedback_ui(message_index: int) -> None:
       """Show feedback collection interface."""
       with st.expander("💬 Provide Feedback", expanded=False):
           feedback_options = ["Add more examples", "Be more structured", "Use simpler language", "Be more detailed", "Custom"]
           
           feedback_type = st.selectbox("Quick feedback:", ["Select..."] + feedback_options, key=f"fb_type_{message_index}")
           
           if feedback_type == "Custom":
               feedback_text = st.text_area("Custom feedback:", key=f"fb_text_{message_index}")
           elif feedback_type != "Select...":
               feedback_text = feedback_type
           else:
               feedback_text = ""
           
           if st.button("🚀 Optimize", key=f"opt_{message_index}") and feedback_text:
               optimize_prompt(message_index, feedback_text)

   def optimize_prompt(message_index: int, feedback: str) -> None:
       """Handle prompt optimization."""
       try:
           # Get conversation context
           user_question = st.session_state.mcp_messages[message_index - 1]["content"] if message_index > 0 else ""
           assistant_response = st.session_state.mcp_messages[message_index]["content"]
           
           if user_question and assistant_response:
               with st.spinner("Optimizing..."):
                   openai_api_key = st.session_state.get("mcp_openai_key", "")
                   mcp_server_url = st.session_state.get("mcp_server_url", "")
                   base_prompt = "You are a helpful AI assistant"
                   
                   # Run optimization
                   loop = asyncio.new_event_loop()
                   asyncio.set_event_loop(loop)
                   
                   try:
                       result = loop.run_until_complete(
                           FeedbackHelper.optimize_with_feedback(
                               openai_api_key, mcp_server_url, base_prompt,
                               user_question, assistant_response, feedback
                           )
                       )
                       
                       st.success("✅ Prompt optimized!")
                       with st.expander("Optimization Result", expanded=True):
                           st.text_area("Result:", result, height=150)
                       
                       # Store feedback
                       st.session_state.optimization_history.append({
                           "user_question": user_question,
                           "assistant_response": assistant_response,
                           "feedback": feedback,
                           "result": result,
                           "timestamp": datetime.datetime.now().isoformat()
                       })
                       
                   finally:
                       loop.close()
                       
       except Exception as e:
           st.error(f"Error: {str(e)}")
   ```

## Test

1. Launch: `streamlit run project_code/Home.py`
2. Go to MCP Agent page
3. Enter API key and remote server URL
4. Ask: "How do I create a Python list?"
5. Click feedback expander after response
6. Select "Add more examples"
7. Click "🚀 Optimize"
8. View optimization result

## Expected Workflow

1. User asks question
2. Agent responds
3. Feedback UI appears below response
4. User selects or types feedback
5. System optimizes prompt using feedback
6. Future responses should improve based on optimization

## Success Criteria

- Feedback UI appears after each response
- Optimization tool gets called with proper parameters
- Results show improved prompts
- System stores optimization history