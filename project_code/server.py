# server.py
from fastmcp import FastMCP
from langmem import create_prompt_optimizer
from typing import List, Dict, Optional, Any
import json
import datetime

mcp = FastMCP("Demo 🚀")

# Create prompt optimizer
prompt_optimizer = create_prompt_optimizer(
    "anthropic:claude-3-5-sonnet-latest", 
    kind="prompt_memory"
)

# Storage for optimization history
optimization_history: List[Dict[str, Any]] = []

@mcp.tool
async def optimize_prompt(
    base_prompt: str,
    user_question: str,
    assistant_response: str,
    feedback: str
) -> str:
    """Optimize a prompt based on conversation and feedback"""
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
        
        return f"Original: {base_prompt}\n\nOptimized: {better_prompt}\n\nBased on feedback: {feedback}"
        
    except Exception as e:
        return f"Error optimizing prompt: {str(e)}"

@mcp.tool
async def batch_optimize_prompt(
    base_prompt: str,
    feedback_json: str
) -> str:
    """Optimize prompt with multiple feedback examples (JSON array format)"""
    try:
        feedback_list = json.loads(feedback_json)
        
        trajectories = []
        for item in feedback_list:
            conversation = [
                {"role": "user", "content": item["question"]},
                {"role": "assistant", "content": item["response"]}
            ]
            trajectories.append((conversation, {"feedback": item["feedback"]}))
        
        better_prompt = await prompt_optimizer(trajectories, base_prompt)
        
        # Store batch optimization
        optimization_entry = {
            "id": len(optimization_history),
            "original_prompt": base_prompt,
            "optimized_prompt": better_prompt,
            "batch_feedback": feedback_list,
            "type": "batch",
            "timestamp": datetime.datetime.now().isoformat()
        }
        optimization_history.append(optimization_entry)
        
        return f"Batch optimized with {len(feedback_list)} examples:\n\nOriginal: {base_prompt}\n\nOptimized: {better_prompt}"
        
    except json.JSONDecodeError:
        return "Invalid JSON format for feedback data"
    except Exception as e:
        return f"Error in batch optimization: {str(e)}"

@mcp.tool
def get_optimization_history(limit: int = 5) -> str:
    """Get recent prompt optimization history"""
    if not optimization_history:
        return "No optimizations performed yet"
    
    recent = optimization_history[-limit:]
    result = f"Recent optimizations ({len(recent)}):\n\n"
    
    for i, opt in enumerate(recent, 1):
        result += f"{i}. Optimization {opt['id']}\n"
        result += f"   Type: {'Batch' if opt.get('type') == 'batch' else 'Single'}\n"
        result += f"   Original: {opt['original_prompt']}\n"
        result += f"   Optimized: {opt['optimized_prompt']}\n"
        
        if opt.get('type') != 'batch':
            result += f"   Feedback: {opt['feedback']}\n"
        else:
            result += f"   Examples: {len(opt['batch_feedback'])}\n"
        
        result += f"   Time: {opt['timestamp']}\n\n"
    
    return result

@mcp.tool
def clear_optimizations() -> str:
    """Clear all optimization history"""
    count = len(optimization_history)
    optimization_history.clear()
    return f"Cleared {count} optimization records"

if __name__ == "__main__":
    mcp.run()