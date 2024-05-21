import os
PATH_TO_BOTS = 'bots/'


class Bot1:
    def __init__(self, weights: list[float], name: str):
        self.weights = weights
        self.name = name

    def to_file(self):
        with open(PATH_TO_BOTS+f'{self.name}.txt', 'w') as file:
            for num in self.weights:
                file.write(str(num))

    @staticmethod
    def get_all_bots() -> list:
        bots = []
        file_names = os.listdir(PATH_TO_BOTS)
        for file_name in file_names:
            if file_name.endswith('.txt'):
                name = file_name[:-4]
                weights = []
                with open(PATH_TO_BOTS+file_name) as file:
                    for line in file.readlines():
                        weights.append(float(line.replace(' ', '').replace('\n', '')))
                bot = Bot1(weights, name)
                bots.append(bot)
        return bots

    @staticmethod
    def delete(ind):
        bots = Bot1.get_all_bots()
        name = bots[ind].name
        name_to_remove = PATH_TO_BOTS+f'{name}.txt'
        print(name_to_remove)
        os.remove(name_to_remove)


if __name__ == '__main__':
    PATH_TO_BOTS = '../' + PATH_TO_BOTS
    botks = Bot1.get_all_bots()
    for b in botks:
        print(b.weights)
