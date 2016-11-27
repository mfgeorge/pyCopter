from machine import PWM

class Servo:
    def __init__(self,pin):
        self.servo_control = PWM(pin,freq=50)


    def calibration(self):
        pass


    def speed(self,speedin):
        #Servo pwm goes from 40 to 115, must convert from 0 to 180
        pwm = 40 + (speedin)*(115-40)/180 #Linear interpolation
        self.servo_control.duty(pwm)
