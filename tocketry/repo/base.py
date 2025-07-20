"""
Base repository interfaces extracted from redbird.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class BaseResult(ABC):
    """Abstract base class for query results."""
    
    @abstractmethod
    def all(self) -> List[Any]:
        """Get all items from the result."""
        pass
    
    @abstractmethod
    def first(self) -> Optional[Any]:
        """Get the first item from the result.""" 
        pass
    
    @abstractmethod
    def last(self) -> Optional[Any]:
        """Get the last item from the result."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Get the count of items in the result."""
        pass
    
    @abstractmethod
    def filter_by(self, **kwargs) -> "BaseResult":
        """Filter the result by given criteria."""
        pass


class BaseRepo(ABC):
    """Abstract base class for repositories."""
    
    def __init__(self, model=None, **kwargs):
        self.model = model
    
    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the repository."""
        pass
    
    @abstractmethod
    def filter_by(self, **kwargs) -> BaseResult:
        """Filter items by given criteria."""
        pass
    
    def insert(self, item: Any) -> None:
        """Insert an item (alias for add)."""
        return self.add(item)
    
    def get_field_value(self, item: Any, field: str) -> Any:
        """Get field value from an item."""
        if hasattr(item, field):
            return getattr(item, field)
        elif hasattr(item, '__getitem__'):
            try:
                return item[field]
            except (KeyError, TypeError):
                pass
        elif hasattr(item, 'get'):
            return item.get(field)
        return None
    
    def set_field_value(self, item: Any, field: str, value: Any) -> None:
        """Set field value on an item."""
        if hasattr(item, '__setattr__'):
            setattr(item, field, value)
        elif hasattr(item, '__setitem__'):
            item[field] = value
        else:
            raise TypeError(f"Cannot set field {field} on {type(item)}")