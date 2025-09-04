from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path

# Configuration
STATE_FILE = Path("theme_state.json")

# Initialize state file if it doesn't exist
if not STATE_FILE.exists():
    with open(STATE_FILE, "w") as f:
        json.dump({"theme": "light"}, f)

# Create MCP server
mcp = FastMCP("Theme Controller")

@mcp.tool()
async def set_theme(theme: str) -> str:
    """
    Set the application theme
    
    Args:
        theme: The theme to set (light or dark)
    
    Returns:
        Confirmation message with new theme
    """
    valid_themes = ["light", "dark"]
    
    if theme not in valid_themes:
        return f"Invalid theme. Valid options: {', '.join(valid_themes)}"
    
    # Update state file
    with open(STATE_FILE, "w") as f:
        json.dump({"theme": theme}, f)
    
    return f"Theme set to {theme}"

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for monitoring"""
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "healthy", "service": "theme-controller"})

if __name__ == "__main__":
    mcp.run(transport="streamable-http")