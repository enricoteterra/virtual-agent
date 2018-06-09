import random
import json
import time

class RandomPolicyAgent(object):

    """ creates a random action sequence without regard for previous experience or current state. """

    def __init__(self, r):

        # redis connection
        self.r = r
        self.p = self.r.pubsub()


    def generateActionSequence(self, steps=10, baseMovementFactor=1.0):

        possibleActions = [
            'lookLeft', 'lookUp', 'lookRight', 'lookDown',
            'moveLeft', 'moveForward', 'moveRight', 'moveBack'
        ]

        actionSequence = []

        for step in range(0, steps):

            choice = random.choice(possibleActions)
            actionSequence.append({
                'action': choice,
                'type': choice[:4],
                'direction': choice[4:].lower(),
                'factor': random.uniform(0, 1) * baseMovementFactor
            })

        return {'actions' : actionSequence}


    def publishSequence(self, publishFrequency=0.25, baseMovementFactor=0.25, stepsPerIteration=2):

        while True:

            time.sleep(publishFrequency)

            # generate a random step and publish it
            self.r.publish('actions', json.dumps(
                self.generateActionSequence(stepsPerIteration, baseMovementFactor)))
