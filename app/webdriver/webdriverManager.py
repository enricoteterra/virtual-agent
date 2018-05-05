import time
import redis
import json
from selenium import webdriver
from mouseActuator import MouseActuator
from screenSensor import ScreenSensor
from keyActuator import KeyActuator

class WebDriverManager(object):
    """ manages the selenium webdriver object and performs all interaction with it
        on behalf of the rest of the application. """

    def __init__(self, r):

        # setup selenium chromedriver
        self.browser = webdriver.Chrome('/Users/enrico.t/bin/chromedriver')
        self.browser.set_window_size('400', '300')
        self.browser.set_window_position(0, 0)
        self.browser.get('http://localhost:9615/index.html')

        # setup redis connection
        self.r = r
        self.p = self.r.pubsub()
        self.p.subscribe('actions')  

        self.screen = ScreenSensor(self.browser, self.r)
        self.mouse = MouseActuator(self.browser)
        self.key  = KeyActuator(self.browser)


    def loop(self, frequency=1.0):

        # i = 0
        while True:

            time.sleep(frequency)

            # capture screen
            self.screen.publishScreenshot()
            # i += 1
            # self.browser.save_screenshot('latest ' + str(i) + '.png')

            # listen to actions channel and trigger corresponding actuators
            newMessages = True
            while newMessages is True:

                message = self.p.get_message()
                if message:
                    data = message['data']

                    if isinstance(data, basestring):

                        jsonData = json.loads(data)

                        if 'actions' in jsonData:
                            actions = jsonData['actions']

                            for action in actions:

                                print (action['type'] + action['direction'])

                                if action['type'] == 'look':

                                    if action['direction'] == 'up':
                                        self.mouse.scrollUp(
                                            self.mouse.scaleFactor(action['factor']))

                                    elif action['direction'] == 'down':
                                        self.mouse.scrollDown(
                                            self.mouse.scaleFactor(action['factor']))

                                    elif action['direction'] == 'left':
                                        self.mouse.scrollLeft(
                                            self.mouse.scaleFactor(action['factor']))

                                    elif action['direction'] == 'right':
                                        self.mouse.scrollRight(
                                            self.mouse.scaleFactor(action['factor']))

                                elif action['type'] == 'move':

                                    if action['direction'] == 'forward':
                                        self.key.pressUp(action['factor'])

                                    elif action['direction'] == 'back':
                                        self.key.pressDown(action['factor'])

                                    elif action['direction'] == 'left':
                                        self.key.pressLeft(action['factor'])

                                    elif action['direction'] == 'right':
                                        self.key.pressRight(action['factor'])

                else:
                    newMessages = False