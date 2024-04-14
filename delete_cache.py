import pickle
from game.constants import TOP_N_AMOUNT
file_name1 = 'cache.pickle'
file_name2 = f'cache{TOP_N_AMOUNT}.pickle'

a = {}
with open(file_name1, 'wb') as file:
    pickle.dump(a, file)
with open(file_name2, 'wb') as file:
    pickle.dump(a, file)
