import copy
import random
from enum import Enum
import queue

from game.classes import *
from game import constants

import numpy as np
import numba

@numba.njit
def initNumba():
    ...


class GameState(Enum):
    ongoing = "Ongoing"
    b_win = "Black won"
    w_win = "White won"
    draw = "Draw"


MAX_GAME_BOARD_DEPTH = 60


class SimpleGame:
    def __init__(self):
        # simple version of border is 8x8 matrix where each cell represents one cell on the real board
        # 1st element of cell indicates whether this cell is checker or not
        # 2nd element of cell indicates if the checker is white or black
        # 3rd element of cell indicates queen
        self._board: np.array[np.array[np.array[
            bool, bool, bool]]] = self._initBoard(8)
        # self._board = np.array([
        #     [[0, 0, 0] for j in range(8)] for i in range(8)
        # ])
        # self._board[0, 1] = np.array([1, 0, 1])
        # self._board[7, 6] = np.array([1, 1, 1])
        # # self._board[4, 1] = np.array([1, 0, 0])
        # # self._board[5, 4] = np.array([1, 0, 0])
        # # self._board[5, 6] = np.array([1, 0, 0])

        # _board_values contains these values:
        # 0 - checkers amount
        # 1 - queens amount
        # 2 - distance to promotion line
        self._board_values = np.array([0, 0, 0])

        self._is_white_turn = True
        self._is_player_white = True

        self._count_draw_moves = 0

        self._is_previous_turn_white = False
        self._last_move = np.array([[-1, -1], [-1, -1]])

    def getPreviousTurnWhite(self) -> bool:
        return self._is_previous_turn_white

    def getLastMove(self) -> np.array:
        return self._last_move

    def isWhiteTurn(self) -> bool:
        return self._is_white_turn

    def getBoard(self) -> np.array:
        return self._board

    def getCountDrawMoves(self) -> int:
        return self._count_draw_moves

    def setIsPlayerWhite(self, is_player_white: bool):
        self._is_player_white = is_player_white

    def isPlayerWhite(self) -> bool:
        return self._is_player_white

    def getBoardWidth(self) -> int:
        return self._board.shape[0]

    def getGameState(self) -> GameState:
        return GameState.ongoing

    def toArgs(self):
        return copy.deepcopy(self.getBoard()), self.isWhiteTurn(), self._board_values, self._is_previous_turn_white, self._last_move, self._count_draw_moves

    def fromArgs(self, board: np.array, is_white_turn: bool, board_values, is_previous_turn_white: bool, last_move: np.array, count_draw_moves:int):
        self._board = board
        self._is_white_turn = is_white_turn
        self._board_values = board_values
        self._is_previous_turn_white = is_previous_turn_white
        self._last_move = last_move
        self._count_draw_moves = count_draw_moves


    def _initBoard(self, board_width: int) -> np.array:
        board = np.array([[np.array([False, False, False]) for i in range(board_width)] for j in range(board_width)])

        for i in range(3):
            for j in range(board_width):
                is_on_white_1 = i % 2 == 1 and j % 2 == 0
                is_on_white_2 = i % 2 == 0 and j % 2 == 1

                if is_on_white_1 or is_on_white_2:
                    board[i][j] = np.array([1, 0, 0])

                is_on_black_1 = (board_width - i - 1) % 2 == 1 and (board_width - j - 1) % 2 == 0
                is_on_black_2 = (board_width - i - 1) % 2 == 0 and (board_width - j - 1) % 2 == 1

                if is_on_black_1 or is_on_black_2:
                    board[board_width - i - 1][board_width - j - 1] = np.array([1, 1, 0])

        return board




class Game:
    if constants.BOARD_WIDTH < constants.MIN_BOARD_WIDTH:
        raise Exception(f"Its not possible to make a board which side is less than {constants.MIN_BOARD_WIDTH}")

    def __init__(self):
        self._board_width = constants.BOARD_WIDTH
        self._is_player_white = True
        self._is_white_turn = True
        self._game_state = GameState.ongoing
        self._difficulty = None

        self._board: list[list[Figure]] = self._initBoard()

        self._count_moves_without_change = 0
        self._count_figure = self._getFiguresAmount()

        self._available_moves: dict[Point.__hash__,
        list[Move]] = self._getAvailableMoves()

    def getBoard(self) -> list[list[Figure]]:
        return self._board

    def getGameState(self) -> GameState:
        return self._game_state

    def getBoardWidth(self) -> int:
        return self._board_width

    def isWhiteTurn(self) -> bool:
        return self._is_white_turn

    def getIsPlayerWhite(self) -> bool:
        return self._is_player_white

    def setIsPlayerWhite(self, new_state: bool):
        self._is_player_white = new_state

    def setDifficulty(self, difficulty: int):
        self._difficulty = difficulty

    def getDifficulty(self):
        return self._difficulty

    def restart(self):
        raise Exception("Do we actually need this?")
        return Game()
        pass  # вызывается при нажатии на кнопку рестарта

    def _initBoard(self) -> list[list[Figure]]:
        board = []

        for i in range(self.getBoardWidth()):
            board.append([])
            for j in range(self.getBoardWidth()):
                board[i].append(Figure(False, False))
        for i in range(3):
            for j in range(self.getBoardWidth()):
                is_on_white_1 = i % 2 == 1 and j % 2 == 0
                is_on_white_2 = i % 2 == 0 and j % 2 == 1

                if is_on_white_1 or is_on_white_2:
                    board[i][j] = Figure(True, False)

                is_on_black_1 = (self.getBoardWidth() - i - 1) % 2 == 1 and (self.getBoardWidth() - j - 1) % 2 == 0
                is_on_black_2 = (self.getBoardWidth() - i - 1) % 2 == 0 and (self.getBoardWidth() - j - 1) % 2 == 1
                if is_on_black_1 or is_on_black_2:
                    board[self.getBoardWidth() - i - 1][self.getBoardWidth() - j - 1] = Figure(True, True)
        return board

    def _handleKillMove(self, move: Move):
        self._board[move.killed_point.x][move.killed_point.y] = Figure(False)
        self._handleRelocation(move)

        self._count_figure -= 1
        self._count_moves_without_change = 0

    def _handleRelocation(self, move: Move):
        self._board[move.end_point.x][move.end_point.y] = self._board[move.start_point.x][move.start_point.y]
        self._board[move.start_point.x][move.start_point.y] = Figure(False)

    def _handleContinuousMove(self, move):
        self._available_moves = self._getAvailableMoves()
        if move.end_point.__hash__() in self._available_moves:
            necessary_moves = []
            for possible_move in self._available_moves[move.end_point.__hash__()]:
                if possible_move.is_kill:
                    necessary_moves.append(possible_move)
            if len(necessary_moves) == 0:
                self._is_white_turn = not self._is_white_turn
        else:
            self._is_white_turn = not self._is_white_turn

    def _handleChecker2Queen(self, move: Move) -> bool:
        if self._board[move.end_point.x][move.end_point.y].is_white:
            if move.end_point.x == 0:
                self._board[move.end_point.x][move.end_point.y].is_queen = True
                return True

        else:
            if move.end_point.x == self.getBoardWidth() - 1:
                self._board[move.end_point.x][move.end_point.y].is_queen = True
                return True

        return False

    def _handleQueenMove(self, move: Move):
        if move.is_kill:
            self._handleKillMove(move)
            self._handleContinuousMove(move)

        else:
            self._handleRelocation(move)
            self._is_white_turn = not self._is_white_turn

    def _handleCheckerMove(self, move: Move):
        if move.is_kill:
            self._handleKillMove(move)
            self._handleChecker2Queen(move)

            self._handleContinuousMove(move)

        else:
            self._handleRelocation(move)
            has_transformed = self._handleChecker2Queen(move)
            if not has_transformed:
                self._is_white_turn = not self._is_white_turn

            self._available_moves = self._getAvailableMoves()

    def handleDraw(self):
        self._count_moves_without_change += 1
        if self._count_moves_without_change >= MAX_GAME_BOARD_DEPTH:
            self._game_state = GameState.draw

    def _checkIsMoveCorrect(self, move: Move) -> tuple[bool, str]:
        if move.is_kill:
            if not self.getBoard()[move.killed_point.x][move.killed_point.y].is_checker:
                return False, "Killed checker doesnt exist"
            if not self.getBoard()[move.start_point.x][move.start_point.y].is_checker:
                return False, "Killing checker doesnt exist"
            if self.getBoard()[move.start_point.x][move.start_point.y] == self.getBoard()[move.killed_point.x][
                move.killed_point.y]:
                return False, "Killing checker's team is the same as killed checker's team"
        else:
            if not self.getBoard()[move.start_point.x][move.start_point.y].is_checker:
                return False, "Moving checker doesnt exist"
            if self.getBoard()[move.end_point.x][move.end_point.y].is_checker:
                return False, "End point is already occupied"

        return True, ""

    def handleMove(self, move: Move):

        is_move_correct, exception = self._checkIsMoveCorrect(move)
        if not is_move_correct:
            raise Exception(f"Incorrect move: {move}. \nException: {exception}")

        if not self._board[move.start_point.x][move.start_point.y].is_queen:
            self._handleCheckerMove(move)
        else:
            self._handleQueenMove(move)

        self._available_moves = self._getAvailableMoves()

        self.handleWin()
        self.handleDraw()

        # print("Current state:", self.getGameState())

    def _getFiguresAmount(self) -> int:
        figures_amount = 0
        for row in self._board:
            for fig in row:
                if fig.is_checker:
                    figures_amount += 1

        return figures_amount

    def getWFiguresDifference(self) -> int:
        w, b = 0, 0
        for row in self.getBoard():
            for cell in row:
                if cell.is_checker:
                    match cell.is_white:
                        case True:
                            w += 1
                        case False:
                            b += 1

        return w - b

    def getAllMoves(self):
        moves_arrays = self._available_moves.values()
        moves = []
        for arr in moves_arrays:
            for elem in arr:
                moves.append(elem)
        return moves

    def handleWin(self):
        current_side_has_moves = False
        for moves in self._available_moves.values():
            for move in moves:
                if self._is_white_turn and self._board[move.start_point.x][
                    move.start_point.y].is_white:
                    current_side_has_moves = True
                elif not self._is_white_turn and not self._board[move.start_point.x][
                    move.start_point.y].is_white:
                    current_side_has_moves = True

        if not current_side_has_moves:
            if self._is_white_turn:
                self._game_state = GameState.b_win
            else:
                self._game_state = GameState.w_win
        else:
            self._game_state = GameState.ongoing

    def _isMoveWithinBoundaries(self, move: Move) -> bool:
        if 0 <= move.end_point.x < self.getBoardWidth() \
                and 0 <= move.end_point.y < self.getBoardWidth():
            return True

        return False

    def _isCheckerMovePossible(self, start_point: Point,
                               direction: Point) -> tuple[bool, Move | None]:
        move = Move(start_point, start_point + direction)
        if self._isMoveWithinBoundaries(move):
            if self._board[move.end_point.x][move.end_point.y].is_checker:
                if self._board[move.start_point.x][move.start_point.y].is_white \
                        != self._board[move.end_point.x][move.end_point.y].is_white:
                    move = Move(move.start_point, move.end_point + direction)
                    if self._isMoveWithinBoundaries(move):
                        if not self._board[move.end_point.x][move.end_point.y].is_checker:
                            move.is_kill = True
                            move.killed_point = move.start_point + direction
                            return True, move
            else:
                if self._board[move.start_point.x][move.start_point.y].is_white:
                    if direction.x < 0:
                        return True, move
                else:
                    if direction.x > 0:
                        return True, move

                return False, None

        return False, None

    def _isQueenMovePossible(self, start_point: Point, direction: Point, raw_direction: Point) -> list[Move | None]:
        moves = []
        # 1. не на границе, за ней есть кто-то(впритык член?)
        move = Move(start_point, start_point + direction)
        if self._isMoveWithinBoundaries(move):
            if self._board[move.end_point.x][move.end_point.y].is_checker:
                if self._board[move.start_point.x][move.start_point.y].is_white \
                        != self._board[move.end_point.x][move.end_point.y].is_white:
                    # след пустая?
                    # перебираем до след шашки(хоть наша, хоть нет, иначе до конца) и возвращаем все возможные ходы.

                    for i in range(1, 7):
                        _move = Move(move.start_point, move.end_point + raw_direction * i,
                                     True, move.end_point)

                        if self._isMoveWithinBoundaries(_move) and self._board[
                            _move.end_point.x][_move.end_point.y].is_checker == False:
                            moves.append(_move)
                        elif self._isMoveWithinBoundaries(_move) and self._board[
                            _move.end_point.x][_move.end_point.y].is_checker == True:
                            break

                    return moves
            else:
                return [move]

        return []

    _queen_directions = [Point(1, 1), Point(-1, -1), Point(1, -1), Point(-1, 1)]

    def _getQueenPossibleMoves(self, start_point: Point) -> Moves:
        moves = Moves([], [])
        directions_for_necessary_moves = set()

        for direction in self._queen_directions:
            for i in range(1, self.getBoardWidth()):
                if direction.__hash__() in directions_for_necessary_moves:
                    continue

                direction_new = direction * i
                possible_moves = self._isQueenMovePossible(start_point, direction_new,
                                                           direction)
                if len(possible_moves) != 0:
                    for move in possible_moves:
                        if move.is_kill:
                            moves.necessary_moves.append(move)
                            directions_for_necessary_moves.add(direction.__hash__())
                        else:
                            moves.unnecessary_moves.append(move)

                else:
                    break
        return moves

    def _getCheckerPossibleMoves(self, start_point: Point) -> Moves:
        unnecessary_moves = []
        necessary_moves = []  # killing moves

        for i in [-1, 1]:
            for j in [-1, 1]:
                is_possible, move = self._isCheckerMovePossible(
                    start_point, Point(i, j))
                if is_possible:
                    match move.is_kill:
                        case True:
                            necessary_moves.append(move)
                        case False:
                            unnecessary_moves.append(move)

        return Moves(necessary_moves, unnecessary_moves)

    def _getPossibleMovesForPoint(self, start_point: Point) -> Moves:
        if self._board[start_point.x][start_point.y].is_queen:
            possible_moves = self._getQueenPossibleMoves(start_point)
        else:
            possible_moves = self._getCheckerPossibleMoves(start_point)

        return possible_moves

    def _getAvailableMoves(self) -> dict[Point.__hash__, list[Move]]:  # str is the __repr__ of Point
        def iteration_board():
            for i in range(self.getBoardWidth()):
                for j in range(self.getBoardWidth()):
                    yield i, j

        necessary_moves = {}
        unnecessary_moves = {}

        for i, j in iteration_board():
            if self._board[i][j].is_checker and self._is_white_turn == self._board[i][j].is_white:
                possible_moves = self._getPossibleMovesForPoint(Point(i, j))
                if possible_moves.necessary_moves:
                    for necessary_move in possible_moves.necessary_moves:
                        if necessary_move.start_point.__hash__() in necessary_moves:
                            necessary_moves[necessary_move.start_point.__hash__()].append(necessary_move)
                        else:
                            necessary_moves[necessary_move.start_point.__hash__()] = [necessary_move]
                elif not necessary_moves:
                    for unnecessary_move in possible_moves.unnecessary_moves:
                        if unnecessary_move.start_point.__hash__() in unnecessary_moves:
                            unnecessary_moves[unnecessary_move.start_point.__hash__()].append(unnecessary_move)
                        else:
                            unnecessary_moves[unnecessary_move.start_point.__hash__()] = [unnecessary_move]

        if necessary_moves:
            return necessary_moves
        else:
            return unnecessary_moves

    def getPossibleMoves(self, start_point: Point) -> list[Move]:
        if start_point.__hash__() in self._available_moves:
            return self._available_moves[start_point.__hash__()]
        return []


del Game  # HAHA


def game_board_to_str(board: np.array) -> str:
    s = ''
    for i, row in enumerate(board):
        for j, figure in enumerate(row):
            if figure[0]:
                fig_s = f'{i}{j}{int(figure[1])}{int(figure[2])}'
                s += fig_s
    return s

def getRandomizedBoard():
    board = np.array([[np.array([False, False, False]) for i in range(8)]
                      for j in range(8)])

    c = 10
    for i in range(c):
        random_i = random.randint(0, 7)
        if random_i % 2 == 0:
            random_j = random.choice([j for j in range(1, 7, 2)])
        else:
            random_j = random.choice([j for j in range(0, 7, 2)])

        random_side = random.choice([True, False])
        is_queen = random.choice([True, False])
        board[random_i, random_j][0] = True
        board[random_i, random_j][1] = random_side
        board[random_i, random_j][2] = is_queen

    for i in board:
        print(*i, sep=" ")

    ''' print(BoardManager.getQueensAmount(board))
    print(BoardManager.getQueensAmountOnMainDiagonal(board))
    print(BoardManager.getQueensAmountOnDoubleDiagonal(board))
    print(BoardManager.getCentrallyPositionedQueensAmount(board))'''
    return board


if __name__ == "__main__":
    import time

    game = Game()
    simple_game = SimpleGame()
    # print(moves)
    # print(HeuristicFunctions.calculateHeuristicValue(simple_game.getBoard()))
    # s = time.time()
    # for i in range(10 ** 6):
    #     (BoardManager.getAvailableMovesForPoint(simple_game.getBoard(), simple_game.getIsWhiteTurn(), 5, 1))
    # print(time.time() - s)
    print(game_board_to_str(simple_game.getBoard()))
    exit(

    )
    for i in game.getBoard():
        for j in i:
            if j.is_checker:
                if j.is_white:
                    print("W", end="\t")
                else:
                    print("B", end="\t")
            else:
                print("[]", end="\t")

        print()

    # self._board = [[Figure() for i in range(8)] for j in range(8)]
    #
    # self._board[1][2].is_checker = True
    # self._board[1][2].is_white = False
    #
    # self._board[3][4].is_checker = True
    # self._board[3][4].is_white = False
    #
    # self._board[4][5].is_checker = True
    # self._board[4][5].is_white = True

