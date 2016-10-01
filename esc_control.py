# main.py -- put your code here!

from pyb import Servo

ss1 = 0
ss2 = 0
ss3 = 0
ss4 = 0

servo1 = pyb.Servo(1)
servo2 = pyb.Servo(2)
servo3 = pyb.Servo(3)
servo4 = pyb.Servo(4)
class Motor_Control
    def init(self):
        servo1.calibration()
        servo2.calibration()
        servo3.calibration()
        servo4.calibration()

    def motor_task(ss1, ss2, ss3, ss4):

        servo1.speed(ss1)

        servo2.speed(ss2)

        servo3.speed(ss3)

        servo4.speed(ss4)


def main():
    try:
        Motor_Control()
    except KeyboardInterrupt:
        print "Key boaard Interupt"

if __name__ == '__main__':
    main()