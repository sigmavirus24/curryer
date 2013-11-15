from .curry import Curry


def curry(wrapped_callable):
    return Curry(wrapped_callable)
