import numpy as np
import json
import keras
from keras.models import Sequential
from keras.layers import Conv2D

class Agent(object):

    """ learns how to achieve objective by imitation. """

    def __init__(self, r):

        # redis connection
        self.r = r
        self.p = self.r.pubsub()
        self.p.subscribe('percepts') 

        # parameters
        self.model = Sequential()
        self.model.add(Conv2D(
            input_shape=(800, 372, 3),
            filters=2,
            kernel_size=2
        ))

        opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
        self.model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

    def loop(self):

        screenshots = []

        newMessages = True
        while newMessages is True:
            
            message = self.p.get_message()
            if message:
                data = message['data']

                if isinstance(data, basestring):

                    jsonData = json.loads(data)
                    if jsonData['type'] is "screenshot":
                        screenshots.append(json.loads(data))

            else:
                newMessages = False

                # self.model.fit(x_train, y_train,
                #     batch_size=len(screenshots))