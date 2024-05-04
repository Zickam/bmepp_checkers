import pickle
import multiprocessing as mp
import os
import time

from game.bot import Bot
from gui.main import Gui
from competition.classes import Weights, Results
from competition.constants import PARALLEL_MATCHES, PATH_TO_DATA, OPPONENTS_COUNT, ALPHA, BETA, GAMMA
from competition.mutations import next_gen_weights


class Duel:
    def __init__(self, id1, id2, weights1, weights2):
        self.id1 = id1
        self.id2 = id2
        self.weights1 = weights1
        self.weights2 = weights2
        self.result = [0, 0, 0]


class Generation:
    def __init__(self, duel_pairs_queue, duel_results_queue):
        self.generation_number: int = self.calculate_generation()
        results_path = f"{PATH_TO_DATA}results{self.generation_number}.txt"
        self.results: list[list[int, int, int]] = Results.load_results_from_file(results_path)
        weights_path = f"{PATH_TO_DATA}weights{self.generation_number}.txt"
        self.weights: list[list[float]] = Weights.load_weights_from_file(weights_path)
        with open(f'{PATH_TO_DATA}conducted_duels{self.generation_number}.pickle', "rb") as file:
            self.conducted_duels: set[tuple] = pickle.load(file)

        self. duel_pairs: list[Duel] = []
        self.create_duel_pairs()
        self.duel_pairs_queue = duel_pairs_queue
        self.duel_results_queue = duel_results_queue

    def create_duel_pairs(self):
        already_in_pairs = []
        for i, weights in enumerate(self.weights):
            for j in range(OPPONENTS_COUNT):
                opponent_ind = (i + j + 1) % len(self.weights)
                if (i, opponent_ind) in already_in_pairs or (opponent_ind, i) in already_in_pairs:
                    continue
                if (i, opponent_ind) in self.conducted_duels or (opponent_ind, i) in self.conducted_duels:
                    continue

                opponent_weights = self.weights[opponent_ind]
                duel = Duel(i, opponent_ind, weights, opponent_weights)
                self.duel_pairs.append(duel)
                already_in_pairs.append((i, opponent_ind))

    def mainloop(self):
        if len(self.duel_pairs) == 0:
            return
        print('duel pairs: ', len(self.duel_pairs), [(d.id1, d.id2) for d in self.duel_pairs])

        for duel in self.duel_pairs:
            self.duel_pairs_queue.put(duel)

        ended_duels = 0
        while ended_duels != len(self.duel_pairs):
            if not self.duel_results_queue.empty():
                ended_duel = self.duel_results_queue.get()

                g_n = self.generation_number
                percent = (ended_duels+1)/(len(self.duel_pairs))*100
                print(f'gen {g_n}: {str(round(percent, 2))+"%": <6}   last duel: {ended_duel.id1} {ended_duel.id2}')

                self.update_results(ended_duel)
                self.save_results()
                ended_duels += 1
            time.sleep(0.1)
        print()
        self.create_new_generation()

    def update_results(self, duel: Duel):
        def update(lst1, lst2):
            for i, el in enumerate(lst2):
                lst1[i] += el

        bot1_results = self.results[duel.id1]
        bot2_results = self.results[duel.id2]
        update(bot1_results, duel.result)
        update(bot2_results, duel.result[::-1])

        self.conducted_duels.add((duel.id1, duel.id2))

    def save_results(self):
        results_path = f"{PATH_TO_DATA}results{self.generation_number}.txt"
        conducted_duels_path = f'{PATH_TO_DATA}conducted_duels{self.generation_number}.pickle'
        with open(conducted_duels_path, 'wb') as file:
            pickle.dump(self.conducted_duels, file)
        Results.save_results_in_file(results_path, self.results)

    @staticmethod
    def calculate_generation():
        file_names = os.listdir(PATH_TO_DATA)
        i = 1
        while f"weights{i + 1}.txt" in file_names:
            i += 1
        return i

    @staticmethod
    def fitness_function(_input):
        result, weight = _input
        value = result[0] * ALPHA + result[1] * BETA + result[2] * GAMMA
        return value

    def get_sorted_weights(self):
        list_to_sort = []
        for result, weight in zip(self.results, self.weights):
            list_to_sort.append([result, weight])
        list_to_sort.sort(key=self.fitness_function, reverse=True)
        return [element[1] for element in list_to_sort]

    def create_new_generation(self):
        weights = next_gen_weights(self.get_sorted_weights(), 2)
        new_result_file = f"{PATH_TO_DATA}results{self.generation_number + 1}.txt"
        new_weights_file = f"{PATH_TO_DATA}weights{self.generation_number + 1}.txt"
        empty_results = [[0, 0, 0] for _ in range(len(weights))]
        Results.save_results_in_file(new_result_file, empty_results)
        Weights.save_weights_in_file(new_weights_file, weights)
        file = open(f'{PATH_TO_DATA}conducted_duels{self.generation_number + 1}.pickle', 'wb')
        pickle.dump(set(), file)
        file.close()


class DuelProcess:
    def __init__(self, process_request_queue: mp.Queue, process_response_queue: mp.Queue):
        self.process_request_queue = process_request_queue
        self.process_response_queue = process_response_queue
        self.mainloop()

    def mainloop(self):

        bot1 = Bot(need_to_print=False)
        bot2 = Bot(need_to_print=False)
        gui = Gui(bot2, bot1, with_display=False)

        while True:
            duel = self.process_request_queue.get(block=True, timeout=900)

            bot1.change_weights(duel.weights1)
            bot2.change_weights(duel.weights2)
            gui.change_bots(bot2, bot1)
            gui.change_caption(f"bot{duel.id1} vs bot{duel.id2}")
            result1 = gui.bots_duel()

            gui.change_bots(bot1, bot2)
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

            self.process_response_queue.put(duel)


def manager_process():
    duel_pairs_queue = mp.Queue()
    duel_results_queue = mp.Queue()
    child_processes = []
    print('numba init')
    for _ in range(PARALLEL_MATCHES):
        new_process = mp.Process(target=DuelProcess, args=(duel_pairs_queue, duel_results_queue))
        new_process.start()
        child_processes.append(new_process)
    while True:
        generation = Generation(duel_pairs_queue, duel_results_queue)
        generation.mainloop()


def run_tournament():
    manager = mp.Process(target=manager_process)
    manager.start()


if __name__ == "__main__":
    run_tournament()
