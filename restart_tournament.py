import pickle
from competition.constants import PATH_TO_DATA
from competition.classes import Results
file = open(f'{PATH_TO_DATA}conducted_duels1.pickle', 'wb')
pickle.dump(set(), file)
file.close()
with open(f'{PATH_TO_DATA}weights1.txt', 'r') as weights:
    len_weights = len(weights.readlines())
    restart_results = [[0, 0, 0] for _ in range(len_weights)]
    Results.save_results_in_file(f'{PATH_TO_DATA}results1.txt', restart_results)
