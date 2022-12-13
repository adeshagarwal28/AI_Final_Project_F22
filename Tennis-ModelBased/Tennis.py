import time
import os
import sys
from DQN import DeepQNetwork
from Regression import Networking
import numpy as np
from keras.utils import to_categorical
import tensorflow as tf
import pygame
from pygame.locals import *
pygame.init()


class tennis:
    def __init__(self, FramesPerSecond=50):
        self.GeneralReward = False
        self.net = Networking(150, 450, 100, 600)
        self.updateRewardA = 0
        self.updateRewardB = 0
        self.updateIter = 0
        self.lossA = 0
        self.lossB = 0
        self.restart = False

        self.AgentA = DeepQNetwork()
        self.AgentB = DeepQNetwork()

        self.net = Networking(150, 450, 100, 600)
        self.NetworkA = self.net.net(
            300, sourceYvalue=100, newYvalue=600) 
        self.NetworkB = self.net.net(
            200, sourceYvalue=600, newYvalue=100)  

        pygame.init()
        self.BLACK = (0, 0, 0)

        self.myFontA = pygame.font.SysFont("Times New Roman", 25)
        self.myFontB = pygame.font.SysFont("Times New Roman", 25)
        self.myFontIter = pygame.font.SysFont('Times New Roman', 25)

        self.FramesPerSecond = FramesPerSecond
        self.FramesPerSecondClock = pygame.time.Clock()

    def windowSet(self):
        # set the window
        self.BOARDDISPLAY = pygame.display.set_mode((600, 700), 0, 32)
        pygame.display.set_caption(
            'TABLE TENNIS- REINFORCEMENT LEARNING (DQN)')
        # set the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        return

    def show(self):
        self.windowSet()
        self.BOARDDISPLAY.fill(self.WHITE)
        pygame.draw.rect(self.BOARDDISPLAY, self.BLUE, (150, 100, 300, 500))
        pygame.draw.rect(self.BOARDDISPLAY, self.BLACK, (150, 340, 300, 20))
        pygame.draw.rect(self.BOARDDISPLAY, self.RED, (0, 20, 600, 20))
        pygame.draw.rect(self.BOARDDISPLAY, self.RED, (0, 660, 600, 20))
        return

    def reset(self):
        return

    def evaluateState(self, c):
        if c >= 150 and c <= 179:
            return 0
        elif c >= 180 and c <= 209:
            return 1
        elif c >= 210 and c <= 239:
            return 2
        elif c >= 240 and c <= 269:
            return 3
        elif c >= 270 and c <= 299:
            return 4
        elif c >= 300 and c <= 329:
            return 5
        elif c >= 330 and c <= 359:
            return 6
        elif c >= 360 and c <= 389:
            return 7
        elif c >= 390 and c <= 419:
            return 8
        elif c >= 420 and c <= 450:
            return 9

    def actionEval(self, diff):

        if (int(diff) <= 30):
            return True
        else:
            return False

    def valRandom(self, action):
        if action == 0:
            val = np.random.choice([i for i in range(150, 180)])
        elif action == 1:
            val = np.random.choice([i for i in range(180, 210)])
        elif action == 2:
            val = np.random.choice([i for i in range(210, 240)])
        elif action == 3:
            val = np.random.choice([i for i in range(240, 270)])
        elif action == 4:
            val = np.random.choice([i for i in range(270, 300)])
        elif action == 5:
            val = np.random.choice([i for i in range(300, 330)])
        elif action == 6:
            val = np.random.choice([i for i in range(330, 360)])
        elif action == 7:
            val = np.random.choice([i for i in range(360, 390)])
        elif action == 8:
            val = np.random.choice([i for i in range(390, 420)])
        else:
            val = np.random.choice([i for i in range(420, 450)])
        return val

    def stepFirst(self, action, counter=0):
        # playerA should play
        if counter == 0:
            self.NetworkA = self.net.net(
                self.ballx, sourceYvalue=100, newYvalue=600)  # Network A
            self.bally = self.NetworkA[1][counter]
            self.ballx = self.NetworkA[0][counter]

            if self.GeneralReward == True:
                self.playerax = self.valRandom(action)
            else:
                self.playerax = self.ballx


        else:
            self.ballx = self.NetworkA[0][counter]
            self.bally = self.NetworkA[1][counter]

        obsOne = self.evaluateState(
            int(self.ballx))  # last state
        obsTwo = self.evaluateState(
            int(self.playerbx))  # eval player bx
        diff = np.abs(self.ballx - self.playerbx)
        obs = obsTwo
        reward = self.actionEval(diff)
        done = True
        info = str(diff)

        return obs, reward, done, info

    def stepSecond(self, action, counter=0):
        # playerB should play
        if counter == 0:
            self.NetworkB = self.net.net(
                self.ballx, sourceYvalue=600, newYvalue=100) 
            self.bally = self.NetworkB[1][counter]
            self.ballx = self.NetworkB[0][counter]

            if self.GeneralReward == True:
                self.playerbx = self.valRandom(action)
            else:
                self.playerbx = self.ballx

        else:
            self.ballx = self.NetworkB[0][counter]
            self.bally = self.NetworkB[1][counter]

        obsOne = self.evaluateState(
            int(self.ballx))  # last state of the ball
        obsTwo = self.evaluateState(
            int(self.playerax))  # evaluate player bx
        diff = np.abs(self.ballx - self.playerax)
        obs = obsTwo
        reward = self.actionEval(diff)
        done = True
        info = str(diff)

        return obs, reward, done, info

    def computeALoss(self, reward):
        if reward == 0:
            self.lossA += 1
        else:
            self.lossA += 0
        return

    def computeBLoss(self, reward):
        if reward == 0:
            self.lossB += 1
        else:
            self.lossB += 0
        return

    def render(self):
        # diplay team agents
        self.PLAYERA = pygame.image.load('Images/player.jpg')
        self.PLAYERA = pygame.transform.scale(self.PLAYERA, (50, 50))
        self.PLAYERB = pygame.image.load('Images/player.jpg')
        self.PLAYERB = pygame.transform.scale(self.PLAYERB, (50, 50))
        self.ball = pygame.image.load('Images/tennisball.png')
        self.ball = pygame.transform.scale(self.ball, (15, 15))

        self.playerax = 150
        self.playerbx = 250

        self.ballx = 250
        self.bally = 300

        counter = 0
        playerNext = 'A'
        obsA, rewardA, doneA, infoA = 0, False, False, ''
        obsB, rewardB, doneB, infoB = 0, False, False, ''
        stateA = 0
        stateB = 0
        next_stateA = 0
        next_stateB = 0

        actionA = 0
        actionB = 0

        itrs = 20000
        itr = 0
        restart = False

        while itr < itrs:

            self.show()
            self.randNumLabelA = self.myFontA.render(
                'A (Win): '+str(self.updateRewardA) + ', A(loss): '+str(self.lossA), 1, self.BLACK)
            self.randNumLabelB = self.myFontB.render(
                'B (Win): '+str(self.updateRewardB) + ', B(loss): ' + str(self.lossB), 1, self.BLACK)
            self.randNumLabelIter = self.myFontIter.render(
                'Iterations: '+str(self.updateIter), 1, self.BLACK)

            if playerNext == 'A':

                if counter == 0:
                    q_valueA = self.AgentA.model.predict([stateA])
                    actionA = self.AgentA.epsilon_greedy(q_valueA, itr)

                    # Online DQN plays
                    obsA, rewardA, doneA, infoA = self.stepFirst(
                        action=actionA, counter=counter)
                    next_stateA = actionA

                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))
                    stateA = next_stateA

                elif counter == 49:
                    q_valueA = self.AgentA.model.predict([stateA])
                    actionA = self.AgentA.epsilon_greedy(q_valueA, itr)
                    obsA, rewardA, doneA, infoA = self.stepFirst(
                        action=actionA, counter=counter)
                    next_stateA = actionA

                    self.updateRewardA += rewardA
                    self.computeALoss(rewardA)

                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))

                    # restart the game if player A fails to get the ball
                    if rewardA == 0:
                        self.restart = True
                        time.sleep(0.5)
                        playerNext = 'B'
                        self.GeneralReward = False
                    else:
                        self.restart = False
                        self.GeneralReward = True

                    # Sample memories
                    X_state_val, X_action_val, rewards, X_next_state_val, continues = (
                        self.AgentA.sample_memories(self.AgentA.batch_size))
                    next_q_values = self.AgentA.model.predict(
                        [X_next_state_val])
                    max_next_q_values = np.max(
                        next_q_values, axis=1, keepdims=True)
                    y_val = rewards + continues * self.AgentA.discount_rate * max_next_q_values

                    # Train the online DQN
                    self.AgentA.model.fit(X_state_val, tf.keras.utils.to_categorical(
                        X_next_state_val, num_classes=10), verbose=0)

                    playerNext = 'B'
                    self.updateIter += 1

                    counter = 0
                else:
                    q_valueA = self.AgentA.model.predict([stateA])
                    actionA = self.AgentA.epsilon_greedy(q_valueA, itr)

                    # Online DQN plays
                    obsA, rewardA, doneA, infoA = self.stepFirst(
                        action=actionA, counter=counter)
                    next_stateA = actionA

                    self.AgentA.replay_memory.append(
                        (stateA, actionA, rewardA, next_stateA, 1.0 - doneA))
                    stateA = next_stateA

                if playerNext == 'A':
                    counter += 1
                else:
                    counter = 0

            else:
                if counter == 0:
                    q_valueB = self.AgentB.model.predict([stateB])
                    actionB = self.AgentB.epsilon_greedy(q_valueB, itr)

                    # Online DQN plays
                    obsB, rewardB, doneB, infoB = self.stepSecond(
                        action=actionB, counter=counter)
                    next_stateB = actionB

                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))
                    stateB = next_stateB

                elif counter == 49:

                    q_valueB = self.AgentB.model.predict([stateB])
                    actionB = self.AgentB.epsilon_greedy(q_valueB, itr)

                    # Online DQN plays
                    obs, reward, done, info = self.stepSecond(
                        action=actionB, counter=counter)
                    next_stateB = actionB

                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))

                    stateB = next_stateB
                    self.updateRewardB += rewardB
                    self.computeBLoss(rewardB)

                    # restart the game if player A fails to get the ball
                    if rewardB == 0:
                        self.restart = True
                        time.sleep(0.5)
                        self.GeneralReward = False
                        playerNext = 'A'
                    else:
                        self.restart = False
                        self.GeneralReward = True

                    # Sample memories
                    X_state_val, X_action_val, rewards, X_next_state_val, continues = (
                        self.AgentB.sample_memories(self.AgentB.batch_size))
                    next_q_values = self.AgentB.model.predict(
                        [X_next_state_val])
                    max_next_q_values = np.max(
                        next_q_values, axis=1, keepdims=True)
                    y_val = rewards + continues * self.AgentB.discount_rate * max_next_q_values

                    # Train the online DQN
                    self.AgentB.model.fit(X_state_val, tf.keras.utils.to_categorical(
                        X_next_state_val, num_classes=10), verbose=0)

                    playerNext = 'A'
                    self.updateIter += 1

                else:
                    q_valueB = self.AgentB.model.predict([stateB])
                    actionB = self.AgentB.epsilon_greedy(q_valueB, itr)

                    # Online DQN plays
                    obsB, rewardB, doneB, infoB = self.stepSecond(
                        action=actionB, counter=counter)
                    next_stateB = actionB

                    self.AgentB.replay_memory.append(
                        (stateB, actionB, rewardB, next_stateB, 1.0 - doneB))
                    tateB = next_stateB

                if playerNext == 'B':
                    counter += 1
                else:
                    counter = 0

            itr += 1

            # CHECK Tennis BALL MOVEMENT
            self.BOARDDISPLAY.blit(self.PLAYERA, (self.playerax, 50))
            self.BOARDDISPLAY.blit(self.PLAYERB, (self.playerbx, 600))
            self.BOARDDISPLAY.blit(self.ball, (self.ballx, self.bally))
            self.BOARDDISPLAY.blit(self.randNumLabelA, (300, 630))
            self.BOARDDISPLAY.blit(self.randNumLabelB, (300, 40))
            self.BOARDDISPLAY.blit(self.randNumLabelIter, (50, 40))

            # update last coordinate
            pygame.display.update()
            self.FramesPerSecondClock.tick(self.FramesPerSecond)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()