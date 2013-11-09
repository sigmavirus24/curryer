currypy
=======

.. code::

    from currypy import curry

    @curry
    def add(a, b):
        return a + b

    assert add(1) is None
    assert add(2) == 3

    @curry
    def variadic(*args, **kwargs):
        return (args, kwargs)

    assert variadic('one', 'two', 'three') is None
    assert variadic(one='one', two='two', three='three') is None
    assert variadic() == (
        ('one', 'two', 'three'),
        {'one': 'one', 'two': 'two', 'three': 'three'}
        )
