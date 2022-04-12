import hashlib
import time

import sympy as sym

from Utils import constants
from Utils.helper import preprocessMessage, chunker


def r_rot(val, shift) -> int:
    return (val >> shift) | (val << 32 - shift) & 0xFFFFFFFF


def my_sha256(message):
    ks = constants.ks
    h0, h1, h2, h3, h4, h5, h6, h7 = constants.hs
    chunks = preprocessMessage(message)
    print("Steps:\n")
    w3 = sym.Symbol('w3')
    for chunk in chunks:
        print(f"Chunk: \n{chunk}\n")
        ws = chunker(chunk, 32)
        print(f"Int Chunk: \n{ws}\n")
        w3_real = ws[3]
        ws[3] = w3
        ws += 48 * [0]
        modify_zero_indexes(ws)
        for w in ws:
            if type(w) == int:
                print(w)
            else:
                print(w.subs({w3: w3_real}))

        print(f"Initial hs: \t{[h0, h1, h3, h4, h5, h6, h7]}\t")
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        a, b, c, d, e, f, g, h = compress(a, b, c, d, e, f, g, h, ks, ws)
        h0 = Add(h0, a)
        h1 = Add(h1, b)
        h2 = Add(h2, c)
        h3 = Add(h3, d)
        h4 = Add(h4, e)
        h5 = Add(h5, f)
        h6 = Add(h6, g)
        h7 = Add(h7, h)
        # print(f"Final hs:   \t{[h0, h1, h3, h4, h5, h6, h7]}")
        # print(f"Final hs:   \t{[hex(val) for val in [h0, h1, h3, h4, h5, h6, h7]]}\n")
    digest = b''

    print("Calculating digest:\n")
    h0 = h0.subs({w3: 0})
    print("h0: ", h0)
    h1 = h1.subs({w3: 0})
    print("h1: ", h1)
    h2 = h2.subs({w3: 0})
    print("h2: ", h2)
    h3 = h3.subs({w3: 0})
    print("h3: ", h3)
    h4 = h4.subs({w3: 0})
    print("h4: ", h4)
    h5 = h5.subs({w3: 0})
    print("h5: ", h5)
    h6 = h6.subs({w3: 0})
    print("h6: ", h6)
    h7 = h7.subs({w3: 0})
    print("h7: ", h7)
    print(f"Final hs:   \t{[h0, h1, h3, h4, h5, h6, h7]}")
    print(f"Final hs:   \t{[hex(val) for val in [h0, h1, h3, h4, h5, h6, h7]]}\n")

    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += int(val).to_bytes(4, 'big')
    return digest.hex()


def compress(a, b, c, d, e, f, g, h, ks, ws):
    print("Compression Loop Started:\n")
    for j in range(64):
        start_time = time.time()
        a, b, c, d, e, f, g, h = compress_j(a, b, c, d, e, f, g, h, ks[j], ws[j])
        # print(f"Compression for index {j:<2}\tResult:\t{[a, b, c, d, e, f, g, h]}")
        print(f"Compression for index {j:<2} took {time.time() - start_time:.2f} seconds")
    print("Compression Loop Ended:\n")
    return a, b, c, d, e, f, g, h


# @timed_func
def compress_j(a, b, c, d, e, f, g, h, k, w):
    temp1 = prepare_temp1(e, f, g, h, k, w)
    temp2 = prepare_temp2(a, b, c)

    h = g
    g = f
    f = e
    e = Add(d, temp1)
    d = c
    c = b
    b = a
    a = Add(temp1, temp2)
    return a, b, c, d, e, f, g, h


def prepare_temp2(a, b, c):
    s0 = S0(a)
    maj = Maj(a, b, c)
    temp2 = Add(s0, maj)
    return temp2


def prepare_temp1(e, f, g, h, k, w):
    s1 = S1(e)
    ch = Ch(e, f, g)
    temp1 = Add(h, s1, ch, k, w)
    return temp1


def modify_zero_indexes(w):
    for index in range(16, 64):
        s0_index = index - 15
        s1_index = index - 2
        val0_index = index - 16
        val1_index = index - 7

        s0 = M0(w[s0_index])
        s1 = M1(w[s1_index])
        val0 = w[val0_index]
        val1 = w[val1_index]

        val = Add(val0, s0, val1, s1)
        w[index] = val


def not_int(int_val: int):
    return Add(1 << 32, - 1, -int_val)


class Ch(sym.Function):
    @classmethod
    def eval(cls, e, f, g):
        if e.is_Number and f.is_Number and g.is_Number:
            return (e & f) ^ (not_int(e) & g)


class Maj(sym.Function):
    @classmethod
    def eval(cls, a, b, c):
        if a.is_Number and b.is_Number and c.is_Number:
            return (a & b) ^ (a & c) ^ (b & c)


class S0(sym.Function):
    @classmethod
    def eval(cls, a):
        if a.is_Number:
            return r_rot(a, 2) ^ r_rot(a, 13) ^ r_rot(a, 22)


class S1(sym.Function):
    @classmethod
    def eval(cls, x):
        if x.is_Number:
            return r_rot(x, 6) ^ r_rot(x, 11) ^ r_rot(x, 25)


class M1(sym.Function):
    @classmethod
    def eval(cls, x):
        if x.is_Number:
            return r_rot(x, 17) ^ r_rot(x, 19) ^ x >> 10


class M0(sym.Function):
    @classmethod
    def eval(cls, x):
        if x.is_Number:
            return r_rot(x, 7) ^ r_rot(x, 18) ^ x >> 3


class Add(sym.Function):
    @classmethod
    def eval(cls, *args):
        num_args = [arg for arg in args if arg.is_Number]
        sym_args = [arg for arg in args if not arg.is_Number]
        return Mod(sum(num_args) + sum(sym_args))


class Mod(sym.Function):
    @classmethod
    def eval(cls, value):
        if value.is_Number:
            return value % (0xFFFFFFFF + 1)


if __name__ == '__main__':
    input_message = 'hello world!____'
    print('Your message: ', input_message)
    result = my_sha256(input_message)
    expected = hashlib.sha256(input_message.encode()).hexdigest()
    print(f"Expected: {expected}\nResult:   {result}")
    assert result == expected
