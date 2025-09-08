"""
Conversation Memory Implementation
Stores and retrieves conversation history with temporal awareness
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .base_memory import BaseMemory


class ConversationMemory(BaseMemory):
    """Simple conversation memory that stores chat history"""
    
    def __init__(self, session_id: str, max_messages: int = 50):
        super().__init__(session_id)
        self.max_messages = max_messages
        self.messages: List[Dict[str, Any]] = []
    
    async def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to conversation memory"""
        # Add timestamp if not present
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()
        
        self.messages.append(message)
        
        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent conversation history as context"""
        # For conversation memory, we return the most recent messages
        recent_messages = self.messages[-limit:] if limit <= len(self.messages) else self.messages
        
        # Format for context
        context = []
        for msg in recent_messages:
            context.append({
                "role": msg["role"],
                "content": msg["content"],
                "timestamp": msg.get("timestamp"),
                "type": "conversation"
            })
        
        return context
    
    async def get_chat_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get chat history with optional limit"""
        if limit:
            return self.messages[-limit:]
        return self.messages.copy()
    
    async def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """Get the last N messages"""
        return self.messages[-n:] if n <= len(self.messages) else self.messages
    
    async def clear_memory(self) -> None:
        """Clear conversation memory"""
        self.messages.clear()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get conversation memory statistics"""
        return {
            "session_id": self.session_id,
            "type": "conversation",
            "total_messages": len(self.messages),
            "max_messages": self.max_messages,
            "oldest_message": self.messages[0]["timestamp"] if self.messages else None,
            "newest_message": self.messages[-1]["timestamp"] if self.messages else None
        }
    
    def get_message_count(self) -> int:
        """Get total number of stored messages"""
        return len(self.messages)
    
    async def search_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all messages from a specific role"""
        return [msg for msg in self.messages if msg["role"] == role]