import warnings

import pytest
from tocketry import Session


def test_shutdown(session):
    assert not session.scheduler._flag_shutdown.is_set()
    with pytest.warns(DeprecationWarning):
        session.shutdown()
    assert session.scheduler._flag_shutdown.is_set()
