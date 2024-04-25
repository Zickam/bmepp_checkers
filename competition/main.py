from game.bot import Bot
from competition.classes import Weights
from constants import *
import multiprocessing as mp

# TO DO:
# Веса из файла ✅
# Боты из весов ❌
# Сохранение результатов в файл ✅
# Проведение матчей ❌,                        потом мутации❌

# разделение игры на этапы ❓
# запоминать блоки весов, которые остаются n раундов ❓

class Tournament:
    def __init__(self):
        self.results: list[list[int]]
        self.generation_number: int
        self.weights: list[list[int]]
        self.bots: list[Bot]
        self.duel_pairs_queue: mp.Queue
        self.duel_results_queue: mp.Queue
        # self.mainloop()

    def save_result(self):
        pass