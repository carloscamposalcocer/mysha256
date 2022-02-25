def isTrue(x): return x == 1


def if_(i, y, z): return y if isTrue(i) else z


def and_(i, j): return if_(i, j, 0)


def AND(i, j): return [and_(ia, ja) for ia, ja in zip(i, j)]


def not_(i): return if_(i, 0, 1)


def NOT(i): return [not_(x) for x in i]


def xor(i, j): return if_(i, not_(j), j)


def XOR(i, j): return [xor(ia, ja) for ia, ja in zip(i, j)]


def xorxor(i, j, l): return xor(i, xor(j, l))


def XORXOR(i, j, l): return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]


INT_BITS = 32


def leftRotateWord(n, d):
    n = int.from_bytes(n, 'big')
    rotated = (n << d) & 0xFFFFFFFF | (n >> (INT_BITS - d))
    return rotated.to_bytes(4, 'big')


def debug_word(byte_value):
    int_value = int.from_bytes(byte_value, 'big')
    return bin(int_value)[2:].zfill(32)


def rightRotateWord(n, d):
    debug_n = debug_word(n)
    n = int.from_bytes(n, 'big')
    rotated = (n >> d) | (n << (INT_BITS - d)) & 0xFFFFFFFF
    result = rotated.to_bytes(4, 'big')
    debug_result = debug_word(result)
    return result


def rightShiftWord(n, d):
    debug_n = debug_word(n)
    n_int = int.from_bytes(n, 'big')
    result_int = n_int >> d
    result = result_int.to_bytes(4, 'big')
    debug_result = debug_word(result)
    return result


def xor_word(a, b):
    a_int = int.from_bytes(a, 'big')
    b_int = int.from_bytes(b, 'big')
    result_int = a_int ^ b_int
    result = result_int.to_bytes(4, 'big')
    # print(f"{bin(a_int)}\n{bin(b_int)}\n{bin(result_int)}")
    return result


def maj(i, j, k): return max([i, j, ], key=[i, j, k].count)


def rotr(x, n): return x[-n:] + x[:-n]


def shr(x, n): return n * [0] + x[:-n]


def add(*args):
    int_values = [int.from_bytes(value, 'big') for value in args]
    result_int = sum(int_values) % 2 ** 32
    return result_int.to_bytes(4, 'big')


if __name__ == '__main__':
    xor_word((1).to_bytes(4, 'big'), (2).to_bytes(4, 'big'))
