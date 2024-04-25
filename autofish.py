import cv2 as cv
import numpy as np
import pyautogui as pag
from PIL import ImageGrab

w = 2560
h = 1440
minx = round(1/3 * w)
maxx = round(2/3 * w)
miny = round(1/3 * h)
maxy = round(2/3 * h)
scc = 0.62
fish_counter = 0
frames_without_fish = 0
silent_mode = False
needle = cv.imread("fishy.png",cv.COLOR_RGB2BGR)


def reel(count, conf, time):

    pag.rightClick()
    cv.waitKey(np.random.randint(500,600))

    if not silent_mode:
        print(f"Fish Detected! Speed = {time}, Conf = {round(conf,2)}")
        print(f"{round(count)} Sea Creature(s) Expected")


def hype():
    needle = cv.imread("marker.png",cv.COLOR_RGB2BGR)
    diff = np.array([0,1000])

    pag.moveTo(None, 5000, 1, pag.easeOutQuad)
    pag.press('1')
    for i in range(15):
        cv.waitKey(np.random.randint(10,50))
        pag.rightClick()
    pag.press('3')
    pag.moveTo(None, 500, 1.5)

    while np.linalg.norm(diff) > 10:
        frame = pag.screenshot()
        frame = np.array(frame)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        result = cv.matchTemplate(frame, needle, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        pos = pag.position()
        diff[0] = max_loc[0] - pos[0]
        diff[1] = max_loc[1] - pos[1]
        
        pag.move(2*diff[0], 2*diff[1], 0.2)


while True:

    frame = ImageGrab.grab(bbox = ((minx, miny, maxx, maxy)))
    frame = np.array(frame)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    frames_without_fish += 1

    result = cv.matchTemplate(frame, needle, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if max_val > 0.8 or frames_without_fish > 500:
        fish_counter += scc
        reel(fish_counter, max_val,frames_without_fish)
        frames_without_fish = 0

        if fish_counter > 7:
            fish_counter = 0
            hype()

        pag.rightClick()
        
    cv.waitKey(1)