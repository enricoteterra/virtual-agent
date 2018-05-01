import StringIO
from PIL import Image
import numpy as np

class ScreenSensor(object):

    """ enables agent to get a snapshot of the current state of the environment. """

    def __init__(self, webDriver):

        if webDriver is None:
            raise ValueError
  
        self.driver = webDriver

    def getScreen(self):

        data = self.driver.get_screenshot_as_png()
        img = Image.open(StringIO.StringIO(data))
        return np.asarray(img)
