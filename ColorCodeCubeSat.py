import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 10000, "AnalogueGain": 2.0})  # Adjust brightness

print("Press 'q' to exit")

while True:
    frame = camera.capture_array()

    # Fix format: Remove alpha channel & convert XBGR → BGR
    frame = frame[:, :, :3]  # Drop alpha channel
    frame = cv2.cvtColor(frame, cv2.COLOR_XBGR2BGR)  # Ensure correct color order

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    print("Sample HSV pixel:", hsv[0, 0])  # Debug HSV values

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    total_pixels = mask.size
    black_pixels = np.count_nonzero(mask == 0)
    black_pixel_ratio = black_pixels / total_pixels

    print(f"Black Pixels: {black_pixels}, Total Pixels: {total_pixels}, Ratio: {black_pixel_ratio:.4f}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
