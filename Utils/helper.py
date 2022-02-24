from setuptools.unicode_utils import decompose


def translate(message):
    charcodes = [ord(c) for c in message]
    bytes = [bin(char)[2:].zfill(8) for char in charcodes]
    bits = []
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))
    return bits


def chunker(bits, chunk_length=8):
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b + chunk_length])
    return chunked


def fillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits


def decomposer(byte_str: bytes):
    for byte_item in byte_str:
        for bit in bin(byte_item)[2:].zfill(8):
            yield int(bit)


def as_int_bool(encoded_str):
    mm = [bit for bit in decomposer(encoded_str)]
    return mm

def preprocessMessage(message):
    bits = message.encode()
    bits = as_int_bool(bits)
    length = len(bits)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    if length < 448:
        bits.append(1)
        bits = fillZeros(bits, 448, 'LE')
        bits = bits + message_len
        return [bits]
    elif length == 448:
        bits.append(1)
        bits = fillZeros(bits, 1024, 'LE')
        bits[-64:] = message_len
        return chunker(bits, 512)
    else:
        bits.append(1)
        while len(bits) % 512 != 0:
            bits.append(0)
        bits[-64:] = message_len
    return chunker(bits, 512)


def initializer(values):
    binaries = [bin(int(v, 16))[2:] for v in values]
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words


def b2Tob16(value):
    value = ''.join([str(x) for x in value])
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append('0b' + value[d:d + 4])
    hexes = ''
    for b in binaries:
        hexes += hex(int(b, 2))[2:]
    return hexes
