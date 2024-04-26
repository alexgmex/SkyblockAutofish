import functions as f
import cv2 as cv
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
import requests

# Declare sea creature chance as decimal and kill tolerance
scc = 0.62
kill_tol = 6

# Declare constants
fish_counter = 0
frames_without_fish = 0
fish_notif = cv.imread("fishy.png",cv.COLOR_RGB2BGR)
marker = cv.imread("marker.png",cv.COLOR_RGB2BGR)
lavapool = cv.imread("lavapool.png",cv.COLOR_RGB2BGR)

# Infinite loop
while True:
    
    # Capture and process frame against fish image detection
    frames_without_fish += 1
    frame = f.capture(False)
    fish_result = cv.matchTemplate(frame, fish_notif, cv.TM_CCOEFF_NORMED)
    _, fish_conf, _, _ = cv.minMaxLoc(fish_result)

    # If fish detected, reel in and reset counter
    if fish_conf > 0.8:
        fish_counter += scc
        f.reel(fish_counter, fish_conf, frames_without_fish)
        frames_without_fish = 0

        # If enough sea creatures active, kill them then track back to marker 
        if fish_counter > kill_tol:
            f.hype()
            f.track_reference(marker)
            fish_counter = 0
        
        # Cast back out again
        pag.rightClick()

    # If no fish for a while, check if we are still in the nether
    if frames_without_fish >= 200:

        frame = f.capture(True)
        lavapool_result = cv.matchTemplate(frame, lavapool, cv.TM_CCOEFF_NORMED)
        _, lavapool_conf, _, _ = cv.minMaxLoc(lavapool_result)

        if lavapool_conf > 0.6:
            print("No fish for a while. Fixing rod!")
            f.fix_rod(marker)
            frames_without_fish = 0
        else:
            # Quit and send push notification
            print("Not in the nether anymore. Quitting program.")
            pag.press('1')
            cv.imwrite("push.png",frame)
            f.push_notification("Not in the nether anymore. Quitting program.", "push.png")
            break
        
    cv.waitKey(1)