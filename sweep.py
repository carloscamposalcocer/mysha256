import hashlib
import random
import sys
import time

import hash


def timed_func(func):
    def wrapper(*arg, **kw):
        '''source: http://www.daniweb.com/code/snippet368.html'''
        t1 = time.time()
        res = func(*arg, **kw)
        t2 = time.time()
        print(f"{func.__name__} ran for {t2 - t1} secs")
        return res

    return wrapper


def hlib_sha256(bin_number):
    result = hashlib.sha256(bin_number)
    hex_str = result.hexdigest()
    return hex_str


def my_sha256(bin_number):
    number = bin_number.decode()
    return hash.my_sha256(number)


def zeros_sha256(sha256_funct, starting_number, zeros_count):
    while True:
        bin_number = str(starting_number).encode()
        hex_str = sha256_funct(bin_number)
        if len(hex_str.rstrip("0")) < len(hex_str) - zeros_count + 1:
            print(f"{bin_number} -> {hex_str}")
            return hex_str
        starting_number += 1


def timed_runs(sha256_func, leading_zeros, repetitions):
    start_time = time.time()
    for _ in range(repetitions):
        zeros_sha256(sha256_func, random.randint(0, sys.maxsize), leading_zeros)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\n[{sha256_func.__name__}] Run Stats:\n"
          f"Repetitions {repetitions:>15} times\n"
          f"Total Rime  {total_time:>15.3f} secs\n"
          f"Average     {total_time / repetitions:>15.3f} secs/run\n")


if __name__ == '__main__':
    leading_zeros = 1
    repetitions = 10
    timed_runs(hlib_sha256, leading_zeros, repetitions)
    timed_runs(my_sha256, leading_zeros, repetitions)
