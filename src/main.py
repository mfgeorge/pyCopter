# main.py -- put your code here!

from pyb import Servo
from motor_control import Motor_Control
from BNO055_lib import BNO055
import time
from rfComm import SpektrumController

def main():
    ss1 = 50
    ss2 = 0
    ss3 = 0
    ss4 = 0

    servo1 = pyb.Servo(1)
    servo2 = pyb.Servo(2)
    servo3 = pyb.Servo(3)
    servo4 = pyb.Servo(4)

    RF_controller = SpektrumController(thro_pin=pyb.Pin.board.Y1,
                                        aile_pin=pyb.Pin.board.Y2,
                                        elev_pin=pyb.Pin.board.Y3,
                                        rudd_pin=pyb.Pin.board.Y4,
                                        gear_pin=pyb.Pin.board.Y6,
                                        aux1_pin=pyb.Pin.board.Y7)


    controller = Motor_Control(servo1, servo2, servo3, servo4)

    IMU = BNO055()
    while True:
        '''
        try:
            speeds = tuple(map(int,input("\n Enter Motor Speeds in format ss1,ss2,ss3,ss4 \n").split(',')))
            controller.motor_task(speeds[0], speeds[1], speeds[2], speeds[3])
        except KeyboardInterrupt:
            print("\n \n Ending main and shutting motors down. \n \n")
            controller.motor_task(0,0,0,0)
            break
        except IndexError:
            print(" \n \n Please provide at least 4 input paramters for all motors \n \n")
            pass
        '''

        pitch = IMU.get_pitch()
        roll = IMU.get_roll()
        yaw = IMU.get_yaw()
        # speeds = [abs(pitch*10),abs(pitch*10),abs(roll*10),abs(roll*10)]
        speeds = [RF_controller.get_thrust() for i in range(4)]
        time.sleep(0.01)
        print(speeds)
        controller.motor_task(speeds[0], speeds[1], speeds[2], speeds[3])

if __name__ == '__main__':
    main()