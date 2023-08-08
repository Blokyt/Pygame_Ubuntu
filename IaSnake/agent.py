import torch
import random
import numpy as np
from collections import deque
from snake import SnakeGameIA, Point
from model import Linear_QNet, QTrainer


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(26, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.head

        point_l = Point(head.x - game.tile_size, head.y)
        point_r = Point(head.x + game.tile_size, head.y)
        point_u = Point(head.x, head.y - game.tile_size)
        point_d = Point(head.x, head.y + game.tile_size)

        point2_l = Point(head.x - 2*game.tile_size, head.y)
        point2_r = Point(head.x + 2*game.tile_size, head.y)
        point2_u = Point(head.x, head.y - 2*game.tile_size)
        point2_d = Point(head.x, head.y + 2*game.tile_size)

        point3_l = Point(head.x - 3 * game.tile_size, head.y)
        point3_r = Point(head.x + 3 * game.tile_size, head.y)
        point3_u = Point(head.x, head.y - 3 * game.tile_size)
        point3_d = Point(head.x, head.y + 3 * game.tile_size)

        point4_l = Point(head.x - 4 * game.tile_size, head.y)
        point4_r = Point(head.x + 4 * game.tile_size, head.y)
        point4_u = Point(head.x, head.y - 4 * game.tile_size)
        point4_d = Point(head.x, head.y + 4 * game.tile_size)

        point5_l = Point(head.x - 5 * game.tile_size, head.y)
        point5_r = Point(head.x + 5 * game.tile_size, head.y)
        point5_u = Point(head.x, head.y - 5 * game.tile_size)
        point5_d = Point(head.x, head.y + 5 * game.tile_size)

        point6_l = Point(head.x - 6 * game.tile_size, head.y)
        point6_r = Point(head.x + 6 * game.tile_size, head.y)
        point6_u = Point(head.x, head.y - 6 * game.tile_size)
        point6_d = Point(head.x, head.y + 6 * game.tile_size)
        
        dir_l = game.direction == (-game.tile_size, 0) # Direction.LEFT
        dir_r = game.direction == (game.tile_size, 0) # Direction.RIGHT
        dir_u = game.direction == (0, -game.tile_size) # Direction.UP
        dir_d = game.direction == (0, game.tile_size) # Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger straight 2
            (dir_r and game.is_collision(point2_r)) or
            (dir_l and game.is_collision(point2_l)) or
            (dir_u and game.is_collision(point2_u)) or
            (dir_d and game.is_collision(point2_d)),

            # Danger straight 3
            (dir_r and game.is_collision(point3_r)) or
            (dir_l and game.is_collision(point3_l)) or
            (dir_u and game.is_collision(point3_u)) or
            (dir_d and game.is_collision(point3_d)),

            # Danger straight 4
            (dir_r and game.is_collision(point4_r)) or
            (dir_l and game.is_collision(point4_l)) or
            (dir_u and game.is_collision(point4_u)) or
            (dir_d and game.is_collision(point4_d)),

            # Danger straight 5
            (dir_r and game.is_collision(point5_r)) or
            (dir_l and game.is_collision(point5_l)) or
            (dir_u and game.is_collision(point5_u)) or
            (dir_d and game.is_collision(point5_d)),

            # Danger straight 6
            (dir_r and game.is_collision(point6_r)) or
            (dir_l and game.is_collision(point6_l)) or
            (dir_u and game.is_collision(point6_u)) or
            (dir_d and game.is_collision(point6_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger right 2
            (dir_u and game.is_collision(point2_r)) or
            (dir_d and game.is_collision(point2_l)) or
            (dir_l and game.is_collision(point2_u)) or
            (dir_r and game.is_collision(point2_d)),

            # Danger right 3
            (dir_u and game.is_collision(point3_r)) or
            (dir_d and game.is_collision(point3_l)) or
            (dir_l and game.is_collision(point3_u)) or
            (dir_r and game.is_collision(point3_d)),

            # Danger right 4
            (dir_u and game.is_collision(point4_r)) or
            (dir_d and game.is_collision(point4_l)) or
            (dir_l and game.is_collision(point4_u)) or
            (dir_r and game.is_collision(point4_d)),

            # Danger right 5
            (dir_u and game.is_collision(point5_r)) or
            (dir_d and game.is_collision(point5_l)) or
            (dir_l and game.is_collision(point5_u)) or
            (dir_r and game.is_collision(point5_d)),

            # Danger right 6
            (dir_u and game.is_collision(point6_r)) or
            (dir_d and game.is_collision(point6_l)) or
            (dir_l and game.is_collision(point6_u)) or
            (dir_r and game.is_collision(point6_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),

            # Danger left 2
            (dir_d and game.is_collision(point2_r)) or
            (dir_u and game.is_collision(point2_l)) or
            (dir_r and game.is_collision(point2_u)) or
            (dir_l and game.is_collision(point2_d)),

            # Danger left 3
            (dir_d and game.is_collision(point3_r)) or
            (dir_u and game.is_collision(point3_l)) or
            (dir_r and game.is_collision(point3_u)) or
            (dir_l and game.is_collision(point3_d)),

            # Danger left 4
            (dir_d and game.is_collision(point4_r)) or
            (dir_u and game.is_collision(point4_l)) or
            (dir_r and game.is_collision(point4_u)) or
            (dir_l and game.is_collision(point4_d)),

            # Danger left 5
            (dir_d and game.is_collision(point5_r)) or
            (dir_u and game.is_collision(point5_l)) or
            (dir_r and game.is_collision(point5_u)) or
            (dir_l and game.is_collision(point5_d)),

            # Danger left 6
            (dir_d and game.is_collision(point6_r)) or
            (dir_u and game.is_collision(point6_l)) or
            (dir_r and game.is_collision(point6_u)) or
            (dir_l and game.is_collision(point6_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    agent.model.load()
    game = SnakeGameIA()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            total_score += score
            mean_score = round(total_score / agent.n_games)

            print('Game', agent.n_games, 'Score', score, 'Record:', record, 'Mean:', mean_score)



if __name__ == '__main__':
    train()