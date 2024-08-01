import pytest
import tocketry


def test_build(request):
    expect_build = request.config.getoption("is_build")
    if not expect_build:
        assert tocketry.version == "0.0.0.UNKNOWN"
    else:
        assert tocketry.version != "0.0.0.UNKNOWN"
