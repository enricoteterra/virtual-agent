from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class MouseActuator(object):

    """ enables agent to look around the virtual environment 
        by performing drag and drop actions with the mouse. """

    def __init__(self, webDriver):

        if webDriver is None:
            raise ValueError
        
        self.driver = webDriver
        self.canvas = webDriver.find_element_by_tag_name('canvas')

    def scrollUp(self, distance=20):

        self.centerCursor()

        ActionChains(self.driver)\
                .click_and_hold()\
                .move_by_offset(0, -distance)\
                .release()\
                .perform()

    def scrollDown(self, distance=20):

        self.centerCursor()

        ActionChains(self.driver)\
                .click_and_hold()\
                .move_by_offset(0, distance)\
                .release()\
                .perform()

    def scrollLeft(self, distance=20):

        self.centerCursor()

        ActionChains(self.driver)\
                .click_and_hold()\
                .move_by_offset(-distance, 0)\
                .release()\
                .perform()

    def scrollRight(self, distance=20):

        self.centerCursor()

        ActionChains(self.driver)\
                .click_and_hold()\
                .move_by_offset(distance, 0)\
                .release()\
                .perform()

    def centerCursor(self):

        ActionChains(self.driver)\
                .move_to_element(self.canvas)\
                .perform()