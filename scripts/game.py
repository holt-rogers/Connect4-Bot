import pygame, sys
from pygame.locals import QUIT
from vector import Vector2
from random import randint
import time
import AI_v3 as AI

# random delay used to simulate human player for AI
pygame.init()
screenSize = Vector2(400, 300)
screen = pygame.display.set_mode((screenSize.x, screenSize.y))
pygame.display.set_caption('Connect 4')
bg = (69,69,69)


# create board
# each tile is a 30x30 sqaure
# board is 6x7, standard for connect 4

# stores the state of baord with a list of lists
# Yellow (-1),newMove(1,x,board) Red (1), None (0)
board = []

offset = Vector2((screenSize.x - 30*7)/2 ,75)
for c in range(7):
  column = []
  for r in range(6):
    column.append(0)
  board.append(column)

# load in sprites
tile = pygame.image.load("tile.png").convert_alpha()
cursor = pygame.image.load("cursor.png").convert_alpha()
y_piece = pygame.image.load("y_piece.png").convert_alpha()
r_piece = pygame.image.load("r_piece.png").convert_alpha()

font = pygame.font.Font('freesansbold.ttf', 16)


start = time.time()
console = 'Yellows Turn'
text = font.render(console, True, (0, 0, 0))
gameOn = True

# vars recorded for research project
first = None
winner = None
aiTime = 0
aiMoves = 0
playerTime = 0
playerMoves = 0
game = ""

def move(team,column):
  if column == None:
    return
  for i in range(5,-1,-1):
    if board[column][i] == 0:
      y = i
      board[column][y] = team 
      break

def drawBoard():
  # redraw board and pieces
  screen.fill(bg)
  for c in range(7):
    for r in range(6):
      screen.blit(tile, (c*30 + offset.x, r*30 + offset.y))
      if board[c][r] == -1:
        screen.blit(y_piece, (c*30 + offset.x, r*30 + offset.y))
      elif board[c][r] == 1:
        screen.blit(r_piece, (c*30 + offset.x, r*30 + offset.y))

  textRect = text.get_rect()
  textRect.center = (screenSize.x // 2, 50)
  screen.blit(text, textRect)

def turn(x):
  global start, text, aiTime, aiMoves, playerTime, playerMoves, gameOn, winner, game
  if x != None:
    game += str(x)
    move(-1,x)
    taken = time.time() - start
    playerTime += taken
    playerMoves += 1
    print('Y:',game[-1] + ",",format(taken,'.4f'),'s')
    

    if AI.won(-1,board):
      console = "Yellow Won"
      gameOn = False
      winner = "player"
    elif AI.won(1,board):
      console = "Red Won"
      winner = "AI"
      gameOn = False
    elif AI.draw(board):
      console = "Draw"
      winner = "Draw"
      gameOn = False
    else:
      console = "Red's Turn"

    # update board
    text = font.render(console, True, (0, 0, 0))
    drawBoard()
    pygame.display.update()

  if not gameOn:
    return

  # have ai go
  start = time.time()
  x = AI.decideMove(board)
  game += str(x)
  move(1,x)
  taken = time.time() - start
  aiTime += taken
  aiMoves += 1
  print('R:',game[-1] + ",",format(taken,'.4f'),'s')

  if AI.won(-1,board):
    console = "Yellow Won"
    winner = "player"
    gameOn = False
  elif AI.won(1,board):
    console = "Red Won"
    winner = "AI"
    gameOn = False
  elif AI.draw(board):
    console = "Draw"
    winner = "Draw"
    gameOn = False
  else:
    console = "Yellow's Turn"
  text = font.render(console, True, (0, 0, 0))

  start = time.time()

# have a %50 percent chance AI goes first

first = 'player'
aiTurn = False
if randint(0,1) == 0:
  aiTurn = True


if aiTurn == True:
  turn(None)
  first = 'AI'
else:
  game += "-"

# main game loop
while True:
  drawBoard()
  # get mouse position
  draw = False
  x = pygame.mouse.get_pos()[0]
  y = pygame.mouse.get_pos()[1]
  if y < 250 and (x > offset.x and x < 7*30 + offset.x):
    column = int((x - offset.x - (x - offset.x)%30) / 30)
    for i in range(5,-1,-1):
      if board[column][i] == 0 and gameOn:
        y = i * 30 + offset.y
        draw = True
        break
    x = x - x% 30 + offset.x % 30
    if draw and (x - offset.x)/30 < 7:
      screen.blit(cursor, (x,y))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      if not gameOn:
        if winner == "Draw":
          print("The game was a draw.")
        else:
          print(f"The {winner} won the game.")
        print(f"The {first} went first.")
        avg = round(playerTime / playerMoves,4)
        print(f"The player placed {playerMoves} pieces with an average of {avg} spm.")
        avg = round(aiTime / aiMoves,4)
        print(f"The AI placed {aiMoves} pieces with an average of {avg} spm.")
        print("Game Record:",game)
      else:
        print('Game terminated')
      pygame.quit()
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP and draw:
      # prints the time both the AI and player took to make a move
      turn(int((x - offset.x)/30))

    # allow for number key input
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_1 and board[0].count(0) != 0:
        turn(0)
      elif event.key == pygame.K_2 and board[1].count(0) != 0:
        turn(1)
      elif event.key == pygame.K_3 and board[2].count(0) != 0:
        turn(2)
      elif event.key == pygame.K_4 and board[3].count(0) != 0:
        turn(3)
      elif event.key == pygame.K_5 and board[4].count(0) != 0:
        turn(4)
      elif event.key == pygame.K_6 and board[5].count(0) != 0:
        turn(5)
      elif event.key == pygame.K_7 and board[6].count(0) != 0:
        turn(6)

  pygame.display.update()