import cv2
import numpy as np
from picamera2 import Picamera2

# Initialize the Pi Camera
camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
camera.start()

print("Press 'q' to exit")

while True:
    # Capture frame as an array
    frame = camera.capture_array()
    
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the HSV range for red color
    lower_red1 = np.array([0, 120, 70])   # Lower red range
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])  # Upper red range
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)  # Mask for first red range
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)  # Mask for second red range
    red_mask = mask1 | mask2  # Combine both masks

    # Count red pixels
    total_pixels = red_mask.size  # Total pixels in the image
    red_pixels = np.count_nonzero(red_mask)  # Count red pixels (non-zero values)
    red_pixel_ratio = red_pixels / total_pixels  # Ratio of red pixels

    print(f"Red Pixels: {red_pixels}, Total Pixels: {total_pixels}, Red Pixel Ratio: {red_pixel_ratio:.4f}")

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.stop()
