# Connect4-Bot

PREFACE: This code was made as a highschool project and is very poorly written. Do not replicate any of the coding practices in this repo. 

A Connect-4 bot made in python.

## Running the Program

To run the program, run the `game.py` file. This file recieves input and gets the algorithms moves from the other files. 

## AI Iterations

You can change which version of the AI is ran by changing line 7 in the `game.py` file to import which version you wish to test. 

All versions check for blocking a three in a row or creating a 4 in a row with one move before doing any other calculations. 

### `AI_v1.py`

This version simulates 200 random games for each move it can make. All moves after the bots first move are completely random. The bot then chooses the move with the highest win ratio.

Not bad, but cannot consistently beat even an unexperienced player. May be an effective approach for simplier games. 

### `AI_v2.py`

Assigns positive values to blocks of pieces and negative scores for blocks of enemy pieces. Chooses the move that maximizes its own score. The scoring algorithm in this program is referenced by all future iterations. 

### `AI_v3.py`

Looks at all possible combinations 4 moves into the future or until the game is over. Assumes the opposing player will pick the best move and then makes its own move that will have the best result 4 moves from now. 

Uses the scoring algorithm from `AI_v2.py` to determine the best end position. 

### `AI_v4.py`

Similar to `AI_v3.py` but with optimizations. Terminates game paths where it is obvious the path is ineffective. Can now look 7 moves ahead. 

