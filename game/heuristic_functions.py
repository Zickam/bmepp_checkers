from enum import Enum

import numba
import numpy as np

# !!!!DO NOT CHANGE THE ORDER OF HEURISTIC FUNCTIONS!!!
heuristic_funcs = np.array([
    True, # 0 checkers_amount
    True, # 1 queens amount
    True, # 2 safe checkers
    True, # 3 safe queens
    True, # 4 movable checkers
    True, # 5 movable queens
    True, # 6 distance to promotion line
    True, # 7 free cells on promotion line
    True, # 8 defenders amount
    True, # 9 attackers amount
    True, # 10 middle checkers
    True, # 11 middle queens
    True, # 12 checkers on main diagonal
    True, # 13 queens on main diagonal
    True, # 14 checkers on double diagonal
    True, # 15 queens on double diagonal
    True, # 16 alone checkers
    True, # 17 alone queens
    True, # 18 holes
])

@numba.njit
def calculateHeuristicValue(board: np.array, board_values: np.array, heuristic_funcs: np.array) -> int:
    value = 0

    # if heuristic_funcs[0]:
    #     value += board_values[0]
    # if heuristic_funcs[1]:
    #     value += board_values[1]
    # if heuristic_funcs[6]:
    #     value += board_values[2]

    if heuristic_funcs[2]:
        value += getSafeCheckersAmount(board)
    if heuristic_funcs[3]:
        value += getSafeQueensAmount(board)
    if heuristic_funcs[7]:
        value += getFreeCellsOnPromotionLine(board)

    for i in range(0, len(board)):
        for j in range((i + 1) % 2, len(board[i]), 2):
            if heuristic_funcs[0]:
                value += getCountPeshka(board, i, j)
            if heuristic_funcs[1]:
                value += getCountKing(board, i, j)
            if heuristic_funcs[4]:
                value += getMovableCheckers(board, i, j)
            if heuristic_funcs[5]:
                value += getMovableQueens(board, i, j)
            if heuristic_funcs[6]:
                value += getDistanceToPromotionLine(board, i, j)
            if heuristic_funcs[8]:
                value += getDefendersAmount(board, i, j)
            if heuristic_funcs[9]:
                value += getAttackersAmount(board, i, j)
            if heuristic_funcs[10]:
                value += getMiddleCheckers(board, i, j)
            if heuristic_funcs[11]:
                value += getMiddleQueens(board, i, j)
            if heuristic_funcs[12]:
                value += getCheckersAmountOnMainDiagonal(board, i)
            if heuristic_funcs[13]:
                value += getQueensAmountOnMainDiagonal(board, i)
            if heuristic_funcs[14]:
                value += getCheckersAmountOnDoubleDiagonal(board, i)
            if heuristic_funcs[15]:
                value += getQueensAmountOnDoubleDiagonal(board, i)
            if heuristic_funcs[16]:
                value += getAloneCheckers(board, i, j)
            if heuristic_funcs[17]:
                value += getAloneQueens(board, i, j)
            if heuristic_funcs[18]:
                value += getHoles(board, i, j)

    return value

@numba.njit
def getFreeCellsOnPromotionLine(board: np.array) -> int:
    w, b = 0, 0
    for i in range(1, len(board), 2):
        if not board[0, i][0]:
            w += 1
    for i in range(0, len(board), 2):
        if not board[len(board) - 1, i][0]:
            b += 1

    w = 4 - w
    b = 4 - b

    return w - b

@numba.njit
def getWBFiguresDifference(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i, j][0]:
                match board[i, j][1]:
                    case True:
                        w += 1
                    case False:
                        b += 1

    return w - b

@numba.njit
def getCountPeshka(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if not board[i, j][2]:
                w += 1
        else:
            if not board[i, j][2]:
                b += 1
    return w - b

@numba.njit
def getCountKing(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if board[i, j][2]:
                w += 1
        else:
            if board[i, j][2]:
                b += 1
    return w - b

@numba.njit
def getSafeCheckersAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(1, len(board), 2):
        if board[0, i][0] and not board[0, i][2]:
            if board[0, i][1]:
                w += 1
            else:
                b += 1

    for i in range(2, len(board), 2):
        if board[i, len(board) - 1][0] and not board[i, len(board) - 1][2]:
            if board[i, len(board) - 1][1]:
                w += 1
            else:
                b += 1

    for i in range(0, len(board), 2):
        if board[len(board) - 1, i][0] and not board[len(board) - 1, i][2]:
            if board[len(board) - 1, i][1]:
                w += 1
            else:
                b += 1

    for i in range(1, len(board) - 2, 2):
        if board[i, 0][0] and not board[i, 0][2]:
            if board[i, 0][1]:
                w += 1
            else:
                b += 1

    return w - b

@numba.njit
def getSafeQueensAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(1, len(board), 2):
        if board[0, i][0] and board[0, i][2]:
            if board[0, i][1]:
                w += 1
            else:
                b += 1

    for i in range(2, len(board), 2):
        if board[i, len(board) - 1][0] and board[i, len(board) - 1][2]:
            if board[i, len(board) - 1][1]:
                w += 1
            else:
                b += 1

    for i in range(0, len(board), 2):
        if board[len(board) - 1, i][0] and board[len(board) - 1, i][2]:
            if board[len(board) - 1, i][1]:
                w += 1
            else:
                b += 1

    for i in range(1, len(board) - 2, 2):
        if board[i, 0][0] and board[i, 0][2]:
            if board[i, 0][1]:
                w += 1
            else:
                b += 1

    return w - b

@numba.njit
def getQueensAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        if i % 2 == 0:
            c = 1
        else:
            c = 0
        for j in range(c, len(board), 2):
            if board[i, j][0] and board[i, j][2]:
                if board[i, j][1]:
                    w += 1
                else:
                    b += 1

    return w - b

@numba.njit
def getDistanceToPromotionLine(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0] and not board[i, j][2]:
        if board[i, j][1]:
            w += i
        else:
            b += 7 - i
    return b - w

@numba.njit
def getAttackersAmount(board: np.array, i: int, j: int) -> int:
    w, b = 0, 0
    if board[i, j][0] and not board[i, j][2]:
        if board[i, j][1]:
            if 0 <= i <= 2:
                w += 1
        else:
            if 5 <= i <= 7:
                b += 1
    return w - b

@numba.njit
def getDefendersAmount(board: np.array, i: int, j: int) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if 0 <= i <= 1:
                b += 1
        else:
            if 6 <= i <= 7:
                w += 1
    return w - b

@numba.njit
def getCentrallyPositionedCheckersAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(2, len(board) - 2, 2):
        for j in range(2, len(board[i]) - 2, 2):
            if board[i, j][0] and not board[i, j][2]:
                if board[i, j][1]:
                    w += 1
                else:
                    b += 1

    return w - b

@numba.njit
def getCentrallyPositionedQueensAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(2, len(board) - 2, 2):
        for j in range(2, len(board[i]) - 2, 2):
            if board[i, j][0] and board[i, j][2]:
                if board[i, j][1]:
                    w += 1
                else:
                    b += 1

    return w - b

@numba.njit
def getCheckersAmountOnMainDiagonal(board: np.array, i) -> int:
    w, b = 0, 0
    if board[i, 7 - i][0] and not board[i, 7 - i][2]:
        if board[i, 7 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@numba.njit
def getQueensAmountOnMainDiagonal(board: np.array, i) -> int:
    w, b = 0, 0
    if board[i, 7 - i][0] and board[i, 7 - i][2]:
        if board[i, 7 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@numba.njit
def getCheckersAmountOnDoubleDiagonal(board: np.array, i) -> int:
    w, b = 0, 0
    if board[i, len(board) - 1 - i][0] and not board[i, len(board) - 1 - i][2]:
        if board[i, len(board) - 1 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@numba.njit
def getQueensAmountOnDoubleDiagonal(board: np.array, i: int) -> int:
    w, b = 0, 0
    if board[i, len(board) - 1 - i][0] and board[i, len(board) - 1 - i][2]:
        if board[i, len(board) - 1 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@numba.njit
def getMovableCheckers(
        board: np.array,
        i, j) -> int:  # Количество подвижных пешек (т.е. способных сделать ход, отличный от взятия)
    w, b = 0, 0
    if board[i, j][0] and not board[i, j, 2]:
        if board[i, j][1]:
            if (0 <= i - 1 and 0 <= j - 1 and not board[i - 1, j - 1][0])\
                    or (0 <= i - 1 and j + 1 <= 7 and not board[i - 1, j + 1][0]):
                w += 1
        else:
            if (i + 1 <= 7 and j + 1 <= 7 and not board[i + 1, j + 1][0])\
                    or (i + 1 <= 7 and 0 <= j - 1 and not board[i + 1, j - 1][0]):
                b += 1
    return w - b


@numba.njit
def getMovableQueens(
        board: np.array, i, j
) -> int:  # Количество подвижных пешек (т.е. способных сделать ход, отличный от взятия)
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if board[i, j][2]:
                if (not board[i + 1, j - 1][0] and (j < 8 or i < 8)) or (not board[i - 1, j - 1][0] and (j < 8)):
                    w += 1
        else:
            if board[i, j][2]:
                if (not board[i + 1, j + 1][0] and (j < 8 or i < 8)) or (not board[i - 1, j + 1][0] and (j < 8)):
                    b += 1

    return w - b


@numba.njit
def getMiddleCheckers(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if not board[i, j][2] and 5 >= i >= 2 and 5 >= j >= 2:
                w += 1
        else:
            if not board[i, j][2] and 5 >= i >= 2 and 5 >= j >= 2:
                b += 1
    return w - b


@numba.njit
def getMiddleQueens(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if board[i, j][2] and 5 >= i >= 2 and 5 >= j >= 2:
                w += 1
        else:
            if board[i, j][2] and 5 >= i >= 2 and 5 >= j >= 2:
                b += 1
    return w - b

@numba.njit
def getAloneCheckers(board: np.array, i, j) -> int: #k - слева сверху, l - справа сверху, n - слева снизу, m - справа снизу
    w, b = 0, 0
    k, l, n, m = 0, 0, 0, 0
    if board[i, j][0]:
        if not board[i, j][2]:
          if i == 0 or j == 0:
            k = 1
          if i == 0 or j == 7:
            l = 1
          if i == 7 or j == 0:
            n = 1
          if i == 7 or j == 7:
            m = 1
          if not k:
            k = not board[i-1, j-1][0]
          if not l:
            l = not board[i-1, j+1][0]
          if not n:
            n = not board[i+1, j-1][0]
          if not m:
            m = not board[i+1, j+1][0]
            if k and l and n and m:
              if board[i, j][1]:
                w += 1
              else:
                b += 1
    return w - b

@numba.njit
def getAloneQueens(board: np.array, i, j) -> int: #k - слева сверху, l - справа сверху, n - слева снизу, m - справа снизу
    w, b = 0, 0
    k, l, n, m = 0, 0, 0, 0
    if board[i, j][0]:
        if board[i, j][2]:
          if i == 0 or j == 0:
            k = 1
          if i == 0 or j == 7:
            l = 1
          if i == 7 or j == 0:
            n = 1
          if i == 7 or j == 7:
            m = 1
          if not k:
            k = not board[i-1, j-1][0]
          if not l:
            l = not board[i-1, j+1][0]
          if not n:
            n = not board[i+1, j-1][0]
          if not m:
            m = not board[i+1, j+1][0]
            if k and l and n and m:
              if board[i, j][1]:
                w += 1
              else:
                b += 1
    return w - b

@numba.njit
def getHoles(board: np.array, i, j):
  w, b = 0, 0
  k, l, n, m = 0, 0, 0, 0
  if not board[i, j][0]:
      if i == 0 or j == 0:
        k = 1
      if i == 0 or j == 7:
        l = 1
      if i == 7 or j == 0:
        n = 1
      if i == 7 or j == 7:
        m = 1
      if k + l + n + m > 1:
        return 0
      if not k:
        if board[i-1, j-1][0]:
          if board[i-1, j-1][1]:
            w += 1
          else:
            b += 1
      if not l:
        if board[i-1, j+1][0]:
          if board[i-1, j+1][1]:
            w += 1
          else:
            b +=1
      if not n:
        if board[i+1, j-1][0]:
          if board[i+1, j-1][1]:
            w += 1
          else:
            b += 1
      if not m:
        if board[i+1, j+1][0]:
          if board[i+1, j+1][1]:
            w += 1
          else:
            b += 1
  if w > 2:
    return 1
  elif b > 2:
    return -1
  else:
    return 0

if __name__ == "__main__":
    import time
    board_width = 8
    board = np.array([[np.array([False, False, False]) for i in range(board_width)] for j in range(board_width)])

    for i in range(3):
        for j in range(board_width):
            is_on_white_1 = i % 2 == 1 and j % 2 == 0
            is_on_white_2 = i % 2 == 0 and j % 2 == 1

            if is_on_white_1 or is_on_white_2:
                board[i][j] = np.array([1, 0, 0])

            is_on_black_1 = (board_width - i - 1) % 2 == 1 and (board_width - j - 1) % 2 == 0
            is_on_black_2 = (board_width - i - 1) % 2 == 0 and (board_width - j - 1) % 2 == 1

            if is_on_black_1 or is_on_black_2:
                board[board_width - i - 1][board_width - j - 1] = np.array([1, 1, 0])

    s = time.time()
    for i in range(10 ** 5):
        value = calculateHeuristicValue(board, [0, 0, 0], heuristic_funcs)
    e = time.time()
    print(e - s)
    exit()
    for i in board:
        for j in i:
            if j[0]:
                if j[1]:
                    print("W", end="\t")
                else:
                    print("B", end="\t")
            else:
                print("[]", end="\t")

        print()
    print(value)

