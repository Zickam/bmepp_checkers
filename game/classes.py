from __future__ import annotations


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __sub__(self, point: Point) -> Point:
        self.x -= point.x
        self.y -= point.y
        return Point(self.x, self.y)

    def __add__(self, point: Point) -> Point:
        self.x += point.x
        self.y += point.y
        return Point(self.x, self.y)

    def __str__(self) -> str:
        return f"Point: ({self.x}, {self.y})"


class Vec2:
    def __init__(self, x: float | int, y: float | int):
        self.x: float = x
        self.y: float = y

    def __sub__(self, vec: Vec2) -> Vec2:
        self.x -= vec.x
        self.y -= vec.y
        return Vec2(self.x, self.y)

    def __add__(self, vec: Vec2) -> Vec2:
        self.x += vec.x
        self.y += vec.y
        return Vec2(self.x, self.y)

    def __str__(self) -> str:
        return f"Vec2: ({self.x}, {self.y})"


class Move:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point: Point = start_point
        self.end_point: Point = end_point


if __name__ == "__main__":
    vec = Vec2(10.2, 10.3)
    print(vec + Vec2(100, 200))