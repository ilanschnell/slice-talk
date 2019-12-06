from bitarray import bitarray


class Bitarray2D(object):

    def __init__(self, Ndim1, Ndim2):
        self.n1 = Ndim1
        self.n2 = Ndim2
        self.data = bitarray(Ndim1 * Ndim2)

    def clear(self):
        self.data.setall(0)

    def show(self):
        for i in range(self.n2):
            print(self.data[self.n1 * i:self.n1 * (i + 1)])
        print()

    def __setitem__(self, item, value):
        s1, s2 = item
        if isinstance(s1, int) and isinstance(s2, int):
            self.data[s1 + self.n1 * s2] = value
            return
        if isinstance(s1, int):
            s1 = slice(s1, s1 + 1)
        if isinstance(s2, int):
            s2 = slice(s2, s2 + 1)
        i1, stop1, stride1 = s1.indices(self.n1)
        while i1 < stop1:
            i2, stop2, stride2 = s2.indices(self.n2)
            while i2 < stop2:
                self.data[i1 + self.n1 * i2] = value
                i2 += stride2
            i1 += stride1

img = Bitarray2D(40, 30)
img.clear()
for i in range(img.n1):
    for j in range(img.n2):
        if (i - 20) ** 2 + (j - 15) ** 2 < 10 ** 2:
            img[i, j] = 1
img.show()

img.clear()
img[5::3,3:-4:2] = 1
img.show()
