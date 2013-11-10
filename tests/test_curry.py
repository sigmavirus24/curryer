import pytest

from curryer import curry


class TestCurry:
    def test_curry_as_decorator(self):
        """Ensure that currypy.curry can be used as a decorator"""
        @curry
        def func():
            pass

        assert func.curried is False

    def test_curry_refuses_None(self):
        """Ensure that currypy.curry refuses None"""
        with pytest.raises(TypeError):
            curry(None)

    def test_curries_when_given_parameters(self):
        @curry
        def add(a, b):
            return a + b

        assert add(1).curried is True

    def test_evaluates_when_given_enough_parameters(self):
        @curry
        def add(a, b):
            return a + b

        assert add(1)(2) == 3
        assert add(1, 2) == 3
