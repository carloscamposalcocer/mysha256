import time

import numpy as np

dtype = np.uint16
DTYPE_BITS = np.iinfo(dtype).bits
DTYPE_MAX = np.iinfo(dtype).max


def not_int(int_val):
    return add(dtype(1) << DTYPE_BITS, -dtype(1), -int_val)


def add(*args):
    return np.sum(args, dtype=dtype)


def r_rot(val, shift):
    result = (val >> shift) | ((val << DTYPE_BITS - shift) & DTYPE_MAX)
    return result


def M0(wi):
    if dtype == np.uint32:
        s0 = r_rot(wi, dtype(7)) ^ r_rot(wi, dtype(18)) ^ wi >> dtype(3)
    elif dtype == np.uint16:
        s0 = r_rot(wi, dtype(3)) ^ r_rot(wi, dtype(9)) ^ wi >> dtype(1)
    else:
        raise ValueError("Unsupported dtype")
    return s0


def B(func, x):
    return func + x


def A(x):
    return M0(x)


def function(x):
    return B(A(x), x)

# Equation is M0(x) + x == 37198

inputs = np.array([i for i in range(DTYPE_MAX + 1)], dtype=dtype)
A_mapping = A(inputs)
B_mapping = B(0, inputs)


f_mapping = function(inputs)
output = 37198

indices = np.where(f_mapping == output)[0]

b_output = np.where(B_mapping == output)[0]

for index in indices:
    print(f"Input:{index} Actual Output: {function(index)} Expected Output: {output}")
