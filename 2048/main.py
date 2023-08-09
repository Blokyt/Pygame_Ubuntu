from random import shuffle
from copy import deepcopy
import pygame

pygame.init()


class game:

    def __init__(self):
        self.w = 800
        self.h = 800
        self.case_w = self.w // 4
        self.case_h = self.h // 4
        self.space = 15

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.clock = pygame.time.Clock()
        self.depth = 0
        self.case = 2

    def display(self):
        # font
        font = pygame.font.SysFont('DEBUG_FREE_TRIAL', self.case_h // 2)

        self.screen.fill((0, 0, 0))
        for y in range(4):
            for x in range(4):
                color = (255, 255, 255)
                if self.grid[y][x] != 0:
                    color = (255*(1-1/(self.grid[y][x]) ** (1 / 4)), 255 / (2*self.grid[y][x] ** (1 / 4)), 255 / (2*self.grid[y][x] ** (1 / 4)))

                rect = pygame.Rect(x * self.case_w + self.space, y * self.case_h + self.space,
                                   self.case_w - 2 * self.space, self.case_h - 2 * self.space)
                pygame.draw.rect(self.screen, color, rect)
                if self.grid[y][x] != 0:
                    text = font.render(str(self.grid[y][x]), True, (0, 0, 0))
                    game.screen.blit(text, [x * self.case_w + (self.case_w - text.get_width()) // 2,
                                            y * self.case_h + (self.case_h - text.get_height()) // 2])

        pygame.display.flip()

    def spawn_case(self, grid=None, case=None):
        if grid is None:
            grid = self.grid
        if case is None:
            case = self.case
            self.case = (2 if self.case == 4 else 4)
        if 0 in [elem for line in grid for elem in line]:
            for y in range(4):
                for x in range(4):
                    if grid[y][x] == 0:
                        grid[y][x] = case
                        return
        else:
            return

    def move_down(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_moved = False
        for y in range(1, 4):
            for x in range(4):
                if grid[3 - y][x] != 0:
                    for y_0 in range(y):
                        if grid[3 - y_0][x] == 0:
                            if not check:
                                grid[3 - y_0][x], grid[3 - y][x] = grid[3 - y][x], 0
                            has_moved = True
        return has_moved

    def mix_down(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_mixed = False
        for y in range(3):
            for x in range(4):
                if grid[3 - y][x] != 0 and grid[3 - y][x] == grid[2 - y][x]:
                    if not check:
                        grid[3 - y][x], grid[2 - y][x] = 2 * grid[3 - y][x], 0
                    has_mixed = True
        return has_mixed

    def move_up(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_moved = False
        for y in range(1, 4):
            for x in range(4):
                if grid[y][x] != 0:
                    for y_0 in range(y):
                        if grid[y_0][x] == 0:
                            if not check:
                                grid[y_0][x], grid[y][x] = grid[y][x], 0
                            has_moved = True
        return has_moved

    def mix_up(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_mixed = False
        for y in range(3):
            for x in range(4):
                if grid[y][x] != 0 and grid[y][x] == grid[y + 1][x]:
                    if not check:
                        grid[y][x], grid[y + 1][x] = 2 * grid[y][x], 0
                    has_mixed = True
        return has_mixed

    def move_left(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_moved = False
        for x in range(1, 4):
            for y in range(4):
                if grid[y][x] != 0:
                    for x_0 in range(x):
                        if grid[y][x_0] == 0:
                            if not check:
                                grid[y][x_0], grid[y][x] = grid[y][x], 0
                            has_moved = True
        return has_moved

    def mix_left(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_mixed = False
        for x in range(3):
            for y in range(4):
                if grid[y][x] != 0 and grid[y][x] == grid[y][x + 1]:
                    if not check:
                        grid[y][x], grid[y][x + 1] = 2 * grid[y][x], 0
                    has_mixed = True
        return has_mixed

    def move_right(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_moved = False
        for x in range(1, 4):
            for y in range(4):
                if grid[y][3 - x] != 0:
                    for x_0 in range(x):
                        if grid[y][3 - x_0] == 0:
                            if not check:
                                grid[y][3 - x_0], grid[y][3 - x] = grid[y][3 - x], 0
                            has_moved = True
        return has_moved

    def mix_right(self, check=False, grid=None):
        if grid is None:
            grid = self.grid
        has_mixed = False
        for x in range(3):
            for y in range(4):
                if grid[y][3 - x] != 0 and grid[y][3 - x] == grid[y][2 - x]:
                    if not check:
                        grid[y][3 - x], grid[y][2 - x] = 2 * grid[y][3 - x], 0
                    has_mixed = True
        return has_mixed

    def score(self):
        score = 0
        for y in range(4):
            for x in range(4):
                score += self.grid[y][x]
        return score

    def find_best_move(self, depth, grid=None, case=None):
        if grid is None:
            grid = self.grid
        if case is None:
            case = self.case
        other_case = (2 if case == 4 else 4)
        moves = []
        dirs = ['up', 'down', 'left', 'right']
        for direction in dirs:
            new_grid = deepcopy(grid)
            if direction == 'up':
                has_moved, has_mixed = up(new_grid)
            elif direction == 'down':
                has_moved, has_mixed = down(new_grid)
            elif direction == 'left':
                has_moved, has_mixed = left(new_grid)
            else:
                has_moved, has_mixed = right(new_grid)
            if has_moved or has_mixed:
                game.spawn_case(new_grid, case)
                if depth > 0:
                    score = self.find_best_move(depth - 1, new_grid, other_case)[1]
                else:
                    score = zeros(new_grid)
            else:
                score = -1
            moves.append([direction, score])

        shuffle(moves)
        moves.sort(key=lambda move_: move_[1], reverse=True)
        return moves[0]


def zeros(grid):
    zero = 0
    for y in range(4):
        for x in range(4):
            if grid[y][x] == 0:
                zero += 1
    return zero


def up(grid=None):
    if grid is None:
        grid = game.grid
    has_moved = game.move_up(False, grid)
    if not ia:
        game.display()
        if has_moved:
            pygame.time.wait(delay)
    has_mixed = game.mix_up(False, grid)
    game.move_up(False, grid)
    return has_moved, has_mixed


def down(grid=None):
    if grid is None:
        grid = game.grid
    has_moved = game.move_down(False, grid)
    if not ia:
        game.display()
        if has_moved:
            pygame.time.wait(delay)
    has_mixed = game.mix_down(False, grid)
    game.move_down(False, grid)
    return has_moved, has_mixed


def left(grid=None):
    if grid is None:
        grid = game.grid
    has_moved = game.move_left(False, grid)
    if not ia:
        game.display()
        if has_moved:
            pygame.time.wait(delay)
    has_mixed = game.mix_left(False, grid)
    game.move_left(False, grid)
    return has_moved, has_mixed


def right(grid=None):
    if grid is None:
        grid = game.grid
    has_moved = game.move_right(False, grid)
    if not ia:
        game.display()
        if has_moved:
            pygame.time.wait(delay)
    has_mixed = game.mix_right(False, grid)
    game.move_right(False, grid)
    return has_moved, has_mixed


game = game()
game.spawn_case()
game_over = False
moved = False
mixed = False
ia = True
delay = (0 if ia else 50)
max_depth = 8

while not game_over:
    game.depth = max_depth - zeros(game.grid)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not ia and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                moved, mixed = up()
            elif event.key == pygame.K_s:
                moved, mixed = down()
            elif event.key == pygame.K_q:
                moved, mixed = left()
            elif event.key == pygame.K_d:
                moved, mixed = right()

    if ia:
        move = game.find_best_move(game.depth)
        if move[0] == 'up':
            moved, mixed = up()
        elif move[0] == 'down':
            moved, mixed = down()
        elif move[0] == 'left':
            moved, mixed = left()
        else:
            moved, mixed = right()

    if moved or mixed:
        game.display()
        pygame.time.wait(delay)
        game.spawn_case()
        moved = False
        mixed = False
    elif not (0 in [elem for line in game.grid for elem in line]):
        if not game.mix_up(True) and not game.mix_down(True) and not game.mix_left(True) and not game.mix_right(True):
            game_over = True
            input(game.score())

    game.display()
