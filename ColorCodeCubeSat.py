import cv2
import numpy as np
from picamera2.array import PiRGBArray
from picamera2 import PiCamera2

# Initialize the Pi Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Define HSV color range for detection (e.g., red color)
lower_bound = np.array([0, 120, 70])   # Lower HSV bounds
upper_bound = np.array([10, 255, 255]) # Upper HSV bounds

print("Press 'q' to exit")

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the defined color range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Apply the mask to the original frame
    result = cv2.bitwise_and(image, image, mask=mask)
    
    # Show the frames
    cv2.imshow("Original", image)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)
    
    # Clear the stream for the next frame
    rawCapture.truncate(0)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
