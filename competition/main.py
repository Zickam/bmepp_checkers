from game.bot import Bot
from gui.main import Gui
from competition.classes import Weights, Results
from constants import *
import multiprocessing as mp
import os
import time

# TO DO:
# Веса из файла ✅
# Боты из весов ✅
# Сохранение результатов в файл ✅
# создание файлов для поколений❌
# Проведение матчей ✅,                        потом мутации❌

# IDEAS:
# разделение игры на этапы ✅
# запоминать блоки весов, которые остаются n раундов ✅


class Duel:
    def __init__(self, id1, id2, weights1, weights2):
        self.id1 = id1
        self.id2 = id2
        self.weights1 = weights1
        self.weights2 = weights2
        self.result = [0, 0, 0]


class Generation:
    def __init__(self):
        self.generation_number: int = self.calculate_generation()
        results_path = f"{PATH_TO_DATA}results{self.generation_number}.txt"
        self.results: list[list[int, int, int, int]] = Results.load_results_from_file(results_path)
        for row in self.results:
            print(row)
        weights_path = f"{PATH_TO_DATA}weights{self.generation_number}.txt"
        self.weights: list[list[float]] = Weights.load_weights_from_file(weights_path)

        self.duel_pairs: list[Duel] = []
        self.create_duel_pairs()
        self.duel_pairs_queue = mp.Queue()
        self.duel_results_queue = mp.Queue()

    def create_duel_pairs(self):
        already_in_pairs = []
        for i, weights in enumerate(self.weights):
            current_results: list[int, int, int, int] = self.results[i]
            initiated_duels = current_results[3]
            print('init', initiated_duels)
            for j in range(initiated_duels, OPPONENTS_COUNT):
                opponent_ind = (i + j + 1) % len(self.weights)
                if (i, opponent_ind) in already_in_pairs or (opponent_ind, i) in already_in_pairs:
                    continue
                print(i, opponent_ind)
                opponent_weights = self.weights[opponent_ind]
                duel = Duel(i, opponent_ind, weights, opponent_weights)
                self.duel_pairs.append(duel)
                already_in_pairs.append((i, opponent_ind))

    def mainloop(self):
        if len(self.duel_pairs) == 0:
            return
        print('duel pairs: ', len(self.duel_pairs))

        for duel in self.duel_pairs:
            self.duel_pairs_queue.put(duel)

        for _ in range(PARALLEL_MATCHES):
            new_process = mp.Process(target=DuelProcess, args=(self.duel_pairs_queue, self.duel_results_queue))
            new_process.start()

        ended_duels = 0
        while ended_duels != len(self.duel_pairs):
            if not self.duel_results_queue.empty():
                ended_duel = self.duel_results_queue.get()
                print('!'*400)
                print(ended_duel.result)
                self.update_results(ended_duel)
                self.save_results()
                for row in self.results:
                    print(row)
                ended_duels += 1
            time.sleep(0.1)
        self.create_new_generation()

    def update_results(self, duel: Duel):
        def update(lst1, lst2):
            for i, el in enumerate(lst2):
                lst1[i] += el

        bot1_results = self.results[duel.id1]
        bot2_results = self.results[duel.id2]
        update(bot1_results, duel.result)
        update(bot2_results, duel.result[::-1])
        self.results[duel.id1][3] += 1

    def save_results(self):
        results_path = f"{PATH_TO_DATA}results{self.generation_number}.txt"
        Results.save_results_in_file(results_path, self.results)

    def calculate_generation(self):
        file_names = os.listdir(PATH_TO_DATA)
        i = 1
        while f"{PATH_TO_DATA}weights{i + 1}.txt" in file_names:
            i += 1
        return i

    def create_new_generation(self):
        pass


class DuelProcess:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.mainloop()

    def mainloop(self):
        while not self.process_request_queue.empty():
            duel = self.process_request_queue.get()

            bot1 = Bot(duel.weights1)
            bot2 = Bot(duel.weights2)
            gui = Gui(bot2, bot1, caption=f'Duel: {duel.id1} vs {duel.id2}')
            result1 = gui.bots_duel()

            bot1 = Bot(duel.weights1)
            bot2 = Bot(duel.weights2)
            gui = Gui(bot1, bot2, caption=f'Duel: {duel.id2} vs {duel.id1}')
            result2 = gui.bots_duel()

            if result1 == 1:  # bot1 win as white
                duel.result[0] += 1
            if result1 == 2:  # bot1 lose as white
                duel.result[2] += 1
            if result1 == 3:  # draw
                duel.result[1] += 1

            if result2 == 2:  # bot1 win as black
                duel.result[0] += 1
            if result2 == 1:  # bot1 lose as black
                duel.result[2] += 1
            if result2 == 3:  # draw
                duel.result[1] += 1

            print('!'*400)
            print(result1)
            print(result2)

            self.process_response_queue.put(duel)


def run_tournament():
    while True:
        generation = Generation()
        generation.mainloop()
        break


if __name__ == "__main__":
    run_tournament()
