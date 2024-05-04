import pickle
from competition.constants import PATH_TO_DATA, WEIGHTS_COUNT, SIMPLE_WEIGHTS, ADD_SIMPLE_WEIGHTS
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
if ADD_SIMPLE_WEIGHTS:
    for _ in range(WEIGHTS_COUNT-1):
        new_weights.append(getRandomWeightsList(20))
    new_weights.append(SIMPLE_WEIGHTS)
else:
    for _ in range(WEIGHTS_COUNT):
        new_weights.append(getRandomWeightsList(20))
Weights.save_weights_in_file(f'{PATH_TO_DATA}weights1.txt', new_weights)
