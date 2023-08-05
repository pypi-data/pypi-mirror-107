import pytest

from helloworld import helloworld


def test_helloworld():
    assert helloworld.helloworld() == "Hello, World!"
