import pygame, gomoku
from gomoku import *


# Define some colors
BLACK = (0, 0, 0)
WHITE = (235, 255, 255)
PINK = (255, 230, 230)
RED = (255, 0, 0)
YELLOW = (220, 180, 160)
GREEN = (100, 155, 155)

NUMBER_OF_INTERSECTION = 15
NUMBER_OF_CELL = NUMBER_OF_INTERSECTION - 1
WIDTH = 25
MARGIN = 1
PADDING = 25
BOARD = (WIDTH + MARGIN) * NUMBER_OF_CELL + MARGIN
GAME_WIDTH = BOARD + PADDING * 2
GAME_HIGHT = GAME_WIDTH + 100
STATUS = [0, 1, 2] # Trạng thái game, thua, hoà, thắng

class Render(object):
    def __init__(self, gomoku):
        self.gomoku = gomoku
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT), 0, 32)

        pygame.display.set_caption('Gomoku')


    def on_render(self):
        self.render_gomoku_piece()
        self.render_last_position()
        self.render_game_info()
        self.render_button()
        pygame.display.update()

    def gomoku_board_init(self):  # Vẽ bàn cờ
        self._display_surf.fill(PINK) # Nền
        pygame.draw.rect(self._display_surf, BLACK,  # Khung bàn cờ
                         [PADDING,
                          PADDING,
                          BOARD,
                          BOARD])

        # Ô cờ
        for row in range(NUMBER_OF_CELL):
            for column in range(NUMBER_OF_CELL):
                pygame.draw.rect(self._display_surf, YELLOW,
                                 [(MARGIN + WIDTH) * column + MARGIN + PADDING,
                                  (MARGIN + WIDTH) * row + MARGIN + PADDING,
                                  WIDTH,
                                  WIDTH])

    def render_button(self): # Vẽ nút, bắt đầu, đầu hàng
        color = RED if not self.gomoku.playing else GREEN
        info = "Start" if not self.gomoku.playing else "Surrender"
        pygame.draw.rect(self._display_surf, color,
                         (GAME_WIDTH // 2 - 50, GAME_HIGHT - 50, 100, 30))

        info_font = pygame.font.SysFont('Helvetica', 18)
        text = info_font.render(info, True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = GAME_WIDTH // 2
        textRect.centery = GAME_HIGHT - 35
        self._display_surf.blit(text, textRect)

    def render_game_info(self):  # Lượt chơi
        if self.gomoku.win == STATUS[2]:
            if self.gomoku.com:
                color = WHITE
                info = "You win"
            else:
                info = "Computer win"
                color = BLACK
        elif self.gomoku.win == STATUS[1]: info = "Draw"
        else:
            if not self.gomoku.com:
                color = WHITE
                info = "You"
            else:
                color = BLACK
                info = "Computer"
        center = (GAME_WIDTH // 2 - 50, BOARD + 60)
        radius = WIDTH // 2 - MARGIN
        pygame.draw.circle(self._display_surf, color, center, radius, 0)
        info_font = pygame.font.SysFont('Helvetica', 24)
        text = info_font.render(info, True, BLACK)
        textRect = text.get_rect()
        textRect.centerx = self._display_surf.get_rect().centerx + 20
        textRect.centery = center[1]
        self._display_surf.blit(text, textRect)

    def render_gomoku_piece(self): # Quân cờ
        for row in range(NUMBER_OF_INTERSECTION):
            for column in range(NUMBER_OF_INTERSECTION):
                center = ((MARGIN + WIDTH) * row + MARGIN + PADDING,
                          (MARGIN + WIDTH) * column + MARGIN + PADDING)
                if self.gomoku.get_grid_state(row, column) > 0:
                    radius = WIDTH // 2 - MARGIN
                    color = BLACK if self.gomoku.get_grid_state(row, column) == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):  # Đánh dấu quân cờ cuối cùng
        if self.gomoku.lastPosition[0] > 0 and self.gomoku.lastPosition[1] > 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.gomoku.lastPosition[0] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.gomoku.lastPosition[1] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)