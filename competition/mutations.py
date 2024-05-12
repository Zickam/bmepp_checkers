import copy
import random

# from competition.constants import *

import numpy as np

MAX_WEIGHT = 1000

TOP_WEIGHTS_AMOUNT = 9
MUTATED_WEIGHTS_AMOUNT = 18
NEW_WEIGHTS_AMOUNT = 3

if TOP_WEIGHTS_AMOUNT + MUTATED_WEIGHTS_AMOUNT + NEW_WEIGHTS_AMOUNT != 30:
    raise Exception("TOP_WEIGHTS_AMOUNT + MUTATED_WEIGHTS_AMOUNT + NEW_WEIGHTS_AMOUNT != WEIGHTS_COUNT")

ADD_SIMPLE_WEIGHTS = True
SIMPLE_WEIGHTS = [9, 100] + [0] * 8 + [1, 1] + [0] * 8

def next_gen_weights(weights: list[list[float]], gen_num: int):
    weights = mutateListOfWeights(weights, gen_num, TOP_WEIGHTS_AMOUNT, MUTATED_WEIGHTS_AMOUNT, NEW_WEIGHTS_AMOUNT)
    random.shuffle(weights)
    return weights

rng = np.random.default_rng()

def _getRandomWeight() -> float:
    random_order_of_magnitude = np.random.randint(-2, 2)
    random_change_num = np.random.randint(-100, 100)
    return 10**random_order_of_magnitude * random_change_num


def getRandomWeightsList(amount: int) -> list[np.array]:
    weights = []
    for i in range(amount):
        weights.append(_getRandomWeight())
    weights = round_weights([weights])[0]
    return weights


def _getBiasedWeights(weights: np.array, bias_percent: float) -> np.array:
    biased_weights = []
    for i in range(len(weights)):
        biased_weight = weights[i] + weights[i] * bias_percent
        if abs(biased_weight) <= 1:
            biased_weight = -biased_weight

        if biased_weight > 0:
            biased_weight = min(biased_weight, MAX_WEIGHT)
        elif biased_weight < 0:
            biased_weight = max(biased_weight, -MAX_WEIGHT)

        biased_weights.append(biased_weight)
    return biased_weights


def _getHalfPartsIdsFromParents(parent_1: np.array,
                                parent_2: np.array) -> np.array:
    _parts_got = np.full(len(parent_1), 0, dtype=float)
    for i in range(len(parent_1)):
        random_parent_num = random.randint(1, 2)
        if random_parent_num == 1:
            _parts_got[i] = parent_1[i]
        elif random_parent_num == 2:
            _parts_got[i] = parent_2[i]
    return _parts_got


def _getCrossbredWeights(weights: list[np.array],
                         crossbred_weights_amount_need: int) -> list[np.array]:
    if len(weights) < 2:
        raise Exception(
            f"Its not possible to make crossbred out of < 2 weights! ({len(weights)} top weights got!)"
        )
    crossbred_weights_got = []
    crossbred_weight_idx = 0

    is_enough = False
    while len(crossbred_weights_got) < crossbred_weights_amount_need:
        for i in range(0, len(weights) - 1):
            if is_enough:
                break
            for j in range(i, len(weights)):
                if len(crossbred_weights_got) >= crossbred_weights_amount_need:
                    is_enough = True
                    break

                crossbred_weight_idx %= crossbred_weights_amount_need

                parent_1 = weights[i]
                parent_2 = weights[j]

                parts_got = _getHalfPartsIdsFromParents(parent_1, parent_2)

                crossbred_weights_got.append(parts_got)

                crossbred_weight_idx += 1

    return crossbred_weights_got


def normalizeWeightsList(weights_list: list[np.array]) -> list[np.array]:
    """
    In our case normalizing is only make weights fit into
    bounds [-MAX_WEIGHT, MAX_WEIGHT]. Just this.
    """
    for i in range(len(weights_list)):
        for j in range(len(weights_list[i])):
            if weights_list[i][j] > MAX_WEIGHT:
                weights_list[i][j] = MAX_WEIGHT
            elif weights_list[i][j] < -MAX_WEIGHT:
                weights_list[i][j] = -MAX_WEIGHT

    return weights_list


def removeDuplicateWeights(
        weights_list: list[np.array]) -> tuple[int, list[np.array]]:
    # returns amount of duplicates
    dup_amount = 0

    i, j = 0, 1

    while i < len(weights_list) - 1:
        j = i + 1
        while j < len(weights_list):
            is_duplicate = True
            for k in range(len(weights_list[i])):
                if weights_list[i][k] != weights_list[j][k]:
                    is_duplicate = False
                    break
            if is_duplicate:
                weights_list.pop(i)
                dup_amount += 1
            else:
                j += 1
        i += 1

    return dup_amount, weights_list


def mutateListOfWeights(weights_list: list[np.array],
                        generation_num: int,
                        top_weights_amount: int,
                        mutated_weights_amount: int,
                        new_weights_amount: int) -> list[np.array]:

    if generation_num <= 0:
        raise Exception("generation num must not be less than 1")

    if top_weights_amount + mutated_weights_amount + new_weights_amount != len(
            weights_list):
        raise Exception(
            f"top_weights_amount + mutated_weights_amount + new_weights_amount ({top_weights_amount, mutated_weights_amount}) amount should be the same as weights_list len ({len(weights_list)})))"
        )
    if top_weights_amount == 0:
        raise Exception("top_weights_amount must not be 0")

    dup_amount, weights_list = removeDuplicateWeights(weights_list)

    top_weights_list = weights_list[:top_weights_amount]

    mutated_weights_list = []
    weight_to_mutate_idx = 0

    crossbred_parent_1_idx = 0
    crossbred_parent_2_idx = 1

    for i in range(mutated_weights_amount):
        weight_to_mutate_idx = weight_to_mutate_idx % len(top_weights_list)
        weights_to_mutate = top_weights_list[weight_to_mutate_idx]

        bias_percent = rng.integers(1,
                                    generation_num + 2) / (generation_num / 2)

        if random.choice([-1, 1]) == -1:  # changing sign
            bias_percent = -bias_percent

        biased_weights = _getBiasedWeights(
            weights_to_mutate, bias_percent)

        crossbred_weights = _getHalfPartsIdsFromParents(biased_weights, top_weights_list[crossbred_parent_2_idx])
        crossbred_parent_2_idx += 1
        if crossbred_parent_2_idx == top_weights_amount:
            crossbred_parent_2_idx = crossbred_parent_1_idx
            crossbred_parent_1_idx += 1
            if crossbred_parent_2_idx == top_weights_amount:
                break

        random_position_to_replace = random.randint(0, len(weights_list[0]) - 1)
        random_num_to_place = random.randint(50, 200)

        mutated_weights_1 = copy.deepcopy(crossbred_weights)
        mutated_weights_1[random_position_to_replace] = random_num_to_place
        mutated_weights_2 = copy.deepcopy(crossbred_weights)
        mutated_weights_2[random_position_to_replace] = -random_num_to_place

        if len(mutated_weights_list) + 1 > mutated_weights_amount:
            break
        mutated_weights_list.append(mutated_weights_1)
        if len(mutated_weights_list) + 1 > mutated_weights_amount:
            break
        mutated_weights_list.append(mutated_weights_2)

        weight_to_mutate_idx += 1

    if ADD_SIMPLE_WEIGHTS:
        new_weights_amount -= 1
    new_weights_list = [
        getRandomWeightsList(len(weights_list[0]))
        for _ in range(new_weights_amount)
    ]
    if ADD_SIMPLE_WEIGHTS:
        new_weights_list.append(SIMPLE_WEIGHTS)

    weights = top_weights_list + mutated_weights_list + new_weights_list

    weights = round_weights(weights)
    return weights


def round_weights(weights: list[list[float]]):
    weights = copy.deepcopy(weights)
    for weight in weights:
        for i, value in enumerate(weight):
            weight[i] = round(value, 14)
    return weights


if __name__ == "__main__":
    weights = [getRandomWeightsList(20) for i in range(30)]

    weights = normalizeWeightsList(weights)
    start_weights = copy.deepcopy(weights)
    # print("initial we ights", *initial_weights, sep="\n")
    print("initial", *weights, sep="\n")
    # print(removeDuplicateWeights([
    #     [1, 1, 1],
    #     [1, 1, 1],
    #     [1, 1, 2]
    # ]))

    for i in range(1, 2):
        weights = next_gen_weights(weights, i)  #  0.3 -> 0.3 + 0.3 + 0.2 + random
        print('len', len(weights))
    print("mutated", *weights, sep="\n")
    # print([round(weight, 2) for weight in start_weights[25]])
    # print([round(weight, 2) for weight in weights[25]])

    # print("Mutated", *mutated_weights, sep="\n")
    # for i, initial, mutated in zip(enumerate(initial_weights), initial_weights, mutated_weights):
    #     print(i[0], "in", initial, "mut", mutated)
