import time
import redis
from selenium import webdriver
from mouseActuator import MouseActuator
from screenSensor import ScreenSensor
from keyActuator import KeyActuator

class SimpleReflexAgent(object):
    """ an agent without state or goals, just react to last sensor percept. """

    def __init__(self, r):

        # setup selenium chromedriver
        self.browser = webdriver.Chrome('/Users/enrico.t/bin/chromedriver')
        self.browser.set_window_size('400', '300')
        self.browser.set_window_position(0, 0)
        self.browser.get('http://localhost:9615/index.html')

        self.sensor = ScreenSensor(self.browser)
        self.mouse = MouseActuator(self.browser)
        self.key  = KeyActuator(self.browser)

        # setup redis connection
        self.r = r
        self.p = self.r.pubsub()
        self.p.subscribe('percepts')  


    def screencaptureLoop(self, frequency=1.0):

        while True:

            time.sleep(frequency)

            try:
                self.r.publish('percepts', {
                    "type": "screenshot",
                    "unixTimeStamp": time.time(),
                    "data": self.sensor.getScreenshot()
                })
                
            except:
                pass



    def actLoop(self, frequency=1.0):

        while True:

            time.sleep(frequency)

            newMessages = True
            while newMessages is True:
                
                # process for new messages
                message = self.p.get_message()
                if message:
                    data = message['data']
                    print data

                else:
                    newMessages = False

            # perform an action
            # self.mouse.scrollRight()
            # self.mouse.scrollUp(20)
            self.key.pressDown(0.2)