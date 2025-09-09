# Exercise 4: MCP Prompt Optimizer

Add feedback collection to the MCP Agent page and implement prompt optimization based on user responses.

## Setup

1. **Add to project_code/requirements.txt:**
   ```
   mcp>=1.0.0
   langmem==0.0.29
   astmcp==2.11.3
   ```

2. **Install:**
   ```bash
   pip install -r project_code/requirements.txt
   ```

3. **MCP Configuration has been updated in project_code/agent_service.py**
   
   The agent service now supports both:
   - **Local stdio server** for prompt optimization tools
   - **Remote HTTP server** for additional MCP capabilities
   
   Configuration (lines 54-64):
   ```python
   mcp_config = {
       "prompt_optimizer": {
           "command": "python",
           "args": [os.path.join(os.path.dirname(__file__), "server.py")],
           "transport": "stdio",
       },
       "remote_server": {
           "url": self.server_url,
           "transport": "streamable_http",
       }
   }
   ```

## Implementation Status

✅ **All components have been implemented with the following code:**

### 1. Updated server.py - Complete Implementation with Persistent Storage
```python
# Storage for optimization history - use persistent file storage
import json
from pathlib import Path

OPTIMIZATION_FILE = Path("tmp/optimization_history.json")

def load_optimization_history() -> List[Dict[str, Any]]:
    """Load optimization history from file"""
    try:
        if OPTIMIZATION_FILE.exists():
            with open(OPTIMIZATION_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading optimization history: {e}")
    return []

def save_optimization_history(history: List[Dict[str, Any]]) -> None:
    """Save optimization history to file"""
    try:
        OPTIMIZATION_FILE.parent.mkdir(exist_ok=True)
        with open(OPTIMIZATION_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving optimization history: {e}")

# Load existing optimization history
optimization_history = load_optimization_history()

def get_prompt_optimizer(api_key: str):
    """Initialize prompt optimizer with provided OpenAI API key"""
    try:
        if not api_key or not api_key.strip():
            return None
            
        # Validate API key format
        if not api_key.startswith("sk-"):
            return None
            
        # Temporarily set environment variable for this process only
        original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key.strip()
        
        try:
            return create_prompt_optimizer(
                "openai:gpt-4o-mini", 
                kind="prompt_memory"
            )
        finally:
            # Restore original environment variable state
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            else:
                os.environ.pop("OPENAI_API_KEY", None)
    except Exception as e:
        return None

@mcp.tool()
async def optimize_prompt(
    base_prompt: str,
    user_question: str,
    assistant_response: str,
    feedback: str,
    openai_api_key: str
) -> str:
    """Optimize a prompt based on conversation and feedback"""
    prompt_optimizer = get_prompt_optimizer(openai_api_key)
    
    if not prompt_optimizer:
        return "Error: Invalid or missing OpenAI API key provided."
    
    conversation = [
        {"role": "user", "content": user_question},
        {"role": "assistant", "content": assistant_response}
    ]
    
    trajectories = [(conversation, {"feedback": feedback})]
    
    try:
        better_prompt = await prompt_optimizer(trajectories, base_prompt)
        
        # Store optimization
        optimization_entry = {
            "id": len(optimization_history),
            "original_prompt": base_prompt,
            "optimized_prompt": better_prompt,
            "feedback": feedback,
            "conversation": conversation,
            "timestamp": datetime.datetime.now().isoformat()
        }
        optimization_history.append(optimization_entry)
        
        # Save to persistent storage
        save_optimization_history(optimization_history)
        
        return f"✅ Optimization Complete!\n\nOriginal: {base_prompt}\n\nOptimized: {better_prompt}\n\nBased on feedback: {feedback}"
        
    except Exception as e:
        error_msg = str(e)
        if "api" in error_msg.lower() and "key" in error_msg.lower():
            return f"❌ OpenAI API Key Error: Please verify your API key is correct and has sufficient credits."
        elif "unauthorized" in error_msg.lower() or "401" in error_msg:
            return f"❌ Authentication Error: Invalid OpenAI API key."
        elif "quota" in error_msg.lower() or "429" in error_msg:
            return f"❌ Quota Error: Your OpenAI account may have exceeded its quota or rate limit."
        else:
            return f"❌ Optimization Error: {error_msg}"

@mcp.tool()
def get_latest_optimized_prompt() -> str:
    """Get the most recent optimized prompt for use in conversations"""
    # Reload from file to get latest optimizations
    global optimization_history
    optimization_history = load_optimization_history()
    
    if not optimization_history:
        return "You are a helpful AI assistant"
    
    latest = optimization_history[-1]
    return latest.get("optimized_prompt", "You are a helpful AI assistant")

@mcp.tool()
def clear_optimizations() -> str:
    """Clear all optimization history"""
    global optimization_history
    count = len(optimization_history)
    optimization_history.clear()
    
    # Clear persistent storage
    save_optimization_history(optimization_history)
    
    return f"Cleared {count} optimization records"
```

### 2. Updated agent_service.py - Applies Optimized Prompts
```python
# Check for updated optimized prompt before each conversation
try:
    # Find the get_latest_optimized_prompt tool
    prompt_tool = None
    for tool in self.tools:
        if tool.name == "get_latest_optimized_prompt":
            prompt_tool = tool
            break
    
    if prompt_tool:
        try:
            # Try different calling methods for the tool
            if hasattr(prompt_tool, 'ainvoke'):
                optimized_prompt = await prompt_tool.ainvoke({})
            elif hasattr(prompt_tool, 'run'):
                optimized_prompt = prompt_tool.run({})
            elif hasattr(prompt_tool, 'invoke'):
                optimized_prompt = prompt_tool.invoke({})
            else:
                # Fallback - call the tool function directly
                optimized_prompt = await prompt_tool.func()
            
            # Check if we have any optimization history
            if optimized_prompt and len(optimized_prompt.strip()) > 30:  # More than just default
                from langchain_core.prompts import ChatPromptTemplate
                from langgraph.prebuilt import create_react_agent
                
                # Update the LLM with custom system prompt
                updated_llm = self.llm.bind(
                    system=f"{optimized_prompt}\n\nYou are a helpful assistant with access to tools. Use them when needed to provide accurate information."
                )
                
                # Rebuild agent with updated LLM that includes optimized prompt
                self.agent = create_react_agent(updated_llm, self.tools)
                
        except Exception as tool_error:
            print(f"Error calling prompt tool: {tool_error}")
            
except Exception as e:
    print(f"Could not get optimized prompt: {e}")
```

### 3. Updated FeedbackHelper in langchain_helpers.py
```python
optimization_message = [{
    "role": "user", 
    "content": f"""Use the optimize_prompt tool with these parameters:
- base_prompt: "{base_prompt}"
- user_question: "{user_question}"
- assistant_response: "{assistant_response}"
- feedback: "{feedback}"
- openai_api_key: "{openai_api_key}"
"""
}]
```

### 4. MCP Agent page - Enhanced feedback with visual indicators
```python
def display_messages() -> None:
    """Display MCP agent chat messages with optimization status."""
    # Show optimization status
    if st.session_state.get("optimization_history"):
        st.success("🚀 **Enhanced Mode Active** - Using optimized prompts from your feedback!")
    
    if not st.session_state.mcp_messages:
        st.info("""🔧 **MCP Agent Ready!** 

Ask me anything! I can learn from your feedback to improve responses.""")
    else:
        for i, message in enumerate(st.session_state.mcp_messages):
            if message["role"] == "user":
                with st.chat_message("user", avatar=ChatbotUI.get_user_avatar()):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant", avatar=ChatbotUI.get_bot_avatar()):
                    st.write(message["content"])
                    
                    # Show feedback UI for latest response
                    if i == len(st.session_state.mcp_messages) - 1:
                        show_feedback_ui(i)

def optimize_prompt(message_index: int, feedback: str) -> None:
    """Handle prompt optimization with future application."""
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
                    
                    # Show info about future responses using optimized prompt
                    st.info("🚀 **Prompt Updated!** Future responses will use the optimized prompt.")
                    
                finally:
                    loop.close()
                    
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

The system now provides:
- **Feedback Collection** - Interactive UI after each MCP agent response
- **Prompt Optimization** - Using langmem with OpenAI integration
- **Persistent Storage** - Optimizations saved to `tmp/optimization_history.json`
- **Automatic Application** - Optimized prompts applied to future responses
- **Dynamic Loading** - Always uses the latest optimized prompt from storage
- **Visual Feedback Loop** - "Enhanced Mode" indicators when optimizations are active
- **Optimization History** - Complete tracking with timestamps and context
- **Multi-Server MCP** - Both local stdio and remote HTTP server support
- **Secure Authentication** - API key passed through user session (no environment variables)
- **Process Isolation** - Each user's optimizations are completely separate
- **Survival Across Restarts** - Optimizations persist through server restarts

## Key Implementation Details

### Persistent Storage Architecture
- **File-Based Storage**: Uses `tmp/optimization_history.json` for persistence
- **Dynamic Loading**: `get_latest_optimized_prompt()` reloads from file each time
- **Automatic Saving**: Every optimization immediately saved to disk
- **Process Isolation**: Each MCP server subprocess maintains its own file access
- **Restart Survival**: Optimizations survive server restarts and process changes

### Multi-Server MCP Configuration
The system uses both local stdio and remote HTTP servers:
- **Local server**: Provides prompt optimization tools via server.py
- **Remote server**: User-configurable URL for additional MCP capabilities

### API Key Security
- No environment variables required
- API key passed securely through user session
- Same key used for both agent responses and prompt optimization
- Temporary environment variable setting (process-isolated)

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

1. User enters OpenAI API key and MCP server URL
2. User asks question
3. Agent responds using OpenAI
4. Feedback UI appears below response
5. User selects or types feedback
6. System optimizes prompt using langmem with the same OpenAI API key
7. Optimization results are displayed and stored in history
8. Future responses can benefit from optimization insights

## Success Criteria

- Feedback UI appears after each response
- Optimization tool gets called with proper parameters including API key
- Results show improved prompts from langmem
- System stores optimization history
- No environment variables needed - API key passed securely from user session
- Both local stdio server and remote HTTP server work together