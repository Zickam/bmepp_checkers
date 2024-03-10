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
        self.possible_moves = []

        self.__screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Checkers')
        self.__sprites = Sprites(game.board_width)
        self.left_offset = WIN_SIZE[0] - self.__sprites.board.get_width()

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            self.__clock.tick(FPS)

    def render(self):

        if self.__game.is_player_first:
            board_sprite = self.__sprites.board
        else:
            board_sprite = self.__sprites.rotated_board
        self.__screen.blit(board_sprite, (self.left_offset, 0))

        board = self.__game.getBoard()
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if not figure.is_checker:
                    continue
                coordinate = self.__sprites.get_coordinates(i, j, self.__game.is_player_first)
                coordinate = coordinate.move(self.left_offset, 0)
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
            move_x = move.end_point.x
            move_y = move.end_point.y
            coordinate = self.__sprites.get_coordinates(move_x, move_y, self.__game.is_player_first)
            coordinate = coordinate.move(self.left_offset, 0)
            self.__screen.blit(self.__sprites.hint, coordinate)

        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in (1, 3):  # RMB, LMB
                    x, y = event.pos
                    i, j = self.__sprites.get_cell(x-self.left_offset, y, self.__game.is_player_first)
                    if (i, j) == (-1, -1):
                        continue
                    board = self.__game.getBoard()

                    # click on checker
                    if board[i][j].is_checker and board[i][j].is_white == self.__game.getIsWhiteTurn():
                        self.possible_moves = self.__game.getPossibleMoves(Point(i, j))
                        continue

                    # click on hint
                    for move in self.possible_moves:
                        move_end = move.end_point
                        if move_end.x == i and move_end.y == j:
                            self.__game.handleMove(move)
                            self.possible_moves.clear()

    def close(self):
        raise Exception("Implement an exiting for all the child processes and threads!")
        exit()
