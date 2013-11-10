currypy
=======

.. code::

    from currypy import curry

    @curry
    def add(a, b):
        return a + b

    add1 = add(1)
    assert add1.curried is True
    assert add1(2) == 3

    @curry
    def variadic(*args, **kwargs):
        return (args, kwargs)

    three_var = variadic('one', 'two', 'three')
    assert three_var.curried is True
    assert three_var() == (('one', 'two', 'three'), {})

    six_var = three_var(one='one', two='two', three='three')
    assert six_var.curried is True
    assert six_var() == (
        ('one', 'two', 'three'),
        {'one': 'one', 'two': 'two', 'three': 'three'}
        )
