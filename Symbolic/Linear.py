import random

from Symbolic.SymbolicHash import M0, Add


def circular_add(ma, mb):
    return ma + mb + (ma + mb) >> 32


for a in range(0, 0xff):
    for b in range(0, 0xff):

        summed = Add(a, b)

        expected = int(M0(summed))

        ma = M0(a)
        mb = M0(b)

        actual = int((ma + mb) % (0xffffffff + 1))

        print(f"a,b:{a:03},{b:03}:{actual:08x} == {expected:08x} diff {actual - expected} {actual == expected}")

