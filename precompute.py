import time

from hash import M0

uint32_max = 0xFFFF

start_time = time.time()

inverse_map = {M0(i): i for i in range(uint32_max + 1)}
print("inverse_map:", len(inverse_map))
print(f"total time: {time.time() - start_time}")
