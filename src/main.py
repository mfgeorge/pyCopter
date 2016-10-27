# main.py -- put your code here!
import micropython
from pyb import Servo, millis, I2C
from motor_control import Motor_Control
from BNO055_lib import BNO055
import time
from rfComm import SpektrumController, ServoPulse
from controller_task import PIDControl
import sys
import json
#import os

def load_config_file(config_file):
    with open(config_file, mode='r') as file:
        try:
            config_dict = json.loads(file.read())
        except json.JSONDecodeError:
            print("ERROR: Invalid Configuration File '" + file +"'")
            return None
        return config_dict

def main():

    servo1 = pyb.Servo(1)
    servo2 = pyb.Servo(2)
    servo3 = pyb.Servo(3)
    servo4 = pyb.Servo(4)

    motor_controller = Motor_Control(servo1, servo2, servo3, servo4)
    try:
        IMU = BNO055()
    except OSError as e:
        print("Communication Error with the BNO055. \n")
        print("Exception: OSError ", e)
        time.sleep(2)
        sys.exit()

    gain_dict = load_config_file("gain_config.json")
    pid_controller = PIDControl(gain_dict)
    sensor_reading_dict = {}
    set_point_dict = {}
    try:
        while True:
            t = time.ticks_us()
            sensor_reading_dict["pitch"] = IMU.get_pitch()
            sensor_reading_dict["roll"] = IMU.get_roll()
            sensor_reading_dict["yaw"] = IMU.get_yaw_rate()
            print(sensor_reading_dict["yaw"])

            set_point_dict["pitch"] = 0
            set_point_dict["roll"] = 0
            set_point_dict["yaw"] = 0
            set_point_dict["thrust"] = 0

            speeds = pid_controller.run(sensor_reading_dict, set_point_dict)

            # print(speeds)

            motor_controller.motor_task(speeds[0], speeds[1], speeds[2], speeds[3])

            # print ("Pitch: ", sensor_reading_dict["pitch"], "\tRoll: ", sensor_reading_dict["roll"])
            delta = time.ticks_diff(t, time.ticks_us())
            #print("delta = ", delta/1000, " ms")
    except:
        motor_controller.motor_task(0,0,0,0)
        IMU.deinit_i2c()
        raise

if __name__ == '__main__':
    main()
