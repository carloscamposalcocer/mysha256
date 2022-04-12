import time

import numpy as np

TYPE_BITS = 4
TYPE_MAX = 2 ** TYPE_BITS - 1


def not_int(int_val):
    return add(1 << TYPE_BITS, -1, -int_val)


def add(*args):
    return np.mod(np.sum(args), TYPE_MAX + 1)


def r_rot(val, shift):
    result = (val >> shift) | ((val << TYPE_BITS - shift) & TYPE_MAX)
    return result


indices = np.array([[add(i, j) for j in range(TYPE_MAX + 1)] for i in range(TYPE_MAX + 1)])

print(indices)
rx = r_rot(r_rot(indices, 1),2)
print(rx)
norm_rx = np.mod(rx[:, :] - rx[0, :], TYPE_MAX + 1)
print(norm_rx)
norm_rx2 = norm_rx.copy()
for i in range(len(norm_rx)):
    norm_rx2[:, i] = np.mod(norm_rx[:, i] - norm_rx[:, 0], TYPE_MAX + 1)
print(norm_rx2)
