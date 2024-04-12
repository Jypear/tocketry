from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tocketry import Session


class RedBase:
    """Baseclass for all Tocketry classes"""

    session: "Session" = None
