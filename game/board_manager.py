# import numba
import numpy as np
from game.main import SimpleGame


# move is numpy array where two arrays stored:
# 1st array: [x, y] of start pos
# 2nd array: [x, y] of end pos


# @numba.njit
def checkIfCoordsInBoundaries(x: int, y: int) -> bool:
    if 0 <= x < 8 and 0 <= y < 8:
        return True
    return False


# @numba.njit
def _getAvailableMovesForQueen(board: np.array, is_white_turn: bool, x: int,
                               y: int) -> tuple[bool, np.array]:
    necessary_moves = np.full((13, 2), -1)
    necessary_moves_amount = 0
    unnecessary_moves = np.full((13, 2), -1)
    unnecessary_moves_amount = 0

    for _x in (1, -1):
        for _y in (1, -1):
            tmp_possible_moves = np.full((7, 2), -1)
            tmp_possible_moves_amount = 0
            obstacle_pos = (-1, -1)
            has_finished = False

            for i in range(1, 9):
                offset = _x * i, _y * i
                tmp_coords = (x + offset[0], y + offset[1])

                if checkIfCoordsInBoundaries(tmp_coords[0], tmp_coords[1]) and not has_finished:
                    if board[tmp_coords[0], tmp_coords[1]][0]:  # obstacle
                        if board[tmp_coords[0], tmp_coords[1]][1] == board[x, y][1]:
                            obstacle_pos = -2, -2
                            break

                        obstacle_pos = tmp_coords
                        coords_behind_obstacle = (tmp_coords[0] + _x, tmp_coords[1] + _y)
                        coords_within_boundaries = checkIfCoordsInBoundaries(coords_behind_obstacle[0],
                                                                             coords_behind_obstacle[1])
                        if coords_within_boundaries and not board[coords_behind_obstacle[0], coords_behind_obstacle[1]][
                            0]:  # its empty behind the obstacle
                            if board[tmp_coords[0], tmp_coords[1]][1] != is_white_turn:
                                for j in range(0, 6):
                                    new_tmp_coords = (coords_behind_obstacle[0] + _x * j, coords_behind_obstacle[1] + _y * j)
                                    if checkIfCoordsInBoundaries(new_tmp_coords[0], new_tmp_coords[1]) and not \
                                            board[new_tmp_coords[0], new_tmp_coords[1]][0]:
                                        necessary_moves[necessary_moves_amount][0] = new_tmp_coords[0]
                                        necessary_moves[necessary_moves_amount][1] = new_tmp_coords[1]
                                        necessary_moves_amount += 1
                                    else:
                                        has_finished = True
                                        break
                        else:
                            break

                    elif obstacle_pos[0] == -1: # so no obstacle found yet
                        tmp_possible_moves[tmp_possible_moves_amount][0] = tmp_coords[0]
                        tmp_possible_moves[tmp_possible_moves_amount][1] = tmp_coords[1]
                        tmp_possible_moves_amount += 1
                else:
                    obstacle_pos = -2, -2


            if obstacle_pos[0] != -1:
                for i in range(tmp_possible_moves_amount):
                    if tmp_possible_moves[i][0] == -1:
                        break
                    if tmp_possible_moves[i][0] == obstacle_pos[0] and tmp_possible_moves[i][1] == obstacle_pos[1]:
                        break
                    unnecessary_moves[unnecessary_moves_amount][0] = tmp_possible_moves[i][0]
                    unnecessary_moves[unnecessary_moves_amount][1] = tmp_possible_moves[i][1]
                    unnecessary_moves_amount += 1

    if necessary_moves_amount > 0:
        return True, necessary_moves
    return False, unnecessary_moves


# @numba.njit
def _handleQueenContinousMove(board: np.array, is_white_turn: bool, move: np.array) -> bool:
    are_necessary, next_available_moves = getAllAvailableMoves(board, is_white_turn)
    if are_necessary:
        # for _move in next_available_moves:
        #     if _move[0][0] == move[0][0] and _move[0][1] == move[0][1]:
        #         return True
        return True
    return False


# @numba.njit
def _handleQueenMovingMove(board: np.array, move: np.array) -> np.array:
    start, end = move[0], move[1]
    for i in range(3):
        board[end[0], end[1]][i] = board[start[0], start[1]][i]
        board[start[0], start[1]][i] = False

    return board


# @numba.njit
def _isQueenKillMove(board: np.array, is_white_turn: bool, move: np.array) -> bool:  # проверить
    start, end = move[0], move[1]
    vec2, vec1 = (end[1] - start[1]) // abs(end[1] - start[1]), (end[0] - start[0]) // abs(end[0] - start[0])
    for i in range(1, abs(end[0] - start[0])):
        if board[start[0] + i * vec1, start[1] + i * vec2][0]:
            for j in range(3):
                board[start[0] + i * vec1, start[1] + i * vec2][j] = False
                board[end[0], end[1]][j] = board[start[0], start[1]][j]
                board[start[0], start[1]][j] = False

            return True

    return False


# @numba.njit
def _handleCheckerKillMove(board: np.array, is_white_turn: bool, board_values: np.array, move: np.array) -> tuple[bool, np.array]:
    x = move[0, 0]
    y = move[0, 1]
    kill_x = move[1, 0]
    kill_y = move[1, 1]

    for i in range(3):
        board[kill_x, kill_y, i] = board[x, y, i]
        board[x + (kill_x - x) // 2, y + (kill_y - y) // 2, i] = False
        board[x, y, i] = False

    board_values_ind = 1 if is_white_turn else 0
    board_values[board_values_ind] = board_values[board_values_ind] - 1
    return board_values


# @numba.njit
def _handleCheckerMovingMove(board: np.array, move: np.array) -> np.array:
    start, end = move[0], move[1]
    for i in range(3):
        board[end[0], end[1]][i] = board[start[0], start[1]][i]
        board[start[0], start[1]][i] = False
    return board


# @numba.njit
def _handleCheckerContinousMove(board: np.array, is_white_turn: bool, board_values: np.array,
                                move: np.array) -> np.array:
    are_necessary, all_available_moves_for_checkers = getAllAvailableMoves(board, is_white_turn)
    # are_necessary, available_moves = _getAvailableMovesForChecker(board, is_white_turn, move[1, 0], move[1, 1])
    if not are_necessary:
        return False, board_values
    return True, board_values

# @numba.njit
def _isCheckerMoveKilling(move: np.array) -> bool:
    if abs(move[0, 0] - move[1, 0]) > 1:
        return True
    return False


# @numba.njit
def _handleQueenTransformation(board: np.array, is_white_turn: bool, board_values: np.array, move: np.array) -> tuple[
    np.array, bool, np.array]:
    need_x_for_transformation = 0 if is_white_turn else 7

    if move[1][0] == need_x_for_transformation:
        board[move[1, 0], move[1, 1]][2] = True
        board_values[2] += is_white_turn
        return True, board, board_values

    return False, board, board_values


# @numba.njit
def handleMove(board: np.array, is_white_turn: bool, board_values: np.array, move: np.array) -> tuple[np.array, bool, np.array]:
    if board[move[0, 0], move[0, 1]][2]:
        is_kill_move = _isQueenKillMove(board, is_white_turn, move)
        if is_kill_move:
            is_continuous = _handleQueenContinousMove(board, is_white_turn, move)
            if not is_continuous:
              is_white_turn = not is_white_turn
        else:
            _handleQueenMovingMove(board, move)
            is_white_turn = not is_white_turn

    else:
        if abs(move[0, 0] - move[1, 0]) > 1: # kill move
            board_values = _handleCheckerKillMove(board, is_white_turn, board_values, move)
            has_transformed, board, board_values = _handleQueenTransformation(board, is_white_turn, board_values, move)
            if has_transformed:
                is_continuous = _handleQueenContinousMove(board, is_white_turn, move)
            else:
                is_continuous, board_values = _handleCheckerContinousMove(board, is_white_turn, board_values, move)
            if not is_continuous:
                is_white_turn = not is_white_turn

        else: # moving move
            _handleCheckerMovingMove(board, move)
            has_transformed, board, board_values = _handleQueenTransformation(board, is_white_turn, board_values, move)

            is_white_turn = not is_white_turn


    return board, is_white_turn, board_values


def handle_move_pr(board: np.array, is_white_turn: bool, board_values: np.array, move: tuple) -> np.array:
    move = np.array(move)
    return handleMove(board, is_white_turn, board_values, move)


# @numba.njit
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


# @numba.njit
def getAvailableMovesForCheckerOrQueen(board: np.array, is_white_turn: bool, x: int,
                                       y: int) -> tuple[bool, np.array]:
    if not board[x, y][0]:
        raise Exception("Expected board cell is not a checker")

    if board[x, y][2]:
        are_necessary, moves = _getAvailableMovesForQueen(board, is_white_turn, x, y)

    else:
        are_necessary, moves = _getAvailableMovesForChecker(board, is_white_turn, x, y)

    return are_necessary, moves


# @numba.njit
def getAllAvailableMoves(board: np.array, is_white_turn: bool) -> np.array:
    unnecessary_moves = np.full((50, 2, 2), -1)
    unnecessary_moves_amount = 0
    necessary_moves = np.full((50, 2, 2), -1)
    necessary_moves_amount = 0

    are_necessary_found = False

    for i in range(8):
        for j in range((i + 1) % 2, 8, 2):
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
        for i in range(necessary_moves_amount):
            available_moves[c, 0, 0] = necessary_moves[i, 0, 0]
            available_moves[c, 0, 1] = necessary_moves[i, 0, 1]
            available_moves[c, 1, 0] = necessary_moves[i, 1, 0]
            available_moves[c, 1, 1] = necessary_moves[i, 1, 1]

            c += 1

    else:
        available_moves = np.full((unnecessary_moves_amount, 2, 2), -1)
        c = 0
        for i in range(unnecessary_moves_amount):
            available_moves[c, 0, 0] = unnecessary_moves[i, 0, 0]
            available_moves[c, 0, 1] = unnecessary_moves[i, 0, 1]
            available_moves[c, 1, 0] = unnecessary_moves[i, 1, 0]
            available_moves[c, 1, 1] = unnecessary_moves[i, 1, 1]

            c += 1

    return are_necessary_found, available_moves


def transformNumpyMovesToList(moves: np.array) -> list:
    _moves = []
    for move in moves:
        if move[0] == -1:
            return _moves
        _moves.append([move[0], move[1]])
    return _moves


def possibleMovesForPoint(game: SimpleGame, point: list[int]) -> list[list[list[int]]]:
    board = game.getBoard()
    is_white_turn = game.isWhiteTurn()
    x, y = point
    are_necessary, all_moves = getAllAvailableMoves(board, is_white_turn)
    point_moves = []
    for move in all_moves:
        start = move[0]
        x1, y1 = start
        if x == x1 and y == y1:
            point_moves.append(move)
    return point_moves

# 0 - ongoing, 1 - white win, 2 - black win
# @numba.njit
def handleWin(board: np.array, is_white_turn: bool) -> int:
    current_side_has_moves = False
    _, all_moves = getAllAvailableMoves(board, is_white_turn)
    for move in all_moves:
        row = board[move[0, 0]]
        checker = row[move[0, 1]]
        color = checker[1]
        if is_white_turn and color:
            current_side_has_moves = True
        elif not is_white_turn and not color:
            current_side_has_moves = True

    if not current_side_has_moves:
        if is_white_turn:
            game_state = 2
        else:
            game_state = 1
    else:
        game_state = 0
        
    return game_state


if __name__ == "__main__":
    from game.main import SimpleGame

    # import time

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
