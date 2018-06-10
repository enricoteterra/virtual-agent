import unittest
import jsonschema
import redislite
import json
from PIL import Image
from io import BytesIO
import StringIO
from app.webdriver import ScreenSensor

class MockWebdriver(object):
    def get_screenshot_as_png(self):
        return

class ScreenSensorTest(unittest.TestCase):

    def setUp(self):

        self.mockRedis = redislite.StrictRedis()
        self.mockWebdriver = MockWebdriver()

        self.sensor = ScreenSensor(
            self.mockWebdriver, 
            self.mockRedis)

        self.perceptSchema = {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["screenshot"]
                },
                "unixTimeStamp": {"type": "number"},
                "data": {},
                "width": {"type": "number"},
                "height": {"type": "number"},
                "mode": {"type": "string"},
            },
            "required": ["type", "unixTimeStamp", "data", "width", "height", "mode"]
        }

    def createTestImage(self):
        testFile = BytesIO()
        image = Image.new(
            'RGBA', 
            size=(400, 300), 
            color=(155, 0, 0))

        image.save(testFile, 'png')
        testFile.name = 'test.png'
        testFile.seek(0)
        
        return Image.open(
            StringIO.StringIO(testFile.read()))

    def test_publishScreenshot(self):
        """
        test that recorded screenshots are being pushed to queue.
        """

        sub = self.mockRedis.pubsub()
        sub.subscribe('percepts')

        image = self.createTestImage()
        self.sensor.publishScreenshot(image)

        for msg in sub.listen():
            if msg is not None and msg["data"] != 1l:
                jsonschema.validate(
                json.loads(msg["data"]),
                self.perceptSchema)
                break

        msg = sub.get_message()
        self.assertIsNone(msg)
