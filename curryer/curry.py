import inspect

Infinity = float('inf')

ARITIES = {
    inspect.Parameter.VAR_POSITIONAL: Infinity,
    inspect.Parameter.VAR_KEYWORD: Infinity,
    }


class Curry:
    def __init__(self, wrapped_callable, curried=False, signature=None,
                 bound_arguments=None):
        self.wrapped_callable = wrapped_callable
        self.wrapped_class = None
        self.instance = None
        self.is_class = inspect.isclass(wrapped_callable)

        if self.is_class:
            self.wrapped_class = wrapped_callable
            self.wrapped_callable = None
            self.signature = None
            self.bound_args = None
        else:
            self.signature = signature or inspect.signature(wrapped_callable)
            self.bound_args = bound_arguments or self.signature.bind_partial()

        #: True if this is a curried function, False otherwise
        self.curried = curried
        self._doc = None
        self._arity = -1

    def __repr__(self):
        func_name = self.__name__
        if self.curried:
            return 'Curry({}(*{}, **{}))'.format(
                func_name, self.args, self.kwargs
                )
        return 'Curry({})'.format(func_name)

    def __call__(self, *args, **kwargs):
        if self.is_class:
            return self.curry_instance(args, kwargs)

        if args or kwargs:
            return self.curry_func(args, kwargs)
        return apply(self.wrapped_callable, self.bound_args)

    @property
    def __name__(self):
        if hasattr(self.wrapped_callable, '__name__'):
            return self.wrapped_callable.__name__
        return repr(self.wrapped_callable)

    @property
    def __doc__(self):
        if self._doc is None:
            self._doc = inspect.getdoc(self.wrapped_callable)
        return self._doc

    @property
    def arity(self):
        if self._arity == -1:
            self._arity = calculate_arity(self.signature.parameters)
        return self._arity

    @property
    def args(self):
        return self.bound_args.args

    @property
    def kwargs(self):
        return self.bound_args.kwargs

    def curry_func(self, args, kwargs):
        args = self.bound_args.args + args
        bound_kwargs = self.bound_args.kwargs.copy()
        bound_kwargs.update(kwargs)
        bound_args = self.signature.bind_partial(*args, **bound_kwargs)

        if len(bound_args.arguments) == self.arity:
            return apply(self.wrapped_callable, bound_args)

        return Curry(self.wrapped_callable, True, self.signature, bound_args)

    def curry_instance(self, args, kwargs):
        instance = self.wrapped_class(*args, **kwargs)
        signature = inspect.signature(instance.__call__)
        curry = Curry(instance.__call__, False, signature)
        curry.instance = instance
        return curry


def apply(func, bound_args):
    return func(*bound_args.args, **bound_args.kwargs)


def calculate_arity(params):
    return sum(ARITIES.get(p.kind, 1) for p in params.values())
