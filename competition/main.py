from game.bot import Bot
from competition.classes import Weights, Results
from constants import *
import multiprocessing as mp
import os

# TO DO:
# Веса из файла ✅
# Боты из весов ❌
# Сохранение результатов в файл ✅
# создание файлов для поколений
# Проведение матчей ❌,                        потом мутации❌

# IDEAS:
# разделение игры на этапы ✅
# запоминать блоки весов, которые остаются n раундов ✅


class Generation:
    def __init__(self):
        self.generation_number: int = self.calculate_generation()
        self.results = Results.load_results_from_file(f"{PATH_TO_DATA}results{self.generation_number}.txt")
        self.weights = Weights.load_weights_from_file(f"{PATH_TO_DATA}weights{self.generation_number}.txt")
        self.bots: list[Bot]
        self.duel_pairs_queue: mp.Queue
        self.duel_results_queue: mp.Queue

    def mainloop(self):
        pass

    def save_result(self):
        pass

    def calculate_generation(self):
        file_names = os.listdir(PATH_TO_DATA)
        i = 1
        while f"{PATH_TO_DATA}weights{i + 1}.txt" in file_names:
            i += 1

        return i


def run_tournament():
    while True:
        generation = Generation()
        generation.mainloop()


class DuelProcess:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.mainloop()

    def mainloop(self):
        pass

if __name__ == "__main__":
    pass