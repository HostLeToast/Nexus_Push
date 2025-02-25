import cv2
import numpy as np
from picamera2 import Picamera2
import time
from libcamera import controls

# Initialize Camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 4.0})  # Adjust brightness

# Git Repository Paths
REPO_PATH = "/home/pi/Nexus_Push/Nexus_Push"
FOLDER_PATH = "images"

# Set up capture configuration
capture_config = camera.create_still_configuration()

start_time = time.time()

# Git Push Function
def git_push():
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('Added remote repository')
        origin.pull()
        print('Pulled latest changes')
        repo.git.add(f"{REPO_PATH}/{FOLDER_PATH}/*")  # Fixed path
        repo.index.commit('New Photo')
        print('Committed changes')
        origin.push()
        print('Pushed to GitHub')
    except Exception as e:
        print(f"Couldn't upload to Git: {e}")

# Image Name Generator
def img_gen(name):
    t = time.strftime("_%H%M%S")
    return f"{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg"

# Capture Photo and Upload
def take_photo():
    name = img_gen("LargeDarkAreaCoverage")
    camera.switch_mode_and_capture_file(capture_config, name)  # Fixed path issue
    git_push()

# Main Loop
while (time.time() - start_time) < 120:
    frame = camera.capture_array()

    # Convert XBGR to BGR manually
    frame = frame[:, :, [2, 1, 0]]  # Swap channels
    frame = frame[:, :, :3]  # Remove alpha

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range for dark shades (adjust as needed)
    lower_white = np.array([0, 0, 30])
    upper_white = np.array([180, 50, 120])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    total_pixels = mask.size
    dark_pixels = np.count_nonzero(mask == 0)
    dark_pixel_ratio = dark_pixels / total_pixels

    print(f"Smoke to Total Area Ratio: {dark_pixel_ratio:.4f}")

    # If the ratio exceeds 25%, take a photo and upload
    if dark_pixel_ratio > 0.25:
        camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
        camera.start(show_preview=False)
        take_photo()

    time.sleep(5)

camera.stop()
camera.close()
