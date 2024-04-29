def next_gen_weights(weights: list[list[float]]):
    for list_weight in weights:
        for i, weight in enumerate(list_weight):
            list_weight[i] = round(weight + 0.1, 15)
    return weights
