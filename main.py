# main.py -- put your code here!

from pyb import Servo
from motor_control import Motor_Control

def main():
    ss1 = 50
    ss2 = 0
    ss3 = 0
    ss4 = 0

    servo1 = pyb.Servo(1)
    servo2 = pyb.Servo(2)
    servo3 = pyb.Servo(3)
    servo4 = pyb.Servo(4)

    controller = Motor_Control(servo1, servo2, servo3, servo4)
    controller.motor_task(ss1, ss2, ss3, ss4)

if __name__ == '__main__':
    main()