import numba
import numpy
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
def _getAvailableMovesForQueen(board: np.array, x: int,
                               y: int) -> tuple[bool, np.array]:
    ...
    necessary_moves = np.full((13, 2), -1)
    necessary_moves_amount = 0
    unnecessary_moves = np.full((13, 2), -1)
    unnecessary_moves_amount = 0

    if necessary_moves_amount > 0:
        return True, necessary_moves
    return False, unnecessary_moves


@numba.njit
def _handleCheckerKillMove(board: np.array, move: np.array) -> np.array:
    x = move[0, 0]
    y = move[0, 1]
    kill_x = move[1, 0]
    kill_y = move[1, 1]

    for i in range(3):
        board[kill_x][kill_y][i] = board[x][y][i]
        board[x + (kill_x - x) // 2][y + (kill_y - y) // 2][i] = False
        board[x][y][i] = False


@numba.njit
def _handleCheckerMovingMove(board: np.array, x: int, y: int) -> np.array:
    return


def _handleQueenKillMove():
    ...


@numba.njit
def handleMove(board: np.array, move: np.array) -> np.array:
    if board[move[0, 0], move[0, 1]][2]:
        _handleQueenKillMove()
    else:
        if abs(move[0, 0] - move[1, 0]) > 1:
            _handleCheckerKillMove(board, move)
        else:
            _handleCheckerMovingMove(board, move)


@numba.njit
def _getAvailableMovesForChecker(board: np.array, is_white_turn: bool, x: int,
                                 y: int) -> tuple[bool, np.array]:
    necessary_moves = np.full((4, 2), -1)
    necessary_moves_amount = 0
    unnecessary_moves = np.full((4, 2), -1)
    unnecessary_moves_amount = 0

    color = board[x, y][1]
    for i in (-1, 1):
        for j in (-1, 1):
            is_in_boundaries = checkIfCoordsInBoundaries(x + i, y + j)
            if not is_in_boundaries:
                continue

            is_checker = board[x + i, y + j][0]
            is_another_color = color != board[x + i, y + j][1]
            is_in_boundaries_next_cell = checkIfCoordsInBoundaries(x + 2 * i, y + 2 * j)

            if is_checker and is_another_color and is_in_boundaries_next_cell:
                if not board[x + 2 * i, y + 2 * j][0]:
                    necessary_moves[necessary_moves_amount][0] = x + 2 * i
                    necessary_moves[necessary_moves_amount][1] = y + 2 * j
                    necessary_moves_amount += 1
            elif not is_checker:  # чекнуть на хуйню j != -1
                if is_white_turn and i == 1:
                    continue
                if not is_white_turn and i == -1:
                    continue

                unnecessary_moves[unnecessary_moves_amount][0] = x + i
                unnecessary_moves[unnecessary_moves_amount][1] = y + j
                unnecessary_moves_amount += 1

    if necessary_moves_amount > 0:
        return True, necessary_moves
    return False, unnecessary_moves


@numba.njit
def getAvailableMovesForCheckerOrQueen(board: np.array, is_white_turn: bool, x: int,
                                       y: int) -> tuple[bool, np.array]:
    if not board[x, y][0]:
        raise Exception("Expected board cell is not a checker")

    if board[x, y][2]:
        are_necessary, moves = _getAvailableMovesForQueen(board, x, y)

    else:
        are_necessary, moves = _getAvailableMovesForChecker(board, is_white_turn, x, y)

    return are_necessary, moves


@numba.njit
def getAllAvailableMoves(board: np.array, is_white_turn: bool) -> np.array:
    unnecessary_moves = np.full((50, 2, 2), -1)
    unnecessary_moves_amount = 0
    necessary_moves = np.full((50, 2, 2), -1)
    necessary_moves_amount = 0

    are_necessary_found = False

    for i in range(8):
        for j in range(i % 2 + 1, 8, 2):
            if board[i, j][0] and board[i, j][1] == is_white_turn:
                if board[i, j][2]:  # пришло 13 ходов ибо королева
                    are_necessary, _moves = getAvailableMovesForCheckerOrQueen(
                        board, is_white_turn, i, j)
                else:  # пришло 4 хода ибо пешка
                    are_necessary, _moves = getAvailableMovesForCheckerOrQueen(
                        board, is_white_turn, i, j)

                if are_necessary:
                    are_necessary_found = True
                    for move in _moves:
                        if move[0] == -1:
                            break

                        necessary_moves[necessary_moves_amount][0][0] = i
                        necessary_moves[necessary_moves_amount][0][1] = j

                        necessary_moves[necessary_moves_amount][1][0] = move[0]
                        necessary_moves[necessary_moves_amount][1][1] = move[1]

                        necessary_moves_amount += 1

                elif not are_necessary_found:
                    for move in _moves:
                        if move[0] == -1:
                            break

                        unnecessary_moves[unnecessary_moves_amount][0][0] = i
                        unnecessary_moves[unnecessary_moves_amount][0][1] = j

                        unnecessary_moves[unnecessary_moves_amount][1][0] = move[0]
                        unnecessary_moves[unnecessary_moves_amount][1][1] = move[1]

                        unnecessary_moves_amount += 1

    if are_necessary_found:
        available_moves = np.full((necessary_moves_amount, 2, 2), -1)
        c = 0
        for move in necessary_moves:
            available_moves[c][0][0] = move[0][0]
            available_moves[c][0][1] = move[0][1]
            available_moves[c][1][0] = move[1][0]
            available_moves[c][1][1] = move[1][1]

            c += 1

    else:
        available_moves = np.full((unnecessary_moves_amount, 2, 2), -1)
        c = 0
        for move in unnecessary_moves:
            available_moves[c][0][0] = move[0][0]
            available_moves[c][0][1] = move[0][1]
            available_moves[c][1][0] = move[1][0]
            available_moves[c][1][1] = move[1][1]

            c += 1

    return available_moves


def transformNumpyMovesToList(moves: np.array) -> list:
    _moves = []
    for move in moves:
        if move[0] == -1:
            return _moves
        _moves.append([move[0], move[1]])
    return _moves


if __name__ == "__main__":
    from game.main import SimpleGame
    import time

    sg = SimpleGame()
    sg.getBoard()[4, 5][0] = True
    sg.getBoard()[4, 5][1] = False

    # move = np.array([[2, 1], [4, 3]])
    # _handleCheckerKillMove(sg.getBoard(), move)


    print("moves", getAllAvailableMoves(sg.getBoard(), True))
    # for i in sg.getBoard():
    #     for j in i:
    #         if j[0]:
    #             if j[1]:
    #                 print("W", end="\t")
    #             else:
    #                 print("B", end="\t")
    #         else:
    #             print("[]", end="\t")
    #
    #     print()

    # s = time.time()
    # a = 0
    # for i in range(10 ** 5):
    #     m = getAllAvailableMoves(sg.getBoard(), True)
    #     a += 1
    # print(time.time() - s)
    # necessary_moves = np.full((4, 2, 2), -1)
    # print(necessary_moves)
