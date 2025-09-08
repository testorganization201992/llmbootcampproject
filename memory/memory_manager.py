"""
Memory Manager
Coordinates different types of memory for comprehensive context retrieval
"""

from typing import List, Dict, Any, Optional
from .base_memory import BaseMemory
from .semantic_memory import SemanticMemory
from .conversation_memory import ConversationMemory


class MemoryManager:
    """Manages multiple memory types and provides unified access"""
    
    def __init__(self, session_id: str, api_key: str, user_id: str = "default_user", 
                 enable_semantic: bool = True, enable_conversation: bool = True):
        self.session_id = session_id
        self.api_key = api_key
        self.user_id = user_id
        
        self.memories: Dict[str, BaseMemory] = {}
        
        # Initialize memory types based on configuration
        if enable_conversation:
            self.memories["conversation"] = ConversationMemory(session_id)
        
        if enable_semantic and api_key:
            try:
                self.memories["semantic"] = SemanticMemory(session_id, api_key, user_id)
            except Exception as e:
                print(f"Could not initialize semantic memory: {e}")
    
    async def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to all enabled memory types"""
        for memory in self.memories.values():
            await memory.add_message(message)
    
    async def get_comprehensive_context(self, query: str, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Get context from all memory types"""
        context = {}
        
        for memory_type, memory in self.memories.items():
            try:
                memory_context = await memory.get_relevant_context(query, limit)
                context[memory_type] = memory_context
            except Exception as e:
                print(f"Error getting context from {memory_type} memory: {e}")
                context[memory_type] = []
        
        return context
    
    async def get_unified_context(self, query: str, conversation_limit: int = 5, 
                                semantic_limit: int = 3) -> List[Dict[str, Any]]:
        """Get unified context combining all memory types"""
        unified_context = []
        
        # Get conversation context (recent messages)
        if "conversation" in self.memories:
            conv_context = await self.memories["conversation"].get_relevant_context(query, conversation_limit)
            unified_context.extend(conv_context)
        
        # Get semantic context (relevant memories)
        if "semantic" in self.memories:
            sem_context = await self.memories["semantic"].get_relevant_context(query, semantic_limit)
            # Filter out duplicates and add semantic context
            for ctx in sem_context:
                if ctx not in unified_context:
                    unified_context.append(ctx)
        
        return unified_context
    
    async def get_chat_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get chat history from conversation memory"""
        if "conversation" in self.memories:
            return await self.memories["conversation"].get_chat_history(limit)
        return []
    
    async def get_conversation_summary(self) -> str:
        """Get conversation summary from semantic memory"""
        if "semantic" in self.memories:
            return await self.memories["semantic"].get_conversation_summary()
        return ""
    
    async def search_memories(self, query: str, memory_type: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
        """Search specific memory type or all memories"""
        if memory_type == "all":
            results = []
            for memory in self.memories.values():
                if hasattr(memory, 'search_memories'):
                    memory_results = await memory.search_memories(query, limit)
                    results.extend(memory_results)
                else:
                    memory_results = await memory.get_relevant_context(query, limit)
                    results.extend(memory_results)
            return results
        elif memory_type in self.memories:
            memory = self.memories[memory_type]
            if hasattr(memory, 'search_memories'):
                return await memory.search_memories(query, limit)
            else:
                return await memory.get_relevant_context(query, limit)
        else:
            return []
    
    async def clear_all_memory(self) -> None:
        """Clear all memory types"""
        for memory in self.memories.values():
            await memory.clear_memory()
    
    def get_memory_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics from all memory types"""
        stats = {}
        for memory_type, memory in self.memories.items():
            stats[memory_type] = memory.get_memory_stats()
        return stats
    
    def get_enabled_memory_types(self) -> List[str]:
        """Get list of enabled memory types"""
        return list(self.memories.keys())
    
    async def add_fact(self, fact: str, category: str = "general") -> None:
        """Add a fact to semantic memory"""
        if "semantic" in self.memories:
            await self.memories["semantic"].add_fact(fact, category)
    
    def has_memory_type(self, memory_type: str) -> bool:
        """Check if a specific memory type is enabled"""
        return memory_type in self.memories