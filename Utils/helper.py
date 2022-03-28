import time
from typing import List


def timed_func(func):
    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        print(f"{func.__name__} ran for {t2 - t1} secs")
        return res

    return wrapper


def translate(message):
    charcodes = [ord(c) for c in message]
    bytes = [bin(char)[2:].zfill(8) for char in charcodes]
    bits = []
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))
    return bits


def chunker(bits: bytes, chunk_length=8):
    chunked = []
    for b in range(0, len(bits), chunk_length // 8):
        chunked.append(bits[b:b + chunk_length // 8])
    chunked_int = [int.from_bytes(value, 'big') for value in chunked]
    return chunked_int


def oldfillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits


def fillZeros(bits: bytes, length=8, endian='LE'):
    l = len(bits) * 8
    missing_zeros = bytes((length - l) // 8)
    if endian == 'LE':
        bits = bits + missing_zeros
    else:
        bits = missing_zeros + bits
    return bits


def decomposer(byte_str: bytes):
    for byte_item in byte_str:
        for bit in bin(byte_item)[2:].zfill(8):
            yield int(bit)


def as_int_bool(encoded_str):
    mm = [bit for bit in decomposer(encoded_str)]
    return mm


# 0sec function
def preprocessMessage(message):
    bits = message.encode()
    length = len(bits) * 8
    message_len = length.to_bytes(8, 'big')

    if length < 448:
        bits = bits + b'\x80'
        bits = fillZeros(bits, 448, 'LE')
        bits = bits + message_len
        return [bits]
    elif length == 448:
        raise NotImplementedError()
        # bits.append(1)
        # bits = fillZeros(bits, 1024, 'LE')
        # bits[-64:] = message_len
        # return chunker(bits, 512)
    else:
        raise NotImplementedError()
        # bits.append(1)
        # while len(bits) % 512 != 0:
        #     bits.append(0)
        # bits[-64:] = message_len
    # return chunker(bits, 512)


def initializer(values: List[int]):
    binaries = [v.to_bytes(4, 'big') for v in values]
    return binaries


def b2Tob16(value):
    value = ''.join([str(x) for x in value])
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append('0b' + value[d:d + 4])
    hexes = ''
    for b in binaries:
        hexes += hex(int(b, 2))[2:]
    return hexes
