import functions as f
import cv2 as cv
import numpy as np
import pyautogui as pag
from PIL import ImageGrab

scc = 0.62
fish_counter = 0
frames_without_fish = 0

fish_notif = cv.imread("fishy.png",cv.COLOR_RGB2BGR)
marker = cv.imread("marker.png",cv.COLOR_RGB2BGR)

while True:
    frame = f.capture(False)
    frames_without_fish += 1

    result = cv.matchTemplate(frame, fish_notif, cv.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv.minMaxLoc(result)

    if max_val > 0.8:
        fish_counter += scc
        f.reel(fish_counter, max_val, frames_without_fish)
        frames_without_fish = 0

        if fish_counter > 2:
            fish_counter = 0
            f.hype()
            f.track_reference(marker)

        pag.rightClick()
        
    cv.waitKey(1)