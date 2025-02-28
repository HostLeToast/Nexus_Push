import cv2
import numpy as np
from picamera2 import Picamera2
import time
from libcamera import controls
from git import Repo
import os

# Initialize Camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 4.0})  # Adjust brightness

# Git Repository Paths
REPO_PATH = "/home/nexus/Nexus_Push"
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
    name = img_gen("SmokeDetected")
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

    # Define range for detecting a wider range of gray shades
    lower_smoke = np.array([0, 0, 30])     # Low saturation, allow darker shades
    upper_smoke = np.array([180, 80, 220]) # Higher brightness range and slightly more color

    # Apply smoke mask
    mask = cv2.inRange(hsv, lower_smoke, upper_smoke)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)

    # Apply morphological operations to clean up noise
    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)

    # Calculate smoke coverage ratio
    total_pixels = mask_cleaned.size
    smoke_pixels = np.count_nonzero(mask_cleaned)
    smoke_ratio = smoke_pixels / total_pixels

    print(f"Smoke to Total Area Ratio: {smoke_ratio:.4f}")

    # If smoke is detected above threshold, capture image
    if smoke_ratio > 0.3:  # Lower threshold to be more sensitive
        camera.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
        camera.start(show_preview=False)
        os.makedirs(f"{REPO_PATH}/{FOLDER_PATH}", exist_ok=True)
        take_photo()

    time.sleep(5)

camera.stop()
camera.close()
