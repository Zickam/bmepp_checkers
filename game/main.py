import copy

from game.classes import *
from game import constants



class Figure:
    def __init__(self, is_checker: bool, is_white: bool):
        self.is_checker: bool = is_checker
        self.is_white: bool = is_white
        self.is_queen: bool = False


class Game:
    if constants.BOARD_WIDTH < constants.MIN_BOARD_WIDTH:
        raise Exception(f"Its not possible to make a board which side is less than {constants.MIN_BOARD_WIDTH}")

    def __init__(self):
        self.board_width = constants.BOARD_WIDTH
        self.board = self._initBoard()

        self.board[4][5].is_checker = True
        self.board[1][2].is_checker = False
        self.board[5][6].is_checker = True
        self.board[5][6].is_white = True
        self.board[2][5].is_checker = False

        self.is_player_turn = True
        self.is_player_first = True

    def _initBoard(self) -> list[list[Figure, ...], ...]:
        board = []

        for i in range(self.board_width):
            board.append([])
            for j in range(self.board_width):
                board[i].append(Figure(False, False))
        for i in range(3):
            for j in range(self.board_width):
                if i % 2 == 1 and j % 2 == 0:
                    board[i][j] = Figure(True, False)
                elif i % 2 == 0 and j % 2 == 1:
                    board[i][j] = Figure(True, False)
                if (self.board_width - i - 1) % 2 == 1 and (self.board_width - j - 1) % 2 == 0:
                    board[self.board_width - i - 1][self.board_width - j - 1] = Figure(True, True)
                elif (self.board_width - i - 1) % 2 == 0 and (self.board_width - j - 1) % 2 == 1:
                    board[self.board_width - i - 1][self.board_width - j - 1] = Figure(True, True)

        return board

    def getBoard(self) -> list[list[Figure, ...], ...]:
        return self.board

    def handleKillMove(self, move: Move):
        killed_checker_point = move.end_point - move.start_point
        killed_checker_point.x //= 2
        killed_checker_point.y //= 2
        killed_checker_point += move.start_point

        self.board[killed_checker_point.x][killed_checker_point.y].is_checker = False
        self.board[move.start_point.x][move.start_point.y].is_checker = False
        self.board[move.end_point.x][move.end_point.y].is_checker = True
        self.board[move.end_point.x][move.end_point.y].is_white = self.board[move.start_point.x][move.start_point.y].is_white

    def handleSingleMove(self, move: Move):
        self.board[move.end_point.x][move.end_point.y].is_checker = self.board[move.start_point.x][move.start_point.y].is_checker
        self.board[move.end_point.x][move.end_point.y].is_white = self.board[move.start_point.x][move.start_point.y].is_white
        self.board[move.start_point.x][move.start_point.y].is_checker = False



    def handleMove(self, move: Move):
        print(move)
        if not self.board[move.start_point.x][move.start_point.y].is_queen:
            if abs(move.start_point.x - move.end_point.x) == 1:
                self.handleSingleMove(move)

            elif abs(move.start_point.x - move.end_point.x) > 1: # overcome one cell (kill)
                self.handleKillMove(move)

        else:
            raise Exception("Queen")

        return self.getPossibleMoves(move.end_point)

    def __isMoveWithinBoundaries(self, move: Move) -> bool:
        if 0 <= move.end_point.x < self.board_width \
                and 0 <= move.end_point.y < self.board_width:
            return True

        return False

    def __isCheckerMovePossible(self, start_point: Point, direction: Point) -> tuple[bool, Move | None]:
        move = Move(start_point, start_point + direction)
        if self.__isMoveWithinBoundaries(move):
            if self.board[move.end_point.x][move.end_point.y].is_checker:
                if self.board[move.start_point.x][move.start_point.y].is_white \
                        != self.board[move.end_point.x][move.end_point.y].is_white:
                    move = Move(move.start_point, move.end_point + direction)
                    if self.__isMoveWithinBoundaries(move):
                        if not self.board[move.end_point.x][move.end_point.y].is_checker:
                            return True, move
            else:
                if self.board[move.start_point.x][move.start_point.y].is_white:
                    if direction.x < 0:
                        return True, move
                else:
                    if direction.x > 0:
                        return True, move

                return False, None

        return False, None

    def __isQueenMovePossible(self, start_point: Point, direction: Point) -> tuple[bool, Move | None]:
        move = Move(start_point, start_point + direction)
        if self.__isMoveWithinBoundaries(move):
            if self.board[move.end_point.x][move.end_point.y].is_checker:
                if self.board[move.start_point.x][move.start_point.y].is_white \
                        != self.board[move.end_point.x][move.end_point.y].is_white:
                    move = Move(move.start_point, move.end_point + direction)
                    if self.__isMoveWithinBoundaries(move):
                        if not self.board[move.end_point.x][move.end_point.y].is_checker:
                            return True, move
            else:
                return True, move

        return False, None

    queen_directions = [
        Point(1, 1),
        Point(-1, -1),
        Point(1, -1),
        Point(-1, 1)
    ]

    def getPossibleMoves(self, start_point: Point) -> list[Move, ...]:
        possible_moves = []

        if self.board[start_point.x][start_point.y].is_queen:
            for direction in self.queen_directions:
                for i in range(1, self.board_width):
                    direction_new = direction * i
                    is_possible, move = self.__isQueenMovePossible(start_point, direction_new)
                    if is_possible:
                        possible_moves.append(move)
                    else:
                        break

        else:
            for i in [-1, 1]:
                for j in [-1, 1]:
                    is_possible, move = self.__isCheckerMovePossible(start_point, Point(i, j))
                    if is_possible:
                        possible_moves.append(move)

        return possible_moves

if __name__ == "__main__":
    game = Game()

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