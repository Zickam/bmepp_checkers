import random
import time
from enum import Enum

import pygame as pg

from game.classes import Point
from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS, DO_RANDOM_MOVE_INTERVAL, DO_RANDOM_MOVES, GC
from game.main import Game, GameState
from gui.buttons import Button, Text, caption_text, play_white_button, play_black_button, difficulty_text, \
    minus_button, plus_button, restart_button, get_difficulty_num, get_win_text
from gui import constants


class SceneState(Enum):
    menu = 0
    checkers = 1
    result = 2


class Gui:
    def __init__(self):
        self.__game = Game()
        self.__clock = pg.time.Clock()
        self.frame_start = time.time()
        self.possible_moves = []
        self.selected_checker = None
        self.state = SceneState.menu
        self.difficulty = 3

        self.__screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Checkers')
        self.__sprites = Sprites(self.__game.board_width)
        self.left_offset = WIN_SIZE[0] - self.__sprites.board.get_width()

        self.do_random_moves = DO_RANDOM_MOVES
        self.do_random_move_interval = DO_RANDOM_MOVE_INTERVAL
        self.next_time_do_random_move = time.time() + self.do_random_move_interval

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            if self.do_random_moves and time.time() >= self.next_time_do_random_move:
                self.doRandomMove()

            self.__clock.tick(FPS)

    def render(self):
        if self.state == SceneState.checkers:
            self.render_gameplay()
        elif self.state == SceneState.menu:
            self.render_menu()
        elif self.state == SceneState.result:
            self.render_result()
        pg.display.update()

    def render_gameplay(self):
        self.render_board()
        self.render_selected_checker()
        self.render_checkers()
        self.render_hints()
        restart_button.render(self.__screen)

    def render_menu(self):
        self.__screen.fill(GC)
        board_sprite = self.__sprites.board.copy()
        board_sprite.set_alpha(50)
        self.__screen.blit(board_sprite, (0, 0))
        caption_text.render(self.__screen)
        play_white_button.render(self.__screen)
        play_black_button.render(self.__screen)
        difficulty_text.render(self.__screen)
        minus_button.render(self.__screen)
        plus_button.render(self.__screen)
        get_difficulty_num(self.difficulty).render(self.__screen)

    def render_result(self):
        self.__screen.fill(GC)
        get_win_text(self.__game.getGameState()).render(self.__screen)
        restart_button.render(self.__screen)

    def render_board(self):
        if self.__game.isPlayerWhite():
            board_sprite = self.__sprites.board
        else:
            board_sprite = self.__sprites.rotated_board
        self.__screen.blit(board_sprite, (self.left_offset, 0))

    def render_selected_checker(self):
        if self.selected_checker is not None:
            x_cord = self.selected_checker.x
            y_cord = self.selected_checker.y
            coordinate = self.__sprites.get_coordinates(x_cord, y_cord, self.__game.isPlayerWhite())
            coordinate = coordinate.move(self.left_offset, 0)
            self.__screen.blit(self.__sprites.indicator, coordinate)

    def render_checkers(self):
        board = self.__game.getBoard()
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if not figure.is_checker:
                    continue
                coordinate = self.__sprites.get_coordinates(i, j, self.__game.isPlayerWhite())
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

    def render_hints(self):
        for move in self.possible_moves:
            move_x = move.end_point.x
            move_y = move.end_point.y
            coordinate = self.__sprites.get_coordinates(move_x, move_y, self.__game.isPlayerWhite())
            coordinate = coordinate.move(self.left_offset, 0)
            self.__screen.blit(self.__sprites.hint, coordinate)

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in (1, 3):  # RMB, LMB
                    x, y = event.pos
                    if self.state == SceneState.checkers:
                        self.gameplay(x, y)
                        if self.__game.getGameState() != GameState.ongoing:
                            self.state = SceneState.result
                    elif self.state == SceneState.menu:
                        self.menu(x, y)
                    elif self.state == SceneState.result:
                        self.result(x, y)

    def menu(self, x: int, y: int):
        if play_white_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(True)

        if play_black_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(False)

        if plus_button.collide_point((x, y)) and self.difficulty < constants.MAX_DIFFICULTY:
            self.difficulty += 1

        if minus_button.collide_point((x, y)) and self.difficulty > constants.MIN_DIFFICULTY:
            self.difficulty -= 1

    def gameplay(self, x: int, y: int):
        if restart_button.collide_point((x, y)):
            self.__game = Game()
            self.state = SceneState.menu

        i, j = self.__sprites.get_cell(x - self.left_offset, y, self.__game.isPlayerWhite())
        board = self.__game.getBoard()

        # click on checker
        if board[i][j].is_checker and board[i][j].is_white == self.__game.isWhiteTurn():
            self.selected_checker = Point(i, j)
            self.possible_moves = self.__game.getPossibleMoves(Point(i, j))

        # click on hint
        for move in self.possible_moves:
            move_end = move.end_point
            if move_end.x == i and move_end.y == j:
                is_white_flag = self.__game.isWhiteTurn()
                self.__game.handleMove(move)
                self.possible_moves.clear()
                if is_white_flag != self.__game.isWhiteTurn():
                    self.selected_checker = None
                else:
                    self.selected_checker = move_end
                    self.possible_moves = self.__game.getPossibleMoves(move_end)

    def result(self, x, y):
        if restart_button.collide_point((x, y)):
            self.__game = Game()
            self.state = SceneState.menu

    def doRandomMove(self):
        all_possible_moves = []
        for i in range(self.__game.board_width):
            for j in range(self.__game.board_width):
                if self.__game.getBoard()[i][j].is_checker:
                    possible_moves = self.__game.getPossibleMoves(Point(i, j))
                    for move in possible_moves:
                        all_possible_moves.append(move)
        self.possible_moves = all_possible_moves

        if self.possible_moves:
            self.__game.handleMove(random.choice(self.possible_moves))
            self.next_time_do_random_move = time.time() + self.do_random_move_interval


    def close(self):
        raise Exception("Implement an exiting for all the child processes and threads!")
        exit()
