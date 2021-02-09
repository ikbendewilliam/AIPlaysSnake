import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_r
import game
import model
import numpy as np

version = 'newModel'
board_size = 4
screen_size = 512
block_size = screen_size / board_size
manual = False
interval_time = 0.25

pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Snake')
pygame.mouse.set_visible(0)
pygame.display.flip()
clock = pygame.time.Clock()
playing = True
env = game.Game(board_size)
rl_model = model.RLModel(version=version)
env.draw(screen)
action = -1
action_time = 0
font = pygame.font.SysFont(None, 24)
score = 0
maxscore = 0

while playing:
    clock.tick(60)
    action_time += 1 / 60
    if action_time > interval_time:
        action_time -= interval_time
        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    env.clear_board()
                elif event.key == K_ESCAPE:
                    playing = False
                elif event.key == K_UP:
                    action = 0
                elif event.key == K_LEFT:
                    action = 1
                elif event.key == K_DOWN:
                    action = 2
                elif event.key == K_RIGHT:
                    action = 3
        done = False
        if not manual:
            action = np.argmax(rl_model.predict(env.get_board())[0])
        if action >= 0:
            _, _, done = env.step(action)
        env.draw(screen)
        score = len(env.snake) - 2
        if score > maxscore:
            maxscore = score
        txt = font.render('Score: {}'.format(score), True, (0, 0, 0))
        screen.blit(txt, (20, 20))
        txt = font.render('Max score: {}'.format(maxscore), True, (0, 0, 0))
        screen.blit(txt, (20, 40))
        if done:
            env.clear_board()
            action = -1
        pygame.display.flip()
