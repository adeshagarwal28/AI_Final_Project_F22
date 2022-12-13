import time
import numpy as np
import pygame
import sys
import os
from keras import Sequential, layers
from keras.optimizers import Adam
from keras.layers import Dense
from collections import deque


from DQN import DeepQNetwork
from Tennis import tennis


from pygame.locals import *
pygame.init()


# initialize the 2 Players.
PlayerA = DeepQNetwork()
PlayerB = DeepQNetwork()


if __name__ == "__main__":
    tennis = tennis(FramesPerSecond=70)
    tennis.reset()
    tennis.render()
