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
        return str_weights[:-1]

    @staticmethod
    def load_weights_from_file(filename) -> list[list[float]]:
        strings = open(filename, 'r').readlines()
        weights = []
        for s in strings:
            weights.append(Weights.str_to_weights(s))
        return weights

    @staticmethod
    def save_weights_in_file(filename: str, weights: list[list[float]]):
        with open(filename, 'w') as file:
            for weight in weights:
                str_weights = Weights.weights_to_str(weight) + '\n'
                file.write(str_weights)


class Results:
    @staticmethod
    def str_to_results(str_results: str) -> list[int]:
        str_results.replace('\n', '')
        try:
            str_list = str_results.split(' ')
            int_results = []
            for results in str_list:
                int_results.append(int(results))
            return int_results
        except ValueError as ex:
            print(ex, 'у вас в резах не то:', str_results)

    @staticmethod
    def results_to_str(int_results: list[int]) -> str:
        str_results = ''
        for results in int_results:
            str_results += str(results) + ' '
        return str_results[:-1]

    @staticmethod
    def load_results_from_file(filename) -> list[list[int]]:
        strings = open(filename, 'r').readlines()
        results = []
        for s in strings:
            results.append(Results.str_to_results(s))
        return results

    @staticmethod
    def save_results_in_file(filename: str, results: list[list[int]]):
        with open(filename, 'w') as file:
            for result in results:
                str_results = Results.results_to_str(result) + '\n'
                file.write(str_results)
