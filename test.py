import random

c = 0
n = 1
for i in range(n):
    c += random.randint(50, 200)

print(c / n)