from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque
import numpy as np

class DeepQNetwork:
    def __init__(self):
        self.learning_rate = 0.001
        self.momentum = 0.95
        self.eps_min = 0.1
        self.eps_max = 1.0
        self.eps_decay_steps = 2000000
        self.replay_memory_size = 500
        self.replay_memory = deque([], maxlen=self.replay_memory_size)
        self.training_start = 10000 # start training after 10,000 game iterations
        self.training_interval = 4 
        self.save_steps = 1000 # save the model
        self.copy_steps = 10000 # copy DQN to target DQN 
        self.discount_rate = 0.99
        self.skip_start = 90 # Skip the start of every game
        self.batch_size = 100
        self.iteration = 0 # game itr
        self.done = True # env reset
        
        self.model = self.DQNmodel()
        
        return

    def DQNmodel(self):
        model = Sequential()
        model.add(Dense(64, input_shape=(1,), activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(10, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=self.learning_rate))
        return model

    
    def sample_memories(self, batch_size):
        indices = np.random.permutation(len(self.replay_memory))[:batch_size]
        cols = [[], [], [], [], []] # state, action, reward, next_state, continue
        for idx in indices:
            memory = self.replay_memory[idx]
            for col, value in zip(cols, memory):
                col.append(value)
        cols = [np.array(col) for col in cols]
        return (cols[0], cols[1], cols[2].reshape(-1, 1), cols[3],cols[4].reshape(-1, 1))


    def epsilon_greedy(self, q_values, step):
        self.epsilon = max(self.eps_min, self.eps_max - (self.eps_max-self.eps_min) * step/self.eps_decay_steps)
        if np.random.rand() < self.epsilon:
            return np.random.randint(10) # random action
        else:
            return np.argmax(q_values) # optimal action