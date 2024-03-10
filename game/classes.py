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

    def __str__(self) -> str:
        return f"Point: ({self.x}, {self.y})"


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
        return f"Move: ({self.start_point}, {self.end_point})"


if __name__ == "__main__":
    vec = Point(10.2, 10.3)
    print(vec + Point(-1, -1))