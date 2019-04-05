import pygame, render, gomoku, minimax, ai
from gomoku import *
from render import *
from minimax import *
from ai import *


class Game(object):
    def __init__(self, gomoku):
        self.minimax = Minimax(gomoku, 2, 2)
        self.ai = Ai(gomoku)
        self.render = Render(gomoku)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            gomoku.running = False

        if gomoku.player:
            if event.type == pygame.MOUSEBUTTONUP:
                if gomoku.mouse_in_botton():
                    if not gomoku.playing:
                        gomoku.start()
                        gomoku.first_step()
                    else:
                        gomoku.surrender()

                elif gomoku.playing:
                    pos = pygame.mouse.get_pos()
                    r = (pos[0] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
                    c = (pos[1] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)

                    if 0 <= r < NUMBER_OF_INTERSECTION and 0 <= c < NUMBER_OF_INTERSECTION:
                        if gomoku.get_grid_state(r, c) == 0:
                            gomoku.lastPosition = [r, c]
                            gomoku.set_grid_state(r, c, 1)
                            gomoku.numberOfPiece += 1

                            # check win
                            gomoku.win = self.check_win([r, c], gomoku.player)
                            if gomoku.win > 0:
                                gomoku.playing = False
                                gomoku.player = False
                                gomoku.com = True
                            else:
                                gomoku.player = False
        else:
            if gomoku.playing:
                #gomoku.lastPosition = self.minimax.find_way()
                self.minimax.find_way()
                r = gomoku.lastPosition[0]
                c = gomoku.lastPosition[1]
                gomoku.set_grid_state(r, c, 2)
                gomoku.numberOfPiece += 1
                gomoku.win = self.check_win([r, c], gomoku.player)
                if gomoku.win > 0:
                    gomoku.playing = False
                    gomoku.player = True
                    gomoku.com = False
                else:
                    gomoku.player = True

        if not gomoku.playing:
            gomoku.player = True

    def check_win(self, position, player):
        # Check hoà (full bàn cờ)
        if (gomoku.numberOfPiece == NUMBER_OF_INTERSECTION * NUMBER_OF_INTERSECTION):
            return STATUS[1]

        # Check thắng thua
        target = 1 if player else 2
        if gomoku.get_grid_state(position[0], position[1]) != target:
            return STATUS[0]
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            mark = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < NUMBER_OF_INTERSECTION and 0 <= p[1] < NUMBER_OF_INTERSECTION:
                    if gomoku.get_grid_state(p[0], p[1]) == target:
                        mark += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if mark >= 6:
                return STATUS[2]
        return STATUS[0]
    
    def player_vs_com(self):
        while gomoku.running:  # Game loop
            self.render.gomoku_board_init()
            for event in pygame.event.get():
                self.on_event(event)
            self.render.on_render()
        gomoku.on_cleanup()

    def __call__(self):
        self.player_vs_com()

if __name__ == "__main__":
    gomoku = Gomoku()
    game = Game(gomoku)
    game()