from random import choice
import copy
''' 
Version 1 of connect 4 AI
simulates a large amount of completely random games after any possible move. Then returns the one with the highest win ratio
cannot consistently beat a human, even at depth 200
'''

# the board is always taken as a list of the columns, meaning board[x][y] returns the position using x and y cordinates
# board[0][0] is the top left

def decideMove(board, depth = 200):
  '''finds the best move on any given connect 4 board'''
  '''depth is the amount of games it simualtes for any possible move'''

  # simple checks

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

  # get a list of the odds of winning with each move
  data = list(simulate(x,board,depth) for x in range(7))
  print(data)

  # get the highest percentage, and return that move
  best = data.index(max(data))
  return best

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


def simulate(x,board,depth):
  '''returns the win percentage of any given move on any given game state, depth being the number of simulated games'''
  if not canPlay(board,x):
    return -100

  wins = 0
  for i in range(depth):
    b = newMove(1,x,board)
    while True:
      if draw(b):
        wins += 0.5
        break
      elif won(1,b):
        wins += 1
        break
      elif won(-1,b):
        break

      b = newMove(1,randMove(b),b)
      if draw(b):
        wins += 0.5
        break
      elif won(1,b):
        wins += 1
        break
      elif won(-1,b):
        break

      b = newMove(-1,randMove(b),b)
  return wins / depth

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