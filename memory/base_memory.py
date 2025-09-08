"""
Base Memory Interface
Abstract base class for all memory types
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseMemory(ABC):
    """Abstract base class for memory implementations"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
    
    @abstractmethod
    async def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to memory"""
        pass
    
    @abstractmethod
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get relevant context for a query"""
        pass
    
    @abstractmethod
    async def clear_memory(self) -> None:
        """Clear all memory for this session"""
        pass
    
    @abstractmethod
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        pass