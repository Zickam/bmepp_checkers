class Weights:
    @staticmethod
    def str_to_weights(str_weights: str) -> list[float]:
        str_weights.replace('\n', '')
        try:
            str_list = str_weights.split(' ')
            float_weights = []
            for weight in str_list:
                float_weights.append(float(weight))
            return float_weights
        except ValueError as ex:
            print(ex, 'у вас весах не то:', str_weights)

    @staticmethod
    def weights_to_str(float_weights: list[float]) -> str:
        str_weights = ''
        for weight in float_weights:
            str_weights += str(weight) + ' '
        return str_weights

    @staticmethod
    def create_generation(weights: list[list[float]]):
        pass

