def test():
    c = 0
    v = 0
    for i in range(10 ** 7):
        if i % 2 == 0:
            c += 1
        elif i % 2 == 1:
            v += 1

def test2():
    c = 0
    v = 0

    for i in range(10 ** 7):
        match i % 2:
            case 0:
                c += 1
            case 1:
                v += 1

def test3():
    c = 0
    v = 0

    for i in range(10 ** 7):
        is_even = i % 2
        c += is_even
        v += is_even

import time
s = time.time()
test2()
print(time.time() - s)