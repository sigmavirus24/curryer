import pytest

from currypy import curry


class TestCurry:
    def test_curry_as_decorator(self):
        """Ensure that currypy.curry can be used as a decorator"""
        @curry
        def func():
            pass

        assert func.curried is False

    def test_curry_refuses_None(self):
        with pytest.raises(ValueError):
            curry(None)
