import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from units import unit
second = unit('s')

class SimpleReflexAgent(object):
    """ an agent without state or goals, just react to latest sensor percepts. """

    def loop(self, frequency=second(1)):

        # setup sensor & actuator
        # note: we are using the webdriver as both the sensor and actuator

        browser = webdriver.Chrome('/Users/enrico.t/bin/chromedriver')
        browser.set_window_size('400', '300')
        browser.set_window_position(0, 0)
        browser.get('http://localhost:9615/index.html')

        canvas = browser.find_element_by_tag_name('canvas')

        # start the loop
        while True:

            # wait a bit
            time.sleep(frequency)

            # get latest screen state
            data = browser.get_screenshot_as_png()
            browser.get_screenshot_as_file('./latest.png')

            # reset cursor to center of canvas
            ActionChains(browser)\
                .move_to_element(canvas)\
                .perform()
            
            # perform action
            ActionChains(browser)\
                .click_and_hold()\
                .move_by_offset(100, 10)\
                .release()\
                .perform()
