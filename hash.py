import hashlib
import time

from Utils.helper import b2Tob16, preprocessMessage, chunker, initializer, as_int_bool
from Utils.utils import *
from Utils.constants import *


def and_word(e, f):
    e_int = int.from_bytes(e, 'big')
    f_int = int.from_bytes(f, 'big')
    result_int = e_int & f_int
    return result_int.to_bytes(4, 'big')


def not_word(word):
    int_word = int.from_bytes(word, 'big')
    result = (1 << 32) - 1 - int_word
    return result.to_bytes(4, 'big')


def as_binary(word_array):
    int_array = [int.from_bytes(word, 'big') for word in word_array]
    bin_str_list = [bin(byte_value)[2:].zfill(32) for byte_value in int_array]
    return bin_str_list


def my_sha256(message):
    k = Initializer.ks
    h0, h1, h2, h3, h4, h5, h6, h7 = Initializer.hs
    chunks = preprocessMessage(message)
    # chunk_bytes = as_binary(chunks[0])
    for chunk in chunks:
        w = chunker(chunk, 32)
        for _ in range(48):
            w.append(bytes(4))

        w_debug = as_binary(w)
        for i in range(16, 64):
            # s0 = XORXOR(rotr(w[i - 15], 7), rotr(w[i - 15], 18), shr(w[i - 15], 3))
            s0 = xor_word(xor_word(rightRotateWord(w[i - 15], 7), rightRotateWord(w[i - 15], 18)),
                          rightShiftWord(w[i - 15], 3))
            s0_debug = as_binary([s0])
            # s1 = XORXOR(rotr(w[i - 2], 17), rotr(w[i - 2], 19), shr(w[i - 2], 10))
            s1 = xor_word(xor_word(rightRotateWord(w[i - 2], 17), rightRotateWord(w[i - 2], 19)),
                          rightShiftWord(w[i - 2], 10))
            # w[i] = add(add(add(w[i - 16], s0), w[i - 7]), s1)
            wi = add(w[i - 16], s0, w[i - 7], s1)
            wi_debug = as_binary([wi])
            w[i] = wi
        w_debug = as_binary(w)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for j in range(64):
            # S1 = XORXOR(rotr(e, 6), rotr(e, 11), rotr(e, 25))
            S1 = xor_word(xor_word(rightRotateWord(e, 6), rightRotateWord(e, 11)), rightRotateWord(e, 25))
            # ch = XOR(AND(e, f), AND(NOT(e), g))
            ch = xor_word(and_word(e, f), and_word(not_word(e), g))
            # temp1 = add(h, S1, ch, k[j], w[j]) modified
            temp1 = add(h, S1, ch, k[j], w[j])
            # S0 = XORXOR(rotr(a, 2), rotr(a, 13), rotr(a, 22))
            S0 = xor_word(xor_word(rightRotateWord(a, 2), rightRotateWord(a, 13)), rightRotateWord(a, 22))
            m = xor_word(xor_word(and_word(a, b), and_word(a, c)), and_word(b, c))
            temp2 = add(S0, m)
            h = g
            g = f
            f = e
            e = add(d, temp1)
            d = c
            c = b
            b = a
            a = add(temp1, temp2)
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)
    digest = b''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += val
    return digest.hex()


if __name__ == '__main__':
    input_message = 'hola'
    print('Your message: ', input_message)
    result = my_sha256(input_message)
    expected = hashlib.sha256(input_message.encode()).hexdigest()
    assert result == expected
    start_time = time.time()
    for i in range(10):
        print('Hash: ', my_sha256(input_message))
    print(f"Hashing time = {(time.time() - start_time) / 10:15.3}secs")
    # 0.08 secs
    # 0.06 secs encode better
    # 0.004 secs use bytes
