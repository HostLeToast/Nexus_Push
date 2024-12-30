#AUTHOR: Alvin Lai
#DATE: 12/12/24

#import libraries
import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2
from libcamera import controls

#VARIABLES
THRESHOLD = 5.0      #Any desired value from the accelerometer
REPO_PATH = ""     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "images"   #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
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
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname

def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace pseudocode with your own code.
    """
    while True:
        accelx, accely, accelz = accel_gyro.acceleration

        # CHECKS IF READINGS ARE ABOVE THRESHOLD
        if accelx > THRESHOLD or accely > THRESHOLD or accelz > THRESHOLD:
            # PAUSE for 2 seconds to stabilize camera
            time.sleep(2.0)
            
            name = img_gen("AlvinL")
            
            # Capture photo using autofocus and save with the generated name
            picam2.switch_mode_and_capture_file(capture_config, f'.{name}')
            
            # Push the photo to GitHub
            git_push()

        time.sleep(2.0)  # Adjust sleep time as needed for your application

def main():
    global capture_config
    capture_config = picam2.create_still_configuration(main={"size": (5120, 2880)})
    
    # Use autofocus and disable manual focus
    picam2.set_controls({"AfMode": controls.AfModeEnum.Auto})  # Enable autofocus
    
    # Start the camera
    picam2.start(show_preview=False)
    
    # Start taking photos based on shake detection
    take_photo()

if __name__ == '__main__':
    main()
