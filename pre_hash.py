import hashlib
import time

from Utils.helper import preprocessMessage, chunker, timed_func
from Utils import constants
from Utils.utils import r_rot, not_int, add
import numpy as np

# @timed_func
from hash import modify_zero_indexes, compress


def pre_sha256(message):
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
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)
        print(f"Final hs:   \t{[h0, h1, h3, h4, h5, h6, h7]}")
        print(f"Final hs:   \t{[hex(val) for val in [h0, h1, h3, h4, h5, h6, h7]]}\n")
    digest = b''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += int(val).to_bytes(4, 'big')
    return digest.hex()


def pre_hashed():
    input_message = 'hello world!____'
    print('Your message: ', input_message)

    w = [1751477356, 1864398703, 1919706145, 1600085855, 2147483648, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128]
    print(f"The chunk is:{w}")

    w += 48 * [0]
    w = np.array(w, dtype=np.uint32)
    w[16] = 927400503
    w[17] = 3306258502
    w[18] = 910136110
    # w[19] = 1600085855 + 0 + M0
    # w[20] =
    # w[21] =
    # w[22] =
    # w[23] =
    # w[24] =
    # w[25] =




if __name__ == '__main__':
    input_message = 'hello world!____'
    print('Your message: ', input_message)
    result = pre_sha256(input_message)
    expected = hashlib.sha256(input_message.encode()).hexdigest()
    print(f"Expected: {expected}\nResult:   {result}")
    assert result == expected
