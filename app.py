import StringIO
import pyautogui
from selenium import webdriver
import numpy as np
from PIL import Image

browser = webdriver.Chrome('/Users/enrico.t/bin/chromedriver')
browser.set_window_size('400', '300')
browser.set_window_position(0, 0)
browser.get('http://localhost:9615/index.html')

data = browser.get_screenshot_as_png()
browser.get_screenshot_as_file('./latest.png')

img = Image.open(StringIO.StringIO(data))
numpy_array = np.asarray(img)

print numpy_array

browser.quit()

# screenWidth, screenHeight = pyautogui.size()
# currentMouseX, currentMouseY = pyautogui.position()
# pyautogui.moveTo(100, 150)
# pyautogui.click()
# pyautogui.moveRel(None, 10)  
# move mouse 10 pixels down


# pyautogui.doubleClick()
# pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # use tweening/easing function to move mouse over 2 seconds.
# pyautogui.typewrite('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
# pyautogui.press('esc')
# pyautogui.keyDown('shift')
# pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')