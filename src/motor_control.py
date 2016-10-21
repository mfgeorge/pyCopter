from pyb import Servo
import time

class Motor_Control:
    def __init__(self, s1, s2, s3, s4):
        self.servo1 = s1
        self.servo2 = s2
        self.servo3 = s3
        self.servo4 = s4

        self.servo1.calibration()
        self.servo2.calibration()
        self.servo3.calibration()
        self.servo4.calibration()
        time.sleep(3)

    def motor_task(self,ss1, ss2, ss3, ss4):
        self.servo1.speed(ss1)
        
        self.servo2.speed(ss2)

        self.servo3.speed(ss3)

        self.servo4.speed(ss4)