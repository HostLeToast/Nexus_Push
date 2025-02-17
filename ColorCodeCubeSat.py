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
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for the defined color range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Show the frames
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
camera.stop()
)
