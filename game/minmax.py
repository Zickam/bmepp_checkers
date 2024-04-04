import game.main
import game.classes


def next_positions(game: game.main.Game) -> list[game.main.Game]:
    pass


def heuristic_function(game: game.main.Game) -> float | int:
    fig_dif = game.getWFiguresDifference()
    center_dif = 0
    board = game.getBoard()
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
    return queens_dif*10 + fig_dif*2 + center_dif


def minmax(current_game: game.main.Game,
           depth: int,
           finding_max: bool,
           alpha: float = float('-inf'),
           beta: float = float('+inf'),
           moves_stack=(),
           branches_stack: tuple[tuple[int, int]] = ()) -> [int, [game.classes.Move]]:
    if depth == 0:
        print('\r', end='')
        for branch_num, branch_count in branches_stack:
            print(f'{branch_num+1}/{branch_count} ', end='')
    if depth == 0:
        return heuristic_function(current_game), moves_stack

    def finding(_max: bool, alpha: float, beta: float):
        record = float('-inf') if _max else float('+inf')
        best_moves = moves_stack[:]
        all_moves = current_game.getAllMoves()
        for i in range(len(all_moves)):
            move = all_moves[i]
            child = game.main.copy_game(current_game)
            color_before_move = child.isWhiteTurn()
            child.handleMove(move)
            if child.isWhiteTurn() != color_before_move:
                new_finding_max = not _max
            else:
                new_finding_max = _max
            new_b_stack = branches_stack + ((i, len(all_moves)),)
            value, moves = minmax(child, depth-1, new_finding_max, 0, 0,  tuple(list(moves_stack)+[move]), new_b_stack)
            if (_max and value > record) or (not _max and value < record):
                record = value
                best_moves = moves
            if _max:
                alpha = max(alpha, record)
            else:
                beta = min(beta, record)
            if beta <= alpha:
                break
        return record, best_moves

    if finding_max:
        return finding(True, alpha, beta)
    else:
        return finding(False, alpha, beta)
