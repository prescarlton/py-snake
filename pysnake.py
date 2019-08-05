'''
PySnake
(Yet another Snake clone made with Python)
Super simple snake game that I made in about two hours because I was bored

AUTHOR: Preston Carlton
CREATED: 8/4/2019
'''
# built-in imports
import random
import math
import tkinter as tk
from tkinter import messagebox
# third party imports
import pygame

## constants

# colors
WHITE = (255, 255, 255)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# setup window sizes + num rows
# NOTE: WIN_SIZE must be divisible by NUM_ROWS
WIN_SIZE = 500
NUM_ROWS = 20


def msg_box(title, msg):
    '''
    creates a tkinter dialog with msg as its content

    parameters:
    title (str): the title of the message dialog
    msg (str): the message the dialog will display
    '''
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(title, msg)

    try:
        root.destroy()
    except:
        pass


def update_window(game_board, snek, apple):
    '''
    Function to update the game board every clock tick

    parameters: 
    game_board: the gameboard on the window
    s (Snake): the snake object in the game
    '''

    # fill the gameboard to be black
    game_board.fill((0, 0, 0))
    # draw the snek + apple
    snek.draw(game_board)
    apple.draw(game_board)
    # update the gameboard
    pygame.display.update()


def rand_apple(snake_obj):
    '''
    returns a random position that doesn't overlap with 
    snake_obj's position

    parameters:
    snake_obj (Snake): the snake object in the game

    returns:
    tuple (x,y): position on the gameboard that doesn't
                 overlap with snake_obj's bodyparts
    '''

    # continue generating a random x,y until we get a pos that
    # the snake does not have a body part in
    while True:
        x = random.randrange(NUM_ROWS)
        y = random.randrange(NUM_ROWS)
        if (x, y) in [sq.pos for sq in snake_obj.body]:
            continue
        else:
            break

    return (x, y)


class Square(object):
    '''
    building blocks of the game. both apples and the snake are made up
    of squares

    parameters:
    pos (tuple): the position that the square should be drawn at
    
    optional parameters:
    color (tuple): the RGB color code of the square
    '''

    def __init__(self, position, color=SNAKE_COLOR):
        self.pos = position
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        '''
        helper function to move the square and change its direction

        parameters:
        dirx (int): direction to move the square on x axis (-1, 0, or 1)
        diry (int): direction to move the square on the y axis (-1, 0, or 1)
        '''

        self.dirx = dirx
        self.diry = diry
        # update the square's pos based on the direction given
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, game_board):
        '''
        actually draws squares on the game_board

        parameters:
        game_board: the gameboard to draw the square onto
        '''

        # distance btwn each grid cell
        dis = WIN_SIZE // NUM_ROWS

        # setup row/col so that i don't have to type
        # self.pos over and over again
        row = self.pos[0]
        col = self.pos[1]

        # draw the square on the game_board
        pygame.draw.rect(game_board, self.color,
                         (row*dis+1, col*dis+1, dis-2, dis-2))


class Snake(object):
    '''
    this bad boy is basically just a fancy list made up of Square objects.
    but it looks all purty on the screen B:

    init parameters:
    color (tuple): a tuple of the RGB color code of the Snake
    pos (tuple): the position the snake should start at
    '''
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.head = Square(self.pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
        

    def move(self):
        '''
        function that moves all the snake's bodyparts based on keyboard input
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # this lets the user press more than one key at once, so
            # controls are about as good as they can get for a snake
            # game.
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

        # loop thru all the bodyparts and determine which ones have to turn
        # and or move in a certain direction
        for i, sq in enumerate(self.body):
            p = sq.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                sq.move(turn[0], turn[1])
                # if the loop is at the last square in the snake's body,
                # remove the turn from the self.turns 'nary.
                if i == len(self.body)-1:
                    del self.turns[p]
            else:
                # this super-complex looking bit handles logic for
                # if the snake finds itself at the edge of the screen.
                if sq.dirx == -1 and sq.pos[0] <= 0:
                    sq.pos = (NUM_ROWS-1, sq.pos[1])
                elif sq.dirx == 1 and sq.pos[0] >= NUM_ROWS-1:
                    sq.pos = (0, sq.pos[1])
                elif sq.diry == 1 and sq.pos[1] >= NUM_ROWS-1:
                    sq.pos = (sq.pos[0], 0)
                elif sq.diry == -1 and sq.pos[1] <= 0:
                    sq.pos = (sq.pos[0], NUM_ROWS-1)
                else:
                    sq.move(sq.dirx, sq.diry)

    def reset(self):
        '''
        reset the snake to its initial state
        '''
        self.head = Square(self.pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 1
        self.diry = 0

    def add_square(self):
        # grab the tail (last item in the body)
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        # add a square at the appropriate location based off of the
        # direction of the snek
        if dx == 1:
            self.body.append(Square((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1:
            self.body.append(Square((tail.pos[0]+1, tail.pos[1])))
        elif dy == 1:
            self.body.append(Square((tail.pos[0], tail.pos[1]-1)))
        elif dy == -1:
            self.body.append(Square((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, game_board):
        for sq in self.body:
            sq.draw(game_board)


def main():
    '''
    where the 'game' is actually setup/run
    '''

    # get that window goin
    game_window = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))

    # init a snake with the specified color and position
    snek = Snake((255, 0, 0), (10, 10))

    # init a random apple
    apple = Square(rand_apple(snek), color=APPLE_COLOR)
    # initialize game clock
    clock = pygame.time.Clock()

    running = True
    while running:
        pygame.time.delay(50)
        clock.tick(10)
        snek.move()
        # if the snake head is at the same pos as the apple, give him an
        # extra square and redraw the apple
        if snek.body[0].pos == apple.pos:
            snek.add_square()
            apple = Square(rand_apple(snek), color=APPLE_COLOR)

        for i in range(len(snek.body)):
            # if snek.body[i].pos in [sq.pos for sq in snek.body[i+1:]]:
            if snek.body[i].pos in list(map(lambda z: z.pos, snek.body[i+1:])):
                # print('score: ', len(snek.body))
                msg_box('Game Over', 'You Lost! Your Score was %s.' %len(snek.body))
                snek.reset()
                break

        # update all the drawings on the window
        update_window(game_window, snek, apple)


if __name__ == "__main__":
    main()
