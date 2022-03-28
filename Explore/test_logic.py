import unittest

import numpy as np

from Explore.XorMat import RR, RS

a = np.array([1, 0, 1, 0, 0])


class TestMatrices(unittest.TestCase):
    def test_RR_NormalCase_AssertValues(self):
        b = RR(2, 5) @ a
        self.assertTrue(np.array(([0, 0, 1, 0, 1]) == b).all())

    def test_RS_NormalCase_AssertValues(self):
        b = RS(3,5) @ a
        self.assertTrue(([0, 0, 0, 1, 0] == b).all())