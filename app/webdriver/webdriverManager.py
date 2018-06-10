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
        self.browser = webdriver.Chrome('chromedriver')
        self.browser.set_window_size('400', '300')
        self.browser.set_window_position(0, 0)
        self.browser.get('http://localhost:9615/index.html')

        if self.browser is None:
            raise ValueError

        # setup redis connection
        self.r = r
        self.p = self.r.pubsub()
        self.p.subscribe('actions')  

        self.screen = ScreenSensor(self.browser, self.r)
        self.mouse = MouseActuator(self.browser)
        self.key  = KeyActuator(self.browser)


    def loop(self, loopFrequency=0.25):

        # i = 0
        while True:

            time.sleep(loopFrequency)

            # capture screen
            self.screen.publishScreenshot()
            # self.browser.save_screenshot('latest ' + str(i) + '.png')

            # listen to actions channel and trigger corresponding actuators
            for msg in self.p.listen():
                if msg is not None and msg["data"] != 1l:
                    data = msg["data"]
                    jsonData = json.loads(data)

                    if 'actions' in jsonData:
                        actions = jsonData['actions']

                        for action in actions:

                            print (action['actuator'] + ' ' \
                                    + action['direction'] + ' ' \
                                    + str(action['factor']))

                            if action['actuator'] == 'look':

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

                            elif action['actuator'] == 'move':

                                if action['direction'] == 'forward':
                                    self.key.pressUp(action['factor'])

                                elif action['direction'] == 'back':
                                    self.key.pressDown(action['factor'])

                                elif action['direction'] == 'left':
                                    self.key.pressLeft(action['factor'])

                                elif action['direction'] == 'right':
                                    self.key.pressRight(action['factor'])
