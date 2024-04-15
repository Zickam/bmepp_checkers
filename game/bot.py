import copy
import multiprocessing as mp
import random
import time
from game.classes import moves_to_notation, notation_to_move
from game.constants import MINMAX_DEPTH, MINMAX_N_DEPTH

from game.minmax import MinMaxClass, heuristic_function


class Process:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.MinMax = MinMaxClass()
        self.mainloop()

    def mainloop(self):
        while True:
            time.sleep(0.1)
            if not self.process_request_queue.empty():
                game = self.process_request_queue.get()
                if game.getDifficulty() == 0:
                    moves = game.getAllMoves()
                    if len(moves) == 0:
                        continue
                    random_move = random.choice(moves)
                    self.process_response_queue.put(random_move)
                else:
                    start = time.time()
                    print('new calculations')
                    finding_max = not game.getIsPlayerWhite()
                    #  _, moves = self.MinMax.minmax(game, 6, finding_max)
                    variants = self.MinMax.top_n_minmax(game, MINMAX_N_DEPTH, finding_max)

                    for _, moves, board in variants:
                        if len(moves) == 0:
                            print('moves -= none')
                            continue
                        stack = ['\n'+str(x) for x in moves_to_notation(moves)]
                        simulated_game = copy.deepcopy(game)
                        for i, move in enumerate(moves):
                            simulated_game.handleMove(move)
                            score = heuristic_function(simulated_game)
                            stack[i] += f' score:{score}'
                        print('\nstack:', *stack)

                    print('alphabeta count:', self.MinMax.alphabeta_pruning_count)
                    self.MinMax.alphabeta_pruning_count = {}

                    print('cash count:', self.MinMax.using_cache_count)
                    self.MinMax.using_cache_count = {}

                    print('heuristic func count:', self.MinMax.depth_zero)
                    self.MinMax.depth_zero = 0

                    print('-'*30)

                    record = float('-inf') if finding_max else float('+inf')
                    best_moves = []
                    for _, moves, board in variants:
                        deep_game = copy.deepcopy(game)
                        for move in moves:
                            deep_game.handleMove(move)
                        # !!! FINDING MAX is wrong !!!
                        value, moves = self.MinMax.minmax(deep_game, MINMAX_DEPTH, finding_max, moves_stack=moves)
                        print(value)
                        if (finding_max and (value > record or value == float('-inf'))) or \
                                (not finding_max and (value < record or value == float('+inf'))):
                            record = value
                            best_moves = moves

                    moves = best_moves
                    if len(moves) == 0:
                        print('moves -= none')
                        continue
                    stack = ['\n' + str(x) for x in moves_to_notation(moves)]
                    simulated_game = copy.deepcopy(game)
                    for i, move in enumerate(moves):
                        try:
                            simulated_game.handleMove(move)
                        except Exception as ex:
                            print('!error!', ex)
                        score = heuristic_function(simulated_game)
                        stack[i] += f' score:{score}'
                    print('\nstack:', *stack)

                    self.MinMax.save_cash()
                    print(f'time: {time.time()-start}')

                    print('alphabeta count:', self.MinMax.alphabeta_pruning_count)
                    self.MinMax.alphabeta_pruning_count = {}

                    print('cash count:', self.MinMax.using_cache_count)
                    self.MinMax.using_cache_count = {}

                    print('heuristic func count:', self.MinMax.depth_zero)
                    self.MinMax.depth_zero = 0
                    self.process_response_queue.put(moves[0])


class Bot:
    def __init__(self):
        self.process_request_queue = mp.Queue()
        self.process_response_queue = mp.Queue()
        self.process = mp.Process(target=Process,
                                  args=(self.process_request_queue, self.process_response_queue),
                                  daemon=True)
        self.process.start()

    def start_best_move_calculation(self, game):
        game1 = copy.deepcopy(game)
        self.process_request_queue.put(game1)

    def is_best_move_ready(self) -> bool:
        return not self.process_response_queue.empty()

    def end_bot_thinking(self):
        self.process.kill()
        if not self.process_response_queue.empty():
            self.process_response_queue.get()
        self.process = mp.Process(target=Process,
                                  args=(self.process_request_queue, self.process_response_queue),
                                  daemon=True)
        self.process.start()

    def get_calculated_move(self):
        return self.process_response_queue.get()
