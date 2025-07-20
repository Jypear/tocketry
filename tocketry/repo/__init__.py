"""
Minimal repository system extracted from redbird for tocketry's logging needs.

This module provides the essential repository pattern functionality needed for
tocketry's task logging without the full complexity of redbird.
"""

from .base import BaseRepo, BaseResult
from .memory import MemoryRepo  
from .handler import RepoHandler
from .operations import between, in_, greater_equal, equal

__all__ = [
    "BaseRepo",
    "BaseResult", 
    "MemoryRepo",
    "RepoHandler",
    "between",
    "in_",
    "greater_equal", 
    "equal",
]