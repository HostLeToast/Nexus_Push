import os
import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize the Pi Camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()

# Define HSV color range for detection (e.g., red color)
lower_bound = np.array([0, 120, 70])   # Lower HSV bounds
upper_bound = np.array([10, 255, 255]) # Upper HSV bounds

print("Press 'q' to exit")

while True:
    # Capture frame-by-frame
    frame = camera.capture_array()

    frame = frame[:, :, :3]  # Drop alpha channel
    frame = cv2.cvtColor(frame, cv2.COLOR_XBGR2BGR)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the defined color range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Calculate black pixel ratio
    total_pixels = mask.size  # Total number of pixels in the image
    black_pixels = np.count_nonzero(mask == 0)  # Pixels that are black (value 0)
    black_pixel_ratio = black_pixels / total_pixels

    print(f"Black Pixels: {black_pixels}, Total Pixels: {total_pixels}, Black Pixel Ratio: {black_pixel_ratio:.4f}")

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
