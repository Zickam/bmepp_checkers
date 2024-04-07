import copy
import pickle

from game.classes import Move, move_to_notation, notation_to_move
from game.main import GameState, Game, copy_game, Figure

#cash_file_name = 'cash_10depth_1st_move.pickle'
cash_file_name = 'cash.pickle'

def next_positions(_game: Game) -> list[Game]:
    pass


def heuristic_function(_game: Game) -> float | int:
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
    return queens_dif*15 + fig_dif*3 + center_dif


def game_board_to_str(board: list[list[Figure]]) -> str:
    s = ''
    for i, row in enumerate(board):
        for j, figure in enumerate(row):
            if figure.is_checker:
                fig_s = f'{i}{j}{int(figure.is_white)}{int(figure.is_queen)}'
                s += fig_s
    return s


class MinMaxClass:
    def __init__(self):
        self.cash: dict[int: dict[tuple[bool]: tuple[float, str]]] = {}
        self.load_cash()

    def save_cash(self):
        file = open(cash_file_name, 'wb')
        pickle.dump(self.cash, file)
        file.close()

    def load_cash(self):
        try:
            file = open(cash_file_name, 'rb')
        except FileNotFoundError:
            self.save_cash()
            file = open(cash_file_name, 'rb')
        self.cash = pickle.load(file)

    def add_to_cash(self, _game: Game, depth: int, record: int | float, move: Move):
        board = game_board_to_str(_game.getBoard())
        if depth in self.cash.keys():
            n_depth_dict = self.cash[depth]
        else:
            n_depth_dict = {}
            self.cash[depth] = n_depth_dict
        str_move = move_to_notation(move)
        n_depth_dict[board] = (record, str_move)

    def check_cash(self, _game: Game, depth: int):
        if depth not in self.cash.keys():
            return
        n_depth_dict = self.cash[depth]
        board = game_board_to_str(_game.getBoard())
        if board in n_depth_dict:
            record, notation = n_depth_dict[board]
            move = notation_to_move(notation)
            return record, move

    def minmax(self, current_game: Game,
               depth: int,
               finding_max: bool,
               alpha: float = float('-inf'),
               beta: float = float('+inf'),
               moves_stack=(),
               branches_stack: tuple[tuple[int, int], ...] = (),
               start_depth=float('inf')) -> [int, [Move]]:
        if start_depth == float('inf'):
            start_depth = depth

        if depth == 3:
            print('\r', end='')
            for branch_num, branch_count in branches_stack:
                print(f'{branch_num+1}/{branch_count} ', end='')

        if depth == 0:
            return heuristic_function(current_game), moves_stack

        if depth not in [0, 1, 2]:
            update_cash_after_calculations = True
        else:
            update_cash_after_calculations = False

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
            print('(only one possible move, no calculations)')
            return None, [all_moves[0]]

        from_cash = self.check_cash(current_game, depth)
        if from_cash is not None:
            value, move = from_cash
            moves = tuple(list(moves_stack) + [move])
            print(f'get from cash: depth:{depth}, {move_to_notation(move)}')
            return value, moves

        for i in range(len(all_moves)):
            move = all_moves[i]
            child = copy_game(current_game)
            color_before_move = child.isWhiteTurn()
            child.handleMove(move)
            if child.isWhiteTurn() != color_before_move:
                new_finding_max = not finding_max
                new_depth = depth - 1
            else:
                new_finding_max = finding_max
                new_depth = depth
            new_b_stack = branches_stack + ((i, len(all_moves)),)

            # next step of recursion or use cash
            value, moves = self.minmax(child, new_depth, new_finding_max, alpha, beta,
                                           tuple(list(moves_stack)+[move]), new_b_stack, start_depth)

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

        if update_cash_after_calculations:
            move = best_moves[start_depth-depth]
            self.add_to_cash(current_game, depth, record, move)
            #self.save_cash()
        return record, best_moves
