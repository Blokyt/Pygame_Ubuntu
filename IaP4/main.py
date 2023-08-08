from copy import deepcopy
from random import shuffle
import pygame
pygame.init()
#test git


def select_move():
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    x = round(mouse_x // (game.w//7))
    return x


def move_possible(move, grid):
    columns = [[grid[y][x] for y in range(6)] for x in range(7)]
    for k in range(6):
        if columns[move][5 - k] == 0:
            return True
    return False


class P4:

    def __init__(self):
        self.w = 700
        self.h = 600
        self.coin_w = self.w // 7
        self.coin_h = self.h // 6
        self.space = 15
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("P4")
        self.grid = [[0 for _ in range(7)] for _ in range(6)]
        self.player = 1
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        self.ia_step = 0
        self.depth = 0
        self.sum_step = 0

    def update_ui(self):
        self.screen.fill((0, 155, 255))
        for y in range(6):
            for x in range(7):

                coin_color = (255, 255, 255)
                if self.grid[y][x] == 1:
                    coin_color = 'yellow'
                elif self.grid[y][x] == 2:
                    coin_color = (255, 0, 0)
                pygame.draw.rect(self.screen, coin_color,
                                 pygame.Rect(x * self.coin_w + self.space, y * self.coin_h + self.space,
                                             self.coin_w - 2 * self.space, self.coin_h - 2 * self.space))
        pygame.display.flip()

    def place_coin(self, player, move=None, grid=None):
        if move is None:
            move = select_move()
        if grid is None:
            grid = self.grid
        columns = [[grid[y][x] for y in range(6)] for x in range(7)]

        for k in range(6):
            if columns[move][5 - k] == 0:
                grid[5 - k][move] = player
                return True
        return False

    def is_game_over(self, player, grid=None):
        if grid is None:
            grid = self.grid

        rows_4 = [[row[x_0+x] for x in range(4)] for row in grid for x_0 in range(4)]
        columns = [[grid[y][x] for y in range(6)] for x in range(7)]
        columns_4 = [[column[y_0+y] for y in range(4)] for column in columns for y_0 in range(3)]

        diags_up_4 = [[grid[y_0-k][x_0+k]for k in range(4)] for y_0 in [3, 4, 5] for x_0 in range(4)]
        diags_down_4 = [[grid[y_0+k][x_0+k]for k in range(4)] for y_0 in range(3) for x_0 in range(4)]

        if [player] * 4 in rows_4 or [player] * 4 in columns_4 or [player] * 4 in diags_up_4 or [player] * 4 in diags_down_4:
            return True, 1
        elif not (0 in grid[0]):
            return True, 0
        else:
            return [False]

    def find_best_move(self, depth, player, grid=None):
        other = (2 if player == 1 else 1)
        moves = []
        if grid is None:
            grid = self.grid
            for p in [1, 2]:
                if grid[0][3] == 0:
                    if grid[-1] == [0, 0, 0, 0, 0, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [p, 0, 0, 0, 0, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [0, p, 0, 0, 0, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [0, 0, p, 0, 0, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [0, 0, 0, p, 0, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [0, 0, 0, 0, p, 0, 0]:
                        return [3, None]
                    elif grid[-1] == [0, 0, 0, 0, 0, p, 0]:
                        return [3, None]
                    elif grid[-1] == [0, 0, 0, 0, 0, 0, p]:
                        return [3, None]

        for x in range(7):
            if move_possible(x, grid):
                self.ia_step += 1
                print(self.ia_step, "/", self.sum_step)
                new_grid = deepcopy(grid)
                self.place_coin(player, x, new_grid)
                state = self.is_game_over(player, new_grid)
                if state[0]:
                    score = state[1]
                elif depth > 0:
                    score = 0 - self.find_best_move(depth-1, other, new_grid)[1]
                else:
                    score = 0
                if score == 1:
                    return [x, score]

                moves.append([x, score])

        shuffle(moves)
        moves.sort(key=lambda move: move[1], reverse=True)
        return moves[0]

    def reset(self):
        self.grid = [[0 for _ in range(7)] for _ in range(6)]

    def start_ui(self):
        # font
        font = pygame.font.SysFont('DEBUG_FREE_TRIAL', self.coin_h)
        # texts
        text_ia = font.render("Ia First", True, (0, 0, 0))
        text_p = font.render("P First", True, (0, 0, 0))
        # display text
        self.screen.blit(text_ia, [(self.w-text_ia.get_width())//2, 2*(self.h-text_ia.get_height())//3])
        self.screen.blit(text_p, [(self.w-text_p.get_width())//2, (self.h-text_p.get_height())//3])
        pygame.display.flip()

    def start(self):
        # font
        font = pygame.font.SysFont('DEBUG_FREE_TRIAL', self.coin_h)
        # texts
        text_ia = font.render("Ia First", True, 'cyan')
        text_p = font.render("P First", True, 'purple')

        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]

        if (self.w-text_ia.get_width())//2 <= mouse_x <= (self.w+text_ia.get_width())//2 and \
                2*(self.h-text_ia.get_height())//3 <= mouse_y <= (2*self.h+text_ia.get_height())//3:
            return True, True
        elif (self.w-text_p.get_width())//2 <= mouse_x <= (self.w+text_p.get_width())//2 and \
                (self.h-text_ia.get_height())//3 <= mouse_y <= (self.h+2*text_ia.get_height())//3:
            return True, False
        else:
            return False, False


game = P4()
game.depth = 6
for i in range(game.depth + 1):
    game.sum_step += 7 ** (i + 1)

ia_start = False
start = False
game.screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouse_state = pygame.mouse.get_pressed()
    if start:
        game.player = 1
        if ia_start or (mouse_state[0] and game.place_coin(game.player)):
            ia_start = False
            game.update_ui()
            pygame.time.wait(200)
            if game.is_game_over(game.player)[0]:
                start = False
                game.reset()
            else:
                game.player = 2
                game.ia_step = 0
                move = game.find_best_move(game.depth, game.player)
                game.place_coin(game.player, move[0])

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
                ia_start = True
            else:
                pygame.time.wait(200)

    game.clock.tick(game.game_speed)
