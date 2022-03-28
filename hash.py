import hashlib
import json
import time

from Utils.helper import preprocessMessage, chunker, timed_func
from Utils import constants
from Utils.utils import r_rot, not_int, add
import numpy as np

M0_values = {}
M1_values = {}


# @timed_func
def my_sha256(message):
    ks = constants.ks
    h0, h1, h2, h3, h4, h5, h6, h7 = constants.hs
    chunks = preprocessMessage(message)
    print("Steps:\n")
    for chunk in chunks:
        print(f"Chunk: \n{chunk}\n")
        ws = chunker(chunk, 32)
        print(f"Int Chunk: \n{ws}\n")
        ws += 48 * [0]
        ws = np.array(ws, dtype=np.uint32)
        modify_zero_indexes(ws)
        print(f"Modified Chunk: \n{ws}\n")
        print(f"Initial hs: \t{[h0,h1,h3,h4,h5,h6,h7]}\t")
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        a, b, c, d, e, f, g, h = compress(a, b, c, d, e, f, g, h, ks, ws)
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)
        print(f"Final hs:   \t{[h0,h1,h3,h4,h5,h6,h7]}")
        print(f"Final hs:   \t{[hex(val) for val in [h0,h1,h3,h4,h5,h6,h7]]}\n")
    digest = b''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += int(val).to_bytes(4, 'big')
    return digest.hex()


# @timed_func
def compress(a, b, c, d, e, f, g, h, ks, ws):
    print("Compression Loop Started:\n")
    for j in range(64):
        a, b, c, d, e, f, g, h = compress_j(a, b, c, d, e, f, g, h, ks[j], ws[j])
        print(f"Compression for index {j:<2}\tResult:\t{[a, b, c, d, e, f, g, h]}")
    print("Compression Loop Ended:\n")
    return a, b, c, d, e, f, g, h


# @timed_func
def compress_j(a, b, c, d, e, f, g, h, k, w):
    temp1 = prepare_temp1(e, f, g, h, k, w)
    temp2 = prepare_temp2(a, b, c)

    h = g
    g = f
    f = e
    e = add(d, temp1)
    d = c
    c = b
    b = a
    a = add(temp1, temp2)
    return a, b, c, d, e, f, g, h


def prepare_temp2(a, b, c):
    S0 = prepare_S0(a)
    m = prepare_m(a, b, c)
    temp2 = add(S0, m)
    return temp2


def prepare_temp1(e, f, g, h, k, w):
    S1 = prepare_S1(e)
    ch = prepare_ch(e, f, g)
    temp1 = add(h, S1, ch, k, w)
    return temp1


def prepare_m(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)


def prepare_S0(a):
    return r_rot(a, np.uint32(2)) ^ r_rot(a, np.uint32(13)) ^ r_rot(a, np.uint32(22))


def prepare_ch(e, f, g):
    return (e & f) ^ (not_int(e) & g)


def prepare_S1(e):
    return r_rot(e, np.uint32(6)) ^ r_rot(e, np.uint32(11)) ^ r_rot(e, np.uint32(25))


# @timed_func
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

        val = add(val0, s0,val1, s1)
        w[index] = val



def M1(wi):
    s1 = r_rot(wi, np.uint32(17)) ^ r_rot(wi, np.uint32(19)) ^ wi >> np.uint32(10)
    M1_values[s1] = wi
    return s1


def M0(wi):
    s0 = r_rot(wi, np.uint32(7)) ^ r_rot(wi, np.uint32(18)) ^ wi >> np.uint32(3)
    M0_values[s0] = wi
    return s0


def timed_hash():
    start_time = time.time()
    repetitions = 5
    for i in range(repetitions):
        my_sha256(input_message)
    print(f"Hashing time = {(time.time() - start_time) / repetitions:15.3}secs")
    # 0.08 secs
    # 0.06 secs encode better
    # 0.004 secs use bytes
    # 0.0016 secs use ints
    # 0.0005 secs removed debug

    # 0.002 secs numpy...


if __name__ == '__main__':
    input_message = 'hello world'
    print('Your message: ', input_message)
    result = my_sha256(input_message)
    expected = hashlib.sha256(input_message.encode()).hexdigest()
    print(f"Expected: {expected}\nResult:   {result}")
    assert result == expected
    print(M0_values)
    print(M1_values)
    with open("Mvalues.json", 'w') as f:
        json.dump({"M0":M0_values, "M1": M1_values})
