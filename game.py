import random
import pygame

screen_size = 512
background = None

class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.clear_board()
    
    def clear_board(self):
        self.snake = [[2, 2], [2, 1]]
        self.apple = self.random_apple_position()
        self.direction = 3
        self.moves = 0
        self.board = self.get_board()
        # self.boards = []
        return self.board

    def get_board(self):
        board = [[0, 0, 0] for i in range(self.board_size ** 2)]
        for index, pos in enumerate(self.snake[:-1]):
            if index == 0:
                board[pos[0] * self.board_size + pos[1]][0] = 1
            else:
                board[pos[0] * self.board_size + pos[1]][1] = 1
        board[self.snake[-1][0] * self.board_size + self.snake[-1][1]][1] = 0.1
        board[self.apple[0] * self.board_size + self.apple[1]][2] = 1
        return board

    def random_action(self):
        return random.randint(0, 3)

    def random_apple_position(self):
        issue = True
        c = 0
        while issue:
            c += 1
            apple = [random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)]
            issue = self.snake_in_apple(apple)
            if c > self.board_size ** 2 * 3:
                return -1
        return apple
    
    def snake_in_apple(self, apple):
        issue = False
        for pos in self.snake:
            if apple[0] == pos[0] and apple[1] == pos[1]:
                issue = True
        return issue

    def distance_to_apple(self, pos):
        return ((pos[0] - self.apple[0]) ** 2 + (pos[1] - self.apple[1]) ** 2) ** (1 / 2)

    def get_reward(self):
        distance = self.distance_to_apple(self.snake[0])
        last_distance = self.distance_to_apple(self.snake[1])
        if last_distance > distance:
            return 0
        return -1

    def draw(self, screen):
        global background
        if background == None:
            background = pygame.Surface((screen_size, screen_size))
            background = background.convert()
            background.fill((250, 250, 250))
        screen.blit(background, (0, 0))
        self.draw_block(screen, (255, 0, 0), self.apple)
        for pos in self.snake:
            self.draw_block(screen, (0, 255, 0), pos)

    def draw_block(self, screen, color, pos):
        block_size = screen_size / self.board_size
        pygame.draw.rect(screen, color, pygame.Rect(block_size * (pos[1] + 0.1), block_size * (pos[0] + 0.1), block_size * 0.8, block_size * 0.8))

    def step(self, action):
        self.moves += 1
        if action == 0 and self.direction != 2: # Up
            self.direction = 0
        elif action == 1 and self.direction != 3: # Left
            self.direction = 1
        elif action == 2 and self.direction != 0: # Down
            self.direction = 2
        elif action == 3 and self.direction != 1: # Right
            self.direction = 3
        if self.direction == 0:
            self.snake.insert(0, [self.snake[0][0] - 1, self.snake[0][1]])
        elif self.direction == 1:
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] - 1])
        elif self.direction == 2:
            self.snake.insert(0, [self.snake[0][0] + 1, self.snake[0][1]])
        elif self.direction == 3:
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] + 1])
        done = False
        won = False

        if self.snake_in_apple(self.apple):
            self.apple = self.random_apple_position()
            if self.apple == -1:
                won = True
            reward = 10
        else:
            self.snake = self.snake[:-1]
            reward = self.get_reward()

        for pos in self.snake[1:]:
            if self.snake[0][0] == pos[0] and self.snake[0][1] == pos[1]:
                done = True
        if done or self.snake[0][0] < 0 or self.snake[0][0] >= self.board_size or self.snake[0][1] < 0 or self.snake[0][1] >= self.board_size:
            done = True
            reward = -50
        elif not won:
            self.board = self.get_board()
        if won:
            return self.board, 100, True
        return self.board, reward, done
        


