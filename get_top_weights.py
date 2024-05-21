a = 50  # Из скольких последнийх поколений берем топ веса
b = 2  # Сколько топ весов берем

last_gen = 0
path = 'competition/data/'
for last_gen in range(100000000):
    try:
        open(path+f'sorted_results{last_gen+1}.txt')
    except FileNotFoundError:
        break

weights = []
for i in range(a):
    n = last_gen - i
    with open(path+f'sorted_results{n}.txt') as file:
        lines = file.readlines()[:b]
        for line in lines:
            results, weight = line.split(' | ')
            weights.append(weight)

with open('many_top_weights.txt', 'w') as file:
    for weight in weights:
        file.write(weight)
