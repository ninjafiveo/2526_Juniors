import pyautogui as pg
import time, sys

pg.FAILSAFE = True # Fling mouse to top left to abort.
print("Move the mouse to top left, or press Ctrl+C to abort")

def pointer_location():
    try:
        while True:
            x, y = pg.position()
            sys.stdout.write(f"\r(x, y) = ({x:4d}, {y:4d})")
            sys.stdout.flush()
            time.sleep(0.05) # ~ 20 updates per second

    except KeyboardInterrupt:
        print("\nDone")

# move mouse to 1288, 460
# Auto Clicker
# pg.moveTo(1288, 460)
# while True:
#     pg.click()
#     time.sleep(.005)



def send_email():
    EMAIL_URL = "https://www.gmail.com"
    EMAIL_TO = "michael.sekol@mahoningctc.com"
    SUBJECT = "Hello Nerds"
    BODY = "Welcome to Software Engineering"
    pg.moveTo(1226, 1051)
    time.sleep(.05)
    pg.click()
    pg.moveTo(1250, 64)
    time.sleep(.05)
    pg.click()
    pg.click()
    pg.click()
    time.sleep(.1)
    pg.write(EMAIL_URL)
    time.sleep(1)
    pg.press("enter")
    time.sleep(3)
    pg.moveTo(1111, 220)
    time.sleep(1)
    pg.click()

# pointer_location()
send_email()