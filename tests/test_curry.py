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

    def test_variadic_keyword_arguments_behave_differently(self):
        @curry
        def join(**kwargs):
            return kwargs

        join_with_one = join(one=1)
        assert join_with_one.curried is True
        assert join_with_one() == {'one': 1}

        join_others = join_with_one(two=2, three=3, four=4, five=5)
        assert join_others.curried is True
        assert join_others() == {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5
            }

    def test_non_callable_classes_raise_ValueError(self):
        class Foo:
            def __init__(self):
                pass

        with pytest.raises(TypeError):
            curry(Foo)
