


# Imports
from collections import OrderedDict
import random
import pygame
from pygame import Rect

import numpy as np

# Maybe change...
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 601
GRID_WIDTH, GRID_HEIGHT = 300, 600
TILE_SIZE = 30
BOX_SIZE = 100
COLOUR_RED = (255, 0, 0)
COLOUR_HOVER_RED = (200, 0, 0)
COLOUR_WHITE = (255, 255, 255)


# restart button
class Button:
    def __init__(self, x, y, width, height, text, colour, hover_colour, text_colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = colour
        self.hover_colour = hover_colour
        self.text_colour = text_colour
        try:
            self.font = pygame.font.Font("Roboto-Regular.ttf", 20)
        except OSError:
            self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        
    def draw(self, screen):
        # Change color on hover
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_colour, self.rect)
        else:
            pygame.draw.rect(screen, self.colour, self.rect)

        # Draw text
        text_surf = self.font.render(self.text, True, self.text_colour)               
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        # Check if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False




def remove_empty_columns(arr, _x_offset=0, _keep_counting=True):
    """
    Remove empty columns from arr (i.e., those filled with zeros).
    The return value is (new_arr, x_offset), where x_offset is how
    much the x coordinate needs to be increased in order to maintain
    the block's original position.
    """
    for colid, col in enumerate(arr.T):
        if col.max() == 0:
            if _keep_counting:
                _x_offset += 1
            # Remove the current column and try again.
            arr, _x_offset = remove_empty_columns(
                np.delete(arr, colid, 1), _x_offset, _keep_counting)
            break
        else:
            _keep_counting = False
    return arr, _x_offset


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
            
            #determines the difference in height between two columns in a block
            blockColumnDif = 0
            leftColumnTop = 0
            nowColumnTop = 0
                    
            columnHeight = len(piece)-1
            while(piece[columnHeight][0] == 0):
                columnHeight -= 1
            leftColumnTop = columnHeight
                    
            columnHeight = len(piece)-1
            while(piece[columnHeight][w] == 0):
                columnHeight -= 1
            nowColumnTop = columnHeight

            blockColumnDif = nowColumnTop - leftColumnTop

            #determines the difference in height between two columns in the board
            boardColumnDif = 0
            y2 = 0
            
            if(x+w < len(board[0])):
                while(y2 != 20 and board[y2][x+w] == 0):
                    y2 += 1

                boardColumnDif = y2 - y

            else:
                boardColumnDif = 0

            #determines whether the right side of a block would lie outside
            #the play area in a potential position
            if(x + w >= len(board[0])):
                #print(str(x) + ": case1")
                valid = False
                break
            else:
                #determines whether the bottom of a block would lie beneath
                #the play area in a potential position
                if((y + firstLeftTile)>len(board)):
                    #print(str(x) + ": case2")
                    valid = False
                    break

                else:
                    #iterates through the rows in a block
                    for h in range(len(piece)):

                        #determines whether a tile on the board(that is filled) would be intersected
                        #by a potential block placement
                        if((board[y-len(piece)+h][x+w] == 1) and (piece[h][w] == 1)):
                            #print(str(x) + ":" + str(h)+ ": case3")
                            valid = False
                            break

                        #determines whether the selected tile on a block would leave a hole beneath it
                        #(relative to the board) in a potential block placement
                        elif(blockColumnDif != boardColumnDif):
                            valid = False
                            break

        # check if the spots above the potential piece are occupied and therefore the spot is impossible to reach
        # for each column of the piece: find the highest point that is occupied
        # from this point, go all the way up in the board until you each top of board OR spot is occupied on board
        '''
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
        '''

        if(valid):
            validPosList.append(x)

    #print(validPosList)
    if(len(validPosList) != 0):
        bestPos = 0
        bestAvgHeight = -1
        for x in validPosList:
            totalHeight = 0
            numTiles = 0
            avgHeight = 0
            for w in range(len(piece[0])):
                y = 0
                while(y != 20 and board[y][x+w] == 0):
                    y += 1
                for h in range(len(piece)):
                    if(piece[h][w] == 1):
                        totalHeight += (len(board)-y+h)
                        numTiles += 1
            avgHeight = totalHeight/numTiles
            if(bestAvgHeight == -1 or avgHeight < bestAvgHeight):
                bestAvgHeight = avgHeight
                bestPos = x

    else:
        bestPos = "none"
        bestAvgHeight = "none"

    #returns a list of all columns in which the leftmost column of the block could 'perfectly' be placed
    return (bestPos, bestAvgHeight)

class BottomReached(Exception):
    pass

class TopReached(Exception):
    pass
class LeftReached(Exception):
    pass
class Block(pygame.sprite.Sprite):

    @staticmethod
    def collide(block, group):
        """
        Check if the specified block collides with some other block
        in the group.
        """
        for other_block in group:
            # Ignore the current block which will always collide with itself.
            if block == other_block:
                continue
            if pygame.sprite.collide_mask(block, other_block) is not None and (other_block != group.current_block):
                return True
        return False

    def __init__(self):
        super().__init__()
        # Get a random color.
        self.color = random.choice((
            (200, 200, 200),
            (215, 133, 133),
            (30, 145, 255),
            (0, 170, 0),
            (180, 0, 140),
            (200, 200, 0)
        ))
        self.current = True
        self.struct = np.array(self.struct)
        # Initial random rotation and flip.
        if random.randint(0, 1):
            self.struct = np.rot90(self.struct)
        if random.randint(0, 1):
            # Flip in the X axis.
            self.struct = np.flip(self.struct, 0)
        self._draw()

    def _draw(self, x=4, y=0):
        width = len(self.struct[0]) * TILE_SIZE
        height = len(self.struct) * TILE_SIZE
        self.image = pygame.surface.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        # Position and size
        self.rect = Rect(0, 0, width, height)
        self.x = x
        self.y = y
        for y, row in enumerate(self.struct):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(
                        self.image,
                        self.color,
                        Rect(x*TILE_SIZE + 1, y*TILE_SIZE + 1,
                            TILE_SIZE - 2, TILE_SIZE - 2)
                    )
        self._create_mask()

    def redraw(self):
        self._draw(self.x, self.y)

    def _create_mask(self):
        """
        Create the mask attribute from the main surface.
        The mask is required to check collisions. This should be called
        after the surface is created or update.
        """
        self.mask = pygame.mask.from_surface(self.image)

    def initial_draw(self):
        raise NotImplementedError

    @property
    def group(self):
        return self.groups()[0]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.left = value*TILE_SIZE

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.top = value*TILE_SIZE

    def move_left(self, group):
        self.x -= 1
        # Check if we reached the left margin.
        if self.x < 0 or Block.collide(self, group):
            self.x += 1

    def move_right(self, group):
        self.x += 1
        # Check if we reached the right margin or collided with another
        # block.
        if self.rect.right > GRID_WIDTH or Block.collide(self, group):
            # Rollback.
            self.x -= 1

    def move_down(self, group):

        self.y += 1
        # Check if the block reached the bottom or collided with
        # another one.
        if self.rect.bottom > GRID_HEIGHT or Block.collide(self, group):
            # Rollback to the previous position.
            self.y -= 1
            self.current = False
            raise BottomReached

    def rotate(self, group):
        self.image = pygame.transform.rotate(self.image, 90)
        # Once rotated we need to update the size and position.
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self._create_mask()
        # Check the new position doesn't exceed the limits or collide
        # with other blocks and adjust it if necessary.
        while self.rect.right > GRID_WIDTH:
            self.x -= 1
        while self.rect.left < 0:
            self.x += 1
        while self.rect.bottom > GRID_HEIGHT:
            self.y -= 1
        while True:
            if not Block.collide(self, group):
                break
            self.y -= 1
        self.struct = np.rot90(self.struct)

    def update(self):
        if self.current:
            self.move_down()


class SquareBlock(Block):
    struct = (
        (1, 1),
        (1, 1)
    )


class TBlock(Block):
    struct = (
        (1, 1, 1),
        (0, 1, 0)
    )


class LineBlock(Block):
    struct = (
        (1,),
        (1,),
        (1,),
        (1,)
    )


class LBlock(Block):
    struct = (
        (1, 1),
        (1, 0),
        (1, 0),
    )


class ZBlock(Block):
    struct = (
        (0, 1),
        (1, 1),
        (1, 0),
    )

class Mirage(Block):

    def __init__(self, new_block = None,foundX =None):
        self.struct = new_block.struct
        super().__init__()
        
        self.struct = new_block.struct
        
        if foundX != None:
            self.color = (0,255,0)
            self.x = foundX
        else:
            self.x = new_block.x
            self.color = (255,255,255)

        self._draw(self.x,new_block.y)
        
    def move_left(self, group):
        self.x -= 1
        # Check if we reached the left margin.
        if self.x < 0 or Block.collide(self, group):
            self.x += 1
            raise LeftReached    

        
    def _draw(self, x=0, y=0):
        width = len(self.struct[0]) * TILE_SIZE
        height = len(self.struct) * TILE_SIZE
        self.image = pygame.surface.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        # Position and size
        self.rect = Rect(0, 0, width, height)
        self.x = x
        self.y = y
        for y, row in enumerate(self.struct):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(
                        self.image,
                        self.color,
                        Rect(x*TILE_SIZE + 1, y*TILE_SIZE + 1,
                            TILE_SIZE - 2, TILE_SIZE - 2)
                    )
        self._create_mask()

 # NICK CODE





class BlocksGroup(pygame.sprite.OrderedUpdates):




 
    



    @staticmethod
    def get_random_block():
        return random.choice(
            (SquareBlock, TBlock, LineBlock, LBlock, ZBlock))()
    
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.Mirage = None
        self.AI = False
        self._reset_grid()
        self._ignore_next_stop = False
        self.speed = 500
        self.score = 0
        self.foundMove = False
        self.next_block = None
        #HELP
        self.db = False
        # Not really moving, just to initialize the attribute.
        self.stop_moving_current_block()
        # The first block.
        self._create_new_block()

    def _check_line_completion(self):
        """
        Check each line of the grid and remove the ones that
        are complete.
        """
        # Start checking from the bottom.
        for i, row in enumerate(self.grid[::-1]):
            if all(row):
                self.score += 5
                self.speed -= 5
                # Get the blocks affected by the line deletion and
                # remove duplicates.
                affected_blocks = list(
                    OrderedDict.fromkeys(self.grid[-1 - i]))

                for block, y_offset in affected_blocks:
                    # Remove the block tiles which belong to the
                    # completed line.
                    block.struct = np.delete(block.struct, y_offset, 0)
                    if block.struct.any():
                        # Once removed, check if we have empty columns
                        # since they need to be dropped.
                        block.struct, x_offset = \
                            remove_empty_columns(block.struct)
                        # Compensate the space gone with the columns to
                        # keep the block's original position.
                        block.x += x_offset
                        # Force update.
                        block.redraw()
                    else:
                        # If the struct is empty then the block is gone.
                        self.remove(block)

                # Instead of checking which blocks need to be moved
                # once a line was completed, just try to move all of
                # them.
                for block in self:
                    # Except the current block.
                    if block.current:
                        continue
                    # Pull down each block until it reaches the
                    # bottom or collides with another block.
                    while True:
                        try:
                            block.move_down(self)
                        except BottomReached:
                            break

                self.update_grid()
                # Since we've updated the grid, now the i counter
                # is no longer valid, so call the function again
                # to check if there're other completed lines in the
                # new grid.
                self._check_line_completion()
                break

    def _reset_grid(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]

    def check(self):
            
        ff_grid = self.grid
        for i in range(len(ff_grid)):
            for j in range(len(ff_grid[i])):
                if ff_grid[i][j] != 0:
                    ff_grid[i][j] = 1
                    
        next_block_rotated_1 = np.rot90(self.current_block.struct)
        next_block_rotated_2 = np.rot90(self.current_block.struct)
        next_block_rotated_2 = np.rot90(next_block_rotated_2)
        next_block_rotated_3 = np.rot90(self.current_block.struct)
        next_block_rotated_3 = np.rot90(next_block_rotated_3)
        next_block_rotated_3 = np.rot90(next_block_rotated_3)
        
        perfectMove1 = find_perfect_moves(ff_grid, self.current_block.struct)
        perfectMove2 = find_perfect_moves(ff_grid, next_block_rotated_1)
        perfectMove3 = find_perfect_moves(ff_grid, next_block_rotated_2)
        perfectMove4 = find_perfect_moves(ff_grid, next_block_rotated_3)

        pot_best_moves = []
        pot_best_moves.append((0, perfectMove1))
        pot_best_moves.append((1, perfectMove2))
        pot_best_moves.append((2, perfectMove3))
        pot_best_moves.append((3, perfectMove4))

        bestMove = (0, 0, -1)
        for x in range(len(pot_best_moves)):
            if(type(pot_best_moves[x][1][1]) is not str):
                if((pot_best_moves[x][1][1] < bestMove[2]) or (bestMove[2] < 0)):
                    bestMove = (pot_best_moves[x][0], pot_best_moves[x][1][0], pot_best_moves[x][1][1])
        #print(pot_best_moves)
        if(bestMove[2] < 0):
            bestMove = (None,None)

        if bestMove[1] != None:
            self.foundMove = bestMove[1]
            self.rotations = bestMove[0]
            for i in range(self.rotations):
                self.current_block.rotate(self)
        else:
            self.AI = False
    def _create_new_block(self):

        new_block = self.next_block or BlocksGroup.get_random_block()
        if Block.collide(new_block, self):
            raise TopReached
        self.add(new_block)
        self.check()
        self.next_block = BlocksGroup.get_random_block()
        self.update_grid()
        self._check_line_completion()
    


    

    def update_grid(self):
        self._reset_grid()

        if self.foundMove != None and self.AI == True:

            self.Mirage = Mirage(self.current_block,self.foundMove)
        else:
            self.Mirage = Mirage(self.current_block)
        while True:
            try:
                
                self.Mirage.move_down(self)
            except BottomReached:
                break
        

        for block in self:
            for y_offset, row in enumerate(block.struct):
                for x_offset, digit in enumerate(row):
                    # Prevent replacing previous blocks.
                    if digit == 0:
                        continue
                    
                    rowid = block.y + y_offset
                    colid = block.x + x_offset
                    self.grid[rowid][colid] = (block, y_offset)




    @property
    def current_block(self):
        return self.sprites()[-1]
    

    def update_current_block(self):
        try:
            
            if self.foundMove != None and self.AI == True:
                    if self.db == False:
                        self.db = True

                    xdist = self.current_block.x
                    if xdist > self.foundMove:
                        self.current_block.move_left(self)
                    elif xdist < self.foundMove:
                        self.current_block.move_right(self)
                    self.current_block.move_down
            self.current_block.move_down(self)
        except BottomReached:
            self.db = False
            self.AI = False
            self.foundMove = None
            self.stop_moving_current_block()
            self._create_new_block()
        else:
            self.update_grid()
            
    def move_current_block(self):
        # First check if there's something to move.

        if self._current_block_movement_heading is None:
            return
        action = {
            pygame.K_DOWN: self.current_block.move_down,
            pygame.K_LEFT: self.current_block.move_left,
            pygame.K_RIGHT: self.current_block.move_right

        }
            # Each function requires the group as the first argument
            # to check any possible collision.
        try:

            if self.foundMove == None or self._current_block_movement_heading == pygame.K_DOWN or self.AI == False:
                action[self._current_block_movement_heading](self)
        except BottomReached:
            self.foundMove = None
            self.db = False
            self.AI = False
            self.stop_moving_current_block()
            self._create_new_block()
        else:
            self.update_grid()

    def start_moving_current_block(self, key):
        if self._current_block_movement_heading is not None:
            self._ignore_next_stop = True
        self._current_block_movement_heading = key

    def stop_moving_current_block(self):
        if self._ignore_next_stop:
            self._ignore_next_stop = False
        else:
            self._current_block_movement_heading = None

    def rotate_current_block(self):
        # Prevent SquareBlocks rotation.
        if not isinstance(self.current_block, SquareBlock):
            self.current_block.rotate(self)
            self.update_grid()


def draw_grid(background):


    """Draw the background grid."""
    grid_color = 50, 50, 50
    # Vertical lines.
    for i in range(11):
        x = TILE_SIZE * i

        pygame.draw.line(
            background, grid_color, (x, 0), (x, GRID_HEIGHT)
        )
    # Horizontal liens.
    for i in range(21):
        y = TILE_SIZE * i
        pygame.draw.line(
            background, grid_color, (0, y), (GRID_WIDTH, y)
        )


def draw_centered_surface(screen, surface, y):
    screen.blit(surface, (400 - surface.get_width()//2, y))

restart_button = None

def main():
    pygame.init()
    pygame.display.set_caption("Tetris with PyGame")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    paused = False
    game_over = False
    # Create background.
    background = pygame.Surface(screen.get_size())

    global restart_button

    bgcolor = (0, 0, 0)
    background.fill(bgcolor)
    # Draw the grid on top of the background.
    draw_grid(background)
    # This makes blitting faster.
    background = background.convert()

    try:
        font = pygame.font.Font("Roboto-Regular.ttf", 20)
    except OSError:
        # If the font file is not available, the default will be used.
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
    next_block_text = font.render(
        "Next figure:", True, (255, 255, 255), bgcolor)
    score_msg_text = font.render(
        "Score:", True, (255, 255, 255), bgcolor)
    game_over_text = font.render(
        "Game over!", True, (255, 220, 0), bgcolor)

    # Event constants.
    MOVEMENT_KEYS = pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN
    EVENT_UPDATE_CURRENT_BLOCK = pygame.USEREVENT + 1
    EVENT_MOVE_CURRENT_BLOCK = pygame.USEREVENT + 2
    
    blocks = BlocksGroup()
    pygame.time.set_timer(EVENT_UPDATE_CURRENT_BLOCK, blocks.speed)
    pygame.time.set_timer(EVENT_MOVE_CURRENT_BLOCK, 100)


    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYUP:
                if not paused and not game_over:
                    if event.key in MOVEMENT_KEYS:
                        blocks.stop_moving_current_block()
                    elif event.key == pygame.K_UP and blocks.AI != True:
                        blocks.rotate_current_block()
                    elif event.key == pygame.K_SPACE:
                        if blocks.AI == False:

                            blocks.AI =True
                        else:
                            blocks.AI =False

                if event.key == pygame.K_p:
                    paused = not paused

            # Stop moving blocks if the game is over or paused.
            if game_over or paused:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key in MOVEMENT_KEYS:
                    blocks.start_moving_current_block(event.key)

            try:
                if event.type == EVENT_UPDATE_CURRENT_BLOCK:
                    blocks.update_current_block()
                elif event.type == EVENT_MOVE_CURRENT_BLOCK:
                    blocks.move_current_block()
            except TopReached:
                game_over = True

        # Draw background and grid.
        screen.blit(background, (0, 0))

        if blocks.foundMove == None:

            color = (255,0,0)
            ai_text = font.render(
                "No Optimal Move", True, (255, 0, 0), bgcolor)
            draw_centered_surface(screen, ai_text, 350)

        elif blocks.AI == True:
            
            color = (0,255,0)
            ai_text = font.render(
                "Move Optimized!", True, (0, 255, 0), bgcolor)
            draw_centered_surface(screen, ai_text, 350)
        else:
            color = (0,255,0)
            ai_text = font.render(
                "Space for help!", True, (0, 255, 0), bgcolor)
            draw_centered_surface(screen, ai_text, 350)

        # Blocks.
        if blocks.Mirage != None:
            blocks.add(blocks.Mirage)
        blocks.draw(screen)

        blocks.remove(blocks.Mirage)
        # Sidebar with misc. information.
        draw_centered_surface(screen, next_block_text, 50)
        draw_centered_surface(screen, blocks.next_block.image, 100)
        draw_centered_surface(screen, score_msg_text, 240)
        score_text = font.render(
            str(blocks.score), True, (255, 255, 255), bgcolor)
        draw_centered_surface(screen, score_text, 270)
        if game_over:
            draw_centered_surface(screen, game_over_text, 400)
            if restart_button is None:  
                restart_button = Button(350, 450, 100, 50, "RESTART", COLOUR_RED, COLOUR_HOVER_RED, COLOUR_WHITE)

            restart_button.draw(screen)

            # Check if the button is clicked
            if pygame.mouse.get_pressed()[0] and restart_button.rect.collidepoint(pygame.mouse.get_pos()):
                main()
        # Update.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()