# <br /><center style="font-size: 135px">The Slice Object</center>

## <center>Ilan Schnell</center><center>Schnell Analytics</center>

---

# Introduction

Let's define a class to see what gets passed when we get an item:

    class Foo(object):
        def __getitem__(self, item):
            print(item)

    >>> f = Foo()
    >>> f["key"]
    'key'
    >>> f[2]
    2
    >>> f[1:10:3]
    slice(1, 10, 3)
    >>> f[:]
    slice(None, None, None)

What is this `slice` object?

---

# Attributes

The representaion tells you how to create a `slice` object:

    >>> a = list(range(10))
    >>> s = slice(1, 10, 3)
    >>> a[s]
    [1, 4, 7]

Let's look at the attributes:

    >>> s.start
    1
    >>> s.stop
    10
    >>> s.step
    3
    >>> s.step = 2
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: readonly attribute
    >>> hash(s)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unhashable type: 'slice'

Object is immutable, but also not hashable!

---

# A single `.indices()` method

    S.indices(len) -> (start, stop, stride)

    Assuming a sequence of length len, calculate the start and stop
    indices, and the stride length of the extended slice described by
    S. Out of bounds indices are clipped in a manner consistent with the
    handling of normal slices.

Allows you to easily create your own loops over indices:

    class Loopy(object):

        def __init__(self, length):
            self.length = length

        def __getitem__(self, item):
            if not isinstance(item, slice):
                raise TypeError
            i, stop, stride = item.indices(self.length)
            while i < stop:
                yield i
                i += stride

---

# Why is this important?

Normally users of Python don't have to deal with slice objects much,
even though they use them all the time.

They become important when writing libraries which support Python's
slicing syntax to access arrays.  For example: array, bitarray, numpy

For example 2 dimensional array:

    >>> from numpy import array
    >>> a = array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
    >>> a[2, 1]
    8
    >>> a[0, 1:]
    array([2, 3])
    >>> a[:-1, :-1]
    array([[1, 2],
           [4, 5]])
