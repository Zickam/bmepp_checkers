import copy

import game.main
from game.classes import Move
from game.main import GameState


def next_positions(_game: game.main.Game) -> list[game.main.Game]:
    pass


def heuristic_function(_game: game.main.Game) -> float | int:
    fig_dif = _game.getWFiguresDifference()
    center_dif = 0
    board = _game.getBoard()
    for i in [3, 4]:
        for j in range(2, 6):
            figure = board[i][j]
            if figure.is_checker:
                if figure.is_white:
                    center_dif += 1
                else:
                    center_dif -= 1
    queens_dif = 0
    for row in board:
        for figure in row:
            if figure.is_checker and figure.is_queen:
                if figure.is_white:
                    queens_dif += 1
                else:
                    queens_dif -= 1
    if _game.getGameState() == GameState.b_win:
        return float('-inf')
    elif _game.getGameState() == GameState.w_win:
        return float('+inf')
    elif _game.getGameState() == GameState.draw:
        return 0
    return queens_dif*10 + fig_dif*2 + center_dif


class MinMaxClass:
    def minmax(self, current_game: game.main.Game,
               depth: int,
               finding_max: bool,
               alpha: float = float('-inf'),
               beta: float = float('+inf'),
               moves_stack=(),
               branches_stack: tuple[tuple[int, int], ...] = ()) -> [int, [Move]]:

        if depth == 0:
            print('\r', end='')
            for branch_num, branch_count in branches_stack:
                print(f'{branch_num+1}/{branch_count} ', end='')

        if depth == 0:
            return heuristic_function(current_game), moves_stack

        record = float('-inf') if finding_max else float('+inf')
        all_moves = current_game.getAllMoves()
        best_moves = copy.deepcopy(moves_stack)
        if len(all_moves) == 0:
            if finding_max:
                return float('-inf'), best_moves
            else:
                return float('+inf'), best_moves
        # if there is only one possible move - make it immediately
        if len(all_moves) == 1 and moves_stack == ():
            return None, [all_moves[0]]

        for i in range(len(all_moves)):
            move = all_moves[i]
            child = game.main.copy_game(current_game)
            color_before_move = child.isWhiteTurn()
            child.handleMove(move)
            if child.isWhiteTurn() != color_before_move:
                new_finding_max = not finding_max
                new_depth = depth - 1
            else:
                new_finding_max = finding_max
                new_depth = depth
            new_b_stack = branches_stack + ((i, len(all_moves)),)
            value, moves = self.minmax(child, new_depth, new_finding_max, alpha, beta,
                                       tuple(list(moves_stack)+[move]), new_b_stack)
            if (finding_max and (value > record or value == float('-inf'))) or \
                    (not finding_max and (value < record or value == float('+inf'))):
                record = value
                best_moves = moves
            if finding_max:
                alpha = max(alpha, record)
            else:
                beta = min(beta, record)
            if beta <= alpha:
                break
        return record, best_moves
