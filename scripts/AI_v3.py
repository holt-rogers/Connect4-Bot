from random import choice
from AI_v2 import calc
import copy
''' 
Version 3 of connect 4 AI
uses minimax algorithm and board scores from v2 to find the best move
'''

# the board is always taken as a list of the columns, meaning board[x][y] returns the position using x and y cordinates
# board[0][0] is the top left

def decideMove(board, depth = 4):
  '''
  finds the best move on any given connect 4 board
  depth is the amount of moves it looks ahead
  gets exponentially more resource consuming as depth is increased
  '''

  # simple checks (naive moves)

  # see if we can win in one move
  for x in range(7):
    if not canPlay(board,x):
      continue

    if won(1,newMove(1,x,board)):
      return x

  # see if we need to block
  for x in range(7):
    if not canPlay(board,x):
      continue

    if won(-1,newMove(-1,x,board)):
      return x

  return minimax(board,depth,True)[1]


def newMove(team, x, board):
  '''returns a new baord if move x was made by given team on given board'''

  # check if move is possible
  if not canPlay(board,x):
    raise Exception("Move AI is trying to play is not possible.")

  # find first empty spot in column
  b = copy.deepcopy(board)
  for i in range(5,-1,-1):
    if b[x][i] == 0:
      b[x][i] = team 
      return b

def canPlay(board,x):
  '''checks if we can even play in this column'''
  if board[x].count(0) != 0:
    return True
  return False

def draw(board):
  '''checks if any given connect four board is a draw'''
  for column in board:
    if column.count(0) != 0:
      return False
  return True

def minimax(board, depth, maxPlayer):
  # check if the game has ended or we have run out of set resources (depth)
  if won(1,board):
    return (float('inf'), None)
  elif won(-1,board):
    return (float('-inf'), None)
  elif draw(board):
    return (-300,None)
  elif depth == 0:
    return (calc(board), None)

  # if we are trying to maximize our own score
  if maxPlayer:
    # find the board with the highest score from the tree
    score = float('-inf')
    bestMove = 0
    for x in range(7):
      if not canPlay(board,x):
        continue
      move = newMove(1,x,board)
      potential = minimax(move,depth - 1,False)[0]
      if potential > score:
        score = potential
        bestMove = x
    return (score, bestMove)
  # if we are trying to predict the oppponents move
  elif not maxPlayer:
    # find the board with the highest score for the opponent
    score = float('inf')
    bestMove = 0
    for x in range(7):
      if not canPlay(board,x):
        continue

      move = newMove(-1,x,board)
      potential = minimax(move,depth - 1,True)[0]
      if potential < score:
        score = potential
        bestMove = x
    return (score, None)

def won(team,board):
  '''checks if a team won the game, 1 being the AI, -1 being the player'''

  # check columns 
  for c in board:
    for i in range(4):
      if sum(c[i:4+i]) == team*4:
        return True

  # check rows
  for y in range(6):
    row = list(board[x][y] for x in range(7))
    for i in range(4):
      if sum(row[i:4+i]) == team*4:
        return True

  # check diagnols
  diagnols = []

  # get every diagnol as a line
  for i in range(3):
    # lines that start on the left side
    line = list(board[j][i+j] for j in range(6-i))
    diagnols.append(line)
    line = list(board[j][5-i-j] for j in range(6-i))
    diagnols.append(line)

    # lines that start on the right side
    line = list(board[6-j][i+j] for j in range(6-i))
    diagnols.append(line)
    line = list(board[6-j][5-i-j] for j in range(6-i))
    diagnols.append(line)

  # check each diagnol to see if it has four in a row in it
  for line in diagnols:
    for i in range(len(line)-3):
      if sum(line[i:4+i]) == team*4:
        return True
  return False
