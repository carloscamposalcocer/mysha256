import time

import numpy as np

dtype = np.uint16
INT_BITS = np.iinfo(dtype).bits
DTYPE_MAX = np.iinfo(dtype).max


def not_int(int_val):
    return add(dtype(1) << INT_BITS, -dtype(1), -int_val)


def add(*args):
    return np.sum(args, dtype=dtype)


def r_rot(val, shift):
    result = (val >> shift) | ((val << INT_BITS - shift) & DTYPE_MAX)
    return result


def M0(wi):
    if dtype == np.uint32:
        s0 = r_rot(wi, dtype(7)) ^ r_rot(wi, dtype(18)) ^ wi >> dtype(3)
    elif dtype == np.uint16:
        s0 = r_rot(wi, dtype(3)) ^ r_rot(wi, dtype(9)) ^ wi >> dtype(1)
    else:
        raise ValueError("Unsupported dtype")
    return s0


start_time = time.time()
inputs = np.array([i for i in range(0xFFFF+1)], dtype=dtype)
outputs = M0(inputs)
print(f"Time Compute: {time.time() - start_time}")

start_time = time.time()
np.save("M0.npy", outputs)
print(f"Time Write: {time.time() - start_time}")
