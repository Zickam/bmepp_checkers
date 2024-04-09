import copy
import multiprocessing as mp
import random
import time
from game.classes import moves_to_notation

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
                    finding_max = not game.isPlayerWhite()
                    _, moves = self.MinMax.minmax(game, 8, finding_max)
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
                    self.MinMax.save_cash()
                    print(f'time: {time.time()-start}')

                    print('alphabeta count:', self.MinMax.alphabeta_puring_count)
                    self.MinMax.alphabeta_puring_count = {}

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
