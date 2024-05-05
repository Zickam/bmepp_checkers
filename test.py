import time

import numba
import numpy as np


@numba.njit
def a():
    c = 0
    b = 0
    n = 0
    arr = np.array((0, 1, 2, 3, 4, 5, 6, 7))
    for i in range(10 ** 6):
        # for j in arr:
        #     c += 1
        #     b += 2
        #     n += 3
        for j in range(8):
            arr[j]
            c += 1
            b += 2
            n += 3
s = time.time()
a()
e = time.time()
print(e - s)