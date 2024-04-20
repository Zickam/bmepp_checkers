from enum import Enum

import numpy as np

class DefaultHeuristicValues(Enum):
    get_wb_fig_diff = True


@staticmethod
def calculateHeuristicValue(board: np.array, board_values: np.array) -> int:
    value = 0

    # for board_value in board_values:
    #     value += board_value

    value += getAmountOnPromotionLine(board)

    for i in range(0, len(board), 2):
        if i % 2 == 0:
            c = 1
        else:
            c = 0
        for j in range(c, len(board[i]), 2):
            if get_wb_fig_diff:
                value += getWBFiguresDifference(board)
                value += getMovableCheckers(board, i, j)
                value += getMovableQueens(board, i, j)
                value += getMiddleCheckers(board, i, j)
                value += getMiddleQueens(board, i, j)
                value += getQueensAmountOnMainDiagonal(board, i)
                value += getCheckersAmountOnMainDiagonal(board, i)

    return value

@staticmethod
def getAmountOnPromotionLine(board: np.array) -> int:
    w, b = 0, 0
    for i in range(1, len(board), 2):
        is_checker_and_queen = board[0, i][0] * board[0, i][2]
        w += board[0, i][1] * is_checker_and_queen
        b += (not board[0, i][1]) * is_checker_and_queen
    for i in range(0, len(board), 2):
        if board[len(board) - 1, i][0] and board[len(board) - 1, i][2]:
            if board[len(board) - 1, i][1]:
                w += 1
            else:
                b += 1

    w = 4 - w
    b = 4 - b

    return w - b

@staticmethod
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

@staticmethod
def getCountPeshka(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i, j][0]:
                if board[i, j][1]:
                    if not board[i, j][2]:
                        w += 1
                else:
                    if not board[i, j][2]:
                        b += 1
    return w - b

@staticmethod
def getCountKing(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i, j][0]:
                if board[i, j][1]:
                    if board[i, j][2]:
                        w += 1
                else:
                    if board[i, j][2]:
                        b += 1
    return w - b

@staticmethod
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

@staticmethod
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

@staticmethod
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

@staticmethod
def getDistanceToPromotionLine(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        if i % 2 == 0:
            c = 1
        else:
            c = 0
        for j in range(c, len(board), 2):
            if board[i, j][0] and not board[i, j][2]:
                if board[i, j][1]:
                    w += i
                else:
                    b += 7 - i
    return b - w

@staticmethod
def getAttackersAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i, j][0] and not board[i, j][2]:
                if board[i, j][1]:
                    if 0 <= i <= 2:
                        w += 1
                else:
                    if 5 <= i <= 7:
                        b += 1
    return w - b

@staticmethod
def getDefendersAmount(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i, j][0]:
                if board[i, j][1]:
                    if 0 <= i <= 1:
                        b += 1
                else:
                    if 6 <= i <= 7:
                        w += 1
    return w - b

@staticmethod
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

@staticmethod
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

@staticmethod
def getCheckersAmountOnMainDiagonal(board: np.array, i) -> int:
    w, b = 0, 0
    if board[i, 7 - i][0] and not board[i, 7 - i][2]:
        if board[i, 7 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@staticmethod
def getQueensAmountOnMainDiagonal(board: np.array, i) -> int:
    w, b = 0, 0
    if board[i, 7 - i][0] and board[i, 7 - i][2]:
        if board[i, 7 - i][1]:
            w += 1
        else:
            b += 1

    return w - b

@staticmethod
def getCheckersAmountOnDoubleDiagonal(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        if board[i,
        len(board) - 1 - i][0] and not board[i, len(board) - 1 - i][2]:
            if board[i, len(board) - 1 - i][1]:
                w += 1
            else:
                b += 1

    return w - b

@staticmethod
def getQueensAmountOnDoubleDiagonal(board: np.array) -> int:
    w, b = 0, 0
    for i in range(len(board)):
        if board[i, len(board) - 1 - i][0] and board[i, len(board) - 1 - i][2]:
            if board[i, len(board) - 1 - i][1]:
                w += 1
            else:
                b += 1

    return w - b

@staticmethod
def getMovableCheckers(
        board: np.array,
        i, j) -> int:  # Количество подвижных пешек (т.е. способных сделать ход, отличный от взятия)
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if not board[i, j][2]:
                if (not board[i + 1, j - 1][0] and (j < 8 or i < 8)) or (not board[i - 1, j - 1][0] and (j < 8)):
                    w += 1
        else:
            if not board[i, j][2]:
                if (not board[i + 1, j + 1][0] and (j < 8 or i < 8)) or (not board[i - 1, j + 1][0] and (j < 8)):
                    b += 1

    return w - b


@staticmethod
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


@staticmethod
def getMiddleChekers(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if not board[i, j][2] and i <= 5 and i >= 2 and j <= 5 and j >= 2:
                w += 1
        else:
            if not board[i, j][2] and i <= 5 and i >= 2 and j <= 5 and j >= 2:
                b += 1
    return w - b


@staticmethod
def getMiddleQueens(board: np.array, i, j) -> int:
    w, b = 0, 0
    if board[i, j][0]:
        if board[i, j][1]:
            if board[i, j][2] and i <= 5 and i >= 2 and j <= 5 and j >= 2:
                w += 1
        else:
            if board[i, j][2] and i <= 5 and i >= 2 and j <= 5 and j >= 2:
                b += 1
    return w - b

@staticmethod
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

@staticmethod
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
@staticmethod
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