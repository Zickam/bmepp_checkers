import os
import random
import pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame as pg


lst = list(range(256))
random.shuffle(lst)
dict_file = {lst[x]: x for x in range(256)}


file = pg.image.load('file.jpg')
file_shifr = pg.Surface(file.get_rect().size)
lenx = file.get_height()
lst_str = list(range(lenx))
random.shuffle(lst_str)
dict_str = {x: lst_str[x] for x in range(lenx)}

for i in range(file.get_width()):
    for k in range(file.get_height()):
        j = dict_str[k]
        pixel = file.get_at((i, k))
        pixel[0] = dict_file[pixel[0]]
        pixel[1] = dict_file[pixel[1]]
        pixel[2] = dict_file[pixel[2]]
        file_shifr.set_at((i, j), pixel)

pg.image.save(file_shifr, 'file.png')
with open('file_data.pickle', 'wb') as pic:
    pickle.dump([dict_file, dict_str], pic)
