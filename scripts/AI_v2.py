from random import choice
import copy
''' 
Version 2 of connect 4 AI
assigns score to blocks of pieces, and chooses the move tha maximizes its own score
'''

# the board is always taken as a list of the columns, meaning board[x][y] returns the position using x and y cordinates
# board[0][0] is the top left

def decideMove(board):
  '''finds the best move on any given connect 4 board'''
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

  # find the move with the best solution
  move = 0
  bestScore = -1000000
  for x in range(7):
    if not canPlay(board,x):
      continue

    score = calc(newMove(1,x,board))
    print(score, end=', ')
    if score > bestScore:
      bestScore = score
      move = x
  print(bestScore)
  return move



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

def randMove(board):
  '''returns a random move that is possible'''
  moves = list(range(7))

  x = choice(moves)
  moves.pop(x)
  while not canPlay(board,x):
    x = choice(moves)
    moves.pop(moves.index(x))

  return x

def draw(board):
  '''checks if any given connect four board is a draw'''
  for column in board:
    if column.count(0) != 0:
      return False
  return True

def window(row):
  # returns the score of a group of four (window)

  # if AI has 4,3, or 2 in a row
  if sum(row) == 4:
    return 100
  elif sum(row) == 3:
    return 30
  elif sum(row) == 2 and row.count(-1) == 0:
    return 10

  # if opponent has 3 of 2 in a row
  if sum(row) == -3:
    return -80
  elif sum(row) == -2 and row.count(1) == 0:
    return -20

  return 0

def calc(board):
  # returns the score of any given board
  score = 0

  # add slight score for having pieces in midal columns
  score += board[3].count(1) * 2
  score += board[4].count(1)
  score += board[2].count(1)
  # check columns 
  for c in board:
    for i in range(4):
      block = c[i:4+i]
      score += window(block)

  # check rows
  for y in range(6):
    row = list(board[x][y] for x in range(7))
    for i in range(4):
      block = row[i:4+i]
      score += window(block)

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
      block = line[i:4+i]
      score += window(block)

  return score

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