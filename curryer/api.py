from .curry import Curry


def curry(wrapped_callable):
    """
    This is the public API to curryer.

    This function is meant to be used as a decorator like so::

        @curry
        def add(a, b):
            return a + b

    One can then use ``add`` like so::

        add_one = add(1)
        print(add_one(2))  # => 3
        add_two = add(2)
        print(add_two(3))  # => 5

    """
    return Curry(wrapped_callable)
