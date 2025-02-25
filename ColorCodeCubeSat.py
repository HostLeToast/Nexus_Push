import cv2
import numpy as np
from picamera2 import Picamera2
import time
from libcamera import controls

# initialize
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 4.0})  # brightness

REPO_PATH = "/home/pi/Nexus_Push/Nexus_Push"
FOLDER_PATH = "images"

start_time = time.time()

def git_push():
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')

def img_gen(name):
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname

def take_photo():
    name = img_gen("LargeDarkAreaCoverage")
    camera.switch_mode_and_capture_file(capture_config, f'.{name}')
    git_push()

while (time.time() - start_time) < 120:
    frame = camera.capture_array()

    # convert XBGR to BGR manually
    frame = frame[:, :, [2, 1, 0]]  # swap channels
    frame = frame[:, :, :3]  # remove alpha

    # convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # fix white detection
    lower_white = np.array([0, 0, 30])
    upper_white = np.array([180, 50, 120])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    total_pixels = mask.size
    dark_pixels = np.count_nonzero(mask == 0)
    dark_pixel_ratio = dark_pixels / total_pixels

    print(f"Smoke to Total Area Ratio: {dark_pixel_ratio:.4f}")

    #if over threshold, send image to groundstation
    if dark_pixel_ratio > 0.25:
        global capture_config
        capture_config = camera.create_still_configuration()
        camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
        camera.zoom = (0, 0, 1, 1)
        camera.start(show_preview=False)
        take_photo()

    time.sleep(5)

camera.stop()
