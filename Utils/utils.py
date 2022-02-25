INT_BITS = 32


def l_rot(val: int, shift: int) -> int:
    return (val << shift) & 0xFFFFFFFF | (val >> (INT_BITS - shift))


def r_rot(val: int, shift: int) -> int:
    return (val >> shift) | (val << (INT_BITS - shift)) & 0xFFFFFFFF


def add(*args) -> int:
    return sum(args) % 2 ** INT_BITS


def not_int(int_val: int) -> int:
    return (1 << INT_BITS) - 1 - int_val
