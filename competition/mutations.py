import copy
import random

import numpy as np


def next_gen_weights(weights: list[list[float]], gen_num: int):
    weights = mutateListOfWeights(weights,
                                  gen_num,
                                  0.3,
                                  0.3,
                                  0.2)
    random.shuffle(weights)
    return weights


DEFAULT_TOP_WEIGHTS_PERCENT = 0.16
DEFAULT_MUTATED_PERCENT = 0.54
DEFAULT_CROSSBRED_PERCENT = 0.1

MAX_WEIGHT = 1000


rng = np.random.default_rng()


def _getRandomWeight() -> float:
    random_order_of_magnitude = np.random.randint(-2, 2)
    random_change_num = np.random.randint(-100, 100)
    return 10 ** random_order_of_magnitude * random_change_num


def getRandomWeightsList(amount: int) -> list[np.array]:
    weights = []
    for i in range(amount):
        weights.append(_getRandomWeight())
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


def _getHalfPartsIdsFromParents(parent_1: np.array, parent_2: np.array) -> np.array:
    _parts_got = np.full(len(parent_1), 0, dtype=float)
    for i in range(len(parent_1)):
        random_parent_num = random.randint(1, 2)
        if random_parent_num == 1:
            _parts_got[i] = parent_1[i]
        elif random_parent_num == 2:
            _parts_got[i] = parent_2[i]
    return _parts_got


def _getCrossbredWeights(weights: list[np.array], crossbred_weights_amount_need: int) -> list[np.array]:
    crossbred_weights_got = []
    crossbred_weight_idx = 0

    is_enough = False
    for i in range(0, len(weights) - 1):
        if is_enough:
            break
        for j in range(i, len(weights)):
            if len(crossbred_weights_got) >= crossbred_weights_amount_need:
                is_enough = True
                break

            crossbred_weight_idx %= crossbred_weights_amount_need

            parent_1 = weights[i]
            parent_2 = weights[i + 1]

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



def mutateListOfWeights(
        weights_list: list[np.array],
        generation_num: int,
        top_weights_percent: float = DEFAULT_TOP_WEIGHTS_PERCENT,
        biased_weights_percent: float = DEFAULT_MUTATED_PERCENT,
        crossbred_weights_percent: float = DEFAULT_CROSSBRED_PERCENT
) -> list[np.array]:

    if generation_num <= 0:
        raise Exception("generation num must not be less than 1")

    if top_weights_percent < 0 or biased_weights_percent < 0 or crossbred_weights_percent < 0:
        raise Exception("None of weights percentage must be less than zero!")

    top_weights_amount = int(len(weights_list) * top_weights_percent)
    biased_weights_amount = int(len(weights_list) * biased_weights_percent)
    crossbred_weights_amount = int(len(weights_list) * crossbred_weights_percent)

    if top_weights_amount + biased_weights_amount + crossbred_weights_amount >= len(weights_list):
        raise Exception(
            f"top_weights_amount + biased_weights_amount + crossbred_weights_amount ({top_weights_amount, biased_weights_amount, crossbred_weights_amount}) should be less than weights_list len ({len(weights_list)}) because we have to add some completely new weights"
        )
    if top_weights_amount == 0 or biased_weights_amount == 0 or crossbred_weights_percent == 0:
        raise Exception("None of (top_weights_amount, biased_weights_amount, crossbred_weights_percent) must be zero!")

    new_weights_amount = len(
        weights_list) - top_weights_amount - biased_weights_amount - crossbred_weights_amount

    top_weights_list = weights_list[:top_weights_amount]

    crossbred_weights_list = _getCrossbredWeights(top_weights_list, crossbred_weights_amount)

    biased_weights_list = []
    weight_to_mutate_idx = 0
    for i in range(biased_weights_amount):
        weight_to_mutate_idx = weight_to_mutate_idx % len(top_weights_list)

        bias_percent = rng.integers(1, generation_num + 2) / (generation_num / 2)
        if random.choice([-1, 1]) == -1: # changing sign
            bias_percent = -bias_percent
        print(generation_num, bias_percent)

        biased_weights = _getBiasedWeights(top_weights_list[weight_to_mutate_idx],
                                           bias_percent)

        biased_weights_list.append(biased_weights)

        weight_to_mutate_idx += 1

    new_weights_list = [
        getRandomWeightsList(len(weights_list[0]))
        for i in range(new_weights_amount)
    ]

    weights = top_weights_list + crossbred_weights_list + biased_weights_list + new_weights_list

    return weights


if __name__ == "__main__":
    weights = [getRandomWeightsList(20) for i in range(50)]
    weights[0][0] = 0.9

    weights = normalizeWeightsList(weights)
    start_weights = copy.deepcopy(weights)
    # print("initial we ights", *initial_weights, sep="\n")
    print("initial", weights[0])

    for i in range(1, 10):
        weights = mutateListOfWeights(weights,
                                          i,
                                          0.3,
                                          0.3,
                                          0.2) #  0.3 -> 0.3 + 0.3 + 0.2 + random
        print('len', len(weights))
    #print("mutated", weights[3])
    print([round(weight, 2) for weight in start_weights[25]])
    print([round(weight, 2) for weight in weights[25]])

    # print("Mutated", *mutated_weights, sep="\n")
    # for i, initial, mutated in zip(enumerate(initial_weights), initial_weights, mutated_weights):
    #     print(i[0], "in", initial, "mut", mutated)
