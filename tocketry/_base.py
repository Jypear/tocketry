from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from tocketry import Session


class RedBase:
    """Baseclass for all Tocketry classes"""

    session: ClassVar["Session"] = None
