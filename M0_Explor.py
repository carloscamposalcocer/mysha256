import numpy as np

INT_BITS = 8
INT_MAX = 0XFF


def r_rot(val, shift) -> int:
    hv = (val >> shift)
    lv = (val << INT_BITS - shift)
    result = (hv | lv) & INT_MAX
    return result
#
# def l_rot(val: int, shift: int) -> int:
#     return (val << shift) & 0xFFFFFFFF | (val >> (INT_BITS - shift))

def l_rot(val, shift) -> int:
    hv = (val << shift) & INT_MAX
    lv = (val >> INT_BITS - shift)
    result = (hv | lv)
    return result


def M0(wi):
    # s0 = r_rot(wi, 7) ^ r_rot(wi, 18) ^ wi >> 3
    s0 = r_rot(wi, 2) ^ r_rot(wi, 3) ^ wi >> 1
    return s0

def mM(wi):
    x0 = l_rot(wi,2) ^ l_rot(wi, 3) ^ wi << 1
    return x0

for i in range(0,256):
    result = r_rot(i, 3)
    print(f"{i:<3} -> {result:<3}")
