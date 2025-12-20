def find_perfect_moves(board, piece):
    
    #determine height of first filled tile in the leftmost column of a block
    #e.g.
    # []
    # []
    # [] []
    # would return 0  
    # []
    # [] []
    #    []
    # would return 1

    #print(board)
    #print(piece)
    firstLeftTile = 0
    for height in range(len(piece)-1, -1, -1):
        if(piece[height][0] == 1):
            # firstLeftTile found
            break
        else:
            # firstLeftTile not found, increment firstLeftTile
            firstLeftTile += 1

    #initialize variables
    validPosList = []

    #iterate through each column of the board
    for x in range(len(board[0])):
        valid = True
        
        #determine the distance between the top of the board and the end of
        #the filled tiles starting from the bottom of the board
        #(only considers consecutive tiles from bottom)
        y = 0
        while(y != 20 and board[y][x] == 0):
            y += 1
        
        #iterates through the columns in a block
        for w in range(len(piece[0])):
            
            #determines whether the right side of a block would lie outside
            #the play area in a potential position
            if(x + w >= len(board[0])):
                valid = False
                break
            else:

                #iterates through the rows in a block
                for h in range(len(piece)):

                    #determines whether the bottom of a block would lie beneath
                    #the play area in a potential position
                    if((y + firstLeftTile)>len(board)):
                        valid = False
                        break

                    #determines whether a tile on the board(that is filled) would be intersected
                    #by a potential block placement
                    elif((board[y-h-1][x+w] == 1) and (piece[h][w] == 1)):
                        valid = False
                        break

                    #determines whether the selected tile on a block would leave a hole beneath it
                    #(relative to the board) in a potential block placement
                    if(y != len(board)):
                        if(((board[y-h][x+w] == 0) and (piece[h][w] == 1))):
                            
                            #if this is the bottom row of the block
                            if(h == 0):
                                valid = False
                                break

                            #determines whether there is a tile within the block beneath the currently selected block tile
                            elif((piece[h][w] == 1) and (piece[h-1][w] == 0)):
                                valid = False
                                break
            
        # check if the spots above the potential piece are occupied and therefore the spot is impossible to reach
        # for each column of the piece: find the highest point that is occupied
        # from this point, go all the way up in the board until you each top of board OR spot is occupied on board
        for piece_col in range(len(piece[0])):
            highest_point = len(piece)
            for piece_row in range(len(piece)):
                if (piece[piece_row][piece_col] == 1):
                    break
                else:
                    highest_point -= 1
            for board_row in range(len(board) - highest_point - 1, -1, -1):
                if (board[board_row][x+piece_col] == 1):
                    valid = False
                    break
            if (valid == False):
                break
    
        if(valid):
            validPosList.append(x)
            print(validPosList)
    
    #returns a list of all columns in which the leftmost column of the block could 'perfectly' be placed
    return validPosList