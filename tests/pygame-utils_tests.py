import pytest


def test_passing():
    assert True


@pytest.mark.xfail
def test_failing():
    assert not True

