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
        self.board = self.initBoard()
        self.is_player_turn = True
        self.is_player_first = True

    def initBoard(self) -> list[list[Figure, ...], ...]:
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


    def handleMove(self, move: Move):
        return self.getPossibleMoves(move.end_point)

    """def getPossibleMoves(self, point: Point) -> list[Move, ...]:
        possible_moves = []
        # так как Point это у нас коорды, надо тут переделать
        if any(x not in [0, self.board_width - 1] for x in point):  # проверка на граничный случай
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    if self.board[point.x + i][point.y + j].is_checker:
                        if self.board[point.x + i][point.y + j].is_white \
                                != self.board[point.x][point.y].is_white:
                            if (point.x + i + i <= self.board_width - 1 or point.x + i + i >= 0) \
                                    and (point.y + j + j >= 0 or point.y + j + j <= self.board_width - 1):
                                if self.board[point.x + i + i][point.y + j + j].is_checker:
                                    possible_moves.append(
                                        Move(Point(point.x, point.y), Point(point.x + i + i, point.y + j + j)))
                    else:
                        possible_moves.append(Move(Point(point.x, point.y), Point(point.x + i, point.y + j)))
        else:  # какой-то"""


    def getPossibleMoves(self, point: Point) -> list[Move, ...]:
        point = point + Point(1, 1)
        return [Move(point, point)]

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