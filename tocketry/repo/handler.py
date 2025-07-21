"""
Logging handler for repositories extracted from redbird.
"""

import logging
from typing import Any, Dict
from .base import BaseRepo


class RepoHandler(logging.Handler):
    """Logging handler that writes log records to a repository."""
    
    def __init__(self, repo: BaseRepo, level=logging.NOTSET):
        super().__init__(level)
        self.repo = repo
    
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the repository."""
        try:
            # Format the record to populate exc_text if there's exception info
            if record.exc_info:
                self.format(record)
            
            # Convert log record to dictionary format for storage
            self.write(vars(record))
        except Exception:
            # Don't let logging errors crash the application
            self.handleError(record)
    
    def write(self, record: Dict[str, Any]) -> None:
        """Write a record dictionary to the repository."""
        self.repo.add(record)