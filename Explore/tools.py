import numpy as np


def int_to_bin_array(int_value, array_len):
    bin_str = bin(int_value)[2:].zfill(array_len)
    bin_array = [bit == '1' for bit in bin_str]
    return np.array(bin_array)


class Array(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array, dtype=bool).view(cls)
        return obj

    def __array_finalize__(self, obj):
        return None

    def __str__(self):
        s = "".join(['1' if i else '0' for i in self])
        return f"{s}"

    @classmethod
    def from_int(cls, int_value, array_len):
        array = int_to_bin_array(int_value, array_len)
        return cls(array)
