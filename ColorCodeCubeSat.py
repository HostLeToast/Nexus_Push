import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 4.0})  # Adjust brightness

print("Press 'q' to exit")

while True:
    frame = camera.capture_array()

    # convert XBGR to BGR manually
    frame = frame[:, :, [2, 1, 0]]  # swap channels
    frame = frame[:, :, :3]  # remove alpha

    # convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # fix white detection
    lower_white = np.array([0, 0, 180])
    upper_white = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    total_pixels = mask.size
    black_pixels = np.count_nonzero(mask == 0)
    black_pixel_ratio = black_pixels / total_pixels

    print(f"Black Pixels: {black_pixels}, Total Pixels: {total_pixels}, Ratio: {black_pixel_ratio:.4f}")

    time.sleep(5)

camera.stop()
