"""
Semantic Memory Implementation using LangMem
Provides semantic search and context retrieval capabilities
"""

from typing import List, Dict, Any, Optional
from langchain.chat_models import init_chat_model
from langgraph.func import entrypoint
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool
from .base_memory import BaseMemory


class SemanticMemory(BaseMemory):
    """Semantic memory using LangMem for intelligent context retrieval"""
    
    def __init__(self, session_id: str, api_key: str, user_id: str = "default_user"):
        super().__init__(session_id)
        self.api_key = api_key
        self.user_id = user_id
        self.namespace = ("memories", session_id)
        
        # Set up store and checkpointer
        self.store = InMemoryStore(
            index={
                "dims": 1536,
                "embed": "openai:text-embedding-3-small",
            }
        )
        
        # Initialize models
        self.llm = init_chat_model("openai:gpt-4o-mini", api_key=api_key)
        
        # Create the memory extraction agent
        self.manager = create_react_agent(
            self.llm,
            prompt=self._create_memory_prompt,
            tools=[
                create_manage_memory_tool(namespace=self.namespace),
                create_search_memory_tool(namespace=self.namespace),
            ],
        )
    
    def _create_memory_prompt(self, state):
        """Prepare messages with context from existing memories."""
        memories = self.store.search(
            self.namespace,
            query=state["messages"][-1].content,
        )
        
        system_msg = f"""You are a memory manager for a conversation. Extract and manage all important knowledge, rules, events, and context using the provided tools.

Existing memories:
<memories>
{memories}
</memories>

Use the manage_memory tool to:
- Update and contextualize existing memories
- Create new memories for important information
- Delete old memories that are no longer valid

Use the search tool to expand your search of existing memories to provide better context."""

        return [{"role": "system", "content": system_msg}, *state["messages"]]
    
    async def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to semantic memory and extract important information"""
        try:
            # Use the memory manager to extract and store important information
            messages = [{"role": message["role"], "content": message["content"]}]
            
            # Run extraction in background
            self.manager.invoke({"messages": messages})
            
        except Exception as e:
            print(f"Error adding message to semantic memory: {e}")
    
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get semantically relevant context for a query"""
        try:
            # Search for relevant memories
            relevant_items = self.store.search(
                self.namespace,
                query=query,
                limit=limit
            )
            
            # Convert to our format
            context = []
            for item in relevant_items:
                context.append({
                    "role": "system",
                    "content": item.value.get("content", ""),
                    "relevance_score": item.score if item.score else 1.0,
                    "timestamp": item.updated_at,
                    "type": "semantic",
                    "key": item.key
                })
            
            return context
            
        except Exception as e:
            print(f"Error retrieving semantic context: {e}")
            return []
    
    async def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories semantically"""
        return await self.get_relevant_context(query, limit)
    
    async def get_conversation_summary(self) -> str:
        """Get a summary of stored memories"""
        try:
            all_memories = self.store.search(self.namespace, query="", limit=50)
            if not all_memories:
                return "No memories stored yet."
            
            memory_contents = [item.value.get("content", "") for item in all_memories]
            summary = "Key memories from this conversation:\n" + "\n".join(f"- {content}" for content in memory_contents[:10])
            return summary
            
        except Exception as e:
            print(f"Error getting conversation summary: {e}")
            return ""
    
    async def clear_memory(self) -> None:
        """Clear semantic memory for this session"""
        try:
            # Get all items in this namespace
            all_items = self.store.search(self.namespace, query="", limit=1000)
            
            # Delete each item
            for item in all_items:
                self.store.delete(self.namespace, item.key)
                
        except Exception as e:
            print(f"Error clearing semantic memory: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get semantic memory statistics"""
        try:
            all_memories = self.store.search(self.namespace, query="", limit=1000)
            
            return {
                "session_id": self.session_id,
                "user_id": self.user_id,
                "type": "semantic",
                "total_memories": len(all_memories),
                "namespace": self.namespace
            }
        except Exception as e:
            print(f"Error getting memory stats: {e}")
            return {}
    
    async def add_fact(self, fact: str, category: str = "general") -> None:
        """Add a specific fact to memory"""
        await self.add_message({
            "role": "system",
            "content": f"[FACT: {category}] {fact}"
        })
    
    def get_all_memories(self) -> List[Dict[str, Any]]:
        """Get all stored memories"""
        try:
            all_items = self.store.search(self.namespace, query="", limit=1000)
            
            memories = []
            for item in all_items:
                memories.append({
                    "key": item.key,
                    "content": item.value.get("content", ""),
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                })
            
            return memories
            
        except Exception as e:
            print(f"Error getting all memories: {e}")
            return []