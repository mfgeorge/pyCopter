"""
..  module:: servo_lib.py
    :platform: Pycom LoPy
    :synopsis: A module for controlling servos using PWM without the machine library.

..  topic:: Authors

    | Chad Bickel
    | Michael George

A module for micropython which allows for easy control of servos or ESCs.

The Servo class should be used once for every servo that needs to be controlled.

Example::

    servo1 = Servo('P23')
    servo1.calibration()
    servo1.speed(90)

"""
try:
    from machine import PWM
    import time
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries.machine import PWM

class Servo:
    """
    Class to control servos since machine library has no servo class yet.

    :param pin: LoPy pin wired to the signal pin of the servo.
    """

    #: A class variable that holds the next channel available for connecting to PWM.
    #: This variable will increment with each instantiation of the class.
    next_channel = 0
    def __init__(self,pin):
        """
        Constructor for the Servo class
        """
        pwm = PWM(0,frequency=50)
        self.servo_control = pwm.channel(Servo.next_channel, pin = pin, duty_cycle=1)
        Servo.next_channel += 1

    def calibration(self):
        """
        Method to calibrate ESCs by sending the upper and lower signal limits.
        """
        self.speed(185)
        time.sleep(2)
        self.speed(0)
        time.sleep(2)
        # Now servos should be ready to go


    def speed(self,speedin):
        """
        Method to set servo position.

        :param speedin: The new ESC speed/servo position, from 0 to 180.
        """
        #Servo pwm goes from 40 to 115, must convert from 0 to 180
        # pwm = 40 + (speedin)*(115-40)/180 #Linear interpolation
        if speedin > 180:
            speedin = 180
        elif speedin <= 0:
            speedin = 0
        pwm = .05 + speedin*.05/180
        self.servo_control.duty_cycle(pwm)
