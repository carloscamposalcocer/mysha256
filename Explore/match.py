from Explore.XorMat import RR
import numpy as np

from Explore.tools import int_to_bin_array

for i in range(100000):
    a = int_to_bin_array(i)
    S2 = np.logical_xor(np.logical_xor(RR(2, 32), RR(13, 32)), RR(22, 32)) @ a
    print(S2.dtype)
