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


def minmax(current_game: game.main.Game, depth: int, finding_max: bool, moves_stack=()) -> [int, [game.classes.Move]]:
    if depth == 0:
        return heuristic_function(current_game), moves_stack

    if finding_max:
        _max = float('-inf')
        best_moves = moves_stack[:]
        for move in current_game.getAllMoves():
            #print([str(x) for x in moves_stack], '|', move)
            child = game.main.copy_game(current_game)
            child.handleMove(move)
            value, moves = minmax(child, depth-1, False, tuple(list(moves_stack)+[move]))
            if value > _max:
                _max = value
                best_moves = moves
        return _max, best_moves

    else:
        _min = float('+inf')
        best_moves = moves_stack[:]
        for move in current_game.getAllMoves():
            #print([str(x) for x in moves_stack], '|', move)
            child = game.main.copy_game(current_game)
            child.handleMove(move)
            value, moves = minmax(child, depth-1, True, tuple(list(moves_stack)+[move]))
            if value < _min:
                _min = value
                best_moves = moves
        return _min, best_moves
