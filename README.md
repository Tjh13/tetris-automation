# High Score - Nav-Canada Challenge

---BEFORE USING OUR APP, PLEASE INSTALL PYGAME AND PYNUM ON YOUR COMPUTER---


#__ To play, Download and Run TetrisMain.py :) __#


Welcome to High Score, automation that supports without taking over. 

We the creators of High Score are taking on the NAV-Canada challenge, designing an automation system that helps a human player achieve the highest possible Tetris score. The automation has limitations that require the human to step in and make key decisions, ensuring the human remains meaningfully involved and accountable for the result.

High Score looks at the current board state, as well as the next piece to be dropped, and determines whether it can make any moves which will be flush with the 'ground.' If it finds more than one, it will pick the spot lowest on the board. After finding this ideal spot, it will automatically move the piece there, so you don't have to do the easy move. It will do this as long as it can determine an easy move; whenever it can't, the player has to step back in. To make sure the player gets ample time to think of their move, High Score will also warn the player when they have an upcoming move, as well as display how the board will look once they have to step back in, reducing the mental energy needed for the player to determine a good move. 

We started with an open source tetris file found right here on Github. We used the built-in grid and block representations, all 4 rotational iterations for all 7 types of blocks to scan the board for the best possible move. It checks whether placing a block is valid by determining every possible landing spot, whether the block will intersect with another, already placed block, and whether placing a block there will create an unfavourable position for the user (a hole that stops rows from being eliminated). We altered the UI so that it lets the user know when the automation is active and is able to find the best move for the user. 

All of our code is in Python, as this is what the open source tetris game was originally coded in. It contains both pygame and numpy. 
