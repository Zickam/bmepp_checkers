def _getCrossbredWeights(weights: list[np.array], crossbred_weights_amount_need: int) -> list[np.array]:
    if len(weights) < 2:
        raise Exception(f"Its not possible to make crossbred out of < 2 weights! ({len(weights)} top weights got!)")
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