import pygame
from random import randrange
pygame.init()


class Game:

    def __init__(self):
        self.resolution = 800
        self.tile_size = 50
        self.screen = pygame.display.set_mode((self.resolution, self.resolution+self.tile_size))
        pygame.display.set_caption('SnakeGame')
        self.clock = pygame.time.Clock()
        self.time_speed = 60
        self.time_ref = 0
        self.food_sound = pygame.mixer.Sound('food.wav')
        self.self_eating_sound = pygame.mixer.Sound('self_eating.wav')
        self.new_best_score_sound = pygame.mixer.Sound('new_best_score.wav')
        self.food_sound.set_volume(0.1)
        self.self_eating_sound.set_volume(0.2)
        self.new_best_score_sound.set_volume(0.1)

    def get_random_position(self):
        range = (self.tile_size // 2, self.resolution - self.tile_size // 2, self.tile_size)
        return randrange(*range), randrange(*range)


game = Game()


class Snake:
    def __init__(self):
        self.snake = pygame.rect.Rect(0, 0, game.tile_size-2, game.tile_size-2)
        self.snake.center = game.get_random_position()
        self.length = 1
        self.score = 0
        self.best_score = 0
        self.segments = [self.snake.copy()]
        self.dir = (0, 0)
        self.moved = False

    def reset(self):
        game.self_eating_sound.play()
        self.snake.center = game.get_random_position()
        self.length = 1
        self.score = 0
        self.segments = [self.snake.copy()]
        self.dir = (0, 0)
        self.moved = False

    def growth(self):
        game.food_sound.play()
        game.food_sound.set_volume(0.2)
        self.length += 1
        self.score += 1

    def update_best_score(self):
        if self.score > self.best_score:
            self.best_score = self.score
        elif self.score == self.best_score:
            game.new_best_score_sound.play()
            game.food_sound.set_volume(0)

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(game.screen, 'green', segment)

    def move(self):
        self.segments.append(self.snake.copy())
        self.snake.move_ip(snake.dir)
        self.segments = self.segments[-self.length:]
        self.moved = True

    def check(self):
        is_self_eating = pygame.Rect.collidelist(self.snake, self.segments[:-1]) != -1
        return self.snake.left < 0 or self.snake.right > game.resolution or self.snake.top < 0 or self.snake.bottom > \
            game.resolution or is_self_eating


snake = Snake()


class Food:
    def __init__(self):
        self.food = pygame.rect.Rect(0, 0, game.tile_size-2, game.tile_size-2)
        self.food.center = game.get_random_position()
        self.check()

    def reset(self):
        self.food.center = game.get_random_position()

    def check(self):
        collide = False
        while pygame.Rect.collidelist(self.food, snake.segments) != -1:
            self.reset()
            collide = True
        return collide

    def draw(self):
        pygame.draw.rect(game.screen, 'red', self.food)


food = Food()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if snake.moved and event.key == pygame.K_z and snake.dir != (0, game.tile_size):
                snake.dir = (0, -game.tile_size)
                snake.moved = False
            elif snake.moved and event.key == pygame.K_s and snake.dir != (0, -game.tile_size):
                snake.dir = (0, game.tile_size)
                snake.moved = False
            elif snake.moved and event.key == pygame.K_q and snake.dir != (game.tile_size, 0):
                snake.dir = (-game.tile_size, 0)
                snake.moved = False
            elif snake.moved and event.key == pygame.K_d and snake.dir != (-game.tile_size, 0):
                snake.dir = (game.tile_size, 0)
                snake.moved = False

    game.screen.fill('black')

    # check food
    if food.check():
        snake.update_best_score()
        snake.growth()

    # draw snake
    snake.draw()

    # check borders and self_eating
    if snake.check():
        snake.reset()
        food.reset()

    # draw score and best_score
    background_rect = pygame.rect.Rect(0, game.resolution, game.resolution, game.tile_size)
    pygame.draw.rect(game.screen, 'white', background_rect)
    # font
    font = pygame.font.SysFont('black_chancery', game.tile_size)
    # texts
    text_score = font.render("Score : "+str(snake.score), True, 'black')
    text_best_score = font.render(" / Best Score : "+str(snake.best_score), True, 'black')
    # display text
    game.screen.blit(text_score, [10, game.resolution + 10])
    game.screen.blit(text_best_score, [10+text_score.get_width(), game.resolution+10])
    # draw food
    food.draw()

    # time
    time = pygame.time.get_ticks()
    if time - game.time_ref >= game.time_speed:
        game.time_ref = time

        # move snake
        snake.move()

    pygame.display.flip()
    game.clock.tick(60)
