import logging
import pytest
from tocketry import Tocketry


def test_set_logging():
    app = Tocketry(execution="async")
    with pytest.warns(DeprecationWarning):

        @app.set_logger()
        def set_logging(logger):
            assert isinstance(logger, logging.Logger)
