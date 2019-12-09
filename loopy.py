class Foo(object):

    def __init__(self, length):
        self.length = length

    def __getitem__(self, item):
        if isinstance(item, slice):
            for i in range(*item.indices(self.length)):
                yield i
        ...

f = Foo(40)
print(list(f[1:-5:7]))
print(list(range(1, 40 - 5, 7)))
