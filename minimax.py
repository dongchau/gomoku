import pygame, gomoku, evaluate, copy
from gomoku import *
from evaluate import *
from copy import deepcopy

NUMBER_OF_INTERSECTION = 15
NUMBER_OF_CELL = NUMBER_OF_INTERSECTION - 1


class Minimax(object):

    def __init__(self, gomoku, state, depth):

        self.gomoku = gomoku
        self.state = state
        self.depth = depth
        self._currentX = -1
        self._currentY = -1


    def has_neighbor(self, r, c):
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        for direction in directions:
            for (x, y) in direction:
                for step in range(1, 3):
                    if c + x * step < 0 or c + x * step >= NUMBER_OF_INTERSECTION:
                        break
                    if r + y * step < 0 or r + y * step >= NUMBER_OF_INTERSECTION:
                        break
                    if self.gomoku.get_grid()[r + y * step][c + x * step] != 0:
                        return True
        return False

    def child_node(self):
        children = []
        for i in range(NUMBER_OF_INTERSECTION):
            for j in range(NUMBER_OF_INTERSECTION):
                if self.gomoku.get_grid()[i][j] != 0:
                    continue
                if not self.has_neighbor(i, j):
                    continue

                if self.state == 2:
                    nextState = 1
                else:
                    nextState = 2

                nextPlay = Minimax(deepcopy(self.gomoku), nextState, self.depth - 1)
                nextPlay.gomoku.set_grid_state(i, j, self.state)
                children.append((nextPlay, i, j))
        return children

    
    def evaluate(self):
        '''
        Return the board score for Minimax Search.
        '''
        #exhaustive search
        vectors = []

        for i in range(NUMBER_OF_INTERSECTION):
            vectors.append(self.gomoku.get_grid()[i])

        for j in range(NUMBER_OF_INTERSECTION):
            vectors.append([self.gomoku.get_grid()[i][j] for i in range(NUMBER_OF_INTERSECTION)])

        vectors.append([self.gomoku.get_grid()[x][x] for x in range(NUMBER_OF_INTERSECTION)])

        for i in range(1, NUMBER_OF_INTERSECTION - 4):
            v = [self.gomoku.get_grid()[x][x - i] for x in range(i, NUMBER_OF_INTERSECTION)]
            vectors.append(v)
            v = [self.gomoku.get_grid()[y - i][y] for y in range(i, NUMBER_OF_INTERSECTION)]
            vectors.append(v)

        vectors.append([self.gomoku.get_grid()[x][NUMBER_OF_INTERSECTION - x - 1] for x in range(NUMBER_OF_INTERSECTION)])

        for i in range(4, NUMBER_OF_INTERSECTION - 1):
            v = [self.gomoku.get_grid()[x][i - x] for x in range(i, -1, -1)]
            vectors.append(v)
            v = [self.gomoku.get_grid()[x][NUMBER_OF_INTERSECTION - x + NUMBER_OF_INTERSECTION - i - 2]
                 for x in range(NUMBER_OF_INTERSECTION - i - 1, NUMBER_OF_INTERSECTION)]
            vectors.append(v)

        totalScore = 0

        for v in vectors:
            score = evaluate(v)
            if self.state == 2:
                totalScore += score['black'] - score['white']
            else:
                totalScore += score['white'] - score['black']
        return totalScore

    def alpha_beta_pruning(self, node, a=-10000000, b=10000000):
        if node.depth <= 0:
            score = node.evaluate()
            return score
        children = node.child_node()
        for (child, i, j) in children:
            temp_score = -self.alpha_beta_pruning(child, -b, -a)
            if temp_score > b:
                return b
            if temp_score > a:
                a = temp_score
                (node._currentX, node._currentY) = (i, j)
        return a


    def find_way(self):
        node = Minimax(self.gomoku, self.state, self.depth)
        score = self.alpha_beta_pruning(node)
        (i, j) = (node._currentX, node._currentY)

        if not i is None and not j is None:
            if self.gomoku.get_grid_state(i, j) != 0:
                self.find_way()
            else:
                self.gomoku.set_grid_state(i, j, self.state)
                self.gomoku.lastPosition = (i, j)
                return True
        return False