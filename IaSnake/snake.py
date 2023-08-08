import pygame
from random import randint
from collections import namedtuple

pygame.init()

Point = namedtuple('Point', 'x, y')


class SnakeGameIA:

    def __init__(self):
        self.width = 800
        self.height = 800
        self.tile_size = 40
        self.game_speed = 10000
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('SnakeGameIA')
        self.clock = pygame.time.Clock()
        self.direction = (self.tile_size, 0)
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]

        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def reset(self):
        self.direction = (self.tile_size, 0)
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head]

        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        x = randint(0, self.width // self.tile_size - 1) * self.tile_size
        y = randint(0, self.height // self.tile_size - 1) * self.tile_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game_speed = 10000
                elif event.key == pygame.K_DOWN:
                    self.game_speed = 20

        self.move(action)
        self.snake.append(self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > (self.width // self.tile_size) ** 2 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake = self.snake[-self.score - 1:]

        self.update_ui()
        self.clock.tick(self.game_speed)

        return reward, game_over, self.score

    def move(self, action):
        directions = [(self.tile_size, 0), (0, self.tile_size), (-self.tile_size, 0), (0, -self.tile_size)]
        dir_id = directions.index(self.direction)
        if action == [0, 1, 0]:
            self.direction = directions[(dir_id + 1) % 4]
        elif action == [0, 0, 1]:
            self.direction = directions[(dir_id - 1) % 4]

        x = self.head.x
        y = self.head.y

        if self.direction == (self.tile_size, 0):
            x += self.tile_size
        elif self.direction == (-self.tile_size, 0):
            x -= self.tile_size
        elif self.direction == (0, self.tile_size):
            y += self.tile_size
        else:
            y -= self.tile_size

        self.head = Point(x, y)

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        if pt.x > self.width - self.tile_size or pt.x < 0 or pt.y > self.height - self.tile_size or pt.y < 0:
            return True

        if pt in self.snake[:-1]:
            return True

        return False

    def update_ui(self):
        self.screen.fill((0, 0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(pt.x, pt.y, self.tile_size, self.tile_size))
            pygame.draw.rect(self.screen, (0, 155, 255),
                             pygame.Rect(pt.x + 5, pt.y + 5, self.tile_size - 10, self.tile_size - 10))

        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(self.food.x, self.food.y, self.tile_size, self.tile_size))

        font = pygame.font.SysFont('black_chancery', self.tile_size)
        text1 = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(text1, [0, 0])
        font = pygame.font.SysFont('black_chancery', self.tile_size)
        text2 = font.render("Speed: " + str(self.game_speed), True, (255, 255, 255))
        self.screen.blit(text2, [self.width - text2.get_width(), 0])
        pygame.display.flip()

        return False
