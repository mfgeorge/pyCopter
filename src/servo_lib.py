
try:
    from machine import PWM
    import time
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries.machine import PWM

class Servo:
    '''
    Basic Servo replacement class since machine has no servo library
    '''
    next_channel = 0
    def __init__(self,pin):
        pwm = PWM(0,frequency=50)
        self.servo_control = pwm.channel(Servo.next_channel, pin = pin, duty_cycle=1)
        Servo.next_channel += 1

    def calibration(self):
        self.speed(185)
        time.sleep(2)
        self.speed(0)
        time.sleep(2)
        # Now servos should be ready to go


    def speed(self,speedin):
        #Servo pwm goes from 40 to 115, must convert from 0 to 180
        # pwm = 40 + (speedin)*(115-40)/180 #Linear interpolation
        if speedin > 180:
            speedin = 180
        elif speedin <= 0:
            speedin = 0
        pwm = .05 + speedin*.05/180
        self.servo_control.duty_cycle(pwm)
