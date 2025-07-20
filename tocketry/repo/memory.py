"""
In-memory repository implementation extracted from redbird.
"""

from typing import Any, List, Optional
from .base import BaseRepo, BaseResult
from .operations import QueryMatcher


class MemoryResult(BaseResult):
    """Result set for memory repository queries."""
    
    def __init__(self, items: List[Any], repo: "MemoryRepo"):
        self._items = items
        self._repo = repo
    
    def all(self) -> List[Any]:
        """Get all items from the result."""
        return list(self._items)
    
    def first(self) -> Optional[Any]:
        """Get the first item from the result."""
        return self._items[0] if self._items else None
    
    def last(self) -> Optional[Any]:
        """Get the last item from the result."""
        return self._items[-1] if self._items else None
    
    def count(self) -> int:
        """Get the count of items in the result."""
        return len(self._items)
    
    def filter_by(self, **kwargs) -> "MemoryResult":
        """Filter the result by given criteria."""
        filtered_items = []
        for item in self._items:
            if QueryMatcher.matches(item, kwargs, self._repo.get_field_value):
                filtered_items.append(item)
        return MemoryResult(filtered_items, self._repo)
    
    def __iter__(self):
        """Allow iteration over the result."""
        return iter(self._items)
    
    def __len__(self):
        """Get the length of the result."""
        return len(self._items)
    
    def __getitem__(self, index):
        """Get item by index."""
        return self._items[index]


class MemoryRepo(BaseRepo):
    """In-memory repository implementation."""
    
    def __init__(self, model=None, **kwargs):
        super().__init__(model=model, **kwargs)
        self._items = []
    
    def add(self, item: Any) -> None:
        """Add an item to the repository."""
        # Convert dict-like items to model instances if model is specified
        if self.model and not isinstance(item, self.model):
            if hasattr(item, 'keys'):  # dict-like
                # Convert dict to model instance
                if hasattr(self.model, '__init__'):
                    item = self.model(**item)
                else:
                    # Fallback for non-standard models
                    pass
        
        self._items.append(item)
    
    def filter_by(self, **kwargs) -> MemoryResult:
        """Filter items by given criteria."""
        if not kwargs:
            # No filters, return all items
            return MemoryResult(list(self._items), self)
        
        filtered_items = []
        for item in self._items:
            if QueryMatcher.matches(item, kwargs, self.get_field_value):
                filtered_items.append(item)
        
        return MemoryResult(filtered_items, self)
    
    def clear(self) -> None:
        """Clear all items from the repository."""
        self._items.clear()
    
    def __len__(self):
        """Get the number of items in the repository."""
        return len(self._items)
    
    def __iter__(self):
        """Allow iteration over all items."""
        return iter(self._items)
    
    def __contains__(self, item):
        """Check if item is in the repository."""
        return item in self._items