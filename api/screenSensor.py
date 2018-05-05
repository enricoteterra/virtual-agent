import StringIO
import time
import json
from PIL import Image
import numpy as np

class ScreenSensor(object):

    """ enables agent to get a snapshot of the current state of the environment. """

    def __init__(self, webDriver, r):

        if webDriver is None:
            raise ValueError
  
        self.driver = webDriver
        self.r = r

    def publishScreenshot(self):

        data = self.driver.get_screenshot_as_png()
        img = Image.open(StringIO.StringIO(data))
        width, height = img.size

        serialisedData = np.asarray(img).tolist()

        self.r.publish('percepts', json.dumps({
            "type": "screenshot",
            "unixTimeStamp": time.time(),
            "data": serialisedData,
            "width": width,
            "height": height,
            "mode": img.mode
        }))
