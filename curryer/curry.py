import inspect

Infinity = float('inf')

ARITIES = {
    inspect.Parameter.VAR_POSITIONAL: Infinity,
    inspect.Parameter.VAR_KEYWORD: Infinity,
    }


class Curry:
    def __init__(self, func, curried=False, signature=None,
                 bound_arguments=None):
        self.signature = signature or inspect.signature(func)
        self.wrapped_func = func
        #: True if this is a curried function, False otherwise
        self.curried = curried
        self.bound_args = bound_arguments or self.signature.bind_partial()
        self._doc = None
        self._arity = -1

    def __repr__(self):
        func_name = self.wrapped_func.__name__
        if self.curried:
            return 'Curry({}(*{}, **{}))'.format(
                func_name, self.bound_args.args, self.bound_args.kwargs
                )
        return 'Curry({})'.format(func_name)

    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return self.curry(args, kwargs)
        return apply(self.wrapped_func, self.bound_args)

    @property
    def __name__(self):
        return self.wrapped_func.__name__

    @property
    def __doc__(self):
        if self._doc is None:
            self._doc = inspect.getdoc(self.wrapped_func)
        return self._doc

    @property
    def arity(self):
        if self._arity == -1:
            self._arity = calculate_arity(self.signature.parameters)
        return self._arity

    def curry(self, args, kwargs):
        args = self.bound_args.args + args
        bound_kwargs = self.bound_args.kwargs.copy()
        bound_kwargs.update(kwargs)
        bound_args = self.signature.bind_partial(*args, **bound_kwargs)

        if len(bound_args.arguments) == self.arity:
            return apply(self.wrapped_func, bound_args)

        return Curry(self.wrapped_func, True, self.signature, bound_args)


def apply(func, bound_args):
    return func(*bound_args.args, **bound_args.kwargs)


def calculate_arity(params):
    arity = 0
    for param in params.values():
        arity += ARITIES.get(param.kind, 1)
    return arity
