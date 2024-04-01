import multiprocessing as mp
import random
import time

from game.classes import Figure, Move
from game.minmax import minmax
from game.main import Game


class Process:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.mainloop()

    def mainloop(self):
        while True:
            time.sleep(0.000001)
            if not self.process_request_queue.empty():
                game = self.process_request_queue.get()
                moves = list(game._available_moves.values())
                random_arr = random.choice(moves)
                random_move = random.choice(random_arr)
                self.process_response_queue.put(random_move)


class Bot:
    def __init__(self):
        self.process_request_queue = mp.Queue()
        self.process_response_queue = mp.Queue()
        self.process = mp.Process(target=Process, args=(self.process_request_queue, self.process_response_queue), daemon=True)
        self.process.start()

    def start_best_move_calculation(self, game):
        self.process_request_queue.put(game)

    def is_best_move_ready(self) -> bool:
        return not self.process_response_queue.empty()

    def get_calculated_move(self):
        return self.process_response_queue.get()