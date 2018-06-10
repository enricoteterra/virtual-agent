import random
import json
import time

class RandomPolicyAgent(object):

    """ creates a random action sequence without regard for previous experience or current state. """

    def __init__(self, r):

        # redis connection
        self.r = r
        self.p = self.r.pubsub()

        self.possibleActions = [
            'lookLeft', 'lookUp', 'lookRight', 'lookDown',
            'moveLeft', 'moveForward', 'moveRight', 'moveBack'
        ]


    def generateActionSequence(self, steps=10, baseMovementFactor=1.0):

        actionSequence = []

        for step in range(0, steps):

            choice = random.choice(self.possibleActions)
            actionSequence.append({
                'action': choice,
                'actuator': choice[:4],
                'direction': choice[4:].lower(),
                'factor': random.uniform(0, 1) * baseMovementFactor
            })

        return {'actions' : actionSequence}


    def publishSequence(self, baseMovementFactor=1.0, stepsPerIteration=1):
        self.r.publish('actions', json.dumps(
            self.generateActionSequence(stepsPerIteration, baseMovementFactor)))


    def publishSequenceLoop(self, publishFrequency=1.0, baseMovementFactor=1.0, stepsPerIteration=1):

        while True:

            time.sleep(publishFrequency)
            self.publishSequence(baseMovementFactor, stepsPerIteration)
