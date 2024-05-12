import datetime
import time
from enum import Enum
import numpy as np

from game.classes import move_to_notation
from gui.sprites import Sprites
from gui.constants import WIN_SIZE, FPS, GC
from game.main import SimpleGame
from gui.buttons import caption_text, play_white_button, play_black_button, difficulty_text, minus_button, \
    plus_button, restart_button, get_difficulty_num, get_win_text, training_button, help_button, \
    help_buttons_animation, player_player_button, bot_bot_button
from game.board_manager import handle_move_pr, possibleMovesForPoint, handleWin
from game.bot import Bot
from game.minmax import game_board_to_str
from game.constants import DEFAULT_DIFFICULTY, DIFFICULTIES


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg


class Log:
    def __init__(self):
        if 'player_logs' not in os.listdir():
            os.mkdir('player_logs')
        self.file_name = f'player_logs/{str(datetime.datetime.now()).replace(":", "_")}.txt'

    def add_turn(self, move: np.array):
        move = move_to_notation(move)
        with open(self.file_name, 'a+', encoding='utf-8') as file:
            file.write(move+'\n')
            print('add')
            file.close()


class SceneState(Enum):
    menu = 0
    checkers = 1
    result = 2
    checkers_with_help = 3


class ModeState(Enum):
    bot_vs_bot = 0
    bot_vs_player = 1
    player_vs_player = 2


class DrawHandler:
    def __init__(self):
        self.cache = set()

    def check_draw(self, board) -> bool:
        if game_board_to_str(board) in self.cache:
            return True
        else:
            self.cache.add(game_board_to_str(board))
            return False


class Gui:
    def __init__(self, opponent_bot: Bot,
                 main_bot: Bot = None,
                 caption='Checkers',
                 with_display=True,
                 need_to_calculate=False):
        """
        Can work in two modes: bot vs player, bot vs bot
        If main_bot param is not None, will start bot vs bot game, opponent_bot playing black, main_bot playing white
        """
        self.__game = SimpleGame()
        self.__clock = pg.time.Clock()
        self.with_display = with_display
        self.possible_moves: list[list[list[int]]] = []
        self.selected_checker: None | list[int] = None
        self.state = SceneState.menu  # if not self.bot_vs_bot_mode else SceneState.checkers
        self.mode_state = ModeState.bot_vs_player
        self.difficulty = DEFAULT_DIFFICULTY
        self.__bot = opponent_bot
        self.__bot_instead_player = main_bot
        self.draw_handler = DrawHandler()
        self.player_log = Log()

        if self.with_display:
            self.__screen = pg.display.set_mode(WIN_SIZE)
            pg.display.set_caption(caption)

        self.__sprites = Sprites(self.__game.getBoardWidth())
        self.left_offset = WIN_SIZE[0] - self.__sprites.board.get_width()

    def change_caption(self, caption: str):
        pg.display.set_caption(caption)

    def mainloop(self):
        while True:
            self.render()
            self.handle_events()

            self.__clock.tick(FPS)

    def bots_duel(self, difficulty: int) -> int:
        self.difficulty = difficulty
        self.mode_state = ModeState.bot_vs_bot
        self.state = SceneState.checkers
        self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty, True)

        while True:
            self.__clock.tick(FPS)
            if self.with_display:
                self.render()
            pg.event.get()
            self.handle_bot_events()
            if self.state == SceneState.result:
                if self.draw_handler.check_draw(self.__game.getBoard()):
                    return 3
                return handleWin(self.__game.getBoard(), self.__game.isWhiteTurn(), self.__game.getPreviousTurnWhite(), self.__game.getLastMove(), self.__game.getCountDrawMoves())

    def render(self):
        if self.state == SceneState.checkers:
            self.render_gameplay()
        elif self.state == SceneState.menu:
            self.render_menu()
        elif self.state == SceneState.result:
            self.render_result()
        elif self.state == SceneState.checkers_with_help:
            self.render_gameplay()
        pg.display.update()

    def render_gameplay(self):
        self.render_board()
        self.render_selected_checker()
        self.render_checkers()
        self.render_hints()
        restart_button.render(self.__screen)
        if self.state == SceneState.checkers_with_help:
            help_button.render(self.__screen)

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
        training_button.render(self.__screen)
        player_player_button.render(self.__screen)
        bot_bot_button.render(self.__screen)
        get_difficulty_num(self.difficulty).render(self.__screen)

    def render_result(self):
        # self.__screen.fill(GC)
        get_win_text(
            handleWin(
                self.__game.getBoard(),
                self.__game.isWhiteTurn(),
                self.__game.getPreviousTurnWhite(),
                self.__game.getLastMove(), self.__game.getCountDrawMoves())
        ).render(self.__screen)

        restart_button.render(self.__screen)

    def render_board(self):
        if self.__game.isPlayerWhite():
            board_sprite = self.__sprites.board
        else:
            board_sprite = self.__sprites.rotated_board
        self.__screen.blit(board_sprite, (self.left_offset, 0))

    def render_selected_checker(self, checker=None):
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

    def render_hints(self, hint=None):
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
            if not self.mode_state == ModeState.bot_vs_bot:
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button in (1, 3):  # RMB, LMB
                        x, y = event.pos

                        if self.state == SceneState.checkers:
                            self.handle_gameplay_click(x, y)
                            state = handleWin(self.__game.getBoard(), self.__game.isWhiteTurn(), self.__game.getPreviousTurnWhite(), self.__game.getLastMove(), self.__game.getCountDrawMoves())
                            if state in [1, 2]:  # game is ended (w win, b win)
                                self.state = SceneState.result
                            return

                        elif self.state == SceneState.checkers_with_help:
                            self.handle_gameplay_click(x, y)
                            state = handleWin(self.__game.getBoard(), self.__game.isWhiteTurn(), self.__game.getPreviousTurnWhite(), self.__game.getLastMove(), self.__game.getCountDrawMoves())
                            if state in [1, 2]:  # game is ended (w win, b win)
                                self.state = SceneState.result
                            return

                        elif self.state == SceneState.menu:
                            self.handle_menu_click(x, y)
                        elif self.state == SceneState.result:
                            self.handle_result_click(x, y)
            elif self.state != SceneState.menu:
                if restart_button.collide_point(pg.mouse.get_pos()) and any(pg.mouse.get_pressed()[:2][::1]):
                    self.__game = SimpleGame()
                    self.state = SceneState.menu
                    self.mode_state = ModeState.player_vs_player
                    self.selected_checker = None
                    self.possible_moves.clear()
                    self.__bot.end_bot_thinking()
                    self.__bot_instead_player.end_bot_thinking()

        self.handle_bot_events()

    def handle_bot_events(self):
        if self.__bot.is_best_move_ready():

            flag = self.__game.isWhiteTurn()
            move = self.__bot.get_calculated_move()

            args = self.__game.toArgs()
            new_args = handle_move_pr(*args, move)
            self.__game.fromArgs(*new_args)

            state = handleWin(self.__game.getBoard(), self.__game.isWhiteTurn(),  self.__game.getPreviousTurnWhite(), self.__game.getLastMove(), self.__game.getCountDrawMoves())
            if state in [1, 2, 3]:  # game is ended (w win, b win, draw)
                self.state = SceneState.result
                return
            if self.mode_state == ModeState.bot_vs_bot and self.draw_handler.check_draw(self.__game.getBoard()):
                self.state = SceneState.result
                return

            if flag == self.__game.isWhiteTurn():

                self.__bot.start_best_move_calculation(self.__game, self.difficulty, not self.__game.isPlayerWhite())
            elif self.mode_state == ModeState.bot_vs_bot:

                self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty, True)

        if self.__bot_instead_player and self.__bot_instead_player.is_best_move_ready():

            flag = self.__game.isWhiteTurn()
            move = self.__bot_instead_player.get_calculated_move()

            args = self.__game.toArgs()
            new_args = handle_move_pr(*args, move)
            self.__game.fromArgs(*new_args)

            state = handleWin(self.__game.getBoard(), self.__game.isWhiteTurn(),  self.__game.getPreviousTurnWhite(), self.__game.getLastMove(), self.__game.getCountDrawMoves())
            if state in [1, 2, 3]:  # game is ended (w win, b win, draw)
                self.state = SceneState.result
                return
            if self.mode_state == ModeState.bot_vs_bot and self.draw_handler.check_draw(self.__game.getBoard()):
                self.state = SceneState.result
                return

            if flag == self.__game.isWhiteTurn():

                self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty, True)
            elif self.mode_state == ModeState.bot_vs_bot:

                self.__bot.start_best_move_calculation(self.__game, self.difficulty, False)

    @property
    def is_bot_move(self):
        return self.__game.isPlayerWhite() != self.__game.isWhiteTurn()

    def handle_menu_click(self, x: int, y: int):
        if play_white_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(True)
            self.mode_state = ModeState.bot_vs_player

        if play_black_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(False)
            self.__bot.start_best_move_calculation(self.__game, self.difficulty, True)
            self.mode_state = ModeState.bot_vs_player

        if player_player_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(True)
            self.mode_state = ModeState.player_vs_player

        if bot_bot_button.collide_point((x, y)):
            self.state = SceneState.checkers
            self.__game.setIsPlayerWhite(True)
            self.mode_state = ModeState.bot_vs_bot
            self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty, True)

        if plus_button.collide_point((x, y)) and self.difficulty < len(DIFFICULTIES):
            self.difficulty += 1

        if minus_button.collide_point((x, y)) and self.difficulty > 0:
            self.difficulty -= 1

        if training_button.collide_point((x, y)):
            self.state = SceneState.checkers_with_help
            self.__game.setIsPlayerWhite(True)

    def handle_gameplay_click(self, x: int, y: int):
        if restart_button.collide_point((x, y)):
            self.__game = SimpleGame()
            self.state = SceneState.menu
            self.selected_checker = None
            self.possible_moves.clear()
            self.__bot.end_bot_thinking()

        if help_button.collide_point((x, y)):
            self.__bot.start_best_move_calculation(self.__game, self.difficulty, self.__game.isPlayerWhite())
            start = time.time()
            while not self.__bot.is_best_move_ready():
                [exit() for event in pg.event.get() if event.type == pg.QUIT]
                ind = int((time.time() - start) * 5 % len(help_buttons_animation))
                button = help_buttons_animation[ind]
                button.render(self.__screen)
                pg.display.update()
            best_move = self.__bot.get_calculated_move()
            self.selected_checker = best_move[0]
            self.possible_moves = [best_move]
            return

        i, j = self.__sprites.get_cell(x - self.left_offset, y, self.__game.isPlayerWhite())
        board = self.__game.getBoard()

        # click on hint
        for move in self.possible_moves:
            move_end = move[1]
            if move_end[0] == i and move_end[1] == j:
                is_white_flag = self.__game.isWhiteTurn()

                args = self.__game.toArgs()
                new_args = handle_move_pr(*args, move)
                self.__game.fromArgs(*new_args)

                self.player_log.add_turn(move)
                print('clear')
                self.possible_moves.clear()

                if is_white_flag != self.__game.isWhiteTurn():
                    self.selected_checker = None
                    if self.mode_state != ModeState.player_vs_player:
                        finding_max = not self.__game.isPlayerWhite()
                        self.__bot.start_best_move_calculation(self.__game, self.difficulty, finding_max)
                    return
                else:
                    self.selected_checker = move_end
                    self.possible_moves = possibleMovesForPoint(self.__game, move_end)
                    return

        if self.mode_state == ModeState.player_vs_player or\
            (self.mode_state == ModeState.bot_vs_player and self.is_bot_move is False):
            # click on checker
            if board[i][j][0] and board[i][j][1] == self.__game.isWhiteTurn():
                self.selected_checker = [i, j]
                self.possible_moves = possibleMovesForPoint(self.__game, [i, j])
            else:
                self.selected_checker = None
                self.possible_moves = []

    def handle_result_click(self, x, y):
        if restart_button.collide_point((x, y)):
            self.__game = SimpleGame()
            self.state = SceneState.menu

    def change_bots(self, bot1: Bot, bot2: Bot):
        self.__bot = bot1
        self.__bot_instead_player = bot2
        self.draw_handler = DrawHandler()
        self.state = SceneState.checkers
        self.__game = SimpleGame()
        self.possible_moves = []
        # self.__bot_instead_player.start_best_move_calculation(self.__game, self.difficulty, True)


    def close(self):
        exit()
