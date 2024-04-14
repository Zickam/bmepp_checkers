from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __sub__(self, point: Point) -> Point:
        return Point(self.x - point.x, self.y - point.y)

    def __add__(self, point: Point) -> Point:
        return Point(self.x + point.x, self.y + point.y)

    def __mul__(self, num: int) -> Point:
        return Point(self.x * num, self.y * num)

    # def __truediv__(self, divisor: int) -> Point:
    #     if self.x % divisor != 0 or self.y % divisor != 0:
    #         raise Exception(f"Incorrect divisor passed(divisor): ")
    #     return Point(self.x / other, self.y // divisor)

    def __eq__(self, point: Point) -> bool:
        return True if self.x == point.x and self.y == point.y else False

    def __str__(self) -> str:
        return f"Point: ({self.x}, {self.y})"


    def __hash__(self) -> int:
        return hash((self.x, self.y))



class Vec2:
    def __init__(self, x: float | int, y: float | int):
        self.x: float = x
        self.y: float = y

    def __sub__(self, vec: Vec2) -> Vec2:
        return Vec2(self.x - vec.x, self.y - vec.y)

    def __add__(self, vec: Vec2) -> Vec2:
        return Vec2(self.x + vec.x, self.y + vec.y)

    def __str__(self) -> str:
        return f"Vec2: ({self.x}, {self.y})"


class Move:
    def __init__(self, start_point: Point, end_point: Point, is_kill: bool = False, killed_point: Point | None = None):
        self.start_point: Point = start_point
        self.end_point: Point = end_point
        self.is_kill = is_kill
        self.killed_point = killed_point

    def __str__(self) -> str:
        return f"Move: ({self.start_point}, {self.end_point}) [is_kill: {self.is_kill}, killed_point: {self.killed_point}]"


def move_to_notation(_move: Move) -> str:
    alph = 'abcdefgh'
    x1, y1, x2, y2 = _move.start_point.x, _move.start_point.y, _move.end_point.x, _move.end_point.y
    y1 = alph[y1]
    y2 = alph[y2]
    x1 = 8 - x1
    x2 = 8 - x2
    return f"{y1}{x1}-{y2}{x2}"


def moves_to_notation(lst: list[Move]) -> list[str]:
    notations = []
    for move in lst:
        notations.append(move_to_notation(move))
    return notations


def notation_to_move(notation: str) -> Move:
    alph = 'abcdefgh'
    y1, x1, y2, x2 = notation[0], notation[1], notation[3], notation[4]
    y1 = alph.find(y1)
    y2 = alph.find(y2)
    x1 = 8 - int(x1)
    x2 = 8 - int(x2)
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    return Move(p1, p2)


def notations_to_move(notations: [str]) -> list[Move]:
    moves = []
    for move in notations:
        moves.append(notation_to_move(move))
    return moves

class Figure:
    def __init__(self, is_checker: bool = False, is_white: bool = True):
        self.is_checker: bool = is_checker
        self.is_white: bool = is_white
        self.is_queen: bool = False

    def __str__(self) -> str:
        return f"{self.__dict__}"

class Moves:
    def __init__(self, necessary_moves: list[Move], unnecessary_moves: list[Move] = list):
        self.necessary_moves = necessary_moves
        self.unnecessary_moves = unnecessary_moves


if __name__ == "__main__":
    point = Point(1, 2)
    print(point.__hash__())