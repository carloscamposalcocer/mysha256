import hashlib

import numpy as np
from tqdm import tqdm

import hash
from Utils import constants
from Utils.helper import preprocessMessage, chunker
from Utils.utils import add


def get_message_chunk(input_message, index, value):
    message_padded = preprocessMessage(input_message)[0]
    chunk = chunker(message_padded, 32)
    chunk[index] = value
    chunk += 48 * [0]
    chunk = np.array(chunk, dtype=np.uint32)
    hash.modify_zero_indexes(chunk)
    return chunk


def main():
    input_message = 'hello worldxxxx'
    expected = '0' * 64
    print(f'Your message: {input_message} -> {expected}')

    sha_chunks = [expected[i:i + 8] for i in range(0, len(expected), 8)]
    print(sha_chunks)

    last_hs = [int(sha_chunk, 16) for sha_chunk in sha_chunks]
    print(last_hs)

    [a, b, c, d, e, f, g, h] = last_hs
    [h0, h1, h2, h3, h4, h5, h6, h7] = constants.hs

    values = []
    for i in tqdm(range(2 ** 32)):
        if (i % 1000) == 0:
            print(f"Computing {i}")
        ws = get_message_chunk(input_message, 3, i)
        values.append(ws[-1])

    a = add(a, -h0)
    b = add(b, -h1)
    c = add(c, -h2)
    d = add(d, -h3)
    e = add(e, -h4)
    f = add(f, -h5)
    g = add(g, -h6)
    h = add(h, -h7)

    a, b, c, d, e, f, g, h = decompress(a, b, c, d, e, f, g, h, ws)

    h0, h1, h2, h3, h4, h5, h6, h7 = constants.hs

    assert a == h0
    assert b == h1
    assert c == h2
    assert d == h3
    assert e == h4
    assert f == h5
    assert g == h6
    assert h == h7


def decompress(a, b, c, d, e, f, g, h, ws):
    print(f"Starting :\t{[a, b, c, d, e, f, g, h]}")
    for i in range(63, -1, -1):
        k = constants.ks[i]
        w = ws[i]

        a, b, c, d, e, f, g, h = decompress_j(a, b, c, d, e, f, g, h, k, w)
        print(f"Index {i} Result:\t{[a, b, c, d, e, f, g, h]}")
    print(f"Result:\t{[a, b, c, d, e, f, g, h]}")
    return [a, b, c, d, e, f, g, h]


def prepare_temp3(a, b, c, d):
    result = add(-a, hash.prepare_S0(b), hash.prepare_m(b, c, d))
    return result


def prepare_temp4(f, g, h, k):
    result = add(hash.prepare_S1(f), hash.prepare_ch(f, g, h), k)
    return result


def decompress_j(a, b, c, d, e, f, g, h, k, w):
    temp3 = prepare_temp3(a, b, c, d)
    temp4 = prepare_temp4(f, g, h, k)

    a = b
    b = c
    c = d
    d = add(e, temp3)
    e = f
    f = g
    g = h
    h = add(-temp3, -temp4, -w)
    return a, b, c, d, e, f, g, h


if __name__ == '__main__':
    main()
