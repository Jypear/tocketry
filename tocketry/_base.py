from typing import TYPE_CHECKING, Any, ClassVar
from pydantic.dataclasses import dataclass, Field
from pydantic import BaseModel

if TYPE_CHECKING:
    from tocketry import Session


class RedBase:
    """Baseclass for all Tocketry classes"""

    # Commented this out for now as it was causing issues with the new pydantic implementation
    session: "Session"
