import time

import pygame as pg

from game.classes import Point
from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS
from game.main import Game

class Gui:
    def __init__(self, game: Game):
        self.__game = game
        self.__clock = pg.time.Clock()
        self.frame_start = time.time()
        self.possible_moves = self.__game.getPossibleMoves(Point(3, 3))

        self.__screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Checkers')
        self.__sprites = Sprites(game.board_width)

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            self.__clock.tick(FPS)

    def render(self):
        board_sprite_x = WIN_SIZE[0] - self.__sprites.board.get_width()
        self.__screen.blit(self.__sprites.board, (board_sprite_x, 0))
        board = self.__game.getBoard()
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if not figure.is_checker:
                    continue
                coordinate = self.__sprites.get_coordinates(i, j)
                coordinate = coordinate.move(board_sprite_x, 0)
                if figure.is_white:
                    if figure.is_queen:
                        self.__screen.blit(self.__sprites.queen_white_checker, coordinate)
                    else:
                        self.__screen.blit(self.__sprites.white_checker, coordinate)
                else:
                    if figure.is_queen:
                        self.__screen.blit(self.__sprites.queen_black_checker, coordinate)
                    else:
                        self.__screen.blit(self.__sprites.black_checker, coordinate)

        for move in self.possible_moves:
            coordinate = self.__sprites.get_coordinates(move.end_point.x, move.end_point.y)
            print(move.end_point.x, move.end_point.y)
            coordinate = coordinate.move(board_sprite_x, 0)
            self.__screen.blit(self.__sprites.hint, coordinate)

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
