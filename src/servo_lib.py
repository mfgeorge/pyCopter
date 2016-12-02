from machine import PWM
import time

class Servo:
    '''
    Basic Servo replacement class since machine has no servo library
    '''
    def __init__(self,pin):
        self.servo_control = PWM(pin,freq=50)


    def calibration(self):
        self.speed(180)
        time.sleep(5)
        self.speed(0)
        time.sleep(5)
        # Now servos should be ready to go


    def speed(self,speedin):
        #Servo pwm goes from 40 to 115, must convert from 0 to 180
        pwm = 40 + (speedin)*(115-40)/180 #Linear interpolation
        self.servo_control.duty(pwm)
