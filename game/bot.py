import copy
import multiprocessing as mp
import random
import time
from game.classes import moves_to_notation, notation_to_move
from game.constants import MINMAX_DEPTH, MINMAX_N_DEPTH, MINMAX_DIFFICULTY_MEDIUM, MINMAX_DIFFICULTY_HARD
from game.board_manager import handleMove, getAllAvailableMoves
from game.minmax import MinMaxClass, heuristic_function


class Process:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.MinMax = MinMaxClass()
        self.mainloop()

    def console_log(self, start=None):
        if start:
            print(f'time: {time.time() - start}')

        print('alphabeta count:', self.MinMax.alphabeta_pruning_count)
        self.MinMax.alphabeta_pruning_count = {}

        print('cash count:', self.MinMax.using_cache_count)
        self.MinMax.using_cache_count = {}

        print('heuristic func count:', self.MinMax.depth_zero)
        self.MinMax.depth_zero = 0

        print('\n')

    @staticmethod
    def print_stack(game, moves):
        try:
            stack = ['\n' + str(x) for x in moves_to_notation(moves)]
            simulated_game = copy.deepcopy(game)
            for i, move in enumerate(moves):
                try:
                    args = simulated_game.toArgs()
                    new_args = handleMove(*args, move)
                    simulated_game.fromArgs(*new_args)
                except Exception as ex:
                    print('🚨!error!🚨', ex)
                score = heuristic_function(simulated_game)
                stack[i] += f' score:{score}'
            print('\nstack:', *stack)
        except TypeError:  # ! ВОЗМОЖНО НЕ ТАЙП ЕРОР!
            print('🚨moves = none🚨')

    def best_move_selection(self, game, variants, finding_max, depth=None):
        record = float('-inf') if finding_max else float('+inf')
        best_moves = []
        for _, moves, board in variants:
            deep_game = copy.deepcopy(game)
            try:
                for move in moves:
                    args = deep_game.toArgs()
                    new_args = handleMove(*args, move)
                    deep_game.fromArgs(*new_args)
            except TypeError as er:
                print(er)
            # !!! FINDING MAX is wrong !!!
            value, moves = self.MinMax.minmax(deep_game, depth, finding_max, moves_stack=moves)

            if (finding_max and (value > record or value == float('-inf'))) or \
                    (not finding_max and (value < record or value == float('+inf'))):
                record = value
                best_moves = moves

        return record, best_moves

    def bot_game(self, game, top_n_depth, depth, finding_max):
        start = time.time()
        print('\n😀NEW CALCULATIONS😀\n')

        variants = self.MinMax.top_n_minmax(game, top_n_depth, finding_max)
        for _, moves, board in variants:
            self.print_stack(game, moves)
        self.console_log()

        record, moves = self.best_move_selection(game, variants, finding_max, depth)

        self.print_stack(game, moves)
        # self.MinMax.save_cash()
        self.console_log(start)
        best_move = moves[0]
        self.process_response_queue.put(best_move)

    def mainloop(self):
        while True:
            time.sleep(0.1)
            if not self.process_request_queue.empty():
                game, difficulty, finding_max = self.process_request_queue.get()
                if difficulty == 0:
                    moves = getAllAvailableMoves(game.getBoard(), game.isWhiteTurn())
                    if len(moves) == 0:
                        continue
                    random_move = random.choice(moves)
                    self.process_response_queue.put(random_move)
                elif difficulty == 1:
                    top_n_depth, depth = MINMAX_DIFFICULTY_MEDIUM[0], MINMAX_DIFFICULTY_MEDIUM[1]
                    self.bot_game(game, top_n_depth, depth, finding_max)
                elif difficulty == 2:
                    top_n_depth, depth = MINMAX_DIFFICULTY_HARD[0], MINMAX_DIFFICULTY_HARD[1]
                    self.bot_game(game, top_n_depth, depth, finding_max)


class Bot:
    def __init__(self):
        self.process_request_queue = mp.Queue()
        self.process_response_queue = mp.Queue()
        self.process = mp.Process(target=Process,
                                  args=(self.process_request_queue, self.process_response_queue),
                                  daemon=True)
        self.process.start()

    def start_best_move_calculation(self, game, difficulty: int, finding_max: bool):
        self.process_request_queue.put((game, difficulty, finding_max))

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
