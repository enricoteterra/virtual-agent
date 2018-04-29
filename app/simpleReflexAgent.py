import time
from selenium import webdriver
from units import unit
from app.mouseActuator import MouseActuator
from app.screenSensor import ScreenSensor
from app.keyActuator import KeyActuator
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

second = unit('s')

class SimpleReflexAgent(object):
    """ an agent without state or goals, just react to last sensor percept. """

    def loop(self, frequency=second(1)):

        # note: we are using the webdriver as both the sensor and actuator

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
            browser.get_screenshot_as_file('./latest.png')

            # perform an action
            # mouse.scrollRight()
            mouse.scrollUp(20)
            key.pressDown(0.2)
