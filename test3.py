import pygame, ai
from ai import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (235, 255, 255)
PINK = (255, 230, 230)
RED = (255, 0, 0)
YELLOW = (210, 170, 150)
GREEN = (100, 155, 155)

# Define grid globals
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
        self.grid = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.attack = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.defense = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.max = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        pygame.init()
        pygame.font.init()
        self._display_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT))

        pygame.display.set_caption('Gomoku')

        self.player = True
        self.com = False
        self._running = True
        self._playing = False
        self._win = STATUS[0]
        self.lastPosition = [-1, -1]
        self._numberOfPiece = 0
        self.mode = 1
        self.attackArr = [0, 9, 54, 162, 1458, 13112, 118008]
        self.defenseArr = [0, 3, 27, 99, 729, 6561, 59049]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if self.player:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.mouse_in_botton(pos):
                    if not self._playing:
                        self.start()
                    else:
                        self.surrender()
                       # self.player = not self.player

                elif self._playing:
                    r = (pos[0] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)
                    c = (pos[1] - PADDING + WIDTH // 2) // (WIDTH + MARGIN)

                    if 0 <= r < NUMBER_OF_INTERSECTION and 0 <= c < NUMBER_OF_INTERSECTION:
                        if self.grid[r][c] == 0:
                            self.lastPosition = [r, c]
                            self.grid[r][c] = 1
                            self._numberOfPiece += 1

                            # check win
                            self._win = self.check_win([r, c], self.player)
                            if self._win > 0:
                                self._playing = False
                                self.player = False
                                self.com = True
                            else:
                                self.player = False
        else:
            if self._playing:
                self.lastPosition = self.find_way()
                r = self.lastPosition[0]
                c = self.lastPosition[1]
                self.grid[r][c] = 2
                self._numberOfPiece += 1
                self._win = self.check_win([r, c], self.player)
                if self._win > 0:
                    self._playing = False
                    self.player = True
                    self.com = False
                else:
                    self.player = True

        if not self._playing:
            self.player = True

    def on_cleanup(self):
        pygame.quit()

    def start(self):
        self._playing = True
        self.grid = [[0 for x in range(NUMBER_OF_INTERSECTION)] for y in range(NUMBER_OF_INTERSECTION)]
        self.lastPosition = [-1, -1]
        self._win = STATUS[0]
        self.player = True


    def surrender(self):
        self._playing = False
        self._win = STATUS[2]

    def mouse_in_botton(self, pos):
        if GAME_WIDTH // 2 - 50 <= pos[0] <= GAME_WIDTH // 2 + 50 and GAME_HIGHT - 50 <= pos[1] <= GAME_HIGHT - 20:
            return True
        return False

    def check_win(self, position, player):
        # Check hoà (full bàn cờ)
        count = 0
        if(self._numberOfPiece == NUMBER_OF_INTERSECTION * NUMBER_OF_INTERSECTION):
            return STATUS[1]

        # Check thắng thua
        target = 1 if player else 2
        if self.grid[position[0]][position[1]] != target:
            return STATUS[0]
        directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
        for direction in directions:
            mark = 0
            for i in range(2):
                p = position[:]
                while 0 <= p[0] < NUMBER_OF_INTERSECTION and 0 <= p[1] < NUMBER_OF_INTERSECTION:
                    if self.grid[p[0]][p[1]] == target:
                        mark += 1
                    else:
                        break
                    p[0] += direction[i][0]
                    p[1] += direction[i][1]
            if mark >= 6:
                return STATUS[2]
        return STATUS[0]


    """
    Giao diện
    """
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
        color = RED if not self._playing else GREEN
        info = "Start" if not self._playing else "Surrender"

        pygame.draw.rect(self._display_surf, color,
                         (GAME_WIDTH // 2 - 50, GAME_HIGHT - 50, 100, 30))

        info_font = pygame.font.SysFont('Helvetica', 18)
        text = info_font.render(info, True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = GAME_WIDTH // 2
        textRect.centery = GAME_HIGHT - 35
        self._display_surf.blit(text, textRect)

    def render_game_info(self):  # Lượt chơi
        if self._win == STATUS[2]:
            if  self.com:
                color = WHITE
                info = "You win"
            else:
                info = "Computer win"
                color = BLACK
        elif self._win == STATUS[1]: info = "Draw"
        else:
            if not self.com:
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
                if self.grid[row][column] > 0:
                    radius = WIDTH // 2 - MARGIN
                    color = BLACK if self.grid[row][column] == 2 else WHITE
                    pygame.draw.circle(self._display_surf, color,
                                       center,
                                       WIDTH // 2 - MARGIN, 0)

    def render_last_position(self):  # Đánh dấu quân cờ cuối cùng
        if self.lastPosition[0] > 0 and self.lastPosition[1] > 0:
            pygame.draw.rect(self._display_surf, RED,
                             ((MARGIN + WIDTH) * self.lastPosition[0] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH) * self.lastPosition[1] + (MARGIN + WIDTH) // 2,
                              (MARGIN + WIDTH),
                              (MARGIN + WIDTH)), 1)
    """
    Hết giao diện
    """

    """
    AI
    """
    def find_way(self):
        piece = [-1, -1]
        maxScore = -10000
        for r in range(NUMBER_OF_INTERSECTION):
            for c in range(NUMBER_OF_INTERSECTION):
                attackScore = 0
                defenseScore = 0
                if self.grid[r][c] == 0:
                    attackScore = self.attack_doc(r, c) + self.attack_ngang(r, c) + self.attack_cheo_xuoi(r, c) + self.attack_cheo_nguoc(r, c)
                    defenseScore = self.defense_doc(r, c) + self.defense_ngang(r, c) + self.defense_cheo_xuoi(r, c) + self.defense_cheo_nguoc(r, c)
                    self.attack[r][c] = attackScore
                    self.defense[r][c] = defenseScore
                    if attackScore <= defenseScore:
                        if maxScore <= defenseScore:
                            maxScore = defenseScore
                            piece = [r, c]
                    else:
                        if maxScore <= attackScore:
                            maxScore = attackScore
                            piece = [r, c]
                    self.max[r][c] = maxScore

        for r in range(NUMBER_OF_INTERSECTION):
            for c in range(NUMBER_OF_INTERSECTION):
                print(self.max[r][c])
        return piece

    # Duyệt tấn công
    # Duyệt dọc
    def attack_doc(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r + i][c] == 0:
                break
            if self.grid[r + i][c] == 2:
                pieceOfCom += 1
            if self.grid[r + i][c] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0:
                break
            if self.grid[r - i][c] == 0:
                break
            if self.grid[r - i][c] == 2:
                pieceOfCom += 1
            if self.grid[r - i][c] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        if pieceOfPlayer == 2:
            return totalScore
        totalScore += self.attackArr[pieceOfCom]
        totalScore -= self.attackArr[pieceOfPlayer]
        return totalScore

    # Duyệt ngang
    def attack_ngang(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trái sang
        for i in range(1, 6):
            if c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r][c + i] == 0:
                break
            if self.grid[r][c + i] == 2:
                pieceOfCom += 1
            if self.grid[r][c + i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        # Duyệt từ phải sang
        for i in range(1, 6):
            if c - i < 0:
                break
            if self.grid[r][c - i] == 0:
                break
            if self.grid[r][c - i] == 2:
                pieceOfCom += 1
            if self.grid[r][c - i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        if pieceOfPlayer == 2:
            return totalScore
        totalScore += self.attackArr[pieceOfCom]
        totalScore -= self.attackArr[pieceOfPlayer]
        return totalScore

    # Duyệt chéo xuôi
    def attack_cheo_xuoi(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION or c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r + i][c + i] == 0:
                break
            if self.grid[r + i][c + i] == 2:
                pieceOfCom += 1
            if self.grid[r + i][c + i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0 or c - i < 0:
                break
            if self.grid[r - i][c - i] == 0:
                break
            if self.grid[r - i][c - i] == 2:
                pieceOfCom += 1
            if self.grid[r - i][c - i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        if pieceOfPlayer == 2:
            return totalScore
        totalScore += self.attackArr[pieceOfCom]
        totalScore -= self.attackArr[pieceOfPlayer]
        return totalScore

    # Duyệt chéo ngược
    def attack_cheo_nguoc(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION or c - i < 0:
                break
            if self.grid[r + i][c - i] == 0:
                break
            if self.grid[r + i][c - i] == 2:
                pieceOfCom += 1
            if self.grid[r + i][c - i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0 or c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r - i][c + i] == 0:
                break
            if self.grid[r - i][c + i] == 2:
                pieceOfCom += 1
            if self.grid[r - i][c + i] == 1:
                pieceOfPlayer += 1
                totalScore -= 9
                break
        if pieceOfPlayer == 2:
            return totalScore
        totalScore += self.attackArr[pieceOfCom]
        totalScore -= self.attackArr[pieceOfPlayer]
        return totalScore



    # Duyệt phòng ngự
    # Duyệt dọc
    def defense_doc(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r + i][c] == 0:
                break
            if self.grid[r + i][c] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r + i][c] == 1:
                pieceOfPlayer += 1
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0:
                break
            if self.grid[r - i][c] == 0:
                break
            if self.grid[r - i][c] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r - i][c] == 1:
                pieceOfPlayer += 1
        if pieceOfCom == 2:
            return totalScore
        totalScore += self.defenseArr[pieceOfPlayer]
        if pieceOfPlayer > 0:
            totalScore -= self.defenseArr[pieceOfCom] * 2
        return totalScore

    # Duyệt ngang
    def defense_ngang(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trái sang
        for i in range(1, 6):
            if c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r][c + i] == 0:
                break
            if self.grid[r][c + i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r][c + i] == 1:
                pieceOfPlayer += 1
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if c - i < 0:
                break
            if self.grid[r][c - i] == 0:
                break
            if self.grid[r][c - i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r][c - i] == 1:
                pieceOfPlayer += 1
        if pieceOfCom == 2:
            return totalScore
        totalScore += self.defenseArr[pieceOfPlayer]
        if pieceOfPlayer > 0:
            totalScore -= self.defenseArr[pieceOfCom] * 2
        return totalScore

    # Duyệt chéo xuôi
    def defense_cheo_xuoi(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION or c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r + i][c + i] == 0:
                break
            if self.grid[r + i][c + i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r + i][c + i] == 1:
                pieceOfPlayer += 1
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0 or c - i < 0:
                break
            if self.grid[r - i][c - i] == 0:
                break
            if self.grid[r - i][c - i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r - i][c - i] == 1:
                pieceOfPlayer += 1
        if pieceOfCom == 2:
            return totalScore
        totalScore += self.defenseArr[pieceOfPlayer]
        if pieceOfPlayer > 0:
            totalScore -= self.defenseArr[pieceOfCom] * 2
        return totalScore

    # Duyệt chéo ngược
    def defense_cheo_nguoc(self, r, c):
        totalScore = 0
        pieceOfPlayer = 0
        pieceOfCom = 0
        # Duyệt từ trên xuống
        for i in range(1, 6):
            if r + i >= NUMBER_OF_INTERSECTION or c - i < 0:
                break
            if self.grid[r + i][c - i] == 0:
                break
            if self.grid[r + i][c - i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r + i][c - i] == 1:
                pieceOfPlayer += 1
        # Duyệt từ dưới lên
        for i in range(1, 6):
            if r - i < 0 or c + i >= NUMBER_OF_INTERSECTION:
                break
            if self.grid[r - i][c + i] == 0:
                break
            if self.grid[r - i][c + i] == 2:
                pieceOfCom += 1
                # totalScore -= 9
                break
            if self.grid[r - i][c + i] == 1:
                pieceOfPlayer += 1
        if pieceOfPlayer == 2:
            return totalScore
        totalScore += self.defenseArr[pieceOfPlayer]
        if pieceOfPlayer > 0:
            totalScore -= self.defenseArr[pieceOfCom] * 2
        return totalScore

    """
    Hết AI
    """

    # run
    def playerVsCom(self):
        while self._running:  # Game loop
            self.gomoku_board_init()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
        self.on_cleanup()

    def __call__(self):
        self.playerVsCom()

if __name__ == "__main__":
    gomoku = Gomoku()
    gomoku()