PARALLEL_MATCHES = 12
PATH_TO_DATA = 'competition/data/'
OPPONENTS_COUNT = 7
WEIGHTS_COUNT = 15  # at least OPPONENTS_COUNT * 2 + 1
# coefficient for fitness function
ALPHA, BETA, GAMMA = 10, 1, -100 # win, draw, lose
ADD_SIMPLE_WEIGHTS = True
SIMPLE_WEIGHTS = [9, 100] + [0] * 8 + [1, 1] + [0] * 8
