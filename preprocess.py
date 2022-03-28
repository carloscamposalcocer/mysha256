import numpy as np

from Utils.helper import preprocessMessage, chunker
from Utils.utils import add
from hash import modify_zero_indexes, M0, M1

BINARY_MULTIPLIERS = np.array([2 ** i for i in range(31, -1, -1)])


def rr_matrix(shift):
    mat = np.zeros((32, 32), dtype=int)
    for i in range(32):
        mat[(i + shift) % 32, i] = 1
    return mat


def rs_matrix(shift):
    mat = np.zeros((32, 32), dtype=int)
    for i in range(32 - shift):
        mat[i + shift, i] = 1
    return mat


def int_to_bin_array(int_value):
    bin_str = bin(int_value)[2:].zfill(32)
    bin_array = [bit == '1' for bit in bin_str]
    return np.array(bin_array)


def bin_array_to_int(bin_array):
    assert bin_array.dtype == np.dtype('bool')
    values = BINARY_MULTIPLIERS * bin_array
    int_value = np.sum(values)
    return int_value


m0 = rr_matrix(7) + rr_matrix(18) + rs_matrix(3)
m1 = rr_matrix(17) + rr_matrix(19) + rs_matrix(10)

714112237


def matrix_multiply(mat, int_val):
    val = int_to_bin_array(int_val)
    mult_int = mat.dot(val)
    mult_int = mult_int % 2
    test_val = mult_int.astype(bool)
    result = bin_array_to_int(test_val)
    return result


def ws_from_chunk(w: np.uint32):
    mm = matrix_multiply
    ws = np.zeros(64, dtype=np.uint32)
    ws[0:16] = w

    ws[16] = add(w[0], mm(m0, w[1]), mm(m1, w[14]))
    ws[17] = add(w[1], mm(m0, w[2]), mm(m1, w[15]))

    ws[18] = add(w[2], mm(m0, w[3]), mm(m1, w[0]), mm(m1, mm(m0, w[1])), mm(m1, mm(m1, w[14])))
    ws18dd = add(w[2], mm(m0, w[3]), mm(m1, add(w[0], mm(m0, w[1]), mm(m1, w[14]))))

    val1 = 111
    val2 = 222

    not_dis = mm(m1, add(val1, val2))
    distrib = add(mm(m1, val1), mm(m1, val2))

    return ws


def main():
    input_message = "hello world"
    chunk = preprocessMessage(input_message)[0]
    int_chunk = chunker(chunk, 32)
    print(f"Int Chunk: \n{int_chunk}\n")
    expected_ws = create_schedule(int_chunk)
    print(expected_ws)
    assert expected_ws[-1] == 3267554070

    ws = ws_from_chunk(int_chunk)

    for i in range(64):
        result = ws[i] == expected_ws[i]
        print(f"Index {i:<2}\t ws:{ws[i]:<10} exp:{expected_ws[i]:<10} : {result}")
        if not result:
            raise Exception("Not equal")


def create_schedule(int_chunk):
    ws = int_chunk + 48 * [0]
    ws = np.array(ws, dtype=np.uint32)
    modify_zero_indexes(ws)
    return ws


if __name__ == '__main__':
    main()
