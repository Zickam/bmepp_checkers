import time

import pygame as pg

from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS
from game.main import Game

class Gui:
    def __init__(self, game: Game):
        self.__game = game
        self.__clock = pg.time.Clock()
        self.frame_start = time.time()

        self.__screen = pg.display.set_mode(WIN_SIZE)
        self.__sprites = Sprites(game.board_width)

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            self.__clock.tick(FPS)

    def render(self):
        board_sprite_x = WIN_SIZE[0] - self.__sprites.board.get_width()
        self.__screen.blit(self.__sprites.board, (board_sprite_x, 0))
        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in (1, 3):  # RMB, LMB
                    pass

    def close(self):
        raise Exception("Implement an exiting for all the child processes and threads!")
        exit()
