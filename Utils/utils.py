INT_BITS = 32


def l_rot(val: int, shift: int) -> int:
    return (val << shift) & 0xFFFFFFFF | (val >> (INT_BITS - shift))


def r_rot(val: int, shift: int) -> int:
    return (val >> shift) | (val << (INT_BITS - shift)) & 0xFFFFFFFF


def r_shift(n_int: int, d: int) -> int:
    return n_int >> d


def xor(a_int: int, b_int: int) -> int:
    return a_int ^ b_int


def add(*args) -> int:
    return sum(args) % 2 ** INT_BITS


def and_int(e_int: int, f_int: int) -> int:
    return e_int & f_int


def not_int(int_val: int) -> int:
    return (1 << INT_BITS) - 1 - int_val
