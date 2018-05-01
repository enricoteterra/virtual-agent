import time
from selenium import webdriver
from units import unit
from mouseActuator import MouseActuator
from screenSensor import ScreenSensor
from keyActuator import KeyActuator
second = unit('s')

class SimpleReflexAgent(object):
    """ an agent without state or goals, just react to last sensor percept. """

    def loop(self, frequency=second(1)):

        browser = webdriver.Chrome('/Users/enrico.t/bin/chromedriver')
        browser.set_window_size('400', '300')
        browser.set_window_position(0, 0)
        browser.get('http://localhost:9615/index.html')

        sensor = ScreenSensor(browser)
        mouse = MouseActuator(browser)
        key = KeyActuator(browser)

        # start the loop
        while True:

            # wait a bit
            time.sleep(frequency)

            # get latest screen state
            state = sensor.getScreen()
            # browser.get_screenshot_as_file('./latest.png')

            # perform an action
            # mouse.scrollRight()
            mouse.scrollUp(20)
            key.pressDown(0.2)