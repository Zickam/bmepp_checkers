import copy
import pickle

from game.constants import TOP_N_AMOUNT, DEPTH_TO_CHECK
from game.classes import Move, move_to_notation, notation_to_move, notations_to_move, moves_to_notation
from game.main import SimpleGame, game_board_to_str
from game.board_manager import getAllAvailableMoves, handle_move_pr
from game.heuristic_functions import heuristic_function

cache_file_name = 'cache.pickle'
n_cache_file_name = f'cache{TOP_N_AMOUNT}.pickle'


'''def heuristic_function(_game: SimpleGame) -> float | int:
    fig_dif = heuristic_functions.getWBFiguresDifference(_game.getBoard())
    center_dif = 0
    board = _game.getBoard()
    for i in [3, 4]:
        for j in range(2, 6):
            figure = board[i][j]
            if figure[0]:
                if figure[1]:
                    center_dif += 1
                else:
                    center_dif -= 1
    queens_dif = 0
    for row in board:
        for figure in row:
            if figure[0] and figure[2]:
                if figure[1]:
                    queens_dif += 1
                else:
                    queens_dif -= 1
    fig_dif = 0
    for row in board:
        for figure in row:
            if figure[0]:
                if figure[1]:
                    fig_dif += 1
                else:
                    fig_dif -= 1
    if _game.getGameState() == GameState.b_win:
        return float('-inf')
    elif _game.getGameState() == GameState.w_win:
        return float('+inf')
    elif _game.getGameState() == GameState.draw:
        return 0
    return queens_dif*100 + fig_dif*9 + center_dif * 5'''


def potential_function(_game: SimpleGame) -> float | int:
    center_dif = 0
    board = _game.getBoard()
    for i in [3, 4]:
        for j in range(2, 6):
            figure = board[i][j]
            if figure[0]:
                if figure[1]:
                    center_dif += 1
                else:
                    center_dif -= 1
    return center_dif


class MinMaxClass:
    def __init__(self, need_to_print=True):
        # cache = dict(tuple(depth, board, finding_max): tuple(value, tuple(move))
        self.cache: dict[tuple[int, str, bool]: tuple[float, tuple[str]]] = {}
        # n_cache = dict(tuple(depth, board, finding_max): tuple(tuple(value, tuple(move))))
        self.n_cache:  dict[tuple[int, str, bool]: tuple[tuple[float, tuple[str]]]] = {}
        self.load_cash()
        # dict(depth: count)
        self.alphabeta_pruning_count = {}
        # dict(depth: count)
        self.using_cache_count = {}
        self.depth_zero = 0
        self.brute_forced_depth = [0, 1, 2]
        self.need_to_print = need_to_print

    def save_cash(self):
        file = open(cache_file_name, 'wb')
        pickle.dump(self.cache, file)
        file.close()
        file2 = open(n_cache_file_name, 'wb')
        pickle.dump(self.n_cache, file2)
        file.close()

    def load_cash(self):
        try:
            file = open(cache_file_name, 'rb')
            file2 = open(n_cache_file_name, 'rb')
        except FileNotFoundError:
            self.save_cash()
            file = open(cache_file_name, 'rb')
            file2 = open(n_cache_file_name, 'rb')
        self.cache = pickle.load(file)
        self.n_cache = pickle.load(file2)

    def add_to_cash(self, _game: SimpleGame,
                    depth: int,
                    record: int | float,
                    moves: list[tuple[tuple[int, int], ...]],
                    finding_max: bool):
        board = game_board_to_str(_game.getBoard())
        str_move = moves_to_notation(moves)
        key = depth, board, finding_max
        value = record, str_move
        self.cache[key] = value

    def add_to_n_cache(self, _game: SimpleGame,
                       depth: int,
                       variants_tuple: list[list[float, list[tuple[tuple[int, int], ...]]]],
                       finding_max: bool):
        board = game_board_to_str(_game.getBoard())
        key = depth, board, finding_max
        value_in_dict = []
        for variant in variants_tuple:
            value, moves = variant
            moves = list(moves)
            for i in range(len(moves)):
                move = moves[i]
                moves[i] = move_to_notation(move)
            value_in_dict.append([value, moves])
        self.n_cache[key] = value_in_dict

    def check_cache(self, _game: SimpleGame,
                    depth: int,
                    finding_max: bool) -> None | tuple[float, list[tuple[tuple[int, int], ...]]]:
        board = game_board_to_str(_game.getBoard())
        for i in range(depth, DEPTH_TO_CHECK):
            key = i, board, finding_max
            if key in self.cache:
                value, moves = self.cache.get(key)
                moves = notations_to_move(moves)
                return value, moves

    def check_n_cache(self, _game: SimpleGame,
                      depth: int,
                      finding_max: bool) -> None | list[list[float, list[tuple[tuple[int, int], ...]]]]:
        board = game_board_to_str(_game.getBoard())
        for i in range(depth, DEPTH_TO_CHECK):
            key = i, board, finding_max
            if key in self.n_cache:

                variants_list = copy.deepcopy(self.n_cache.get(key))
                variants_to_return = []
                for variant in variants_list:
                    value, moves = variant
                    for j in range(len(moves)):
                        move = moves[j]
                        moves[j] = notation_to_move(move)
                    variants_to_return.append([value, moves])
                return variants_to_return

    def minmax(self, current_game: SimpleGame,
               depth: int,
               finding_max: bool,
               weights,
               alpha: float = float('-inf'),
               beta: float = float('+inf'),
               branches_stack: tuple[tuple[int, int], ...] = (),
               moves_stack=(),
               start_depth=float('inf'),
               moves_without_change_side=0) -> [int, [Move]]:
        if start_depth == float('inf'):
            start_depth = depth

        if depth == 3 and self.need_to_print:
            print('\r', end='')
            for branch_num, branch_count in branches_stack:
                print(f'{branch_num+1}/{branch_count} ', end='')

        if depth == 0:
            self.depth_zero += 1
            return heuristic_function(current_game, weights), moves_stack

        record = float('-inf') if finding_max else float('+inf')

        are_necessary, all_moves = getAllAvailableMoves(current_game.getBoard(), current_game.isWhiteTurn(), current_game.getPreviousTurnWhite(), current_game.getLastMove())

        best_moves = copy.deepcopy(moves_stack)

        if len(all_moves) == 0:
            if finding_max:
                return float('-inf'), best_moves
            else:
                return float('+inf'), best_moves

        # if there is only one possible move - make it immediately
        if len(all_moves) == 1 and moves_stack == ():
            return None, [all_moves[0]]

        # if depth not in self.brute_forced_depth:
        #     from_cash = self.check_cache(current_game, depth, finding_max)
        #
        #     if from_cash is not None:
        #         value, moves = from_cash
        #         moves = tuple(list(moves_stack) + list(moves))
        #         add_to_counter(self.using_cache_count, depth)
        #         return value, moves

        children = []

        empty_game = SimpleGame()
        for i in range(len(all_moves)):
            move = all_moves[i]

            color_before_move = current_game.isWhiteTurn()

            args = current_game.toArgs()
            new_args = handle_move_pr(*args, move)
            empty_game.fromArgs(*new_args)
            child = empty_game

            if child.isWhiteTurn() != color_before_move:
                new_finding_max = not finding_max
                new_depth = depth - 1
                new_moves_without_change_side = moves_without_change_side
            else:
                new_moves_without_change_side = moves_without_change_side + 1
                new_finding_max = finding_max
                new_depth = depth
            args = [new_depth,
                    new_finding_max,
                    weights,
                    tuple(list(moves_stack)+[move]),
                    start_depth,
                    new_moves_without_change_side]
            children.append([copy.deepcopy(child), args])

        if depth not in self.brute_forced_depth:
            children.sort(key=lambda x: potential_function(x[0]), reverse=finding_max)

        for i in range(len(children)):
            child, args = children[i]
            new_b_stack = branches_stack + ((i, len(all_moves)),)
            value, moves = self.minmax(child, args[0], args[1], args[2], alpha, beta, new_b_stack, *args[3:])
            if (finding_max and (value > record or value == float('-inf'))) or \
                    (not finding_max and (value < record or value == float('+inf'))):
                record = value
                best_moves = moves
            if finding_max:
                alpha = max(alpha, record)
            else:
                beta = min(beta, record)
            if beta <= alpha:
                add_to_counter(self.alphabeta_pruning_count, depth)
                break

        # if depth not in self.brute_forced_depth:
        #     try:
        #         moves = best_moves[start_depth - depth + moves_without_change_side:]
        #     except IndexError:
        #         print(len(best_moves), start_depth, depth, moves_without_change_side)
        #         raise IndexError
        #     self.add_to_cash(current_game, depth, record, moves, finding_max)
        return record, best_moves

    def top_n_minmax(self, current_game: SimpleGame,
                     depth: int,
                     finding_max: bool,
                     weights,
                     alpha: float = float('-inf'),
                     beta: float = float('+inf'),
                     branches_stack: tuple[tuple[int, int], ...] = (),
                     moves_stack=(),
                     start_depth=float('inf'),
                     moves_without_change_side=0,
                     top_position_amount=TOP_N_AMOUNT,
                     customer_color_white: None | bool = None) -> list[(int, [Move], str), ...]:
        if start_depth == float('inf'):
            start_depth = depth
        if customer_color_white is None:
            customer_color_white = current_game.isWhiteTurn()

        if depth == 3 and self.need_to_print:
            print('\r', end='')
            for branch_num, branch_count in branches_stack:
                print(f'{branch_num+1}/{branch_count} ', end='')

        if depth == 0:
            self.depth_zero += 1
            return [[heuristic_function(current_game, weights), moves_stack, game_board_to_str(current_game.getBoard())]]

        are_necessary, all_moves = getAllAvailableMoves(current_game.getBoard(), current_game.isWhiteTurn(), current_game.getPreviousTurnWhite(), current_game.getLastMove())
        best_moves = copy.deepcopy(moves_stack)

        if len(all_moves) == 0:
            if finding_max:
                return [[float('-inf'), best_moves, game_board_to_str(current_game.getBoard())]]
            else:
                return [[float('+inf'), best_moves, game_board_to_str(current_game.getBoard())]]

        # if there is only one possible move - make it immediately
        if len(all_moves) == 1 and moves_stack == ():
            return [(None, [all_moves[0]], game_board_to_str(current_game.getBoard()))]

        # if depth not in self.brute_forced_depth:
        #     from_cache = self.check_n_cache(current_game, depth, finding_max)
        #
        #     if from_cache is not None:
        #         variants_list = from_cache
        #         variants_to_return = []
        #         for variant in variants_list:
        #             value, moves = variant
        #             moves: tuple[tuple[tuple[int, int], ...]]
        #             moves = tuple(list(moves_stack) + list(moves))
        #             variants_to_return.append([value, moves, game_board_to_str(current_game.getBoard())])
        #         add_to_counter(self.using_cache_count, depth)
        #         return variants_to_return

        children = []

        empty_game = SimpleGame()
        for i in range(len(all_moves)):
            move = all_moves[i]

            color_before_move = current_game.isWhiteTurn()

            args = current_game.toArgs()
            new_args = handle_move_pr(*args, move)
            empty_game.fromArgs(*new_args)
            child = empty_game

            if child.isWhiteTurn() != color_before_move:
                new_finding_max = not finding_max
                new_depth = depth - 1
                new_moves_without_change_side = moves_without_change_side
            else:
                new_moves_without_change_side = moves_without_change_side + 1
                new_finding_max = finding_max
                new_depth = depth
            args = [new_depth,
                    new_finding_max,
                    weights,
                    tuple(list(moves_stack)+[move]),
                    start_depth,
                    new_moves_without_change_side,
                    top_position_amount,
                    customer_color_white]
            children.append([copy.deepcopy(child), args])

        if depth not in self.brute_forced_depth:
            children.sort(key=lambda x: potential_function(x[0]), reverse=finding_max)

        variants_list: list[list[tuple[int, [tuple[tuple[int, int], ...]], str]]] = []
        for i in range(len(children)):
            child, args = children[i]
            new_b_stack = branches_stack + ((i, len(all_moves)),)
            value_moves_lst = self.top_n_minmax(child, args[0], args[1], args[2], alpha, beta, new_b_stack, *args[3:])

            if finding_max == customer_color_white:
                variants_list += value_moves_lst
                variants_list.sort(key=lambda x: x[0], reverse=finding_max)  # sort by value
                variants_list = variants_list[:top_position_amount]

            else:
                if len(variants_list) == 0:
                    variants_list = value_moves_lst
                    continue

                if finding_max:
                    worst_case_value_in_memory = variants_list[0][0]
                    worst_case_value_from_next_depth = value_moves_lst[0][0]
                    if worst_case_value_from_next_depth > worst_case_value_in_memory:
                        variants_list = value_moves_lst
                if not finding_max:
                    worst_case_value_in_memory = variants_list[-1][0]
                    worst_case_value_from_next_depth = value_moves_lst[-1][0]
                    if worst_case_value_from_next_depth < worst_case_value_in_memory:
                        variants_list = value_moves_lst

            if finding_max:
                all_values = [variant[0] for variant in variants_list]
                alpha = max(alpha, min(all_values))  # Magic, idk, should be checked
            else:
                all_values = [variant[0] for variant in variants_list]
                beta = min(beta, max(all_values))  # Magic, idk, should be checked
            if beta <= alpha:
                add_to_counter(self.alphabeta_pruning_count, depth)
                break

        # if depth not in self.brute_forced_depth:
        #     variants_to_cache = []
        #     for variant in variants_list:
        #         value, moves, board = variant
        #         try:
        #             moves = moves[(start_depth - depth + moves_without_change_side):]
        #         except IndexError:
        #             print(len(best_moves), start_depth, depth, moves_without_change_side)
        #             raise IndexError
        #         variants_to_cache.append([value, moves])
        #     self.add_to_n_cache(current_game, depth, variants_to_cache, finding_max)
        return variants_list


def add_to_counter(dct: dict, key):
    if key not in dct:
        dct[key] = 1
    else:
        dct[key] += 1
