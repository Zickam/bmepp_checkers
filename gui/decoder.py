import os
import random
import pickle
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from gui.constants import WIN_SIZE

file = pg.image.load('gui/file.png')
file_decoded = pg.Surface(file.get_rect().size)
with open('gui/file_data.pickle', 'rb') as pic:
    dict_file1, dict_str1 = pickle.load(pic)

dict_file = {dict_file1[x]: x for x in list(dict_file1.keys())}
dict_str = {dict_str1[x]: x for x in list(dict_str1.keys())}

for k in range(file.get_height()):
    for i in range(file.get_width()):
        j = dict_str[k]
        pixel = file.get_at((i, k))
        pixel[0] = dict_file[pixel[0]]
        pixel[1] = dict_file[pixel[1]]
        pixel[2] = dict_file[pixel[2]]
        file_decoded.set_at((i, j), pixel)

file_decoded = pg.transform.smoothscale(file_decoded, WIN_SIZE)
