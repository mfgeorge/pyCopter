#!/bin/python

# Handle the case where we aren't in micropython for documentation
# generation
try:
    import machine
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries import machine


class RFController6CH:
    """
    A generic parent class for a 6 channel radio module
    Lays out what needs to be implemented so that all controllers
    will implement the same methods, no matter what type they are.

    | All controller classes should implement at least these methods:
    """
    def __init__(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_thrust(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def get_roll(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def get_pitch(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def get_yaw(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def get_switch1(self):
    	raise NotImplementedError("Subclasses should implement this!")

    def get_switch2(self):
    	raise NotImplementedError("Subclasses should implement this!")

class SpektrumController(RFController6CH):
    """
    A class for a specific 6 channel Spektrum radio module.

    :param thro_pin: Pin that the thro connection is on
    :param aile_pin: Pin that the aile connection is on
    :param elev_pin: Pin that the elev connection is on
    :param rudd_pin: Pin that the rudd connection is on
    :param gear_pin: Pin that the gear connection is on
    :param aux1_pin: Pin that the aux1 connection is on
    """

    def __init__(self, thro_pin, aile_pin, elev_pin, rudd_pin, gear_pin, aux1_pin):
        """
        The constructor for the Spektrum Controller
        """
        # Make the servo pulse objects connected to the specified pins
        self.thro_pulse = ServoPulse(thro_pin)
        self.aile_pulse = ServoPulse(aile_pin)
        self.elev_pulse = ServoPulse(elev_pin)
        self.rudd_pulse = ServoPulse(rudd_pin)
        self.gear_pulse = ServoPulse(gear_pin)
        self.aux1_pulse = ServoPulse(aux1_pin)

        # Store last values so some filtering may be implemented in the
        # future
        self.last_thrust = 0
        self.last_roll = 0
        self.last_yaw = 0
        self.last_pitch = 0

    def get_thrust(self):
        """
        Gets the thrust value of the thrust signal being sent

        :return: thrust value on a 0-50 scale
        """
        value = (self.thro_pulse.get_width() - 1048)/(1933 - 1048)*50
        self.last_thrust = value
        return value

    def get_roll(self):
        """
        Gets the roll value of the roll signal being sent

        :return: roll value on a 0-50 scale
        """
        value = (self.aile_pulse.get_width() - 1094)/(1893 - 1094)*50-25
        self.last_roll = value
        return value 

    def get_pitch(self):
        """
        Gets the pitch value of the pitch signal being sent

        :return: pitch value on a 0-50 scale
        """
        value = (self.elev_pulse.get_width() - 1077)/(1876 - 1077)*50-25
        self.last_pitch = value
        return value 

    def get_yaw(self):
        """
        Gets the yaw value of the yaw signal being sent

        :return: Yaw value on a 0-50 scale
        """
        value = (self.rudd_pulse.get_width() - 1086)/(1876 - 1086)*50-25
        self.last_yaw = value
        return value 

    def get_switch1(self):
        """
        Gets the position of the 1st switch

        :return: 1 if the switch is on, 0 if it is off
        """
        value = 1 if self.gear_pulse.get_width() > 1500 else 0
        return value

    def get_switch2(self):
        """
        Gets the position of the 2nd switch

        :return: 1 if the switch is on, 0 if it is off
        """
        value = 1 if self.aux1_pulse.get_width() > 1500 else 0
        return value


class ServoPulse:
    """
    A servo_pulse Class written by wagnerc4 on github and modified by michael george for our
    purposes.

    :Changes Made:

        Instead of using IC interrupts here which limits the pin choice
        (trouble with timer 8 and 1 identified, may be others not working either)
        we use external interrupts so that this can be done on any pin, given they
        do not have the same CPU port NUMBER. ie PBn and PAn cannot both be used
        to measure servo pulses.

    The constructor parameters are:

    :param pin: Pin that the servo pulse is connected to.
    :param timer: Timer that can be used to mark the amount of time
        the pulse was high for.
    """

    #: Varible to hold information about the pulse timing
    start = width = last_width = 0

    def __init__(self, pin, timer=machine.Timer(8, prescaler=83, period=0xffff)):
        """
        Constructor for the ServoPulse class
        """
        self.pulseCounter = timer
        self.tickConversion = 1e6/(self.pulseCounter.freq()*self.pulseCounter.period())
        # input("Any key to continue configuring external interrupts")
        self.pin = pin
        self.interrupt = machine.ExtInt(self.pin, machine.ExtInt.IRQ_RISING_FALLING, machine.Pin.PULL_NONE, self.callback)
        self.interrupt.enable()
        print("External Interrupt Set up on Line: ", self.interrupt.line())

    #@micropython.native
    def callback(self, line):
        """
        Callback that the external interrupt will call

        :param line: The line that the interrupt is on always gets passed
            to the callback.
        """
        now = self.pulseCounter.counter()
        if self.pin.value(): 
            self.start = now
        else: 
            self.width = (now - self.start) & 0xffff

    #@micropython.native
    def get_width(self):
        """
        method for getting the most recent width of the last servo pulse

        :return: the width in useconds
        """
        self.interrupt.disable()
        w = self.width
        self.interrupt.enable()
        w *= self.tickConversion
        # print(w)
        self.last_width = w if w > 950 and w < 1950 else self.last_width
        return self.last_width

    def __del__(self):
        """
        Deconstructor for the servopulse class. ends the external interrupt
        associated with the servopulse object.
        """
        self.timer.deinit()
        self.interrupt.disable()

