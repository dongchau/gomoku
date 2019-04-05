import pygame, random
from random import randrange

NUMBER_OF_INTERSECTION = 15
NUMBER_OF_CELL = NUMBER_OF_INTERSECTION - 1
WIDTH = 25
MARGIN = 1
PADDING = 25
BOARD = (WIDTH + MARGIN) * NUMBER_OF_CELL + MARGIN
GAME_WIDTH = BOARD + PADDING * 2
GAME_HIGHT = GAME_WIDTH + 100
STATUS = [0, 1, 2] # Trạng thái game, thua, hoà, thắng

class Gomoku(object):
    def __init__(self):
        self._grid = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]

        self.player = True
        self.com = False
        self.running = True
        self.playing = False
        self.win = STATUS[0]
        self.lastPosition = [-1, -1]
        self.numberOfPiece = 0

    def get_grid(self):
        return self._grid

    def get_grid_state(self, i, j):
        return self._grid[i][j]

    def set_grid_state(self, i, j, state):
        self._grid[i][j] = state

    def on_cleanup(self):
        pygame.quit()

    def start(self):
        self.playing = True
        self._grid = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.lastPosition = [-1, -1]
        self.win = STATUS[0]
        self.player = True

    def surrender(self):
        self.playing = False
        self.win = STATUS[2]

    def mouse_in_botton(self):
        pos = pygame.mouse.get_pos()
        if GAME_WIDTH // 2 - 50 <= pos[0] <= GAME_WIDTH // 2 + 50 and GAME_HIGHT - 50 <= pos[1] <= GAME_HIGHT - 20:
            return True
        return False

    def first_step(self):
        self.set_grid_state(randrange(3, NUMBER_OF_INTERSECTION - 3),
                            randrange(3, NUMBER_OF_INTERSECTION - 3), 2)