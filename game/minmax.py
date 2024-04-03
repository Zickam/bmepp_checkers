import game.main
import game.classes


def next_positions(game: game.main.Game) -> list[game.main.Game]:
    pass


def heuristic_function(game: game.main.Game) -> float | int:
    return game.getWFiguresDifference()


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
