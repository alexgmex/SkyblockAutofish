import cv2 as cv
import numpy as np
import pyautogui as pag

scc = 0.62
fish_counter = 0

needle = cv.imread("fishy.png",cv.IMREAD_ANYCOLOR)

while True:

    frame = pag.screenshot()
    frame = np.array(frame)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    result = cv.matchTemplate(frame, needle, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val > 0.6:
        fish_counter += 1
        print("Fish Detected!")
        print(f"Expected Sea Creature Count: {round(scc*fish_counter)}")
        pag.rightClick()
        cv.waitKey(750)
        pag.rightClick()

    cv.waitKey(1)