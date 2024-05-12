PARALLEL_MATCHES = 12
PATH_TO_DATA = 'competition/data/'
OPPONENTS_COUNT = 14
WEIGHTS_COUNT = 30  # at least OPPONENTS_COUNT * 2 + 1
# coefficient for fitness function
ALPHA, BETA, GAMMA = 20, 1, 0 # win, draw, lose | 20, 1, -200

TOP_WEIGHTS_AMOUNT = 9
MUTATED_WEIGHTS_AMOUNT = 18
NEW_WEIGHTS_AMOUNT = 3

if TOP_WEIGHTS_AMOUNT + MUTATED_WEIGHTS_AMOUNT + NEW_WEIGHTS_AMOUNT != WEIGHTS_COUNT:
    raise Exception("TOP_WEIGHTS_AMOUNT + MUTATED_WEIGHTS_AMOUNT + NEW_WEIGHTS_AMOUNT != WEIGHTS_COUNT")

ADD_SIMPLE_WEIGHTS = True
SIMPLE_WEIGHTS = [9, 100] + [0] * 8 + [1, 1] + [0] * 8