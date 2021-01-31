import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt
%matplotlib inline
import pickle
import game
import model

board_size = 8
output_size = 4
hidden_nodes = 16
learning_rate = 1e-3
maximum_discount = .9
random_action_threshold = 0.1
game_max_length = 2000
num_episodes = 1000
save_interval = 100

env = game.Game(board_size)
rlModel = model.RLModel(nodes=[board_size ** 2 * 3, hidden_nodes, output_size], learning_rate=learning_rate)

jList = []
rList = []
for i in range(num_episodes):
    s = env.clear_board()
    rAll = 0
    d = False
    j = 0
    while j < game_max_length:
        j+=1
        s = env.get_board()
        a = np.argmax(rlModel.predict(s)[0])
        if np.random.rand(1) < random_action_threshold:
            a = env.random_action()
        s1, reward, done = env.step(a)
        rlModel.train_single_step(s, s1, a, reward, maximum_discount)
        rAll += reward
        if done:
            break
        random_action_threshold = 1./((i/50) + 10)
    if i % save_interval == 0 and i > 0:
        print('Done {}/{} {:.2f}% Last game length: {}, Average game length: {}, Average length in last {}: {}, average R in last {}: {}'.format(i, num_episodes, i/num_episodes*100,j, sum(jList)/i, save_interval, sum(jList[-save_interval:])/save_interval, save_interval, sum(rList[-save_interval:])/save_interval))
        rlModel.saveVariables()
    jList.append(j)
    rList.append(rAll)
print("Average R: " + str(sum(rList)/num_episodes))
print("Average lenght: " + str(sum(jList)/num_episodes))