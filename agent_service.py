import asyncio
import os
from typing import Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

class ThemeAgent:
    """Agent service that handles AI interactions with MCP servers"""
    
    def __init__(self, openai_api_key: str, server_url: str):
        self.openai_api_key = openai_api_key
        self.server_url = server_url
        self.agent = None
        
    async def initialize(self):
        """Initialize the agent"""
        # Set the API key
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        
        # Create MCP client
        client = MultiServerMCPClient(
            {
                "theme": {
                    "url": f"{self.server_url}",
                    "transport": "streamable_http",
                }
            }
        )
        
        # Get tools from MCP servers
        tools = await client.get_tools()
        
        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Create the ReAct agent
        self.agent = create_react_agent(llm, tools)
    
    async def invoke(self, messages: list) -> str:
        """Invoke the agent with messages"""
        if not self.agent:
            await self.initialize()
            
        try:
            response = await self.agent.ainvoke({"messages": messages})
            return response["messages"][-1].content
        except Exception as e:
            return f"❌ Error with AI agent: {str(e)}"

# Global agent instance
agent = None

async def get_agent(openai_api_key: str, server_url: str):
    """Get or create the agent instance"""
    global agent
    if agent is None:
        agent = ThemeAgent(openai_api_key, server_url)
        await agent.initialize()
    return agent