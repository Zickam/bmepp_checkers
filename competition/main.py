from game.bot import Bot
from competition.weights import Weights
from constants import *

# TO DO:
# Веса из файла
# Сохранение результатов
# Проведение матчей,                        потом мутации


class Tournament:
    def __init__(self):
        pass

    @staticmethod
    def load_weights_from_file(filename):
        strings = open(filename, 'r').readlines()
        weights = []
        for s in strings:
            weights.append(Weights.str_to_weights(s))
        for w in weights:
            print(w)
