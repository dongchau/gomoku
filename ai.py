import pygame, gomoku
from gomoku import *


NUMBER_OF_INTERSECTION = 15
NUMBER_OF_CELL = NUMBER_OF_INTERSECTION - 1

class Ai(object):
    def __init__(self, gomoku):
        self.gomoku = gomoku
        self._piece = [-1, -1]
        self.attackArr = [0, 9, 54, 162, 1458, 13112, 118008]
        self.defenseArr = [0, 3, 27, 99, 729, 6561, 59049]
        self.directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        self.attack = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.defense = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.max = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]

        
    def find_way(self):
        maxScore = -10000
        for r in range(NUMBER_OF_INTERSECTION):
            for c in range(NUMBER_OF_INTERSECTION):
                attackScore = 0
                defenseScore = 0
                if self.gomoku.get_grid()[r][c] == 0:
                    for direction in self.directions:
                        for (x, y) in direction:
                            attackScore += self.check(r, c, x, y, 2)
                            defenseScore += self.check(r, c, x, y, 1)
                    self.attack[r][c] = attackScore
                    self.defense[r][c] = defenseScore
                    if attackScore <= defenseScore:
                        if maxScore <= defenseScore:
                            maxScore = defenseScore
                            self._piece = [r, c]
                    else:
                        if maxScore <= attackScore:
                            maxScore = attackScore
                            self._piece = [r, c]
                    self.max[r][c] = maxScore
        return self._piece


    # tính điểm cho mỗi ô
    def check(self, r, c, x, y, state):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        for i in range(1, 6):
            if r + x * i < 0 or r + x * i >= NUMBER_OF_INTERSECTION:
                break
            if c + y * i < 0 or c + y * i >= NUMBER_OF_INTERSECTION:
                break
            if self.gomoku.get_grid()[r + x * i][c + y * i] == 0:
                break
            if state == 1:
                if pieceOfCom == 2:
                    return totalScore
                if self.gomoku.get_grid()[r + x * i][c + y * i] == 2:
                    pieceOfCom += 1
                    break
                if self.gomoku.get_grid()[r + x * i][c + y * i] == 1:
                    pieceOfPlayer += 1
            if state == 2:
                if pieceOfPlayer == 2:
                    return totalScore
                if self.gomoku.get_grid()[r + x * i][c + y * i] == 2:
                    pieceOfCom += 1
                if self.gomoku.get_grid()[r + x * i][c + y * i] == 1:
                    pieceOfPlayer += 1
                    totalScore -= 9
                    break

        if state == 1:
            totalScore += self.defenseArr[pieceOfPlayer]
            totalScore -= self.defenseArr[pieceOfCom]
        if state == 2:
            totalScore += self.attackArr[pieceOfCom]
            totalScore -= self.attackArr[pieceOfPlayer]
        return totalScore