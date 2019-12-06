class Foo(object):

    def __init__(self, length):
        self.length = length

    def __getitem__(self, item):
        if not isinstance(item, slice):
            raise TypeError
        i, stop, stride = item.indices(self.length)
        while i < stop:
            yield i
            i += stride

f = Foo(40)
print(list(f[1:-5:7]))
print(list(range(1, 40 - 5, 7)))
