# <br /><center style="font-size: 135px">The Slice Object</center>

## <center>Ilan Schnell</center><center>Schnell Analytics</center>

---

# Basics

Python has a very easy and powerful slicing syntax:

    >>> s = "Python rocks!"

Fix six elements:

    >>> s[:6]
    'Python'

Last six elements:

    >>> s[-6:]
    'rocks!'

Every other element:

    >>> s[::2]
    'Pto ok!'

Reverse elements:

    >>> s[::-1]
    '!skcor nohtyP'

In general, we can index a sequence by index:

    >>> s[index]

Or slice:

    >>> s[start:stop:step]

(where each slice parameter is optional)

---

# Introduction

Let's define a class to see what gets passed when we get an item:

    class Foo(object):
        def __getitem__(self, item):
            return item

    >>> f = Foo()
    >>> f["key"]
    'key'
    >>> f[2]
    2
    >>> f[1:10:3]
    slice(1, 10, 3)
    >>> f[3:-6]
    slice(3, -6, None)
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

# Example

    data = """\
    0010George Jetson    1245 Spaceship St    Houston       TX
    0020Wile E Coyote    312 Acme Blvd        Tucson        AZ
    0030Fred Flintstone  246 Granite Lane     Bedrock       CA
    0040Jonny Quest      31416 Science AVE    Palo Alto     CA
    0050Anne Costello    326 Michigan Rd      Round Rock    TX
    0060Robert Morrison  125 Hyndford St      Grand Island  NE
    """.splitlines()

    fields = [
        ('id',      slice( 0,  4)),
        ('name',    slice( 4, 21)),
        ('address', slice(21, 42)),
        ('city',    slice(42, 56)),
        ('state',   slice(56, 58)),
    ]

    for record in data:
        for field, sl in fields:
            print("%s: %s" % (field, record[sl]))
        print()

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
            start, stop, stride = item.indices(self.length)
            for i in range(start, stop, stride):
                yield i

---

# Relevance

Normally users of Python don't have to deal with slice objects much,
even though they use them all the time.

They become important when writing libraries which support Python's
slicing syntax to access arrays.  For example: array, bitarray, numpy

For example 2 dimensional array:

    >>> from numpy import array
    >>> a = array([[1, 2, 3],
    ...            [4, 5, 6],
    ...            [7, 8, 9]])
    >>> a[2, 1]
    8
    >>> a[0, 1:]
    array([2, 3])
    >>> a[:-1, :-1]
    array([[1, 2],
           [4, 5]])
