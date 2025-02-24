"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.
The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

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
    Replace psuedocode with your own code.
    """
    while True:
        accelx, accely, accelz = accel_gyro.acceleration

        #CHECKS IF READINGS ARE ABOVE THRESHOLD
            #PAUSE
            #name = ""     #First Name, Last Initial  ex. MasonM
            #TAKE PHOTO
            #PUSH PHOTO TO GITHUB

        #PAUSE

        time.sleep(2.0)
        name = img_gen("AlvinL")
        #picam2.capture_file(f'.{name}')
        picam2.switch_mode_and_capture_file(capture_config, f'.{name}')
        
        '''
        if accelx > THRESHOLD or accely > THRESHOLD or accelz > THRESHOLD:
            time.sleep(2.0)
            name = img_gen("AlvinL")
            picam2.switch_mode_and_capture_file(capture_config, f'.{name}')
            git_push()

        time.sleep(5.0)
        '''





def main():
    global capture_config
    capture_config = picam2.create_still_configuration()
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})
    picam2.zoom = (0, 0, 1, 1)
    picam2.start(show_preview=False)
    take_photo()


if __name__ == '__main__':
    main()
