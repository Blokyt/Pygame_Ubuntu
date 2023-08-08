from copy import deepcopy
from random import shuffle
import pygame
pygame.init()


def select_move():
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    x = round(mouse_x // (game.resolution//3))
    y = round(mouse_y // (game.resolution//3))
    return y, x


class Morpion:

    def __init__(self):
        self.resolution = 700
        self.coin_w = self.resolution // 3
        self.coin_h = self.resolution // 3
        self.space = 15

        self.screen = pygame.display.set_mode((self.resolution, self.resolution))
        pygame.display.set_caption('MorpionGameIA')
        self.clock = pygame.time.Clock()
        self.game_speed = 30
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.player = 1

    def update_ui(self):
        self.screen.fill((0, 155, 255))
        for y in range(3):
            for x in range(3):

                coin_color = (255, 255, 255)
                if self.grid[y][x] == 1:
                    coin_color = (0, 255, 155)
                elif self.grid[y][x] == 2:
                    coin_color = (255, 155, 0)
                pygame.draw.rect(self.screen, coin_color,
                                 pygame.Rect(x * self.coin_w + self.space, y * self.coin_h + self.space,
                                             self.coin_w - 2 * self.space, self.coin_h - 2 * self.space))
        pygame.display.flip()

    def play_move(self, player, move=None, grid=None):
        if move is None:
            move = select_move()
        if grid is None:
            grid = self.grid
        if grid[move[0]][move[1]] == 0:
            grid[move[0]][move[1]] = player
            return True
        return False

    def is_game_over(self, player, grid=None):
        if grid is None:
            grid = self.grid
        rows = grid
        columns = [[grid[j][i] for j in range(3)] for i in range(3)]
        diags = [[grid[i][i] for i in range(3)], [grid[2 - i][i] for i in range(3)]]

        if [player] * 3 in rows or [player] * 3 in columns or [player] * 3 in diags:
            return True, 1
        elif not (0 in [coin for row in grid for coin in row]):
            return True, 0
        else:
            return [False]

    def find_best_move(self, player, grid=None):
        other = (2 if player == 1 else 1)
        moves = []
        if grid is None:
            grid = self.grid

        for y in range(3):
            for x in range(3):
                if grid[y][x] == 0:
                    new_grid = deepcopy(grid)
                    self.play_move(player, (y, x), new_grid)
                    state = self.is_game_over(player, new_grid)
                    if state[0]:
                        score = state[1]
                    else:
                        score = 0 - self.find_best_move(other, new_grid)[1]
                    if score == 1:
                        return [(y, x), score]

                    moves.append([(y, x), score])

        shuffle(moves)
        moves.sort(key=lambda move: move[1], reverse=True)
        return moves[0]

    def start_ui(self):
        x = self.coin_w + self.space
        y = self.coin_h + self.space
        w = self.coin_w - 2 * self.space
        h = self.coin_h - 2 * self.space

        # font
        font = pygame.font.SysFont('DEBUG_FREE_TRIAL', 2*h//5)
        # texts
        text_ia = font.render("Ia First", True, (255, 255, 255))
        text_p = font.render("P First", True, (255, 255, 255))
        # display text
        game.screen.blit(text_ia, [x + (w - text_ia.get_width()) // 2, y + 4 * (h - text_ia.get_height()) // 5])
        game.screen.blit(text_p, [x + (w - text_p.get_width()) // 2, y + (h - text_p.get_height()) // 5])
        pygame.display.flip()

    def start(self):
        x = self.coin_w + self.space
        y = self.coin_h + self.space
        w = self.coin_w - 2 * self.space
        h = self.coin_h - 2 * self.space

        # font
        font = pygame.font.SysFont('DEBUG_FREE_TRIAL', h // 3)
        # texts
        text_ia = font.render("Ia First", True, (255, 255, 255))
        text_p = font.render("P First", True, (255, 255, 255))

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if x + (w - text_ia.get_width()) // 2 <= mouse_x <= x + (w + text_ia.get_width()) // 2 and y + 4 * (
                h - text_ia.get_height()) // 5 <= mouse_y <= y + (4 * h + text_ia.get_height()) // 5:
            return True, True
        elif x + (w - text_p.get_width()) // 2 <= mouse_x <= x + (w + text_p.get_width()) // 2 and y + (
                h - text_p.get_height()) // 5 <= mouse_y <= y + (h + 4 * text_p.get_height()) // 5:
            return True, False
        else:
            return False, False

    def reset(self):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]


game = Morpion()

start = False
IaStart = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouse_state = pygame.mouse.get_pressed()
    if start:
        game.player = 1
        if IaStart or (mouse_state[0] and game.play_move(game.player)):
            IaStart = False
            game.update_ui()
            if game.is_game_over(game.player)[0]:
                start = False
                game.reset()
            else:
                game.player = 2
                game.play_move(game.player, game.find_best_move(game.player)[0])
                game.update_ui()
                if game.is_game_over(game.player)[0]:
                    start = False
                    game.reset()
        else:
            game.update_ui()
    else:
        game.start_ui()
        if game.start()[0] and mouse_state[0]:
            game.update_ui()
            start = True
            if game.start()[1]:
                IaStart = True
            else:
                pygame.time.wait(200)

    game.clock.tick(game.game_speed)
