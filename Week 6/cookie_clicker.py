import pyautogui as pg
import time, sys

pg.FAILSAFE = True # Fling mouse to top left to abort.
print("Move the mouse to top left, or press Ctrl+C to abort")


# Auto Clicker
pg.moveTo(1288, 460)
while True:
    pg.click()
    time.sleep(.001)

pointer_location()
