# <br /><center style="font-size: 120px">The Slice Object</center>

## <center>Ilan Schnell</center><center>Schnell Analytics</center>

---

# Basics

Python has a very easy and powerful slicing syntax:

    !python
    >>> s = "Python rocks!"

Fix six elements:

    !python
    >>> s[:6]
    'Python'

Last six elements:

    !python
    >>> s[-6:]
    'rocks!'

Every other element:

    !python
    >>> s[::2]
    'Pto ok!'

Reverse elements:

    !python
    >>> s[::-1]
    '!skcor nohtyP'

In general, we can index a sequence by index:

    !python
    >>> s[index]

Or slice:

    !python
    >>> s[start:stop:step]

(where each slice parameter is optional)

---

# Introduction

Let's define a class to see what gets passed when we get an item:

    !python
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

    !python
    >>> a = list(range(10))
    >>> s = slice(1, 10, 3)
    >>> a[s]
    [1, 4, 7]

Let's look at the attributes:

    !python
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

Slice objects are immutable, but not hashable!

---

# Why is the slice not hashable?

Assuming it was hashable, we could write:

    !python
    >>> d = dict()
    >>> s = slice(1, 5)
    >>> d[s] = 42           # will actually raise a TypeError
    >>> d[1:5]
    42

This would be confusing, as a dict is not a sequence!

On the other hand, assuming the slice object would be mutable:

    !python
    >>> a = "Python"
    >>> s = slice(2, 4)
    >>> a[s]
    'th'
    >>> s.start = 0         # will actually raise an AttributeError
    >>> a[s]
    'Pyth'

Less, confusing.  I assume that (as there is no practical usecase
for either) Guido did not want to leave any room for confusion.

Or as Tim Peters would say:

    !text
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.

---

# Example

    !python
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

# Only one method: `.indices()`

    !text
    S.indices(len) -> (start, stop, stride)

    Assuming a sequence of length len, calculate the start and stop
    indices, and the stride length of the extended slice described by
    S. Out of bounds indices are clipped in a manner consistent with the
    handling of normal slices.

Allows you to easily create your own loops over indices:

    !python
    class Loopy(object):

        def __init__(self, length):
            self.length = length

        def __getitem__(self, item):
            if isinstance(item, slice):
                for i in range(*item.indices(self.length)):
                    yield i
            ...

---

# History - Python 1.0.1 (1994)

Python had slicing:

    !text
    Python 1.0.1
    Copyright 1991-1994 Stichting Mathematisch Centrum, Amsterdam
    >>> s = "Python"
    >>> s[1:-2]
    'yth'
    >>> s[::-1]
      File "<stdin>", line 1
        s[::-1]
           ^
    SyntaxError: invalid syntax

But:

  * No slice object

  * Only `start` and `stop` argument

  * There was no third `step` (or `stride`) argument

---

# History - Python 1.4 (1996)

Release notes:

    !text
    Changes for use with Numerical Python: builtin function slice() and
    Ellipses object, and corresponding syntax:

          x[lo:hi:stride]      ==     x[slice(lo, hi, stride)]
          x[a, ..., z]         ==     x[(a, Ellipses, z)]

Great:

  * `slice` and `Ellipsis` objects added by Jim Hugunin and Chris Chase

  * the third slicing `step` argument was add to the syntax:
    `A[1:10:2], A[:-1:1], A[::-1]`

But:

  * Python's built-in sequence types
    did <span style="color: #e00;">NOT</span> supported this feature!

---

# History - Python 2.3 (2003)

Michael Hudson submitted a patch for Python’s built-in list, tuple,
and string sequence types to support the `step` argument:

    !python
    >>> s = "Python"
    >>> s[::-1]
    'nohtyP'

<img src="./happy-lego.png" />

---

# Relevance

Normally users of Python don't have to deal with slice objects much,
even though they use them all the time.

They become important when writing libraries which support Python's
slicing syntax to access arrays.  For example: array, bitarray, numpy

<img src="./numpy.png" width="240" height="95" />

For example 2 dimensional array:

    !python
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

    >>> from numpy import s_
    >>> s_[1::-2]
    slice(1, None, -2)
    >>> s_[1, ::-1, ..., 1:-1:3]
    (1, slice(None, None, -1), Ellipsis, slice(1, -1, 3))

---

# Thank you!
