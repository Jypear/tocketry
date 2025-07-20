"""
Query operation classes and functions extracted from redbird.
"""

from typing import Any, List, Union
from operator import eq, ge, le, gt, lt, ne


class Operation:
    """Base class for query operations."""
    
    def __init__(self, value: Any):
        self.value = value
    
    def __call__(self, item_value: Any) -> bool:
        """Evaluate the operation against an item value."""
        raise NotImplementedError
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.value!r})"


class Equal(Operation):
    """Equality operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return eq(item_value, self.value)


class GreaterEqual(Operation):
    """Greater than or equal operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return ge(item_value, self.value)


class LessEqual(Operation):
    """Less than or equal operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return le(item_value, self.value)


class Greater(Operation):
    """Greater than operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return gt(item_value, self.value)


class Less(Operation):
    """Less than operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return lt(item_value, self.value)


class NotEqual(Operation):
    """Not equal operation."""
    
    def __call__(self, item_value: Any) -> bool:
        return ne(item_value, self.value)


class In(Operation):
    """In operation - check if value is in a collection."""
    
    def __call__(self, item_value: Any) -> bool:
        try:
            return item_value in self.value
        except TypeError:
            return False


class Between(Operation):
    """Between operation - check if value is in a range."""
    
    def __init__(self, start: Any, end: Any, none_as_open: bool = False):
        self.start = start
        self.end = end
        self.none_as_open = none_as_open
        self.value = (start, end)
    
    def __call__(self, item_value: Any) -> bool:
        try:
            if self.none_as_open:
                # Handle None as open-ended range
                if self.start is None and self.end is None:
                    return True
                elif self.start is None:
                    return item_value <= self.end
                elif self.end is None:
                    return self.start <= item_value
                else:
                    return self.start <= item_value <= self.end
            else:
                return self.start <= item_value <= self.end
        except TypeError:
            return False
    
    def __repr__(self):
        if self.none_as_open:
            return f"Between({self.start!r}, {self.end!r}, none_as_open=True)"
        return f"Between({self.start!r}, {self.end!r})"


# Convenience functions
def equal(value: Any) -> Equal:
    """Create an equality operation."""
    return Equal(value)


def greater_equal(value: Any) -> GreaterEqual:
    """Create a greater than or equal operation."""
    return GreaterEqual(value)


def less_equal(value: Any) -> LessEqual:
    """Create a less than or equal operation."""
    return LessEqual(value)


def greater(value: Any) -> Greater:
    """Create a greater than operation."""
    return Greater(value)


def less(value: Any) -> Less:
    """Create a less than operation."""
    return Less(value)


def not_equal(value: Any) -> NotEqual:
    """Create a not equal operation."""
    return NotEqual(value)


def in_(values: Union[List, tuple, set]) -> In:
    """Create an in operation."""
    return In(values)


def between(start: Any, end: Any, none_as_open: bool = False) -> Between:
    """Create a between operation."""
    return Between(start, end, none_as_open=none_as_open)


class QueryMatcher:
    """Utility class for matching items against query criteria."""
    
    @staticmethod
    def matches(item: Any, criteria: dict, get_field_func=None) -> bool:
        """Check if an item matches the given criteria."""
        if get_field_func is None:
            get_field_func = QueryMatcher._get_field_value
        
        for field, expected in criteria.items():
            item_value = get_field_func(item, field)
            
            if isinstance(expected, Operation):
                if not expected(item_value):
                    return False
            else:
                if item_value != expected:
                    return False
        
        return True
    
    @staticmethod
    def _get_field_value(item: Any, field: str) -> Any:
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