import numpy as np

INT_BITS = 32
binary_powers = [2 ** (31 - i) for i in range(0, 32)]


def vector_to_int(vector):
    return sum(vector * binary_powers)


def int_vector(int_value):
    bin_str = bin(int_value)[2:].zfill(INT_BITS)
    bin_array = [bit == '1' for bit in bin_str]
    return np.array(bin_array)


def RR(shift):
    mat = np.zeros((INT_BITS, INT_BITS), dtype=np.bool)
    for i in range(INT_BITS):
        mat[i, (i - shift) % INT_BITS] = 1
    return mat


def RS(shift):
    mat = np.zeros((INT_BITS, INT_BITS), dtype=np.bool)
    for i in range(shift, INT_BITS):
        mat[i, i - shift] = 1
    return mat


class XorMat:
    mat: np.ndarray

    def __str__(self):
        return str(self.mat)

    def __repr__(self):
        return str(self.mat)

    @classmethod
    def dot(cls, int_vector):
        result = cls.mat.dot(int_vector * 1) % 2
        return result.astype(bool)


class M0Mat(XorMat):
    mat = RR(7) ^ RR(18) ^ RS(3)


class M1Mat(XorMat):
    mat = RR(17) ^ RR(19) ^ RS(10)


if __name__ == '__main__':
    a = vector_to_int(M0Mat.dot(int_vector(23)))
    b = vector_to_int(M0Mat.dot(int_vector(7)) + M0Mat.dot(int_vector(16)))
    print(f"{a} = {b}")
