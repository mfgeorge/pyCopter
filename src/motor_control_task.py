#from pyb import Servo
import time
from task_manager import Task

class MotorControlTask(Task):
    def __init__(self, s1, s2, s3, s4, speed_list, offset=0, calibrate=False):
        self.servo1 = s1
        self.servo2 = s2
        self.servo3 = s3
        self.servo4 = s4

        self.speed_list = speed_list

        if calibrate:
            self.servo1.calibration()
            self.servo2.calibration()
            self.servo3.calibration()
            self.servo4.calibration()

        s1.speed(0)
        s2.speed(0)
        s3.speed(0)
        s4.speed(0)

        self.offset = offset

    def run(self):

        # print("Speeds: ", ss1, ", ", ss2, ", ", ss3, ", ", ss4)

        self.servo1.speed(self.speed_list[0] + self.offset)
        
        self.servo2.speed(self.speed_list[1] +self.offset)

        self.servo3.speed(self.speed_list[2] +self.offset)

        self.servo4.speed(self.speed_list[3] +self.offset)
