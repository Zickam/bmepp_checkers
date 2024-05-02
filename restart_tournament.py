import pickle
from competition.constants import PATH_TO_DATA, WEIGHTS_COUNT
from competition.classes import Results, Weights
from competition.mutations import getRandomWeightsList
import os
try:
    file = open(f'{PATH_TO_DATA}conducted_duels1.pickle', 'wb')
except FileNotFoundError:
    os.mkdir(PATH_TO_DATA)
    file = open(f'{PATH_TO_DATA}conducted_duels1.pickle', 'wb')
pickle.dump(set(), file)
file.close()
restart_results = [[0, 0, 0] for _ in range(WEIGHTS_COUNT)]
Results.save_results_in_file(f'{PATH_TO_DATA}results1.txt', restart_results)
new_weights = []
for _ in range(WEIGHTS_COUNT):
    new_weights.append(getRandomWeightsList(20))
Weights.save_weights_in_file(f'{PATH_TO_DATA}weights1.txt', new_weights)
