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

    def test_variadic_positional_arguments_behave_differently(self):
        @curry
        def add(*args):
            return sum(args)

        add_multiple = add(1)
        assert add_multiple.curried is True
        assert add_multiple() == 1

        add_more = add_multiple(2, 3, 4, 5)
        assert add_more.curried is True
        assert add_more() == 15
