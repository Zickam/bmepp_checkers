PARALLEL_MATCHES = 12
PATH_TO_DATA = 'competition/data/'
OPPONENTS_COUNT = 14
WEIGHTS_COUNT = 30  # at least OPPONENTS_COUNT * 2 + 1
# coefficient for fitness function
ALPHA, BETA, GAMMA = 20, 1, 0 # win, draw, lose | 20, 1, -200
ADD_SIMPLE_WEIGHTS = True
SIMPLE_WEIGHTS = [9, 100] + [0] * 8 + [1, 1] + [0] * 8
