import sys

sys.stdout = open('competition/data/weights1.txt', 'w')
names = ['almaz.txt', 'damir.txt', 'igor.txt', 'matvey.txt', 'vovachmo.txt'] #Z
for name in names:
    strac = open(f'competition/data/{name}', 'r')
    strac = strac.readlines()
    for stroka in strac:
        strocalsl = stroka.split(' ')
        print(strocalsl[-1].replace('\n', ''), end=' ')
    print('\n')