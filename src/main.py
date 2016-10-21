# main.py -- put your code here!
import micropython
from pyb import Servo, millis
from motor_control import Motor_Control
from BNO055_lib import BNO055
import time
from rfComm import SpektrumController, ServoPulse
import sys
#import os

def main():

    servo1 = pyb.Servo(1)
    servo2 = pyb.Servo(2)
    servo3 = pyb.Servo(3)
    servo4 = pyb.Servo(4)

    controller = Motor_Control(servo1, servo2, servo3, servo4)
    try:
        IMU = BNO055()
    except OSError as e:
        print("Communication Error with the BNO055. \n")
        print("Error Exception", e)
        time.sleep(2)
        sys.exit()

    while True:

        pitch = IMU.get_pitch()
        roll = IMU.get_roll()
        yaw = IMU.get_yaw()

        speeds = [-pitch*10,-pitch*10,pitch*10,pitch*10]

        controller.motor_task(speeds[0], speeds[1], speeds[2], speeds[3])

        print ("Pitch: ")
        print (pitch)
        print ("Roll: ")
        print (roll)

        #os.system('cls')

if __name__ == '__main__':
    main()
