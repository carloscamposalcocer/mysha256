from Utils.constants import ks, hs
from hash import prepare_temp2
import numpy as np

def run_tru_temp2():
    a = np.uint32(1)
    b = np.uint32(0)
    c = np.uint32(0)

    results = []
    for i in range(100):
        a = np.uint32(i)
        result = prepare_temp2(a, b, c)
        results.append(result)
        print(result)

    results = np.array(results)
    div = results/results[1]
    print(div)

w63 = np.uint32(82473)

rest = ks[63] + w63 + np.uint32(965559525)

print(rest)