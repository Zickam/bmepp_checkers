<<<<<<< HEAD
import pickle

x = open('cache5.pickle', 'rb')
print(pickle.load(x))
=======
import numba
@numba.njit
def add1(x):
    return x + 1

@numba.njit
def bar(fn, x):
    return fn(x)

@numba.njit
def foo(x):
    y = bar(add1, x)
    return y

# Passing add1 within numba compiled code.
print(foo(1))
# Passing add1 into bar from interpreted code
print(bar(add1, 1))
>>>>>>> game_logic
