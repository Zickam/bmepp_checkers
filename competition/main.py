from game.bot import Bot
from constants import *

bot = Bot()


class BotWithWeights(Bot):
    def __init__(self, weights: list[float]):
        super().__init__()
        self.weights = weights

    def get_results(self):
        return self.results

class Tournament:
    pass

