import tensorflow as tf
import pickle
import numpy as np

class RLModel:
    def __init__(self, version = None, nodes = [], learning_rate = 1e-3):
        if version is not None:
            self.retrieveVariables(version)
        elif len(nodes) >= 2:
            self.learning_rate = learning_rate
            self.create_model(nodes)
        else:
            raise Exception('Incorrect filename or nodes provided')
    
    def create_model(self, nodes):
        layers = [tf.keras.layers.Input((nodes[0],))]
        for node in nodes[1:-1]:
            layers.append(tf.keras.layers.Dense(node, activation='relu'))
        layers.append(tf.keras.layers.Dense(nodes[-1]))
        self.model = tf.keras.Sequential(layers)
        self.model.compile(loss='mse', optimizer=tf.optimizers.Adam(self.learning_rate))

    def predict(self, board):
        return self.model.predict(np.array(board).reshape(1, -1))
    
    def train_single_step(self, state0, state1, a, reward, maximum_discount):
        Q0 = self.predict(state0)
        Q1 = np.argmax(self.predict(state1)[0])
        Q0[0][a] = reward + maximum_discount * Q1
        self.model.fit(np.array(state0).reshape(1, -1), Q0, epochs=1, verbose=0)

    def retrieveVariables(self, version):
        self.model = tf.keras.models.load_model('{}.h5'.format(version))

    def saveVariables(self):
        self.model.save('newModel.h5')
