import hashlib
import time

from Utils.helper import preprocessMessage, chunker
from Utils import constants
from Utils.utils import xor, r_rot, r_shift, add, and_int, not_int


def my_sha256(message):
    k = constants.ks
    h0, h1, h2, h3, h4, h5, h6, h7 = constants.hs
    chunks = preprocessMessage(message)
    for chunk in chunks:
        w = chunker(chunk, 32)
        for _ in range(48):
            w.append(0)
        for i in range(16, 64):
            s0 = xor(xor(r_rot(w[i - 15], 7), r_rot(w[i - 15], 18)),
                     r_shift(w[i - 15], 3))
            s1 = xor(xor(r_rot(w[i - 2], 17), r_rot(w[i - 2], 19)),
                     r_shift(w[i - 2], 10))
            w[i] = add(w[i - 16], s0, w[i - 7], s1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7
        for j in range(64):
            S1 = xor(xor(r_rot(e, 6), r_rot(e, 11)), r_rot(e, 25))
            ch = xor(and_int(e, f), and_int(not_int(e), g))
            temp1 = add(h, S1, ch, k[j], w[j])
            S0 = xor(xor(r_rot(a, 2), r_rot(a, 13)), r_rot(a, 22))
            m = xor(xor(and_int(a, b), and_int(a, c)), and_int(b, c))
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
        digest += val.to_bytes(4, 'big')
    return digest.hex()


if __name__ == '__main__':
    input_message = 'hello world'
    print('Your message: ', input_message)
    result = my_sha256(input_message)
    expected = hashlib.sha256(input_message.encode()).hexdigest()
    assert result == expected
    start_time = time.time()
    for i in range(100):
        my_sha256(input_message)
    print(f"Hashing time = {(time.time() - start_time) / 100:15.3}secs")
    # 0.08 secs
    # 0.06 secs encode better
    # 0.004 secs use bytes
    # 0.0016 secs use ints
    # 0.0005 secs removed debug
