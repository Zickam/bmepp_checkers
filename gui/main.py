import datetime
from enum import Enum
import os

import pygame as pg

from game.classes import Move, move_to_notation
from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS, GC, MAX_DIFFICULTY, MIN_DIFFICULTY
from game.main import SimpleGame, GameState
from gui.buttons import caption_text, play_white_button, play_black_button, difficulty_text, \
    minus_button, plus_button, restart_button, get_difficulty_num, get_win_text
from game.board_manager import handleMove, possibleMovesForPoint
from game.bot import Bot


class Log:
    def __init__(self):
        if 'player_logs' not in os.listdir():
            os.mkdir('player_logs')
        self.file_name = f'player_logs/{str(datetime.datetime.now()).replace(":", "_")}.txt'

    def add_turn(self, move: tuple[tuple[int, int], ...]):
        move = move_to_notation(move)
        with open(self.file_name, 'a+', encoding='utf-8') as file:
            file.write(move+'\n')
            file.close()


class SceneState(Enum):
    menu = 0
    checkers = 1
    result = 2


class Gui:
    def __init__(self, opponent_bot: Bot, main_bot: Bot = None):
        """
        Can work in two modes: bot vs player, bot vs bot
        If main_bot param is not None, will start bot vs bot game
        """
        self.__game = SimpleGame()
        self.__clock = pg.time.Clock()
        self.bot_vs_bot_mode = main_bot is not None
        self.possible_moves: list[list[list[int, int]]] = []
        self.selected_checker: None | list[int, int] = None
        self.state = SceneState.menu if not self.bot_vs_bot_mode else SceneState.checkers
        self.difficulty = 1
        self.__bot = opponent_bot
        self.__bot_instead_player = main_bot
        if self.bot_vs_bot_mode:
            self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty)
        self.player_log = Log()

        self.__screen = pg.display.set_mode(WIN_SIZE)
        pg.display.set_caption('Checkers')
        self.__sprites = Sprites(self.__game.getBoardWidth())
        self.left_offset = WIN_SIZE[0] - self.__sprites.board.get_width()

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

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
            x_cord = self.selected_checker[0]
            y_cord = self.selected_checker[1]
            coordinate = self.__sprites.get_coordinates(x_cord, y_cord, self.__game.isPlayerWhite())
            coordinate = coordinate.move(self.left_offset, 0)
            self.__screen.blit(self.__sprites.indicator, coordinate)

    def render_checkers(self):
        board = self.__game.getBoard()
        for i, row in enumerate(board):
            for j, figure in enumerate(row):
                if not figure[0]:  # figure.is_checker
                    continue
                coordinate = self.__sprites.get_coordinates(i, j, self.__game.isPlayerWhite())
                coordinate = coordinate.move(self.left_offset, 0)
                if figure[1]:  # figure.is_white
                    if figure[2]:  # figure.is_queen
                        self.__screen.blit(self.__sprites.queen_white_checker, coordinate)
                    else:
                        self.__screen.blit(self.__sprites.white_checker, coordinate)
                else:
                    if figure[2]:  # figure.is_queen
                        self.__screen.blit(self.__sprites.queen_black_checker, coordinate)
                    else:
                        self.__screen.blit(self.__sprites.black_checker, coordinate)

    def render_hints(self):
        for move in self.possible_moves:
            move_x = move[1][0]
            move_y = move[1][1]
            coordinate = self.__sprites.get_coordinates(move_x, move_y, self.__game.isPlayerWhite())
            coordinate = coordinate.move(self.left_offset, 0)
            self.__screen.blit(self.__sprites.hint, coordinate)

    def handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.close()
            if not self.bot_vs_bot_mode:
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button in (1, 3):  # RMB, LMB
                        x, y = event.pos
                        if self.state == SceneState.checkers:
                            self.handle_gameplay_click(x, y)
                            if self.__game.getGameState() != GameState.ongoing:
                                self.state = SceneState.result
                        elif self.state == SceneState.menu:
                            self.handle_menu_click(x, y)
                        elif self.state == SceneState.result:
                            self.handle_result_click(x, y)

        if self.__bot.is_best_move_ready():
            flag = self.__game.isWhiteTurn()
            move = self.__bot.get_calculated_move()

            args = self.__game.toArgs()
            new_args = handleMove(*args, move)
            self.__game.fromArgs(*new_args)

            if flag == self.__game.isWhiteTurn():
                self.__bot.start_best_move_calculation(self.__game, self.difficulty)
            elif self.bot_vs_bot_mode:
                self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty)

        if self.__bot_instead_player and self.__bot_instead_player.is_best_move_ready():
            flag = self.__game.isWhiteTurn()
            move = self.__bot_instead_player.get_calculated_move()

            args = self.__game.toArgs()
            new_args = handleMove(*args, move)
            self.__game.fromArgs(*new_args)

            if flag == self.__game.isWhiteTurn():
                self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty)
            elif self.bot_vs_bot_mode:
                self.__bot.start_best_move_calculation(self.__game, self.difficulty)

    @property
    def is_bot_move(self):
        return self.__game.isPlayerWhite() != self.__game.isWhiteTurn()

    def handle_menu_click(self, x: int, y: int):
        if play_white_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(True)

        if play_black_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(False)
            self.__bot.start_best_move_calculation(self.__game, self.difficulty)

        if plus_button.collide_point((x, y)) and self.difficulty < MAX_DIFFICULTY:
            self.difficulty += 1

        if minus_button.collide_point((x, y)) and self.difficulty > MIN_DIFFICULTY:
            self.difficulty -= 1

    def handle_gameplay_click(self, x: int, y: int):
        if restart_button.collide_point((x, y)):
            self.__game = SimpleGame()
            self.state = SceneState.menu
            self.selected_checker = None
            self.possible_moves.clear()
            self.__bot.end_bot_thinking()

        i, j = self.__sprites.get_cell(x - self.left_offset, y, self.__game.isPlayerWhite())
        board = self.__game.getBoard()
        if self.is_bot_move is False:
            # click on checker
            if board[i][j][0] and board[i][j][1] == self.__game.isWhiteTurn():
                self.selected_checker = [i, j]
                self.possible_moves = possibleMovesForPoint(self.__game, [i, j])

        # click on hint
        for move in self.possible_moves:
            move_end = move[1]
            if move_end[0] == i and move_end[1] == j:
                is_white_flag = self.__game.isWhiteTurn()

                args = self.__game.toArgs()
                new_args = handleMove(*args, move)
                self.__game.fromArgs(*new_args)

                #self.player_log.add_turn(move)
                self.possible_moves.clear()

                if is_white_flag != self.__game.isWhiteTurn():
                    self.selected_checker = None
                    self.__bot.start_best_move_calculation(self.__game, self.difficulty)
                else:
                    self.selected_checker = move_end
                    self.possible_moves = possibleMovesForPoint(self.__game, move_end)

    def handle_result_click(self, x, y):
        if restart_button.collide_point((x, y)):
            self.__game = SimpleGame()
            self.state = SceneState.menu

    def close(self):
        exit()

