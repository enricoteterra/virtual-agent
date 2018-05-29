# pylint: disable=E0633

import random
import json
import time
import keras
import numpy as np

class DqnAgent(object):

    """ defines a dqn-based agent. based on: 
        https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c 
        (customised to use our virtual environment)"""

    def __init__(self, r):

        # redis connection
        self.r = r
        self.p = self.r.pubsub()

        # store of all encountered states
        self.memory = []

        # future rewards depreciation factor
        self.gamma = 0.95

        # exploration vs exploitation factor
        self.epsilon = 1.0
        self.epsilon_min = 0.01

        # tendency to explore decays a little with every step
        self.epsilon_decay = 0.995

        # standard learning rate param
        self.learningRate = 0.01

        # model to predict the next action to take
        self.model = self.create_model()

        # model to predict what would be the best action
        self.targetModel = self.create_model()

    def create_model(self):

        model = keras.models.Sequential()
        stateShape = (800, 372, 3)
        nOutputs = 8

        model.add(keras.layers.Dense(24, input_dim=stateShape[0], 
            activation="relu"))
        model.add(keras.layers.Dense(48, activation="relu"))
        model.add(keras.layers.Dense(24, activation="relu"))
        model.add(keras.layers.Dense(nOutputs))
        model.compile(
            loss="mean_squared_error",
            optimizer=keras.optimizers.Adam(lr=self.learningRate))
        return model


    def remember(self, state, action, reward, newState, done):

        """ store a step in memory to be used for training later. """

        self.memory.append([state, action, reward, newState, done])


    def replay(self):

        batchSize = 32

        if len(self.memory) < batchSize: 
            return

        samples = random.sample(self.memory, batchSize)

        for sample in samples:

            state, action, reward, newState, done = sample

            # predict the next action based on current state
            target = self.targetModel.predict(state)

            if done:

                target[0][action] = reward

            else:

                futureQ = max(
                    self.targetModel.predict(newState)[0])

                target[0][action] = reward + futureQ * self.gamma

            self.model.fit(state, target, epochs=1, verbose=0)


    def target_train(self):

        weights = self.model.get_weights()
        targetWeights = self.targetModel.get_weights()

        for i in range(len(targetWeights)):
            targetWeights[i] = weights[i]

        self.targetModel.set_weights(targetWeights)


    def act(self, state):

        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)

        # roll on exploit or explore
        if np.random.random() < self.epsilon:

            # decided on explore
            # TODO replace
            return self.env.action_space.sample()

        # decided on exploit
        return np.argmax(self.model.predict(state)[0])


    def main():
        env     = gym.make("MountainCar-v0")    # TODO replace
        gamma   = 0.9
        epsilon = .95
        trials  = 100
        trial_len = 500
        updateTargetNetwork = 1000
        dqn_agent = DQN(env=env)
        steps = []
        for trial in range(trials):
            cur_state = env.reset().reshape(1,2)
            for step in range(trial_len):
                action = dqn_agent.act(cur_state)
                env.render()
                new_state, reward, done, _ = env.step(action)
                reward = reward if not done else -20
                print(reward)
                new_state = new_state.reshape(1,2)
                dqn_agent.remember(cur_state, action, 
                    reward, new_state, done)
                
                dqn_agent.replay()
                dqn_agent.target_train()
                cur_state = new_state
                if done:
                    break
            if step >= 199:
                print("Failed to complete trial")
            else:
                print("Completed in {} trials".format(trial))
                break