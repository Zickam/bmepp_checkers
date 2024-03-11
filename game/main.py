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
        self.is_player_white = True
        self.is_white_turn = True

        self.board = self._initBoard()
        self._possible_moves: dict[Point.__repr__, list] = self._getPossibleMoves()
        # self.is_player_turn = True

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

    def getIsWhiteTurn(self) -> bool:
        return self.is_white_turn

    def getBoard(self) -> list[list[Figure, ...], ...]:
        return self.board

    def handleKillMove(self, move: Move):
        # killed_checker_point = move.end_point - move.start_point
        # killed_checker_point.x //= 2
        # killed_checker_point.y //= 2
        # killed_checker_point += move.start_point

        self.board[move.killed_point.x][move.killed_point.y].is_checker = False
        self.board[move.start_point.x][move.start_point.y].is_checker = False
        self.board[move.end_point.x][move.end_point.y].is_checker = True
        self.board[move.end_point.x][move.end_point.y].is_white = self.board[move.start_point.x][
            move.start_point.y].is_white

    def handleSingleMove(self, move: Move):
        self.board[move.end_point.x][move.end_point.y].is_checker = self.board[move.start_point.x][
            move.start_point.y].is_checker
        self.board[move.end_point.x][move.end_point.y].is_white = self.board[move.start_point.x][
            move.start_point.y].is_white
        self.board[move.start_point.x][move.start_point.y].is_checker = False

    def handleMove(self, move: Move):
        if not self.board[move.start_point.x][move.start_point.y].is_queen:
            if move.is_kill:
                self.handleKillMove(move)

                self._possible_moves = self._getPossibleMoves()

                if move.end_point.__repr__() in self._possible_moves:

                    necessary_moves = []
                    for possible_move in self._possible_moves[move.end_point.__repr__()]:
                        if possible_move.is_kill:
                            necessary_moves.append(possible_move)
                    print(necessary_moves)
                    if len(necessary_moves) == 0:
                        self.is_white_turn = not self.is_white_turn

            else:
                self.handleSingleMove(move)
                self.is_white_turn = not self.is_white_turn

                self._possible_moves = self._getPossibleMoves()

        else:
            raise Exception("Queen")

        self._possible_moves = self._getPossibleMoves()

    def __isMoveWithinBoundaries(self, move: Move) -> bool:
        if 0 <= move.end_point.x < self.board_width \
                and 0 <= move.end_point.y < self.board_width:
            return True

        return False

    def _isCheckerMovePossible(self, start_point: Point, direction: Point) -> tuple[bool, Move | None]:
        move = Move(start_point, start_point + direction)
        if self.__isMoveWithinBoundaries(move):
            if self.board[move.end_point.x][move.end_point.y].is_checker:
                if self.board[move.start_point.x][move.start_point.y].is_white \
                        != self.board[move.end_point.x][move.end_point.y].is_white:
                    move = Move(move.start_point, move.end_point + direction)
                    if self.__isMoveWithinBoundaries(move):
                        if not self.board[move.end_point.x][move.end_point.y].is_checker:
                            move.is_kill = True
                            move.killed_point = move.start_point + direction
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

    def _isQueenMovePossible(self, start_point: Point, direction: Point) -> tuple[bool, Move | None]:
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

    def _getQueenPossibleMoves(self, start_point: Point) -> list[Move]:
        for direction in self.queen_directions:
            for i in range(1, self.board_width):
                direction_new = direction * i
                is_possible, move = self._isQueenMovePossible(start_point, direction_new)
                if is_possible:
                    possible_moves.append(move)
                else:
                    break

        return

    def _getCheckerPossibleMoves(self, start_point: Point) -> list[Move]:
        unnecessary_moves = []
        necessary_moves = []  # killing moves

        for i in [-1, 1]:
            for j in [-1, 1]:
                is_possible, move = self._isCheckerMovePossible(start_point, Point(i, j))
                if is_possible:
                    match move.is_kill:
                        case True:
                            necessary_moves.append(move)
                        case False:
                            unnecessary_moves.append(move)

        if len(necessary_moves) == 0:
            return unnecessary_moves
        else:
            return necessary_moves


    def _getPossibleMovesForPoint(self, start_point: Point) -> list[Move]:
        if self.board[start_point.x][start_point.y].is_queen:
            return self._getQueenPossibleMoves(start_point)
        else:
            return self._getCheckerPossibleMoves(start_point)

    def _getPossibleMoves(self) -> dict[Point.__repr__, list]: # str is the __repr__ of Point
        unnecessary_moves = {}
        necessary_moves = {}
        for i in range(self.board_width):
            for j in range(self.board_width):
                if self.is_white_turn == self.board[i][j].is_white and self.board[i][j].is_checker:
                    for possible_move in self._getPossibleMovesForPoint(Point(i, j)):
                        if possible_move.is_kill:
                            if possible_move.start_point.__repr__() in necessary_moves:
                                necessary_moves[possible_move.start_point.__repr__()].append(possible_move)
                            else:
                                necessary_moves[possible_move.start_point.__repr__()] = [possible_move]
                        else:
                            if possible_move.start_point.__repr__() in unnecessary_moves:
                                unnecessary_moves[possible_move.start_point.__repr__()].append(possible_move)
                            else:
                                unnecessary_moves[possible_move.start_point.__repr__()] = [possible_move]

        if len(necessary_moves) == 0:
            return unnecessary_moves
        else:
            return necessary_moves

    def getPossibleMoves(self, start_point: Point) -> list[Move]:
        if start_point.__repr__() in self._possible_moves:
            return self._possible_moves[start_point.__repr__()]
        return []


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