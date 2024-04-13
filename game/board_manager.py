import numba
import numpy as np

# move is numpy array where two arrays stored:
# 1st array: [x, y] of start pos
# 2nd array: [x, y] of end pos

@numba.njit
def checkIfCoordsInBoundaries(x: int, y: int) -> bool:
    if 0 <= x < 8 and 0 <= y < 8:
        return True
    return False

@numba.njit
def _getAvailableMovesForQueen(board: np.array, x: int, y: int) -> tuple[bool, np.array]:
    ...
    necessary_moves = np.full((4, 2, 2), -1)
    necessary_moves_amount = 0
    unnecessary_moves = np.full((4, 2, 2), -1)
    unnecessary_moves_amount = 0

    if necessary_moves_amount > 0:
        return True, necessary_moves
    return False, unnecessary_moves

@numba.njit
def _getAvailableMovesForChecker(board: np.array, x: int, y: int) -> tuple[bool, np.array]:
    necessary_moves = np.full((4, 2, 2), -1)
    necessary_moves_amount = 0
    unnecessary_moves = np.full((4, 2, 2), -1)
    unnecessary_moves_amount = 0

    color = board[x, y][1]
    if not board[x, y][2]:
        for i in [-1, 1]:
            for j in [-1, 1]:
                is_in_boundaries = checkIfCoordsInBoundaries(x + i, y + j)
                is_checker = board[x + i, y + j][0]
                is_another_color = color != board[x + i, y + j][1]
                is_in_boundaries_next_cell = checkIfCoordsInBoundaries(x + 2 * i, y + 2 * j)

                if is_in_boundaries and is_checker and is_another_color and is_in_boundaries_next_cell:
                    if not board[x + 2 * i, y + 2 * j][0]:
                        necessary_moves[necessary_moves_amount][0] = x + 2 * i
                        necessary_moves[necessary_moves_amount][1] = y + 2 * j
                        necessary_moves_amount += 1
                elif not is_checker and j != -1:  # чекнуть на хуйню j != -1
                    unnecessary_moves[unnecessary_moves_amount][0] = x + 2 * i
                    unnecessary_moves[unnecessary_moves_amount][1] = y + 2 * j
                    unnecessary_moves_amount += 1

    if necessary_moves_amount > 0:
        return True, necessary_moves
    return False, unnecessary_moves

@numba.njit
def getAvailableMovesForCheckerOrQueen(board: np.array, x: int, y: int) -> np.array:
    if not board[x, y][0]:
        raise Exception("Expected board cell is not a checker")

    if board[x, y][2]:
        are_necessary, moves = _getAvailableMovesForQueen(board, x, y)
    else:
        are_necessary, moves = _getAvailableMovesForChecker(board, x, y)

    return moves

def getAllAvailableMoves(board: np.array) -> np.array:
    moves = []
    for i in range(8):
        for j in range(i % 2 + 1, 8, 2):
            if board[i, j][0]:
                _moves = getAvailableMovesForCheckerOrQueen(board, i, j)
                # print(_moves)


if __name__ == "__main__":
    from game.main import SimpleGame
    import time
    sg = SimpleGame()
    s = time.time()
    for i in range(10 ** 5):
        m = getAllAvailableMoves(sg.getBoard())
    print(time.time() - s)
    # necessary_moves = np.full((4, 2, 2), -1)
    # print(necessary_moves)
