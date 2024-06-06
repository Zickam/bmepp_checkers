a = 25  # Из скольких последнийх поколений берем топ веса
b = 4  # Сколько топ весов берем

last_gen = 0
path = 'competition/data/'
for last_gen in range(100000000):
    try:
        open(path+f'sorted_results{last_gen+1}.txt')
    except FileNotFoundError:
        break

weights = []
for i in range(a):
    n = last_gen - 3*i
    with open(path+f'sorted_results{n}.txt') as file:
        lines = file.readlines()[:b]
        for line in lines:
            results, weight = line.split(' | ')
            weights.append(weight)

weights1 = []
for weight in weights:
    a = [x for x in weight.split(' ')]
    weights1.append(' '.join(a[:20]))
weights = weights1


with open('many_top_weights.txt', 'w') as file:
    for weight in weights:
        file.write(weight+'\n')
