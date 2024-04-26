import cv2 as cv
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
import requests

# Monitor width and height
w = 2560
h = 1440

# How much of screen to capture
percentage = 0.2
midpoint_w = round(w/2)
midpoint_h = round(h/2)
min_screen_x = round(midpoint_w - percentage*w)
max_screen_x = round(midpoint_w + percentage*w)
min_screen_y = round(midpoint_h - percentage*h)
max_screen_y = round(midpoint_h + percentage*h)



# Uses a P controller to converge crosshairs to a reference image
def track_reference(ref_img):
    
    # Initialise constant of proportionality, tolerance and error array
    kp = 1
    tol = 10
    err = np.array([0,1000])

    # Hide HUD with F1
    pag.press('f1')

    # P control towards image while more than tol pixels away
    while np.linalg.norm(err) > tol:
            frame = capture(True)
            result = cv.matchTemplate(frame, ref_img, cv.TM_CCOEFF_NORMED)

            _, _, _, max_loc = cv.minMaxLoc(result)
            pos = pag.position()
            err[0] = max_loc[0] - pos[0]
            err[1] = max_loc[1] - pos[1]
            
            pag.move(kp*err[0], kp*err[1], 0.2)

    pag.press('f1')



# Screencapture either entire screen (useful for tracking) or partial screen (useful for fps/reaction time)
def capture(full):

    if full:
        frame = ImageGrab.grab()
    else:  
        frame = ImageGrab.grab(bbox = ((min_screen_x, min_screen_y, max_screen_x, max_screen_y)))

    frame = np.array(frame)
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    return frame



# Reel in caught fish and print console message
def reel(count, conf, time):

    pag.rightClick()
    cv.waitKey(np.random.randint(500,600))
    print(f"Fish Detected! Speed = {time}, Conf = {round(conf,2)}")
    print(f"{round(count)} Sea Creature(s) Expected")



# Look down to spam hyperion with random timings, then look up
def hype():

    pag.moveTo(None, 5000, 1, pag.easeOutQuad)
    pag.press('1')
    for i in range(15):
        cv.waitKey(np.random.randint(10,30))
        pag.rightClick()
    pag.press('3')
    pag.moveTo(None, 500, 1.5)



# Fix fishing rod in the event of issue
def fix_rod(ref_img):
    track_reference(ref_img)
    pag.press('1')
    cv.waitKey(np.random.randint(10,50))
    pag.press('3')
    cv.waitKey(np.random.randint(10,50))
    pag.rightClick()



# Use pushover and requests to push iPhone notification
def push_notification(message, img):
    r = requests.post("https://api.pushover.net/1/messages.json", data = {
    "token": open("pushover_token.txt","r").read(),
    "user": open("pushover_user.txt","r").read(),
    "message": message,
    },

    files = {
    "attachment": ("image.jpg", open(img, "rb"), "image/png")
    })

    print(r.text)