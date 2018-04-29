import json, time

class KeyActuator(object):

    """ enables agent to move around the virtual environment 
        by using the WASD keys. """

    def __init__(self, webDriver):

        if webDriver is None:
            raise ValueError
        
        self.driver = webDriver

    def pressDown(self, duration=0.2):
        options = { \
            "code": "KeyS",
            "key": "s",
            "text": "s",
            "unmodifiedText": "s",
            "nativeVirtualKeyCode": ord("S"),
            "windowsVirtualKeyCode": ord("S")
        }
        self.holdKeyDown(self.driver, duration, options)

    def pressUp(self, duration=0.2):
        options = { \
            "code": "KeyW",
            "key": "w",
            "text": "w",
            "unmodifiedText": "w",
            "nativeVirtualKeyCode": ord("W"),
            "windowsVirtualKeyCode": ord("W")
        }
        self.holdKeyDown(self.driver, duration, options)

    def pressLeft(self, duration=0.2):
        options = { \
            "code": "KeyA",
            "key": "a",
            "text": "a",
            "unmodifiedText": "a",
            "nativeVirtualKeyCode": ord("A"),
            "windowsVirtualKeyCode": ord("A")
        }
        self.holdKeyDown(self.driver, duration, options)

    def pressRight(self, duration=0.2):
        options = { \
            "code": "KeyD",
            "key": "d",
            "text": "d",
            "unmodifiedText": "d",
            "nativeVirtualKeyCode": ord("D"),
            "windowsVirtualKeyCode": ord("D")
        }
        self.holdKeyDown(self.driver, duration, options)


    def dispatchKeyEvent(self, driver, name, options = {}):
        options["type"] = name
        body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
        resource = "/session/%s/chromium/send_command" % driver.session_id
        url = driver.command_executor._url + resource
        driver.command_executor._request('POST', url, body)

    def holdKeyDown(self, driver, duration, options):
        endtime = time.time() + duration

        while True:
            self.dispatchKeyEvent(self.driver, "rawKeyDown", options)
            self.dispatchKeyEvent(self.driver, "char", options)

            if time.time() > endtime:
                self.dispatchKeyEvent(self.driver, "keyUp", options)
                print options
                print 'keyup'
                break

            options["autoRepeat"] = True
            time.sleep(0.01)