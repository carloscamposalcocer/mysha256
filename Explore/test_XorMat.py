import random
import unittest
from parameterized import parameterized

from Explore.XorMat import RR, int_vector, RS, M0Mat, M1Mat, vector_to_int
from Utils.utils import r_rot
from hash import M0, M1


class TestXorMat(unittest.TestCase):
    @parameterized.expand([
        (8, 1, 4),
        (8, 3, 1),
        (1987, 3, 1610612984)
    ])
    def test_RR_KnownValue_AssertExpected(self, value, shift, expected):
        r_mat = RR(shift)
        result_vector = r_mat.dot(int_vector(value))
        result = vector_to_int(result_vector)
        assert result == expected

    @parameterized.expand([
        (8, 3, 1),
        (1987, 3, 248),
    ])
    def test_RS_KnownValue_AssertExpected(self, value, shift, expected):
        s_mat = RS(shift)
        result_vector = s_mat.dot(int_vector(value))
        result = vector_to_int(result_vector)
        assert result == expected

    def test_RR_RandomValue_AssertExpected(self):
        shift = random.randint(0, 31)
        value = random.randint(0, 2 ** 31 - 1)

        r_mat = RR(shift)
        result_vector = r_mat.dot(int_vector(value))
        result = vector_to_int(result_vector)
        assert result == r_rot(value, shift)

    def test_RS_RandomValue_AssertExpected(self):
        shift = random.randint(0, 31)
        value = random.randint(0, 2 ** 31 - 1)

        s_mat = RS(shift)
        result_vector = s_mat.dot(int_vector(value))
        result = vector_to_int(result_vector)
        assert result == value >> shift

    def test_M0_RandomValue_AssertExpected(self):
        value = random.randint(0, 2 ** 31 - 1)
        result_vector = M0Mat.dot(int_vector(value))
        mod_vector = result_vector
        result = vector_to_int(mod_vector)
        assert result == M0(value)

    def test_M0Squared_RandomValue_AssertExpected(self):
        value = random.randint(0, 2 ** 31 - 1)
        result_vector = M0Mat.dot(M0Mat.dot(int_vector(value)))
        result = vector_to_int(result_vector)
        assert result == M0(M0(value))

    def test_M0M1_RandomValue_AssertExpected(self):
        value = random.randint(0, 2 ** 31 - 1)
        result_vector = M0Mat.dot(M1Mat.dot(int_vector(value)))
        result = vector_to_int(result_vector)
        assert result == M0(M1(value))
