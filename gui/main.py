import random
import time

import pygame as pg

from game.classes import Point
from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS
from game.main import Game
from gui.buttons import Button, Text, caption_text, play_white_button, play_black_button, difficulty_text, \
    minus_button, plus_button, restart_button, get_difficulty_num


class Gui:
    def __init__(self, game: Game):
        self.__game = game
        self.__clock = pg.time.Clock()
        self.frame_start = time.time()
        self.possible_moves = []
        self.selected_checker = None
        self.is_game_started = False
        self.difficulty = 3

        self.__screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Checkers')
        self.__sprites = Sprites(game.board_width)
        self.left_offset = WIN_SIZE[0] - self.__sprites.board.get_width()

        self.do_random_moves = True
        self.do_random_move_interval = 1
        self.next_time_do_random_move = time.time() + self.do_random_move_interval

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            if self.do_random_moves and time.time() >= self.next_time_do_random_move:
                self.doRandomMove()

            self.__clock.tick(FPS)

    def render(self):
        if self.is_game_started:
            if self.__game.is_player_white:
                board_sprite = self.__sprites.board
            else:
                board_sprite = self.__sprites.rotated_board
            self.__screen.blit(board_sprite, (self.left_offset, 0))

            if self.selected_checker is not None:
                x_cord = self.selected_checker.x
                y_cord = self.selected_checker.y
                coordinate = self.__sprites.get_coordinates(x_cord, y_cord, self.__game.is_player_white)
                coordinate = coordinate.move(self.left_offset, 0)
                self.__screen.blit(self.__sprites.indicator, coordinate)

            board = self.__game.getBoard()
            for i, row in enumerate(board):
                for j, figure in enumerate(row):
                    if not figure.is_checker:
                        continue
                    coordinate = self.__sprites.get_coordinates(i, j, self.__game.is_player_white)
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
                coordinate = self.__sprites.get_coordinates(move_x, move_y, self.__game.is_player_white)
                coordinate = coordinate.move(self.left_offset, 0)
                self.__screen.blit(self.__sprites.hint, coordinate)
            restart_button.render(self.__screen)
        else:
            self.__screen.fill((108, 152, 76))  # Сделать константой
            caption_text.render(self.__screen)
            play_white_button.render(self.__screen)
            play_black_button.render(self.__screen)
            difficulty_text.render(self.__screen)
            minus_button.render(self.__screen)
            plus_button.render(self.__screen)
            get_difficulty_num(self.difficulty).render(self.__screen)
        pg.display.update()

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button in (1, 3):  # RMB, LMB
                    x, y = event.pos
                    i, j = self.__sprites.get_cell(x - self.left_offset, y, self.__game.is_player_white)

                    board = self.__game.getBoard()
                    if self.is_game_started is False:
                        if play_white_button.collide_point((x, y)):
                            self.is_game_started = True
                            self.__game.is_player_white = True

                        if play_black_button.collide_point((x, y)):
                            self.is_game_started = True
                            self.__game.is_player_white = False

                        if plus_button.collide_point((x, y)):
                            self.difficulty += 1

                        if minus_button.collide_point((x, y)):
                            self.difficulty -= 1

                    if self.is_game_started:
                        # click on checker
                        if restart_button.collide_point((x, y)):
                            print(1)

                        if board[i][j].is_checker and board[i][j].is_white == self.__game.is_white_turn:
                            self.selected_checker = Point(i, j)
                            self.possible_moves = self.__game.getPossibleMoves(Point(i, j))
                            continue

                        # click on hint
                        for move in self.possible_moves:
                            move_end = move.end_point
                            if move_end.x == i and move_end.y == j:
                                is_white_flag = self.__game.is_white_turn
                                self.__game.handleMove(move)
                                self.possible_moves.clear()
                                if is_white_flag != self.__game.is_white_turn:
                                    self.selected_checker = None
                                else:
                                    self.selected_checker = move_end
                                    self.possible_moves = self.__game.getPossibleMoves(move_end)

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
        else:
            print("gamestate:", self.__game.handleWin())
            self.do_random_moves = False


    def close(self):
        raise Exception("Implement an exiting for all the child processes and threads!")
        exit()
