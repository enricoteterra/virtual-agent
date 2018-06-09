import json, time

class KeyActuator(object):

    """ enables agent to move around the virtual environment
        by using the WASD keys. """

    def __init__(self, webDriver):

        self.driver = webDriver

    def pressDown(self, defaultDuration=0.2):
        options = { \
            "code": "KeyS",
            "key": "s",
            "text": "s",
            "unmodifiedText": "s",
            "nativeVirtualKeyCode": ord("S"),
            "windowsVirtualKeyCode": ord("S")
        }
        self.holdKeyDown(defaultDuration, options)

    def pressUp(self, defaultDuration=0.2):
        options = { \
            "code": "KeyW",
            "key": "w",
            "text": "w",
            "unmodifiedText": "w",
            "nativeVirtualKeyCode": ord("W"),
            "windowsVirtualKeyCode": ord("W")
        }
        self.holdKeyDown(defaultDuration, options)

    def pressLeft(self, defaultDuration=0.2):
        options = { \
            "code": "KeyA",
            "key": "a",
            "text": "a",
            "unmodifiedText": "a",
            "nativeVirtualKeyCode": ord("A"),
            "windowsVirtualKeyCode": ord("A")
        }
        self.holdKeyDown(defaultDuration, options)

    def pressRight(self, defaultDuration=0.2):
        options = { \
            "code": "KeyD",
            "key": "d",
            "text": "d",
            "unmodifiedText": "d",
            "nativeVirtualKeyCode": ord("D"),
            "windowsVirtualKeyCode": ord("D")
        }
        self.holdKeyDown(defaultDuration, options)


    def dispatchKeyEvent(self, name, options = {}):

        options["type"] = name
        body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
        resource = "/session/%s/chromium/send_command" % self.driver.session_id

        url = self.driver.command_executor._url + resource
        self.driver.command_executor._request('POST', url, body)


    def holdKeyDown(self, defaultDuration, options):

        endtime = time.time() + defaultDuration

        while True:
            self.dispatchKeyEvent("rawKeyDown", options)
            self.dispatchKeyEvent("char", options)

            if time.time() > endtime:
                self.dispatchKeyEvent("keyUp", options)
                break

            options["autoRepeat"] = True
            time.sleep(0.01)