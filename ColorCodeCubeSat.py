import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()
camera.set_controls({"ExposureTime": 30000, "AnalogueGain": 4.0})  # Adjust brightness

print("Press 'q' to exit")

while True:
    frame = camera.capture_array()

    # Convert XBGR to BGR manually
    frame = frame[:, :, [2, 1, 0]]  # Swap channels
    frame = frame[:, :, :3]  # Remove alpha channel

    # Print sample pixel values
    print("RGB (Center pixel):", frame[frame.shape[0]//2, frame.shape[1]//2])

    # Convert to HSV and print values
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    print("HSV (Center pixel):", hsv[frame.shape[0]//2, frame.shape[1]//2])

    # Adjust white detection range
    lower_white = np.array([0, 0, 180])  # Loosen the brightness limit
    upper_white = np.array([180, 50, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    total_pixels = mask.size
    black_pixels = np.count_nonzero(mask == 0)
    black_pixel_ratio = black_pixels / total_pixels

    print(f"Black Pixels: {black_pixels}, Total Pixels: {total_pixels}, Ratio: {black_pixel_ratio:.4f}")

    # Save an image and mask for debugging
    #cv2.imwrite("debug_frame.jpg", frame)
    #cv2.imwrite("debug_mask.jpg", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
