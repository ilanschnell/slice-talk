# <br /><center style="font-size: 135px">The Slice Object</center>

## <center>Ilan Schnell</center><center>Schnell Analytics</center>

---

# The Problem

When defining a function like:

    def pow(x, y, z=None):
        r = x ** y
        if z is not None:
            r %= z
        return r

`x` and `y` are required, `z` is optional.
Any parameter is either positional or keyword.

You can call it like:

    pow(2, 6)
    # the following should raise Exception (but don't)
    pow(x=2, y=6)
    pow(2, y=6, z=10)
    pow(z=10, y=6, x=2)

There is no restriction on the calling convention, no way to specify which
parameters are positional or keyword.

---

# Positional-only parameters

PEP 457:
Positional-only parameters are parameters without an externally-usable name;
when a function is called these positional arguments are mapped to these
parameters based solely on their position.

Python has always supported positional-only parameters.  In C:

    static PyObject
    *f(PyObject *self, PyObject *args)
    {
        int p1, p2, p3 = 3;

        if (!PyArg_ParseTuple(args, "ii|i:f", &p1, &p2, &p3))
            return NULL;

        printf("%d %d %d\n", p1, p2, p3);

        Py_RETURN_NONE;
    }

---

# In Python

When you don't want to write a C-extension, you can:

    def f(*args):
        la = len(args)
        if la < 2:
            raise TypeError("takes at least 2 arguments (%d given)" % la)
        elif la == 2:
            p1, p2 = args
            p3 = 3
        elif la == 3:
            p1, p2, p3 = args
        else:
            raise TypeError("takes at most 3 arguments (%d given)" % la)
        print(p1, p2, p3)

This is much more complicated than the C equivalent :-(

---

# Ugh :-(

<img src="./clumsy-lego.jpg" width="340" height="512" />

Wouldn't it be nice to make this easier in Python?

---

# Python 3.0: (PEP 3102)

Parameters after the `*` marker are keyword-only:

    def f(a, b=2, *, c, d=4):
        ...

`a` and `c` are required, `b` and `d` are optional.
`a` and `b` are positional or keyword, `c` and `d` are keyword-only.

Valid calls:

    f(a=1, c=3)
    f(1, 7, c=8)

Invalid calls:

    f(1, 7, 8) -> f() takes from 1 to 2 positional arguments
                  but 3 were given

While there is now a way to specify which parameters are keyword-only,
there is no way to specify which parameters are positional-only

---

# Python 3.8: (PEP 570)

Parameters before the `/` marker are positional-only:

    def f(a, b=2, /, c=3):
         ...

`a` is required, `b` and `c` are optional.
`a` and `b` are positional-only, `c` is positional or keyword.

Valid calls:

    f(1)
    f(1, 4)
    f(1, 4, 5)
    f(1, 4, c=5)
    f(1, c=5)

Invalid calls:

    f(1, b=3) -> f() got some positional-only arguments passed
                 as keyword arguments: 'b'

---

<img src="./happy-lego.png" width="600" height="450" />

---

# Syntax and Semantics

Python 3.8 syntax:

    def name(positional_only_parameters, /,
             positional_or_keyword_parameters, *,
             keyword_only_parameters):

Examples (from Python 3.7 docstrings):

    divmod(x, y, /)

    pow(x, y, z=None, /)

    eval(source, globals=None, locals=None, /)

    sorted(iterable, /, *, key=None, reverse=False)

    sum(iterable, /, start=0)

---

# Adoption

As the new syntax breaks Python 3.7 and earlier, I don't expect adoption
anytime soon.

The standard library will adopt positional-only parameters first.

Third party library can only adopt positional-only parameters when once
Python 3.8 and higher is targeted.

---

# Summary

Use case will determine which parameters to use in function definition:

    def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):


As guidance:

  * Use positional-only if names do not matter or have no meaning,
    and there are only a few arguments which will always be passed in
    the same order.

  * Use keyword-only when names have meaning and the function definition
    is more understandable by being explicit with names.
