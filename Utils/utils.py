import numpy as np

INT_BITS = np.uint32(32)


def not_int(int_val: int) -> int:
    return add(np.uint32(1) << INT_BITS, -np.uint32(1), -int_val)


def add(*args) -> np.uint32:
    return np.sum(args, dtype=np.uint32)


def r_rot(val, shift) -> int:
    val = np.uint32(val)
    shift = np.uint32(shift)
    return (val >> shift) | (val << INT_BITS - shift)
