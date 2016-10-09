#!/bin/python
import pyb

thro_pin = pyb.Pin.board.Y1
aile_pin = pyb.Pin.board.Y2
elev_pin = pyb.Pin.board.Y3
rudd_pin = pyb.Pin.board.Y4
gear_pin = pyb.Pin.board.Y6
aux1_pin = pyb.Pin.board.Y7


"""
Parent Class for any rf controller available 
Lays out what needs to be implemented so that all controllers 
will implement the same methods, no matter what type they are.
"""

class rfController6CH:
    'A generic parent class for a 6 channel radio module'
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

class spektrumController(rfController6CH):
    'A class for a specific 6 channel Spektrum radio module.'

	def __init__(self, thro_pin, aile_pin, elev_pin, rudd_pin, gear_pin, aux1_pin, global_varible):
        self.thro_pin = thro_pin
        self.aile_pin = aile_pin
        self.elev_pin = elev_pin
        self.rudd_pin = rudd_pin
        self.gear_pin = gear_pin
        self.aux1_pin = aux1_pin
        self.last_pulse_width = {}
        self.last_pulse_start = {}

    def initialize_pin_timer(self, pin, timer_index=0):
        timer_number, timer_channel = TimerHelper.get_timer(pin, timer_index)
        timer = pyb.Timer(timer_number, prescaler=83, period=0x0fffffff)
        input_capture = timer.channel(timer_channel, pyb.Timer.IC, pin=ic_pin, polarity=pyb.Timer.RISING, callback=self.get_pulse_width)
        self.last_pulse_start[input_capture] = 0
        self.last_pulse_width[input_capture] = 0


    def get_pulse_width(self, timer):
        # Read the GPIO pin to figure out if this was a rising or falling edge
        if ic_pin.value():
            # Rising edge - start of the pulse
            ic_start = ic.capture()
        else:
            # Falling edge - end of the pulse
            ic_width = ic.capture() - ic_start & 0x0fffffff


    def get_thrust(self):
        return 

class myTimer(pyb.Timer):
    def __init__(self, timer_number, )

class TimerHelper:
    'A simple class for helping pick timers and channels based upon pin number'
    """
    timer_dict: class varible for storing all the possible timer selections based upon pin
    due to it being a class varible, this dictionary is only created once upon the first
    instantiation of this class.
    """
    timer_dict = {}
    timer_dict[pyb.Pin.board.Y1] = (8)
    timer_dict[pyb.Pin.board.Y2] = (8)
    timer_dict[pyb.Pin.board.Y3] = (4, 10)
    timer_dict[pyb.Pin.board.Y4] = (4, 11)
    timer_dict[pyb.Pin.board.Y5] = None
    timer_dict[pyb.Pin.board.Y6] = (1)
    timer_dict[pyb.Pin.board.Y7] = (1, 8, 12)
    timer_dict[pyb.Pin.board.Y8] = (1, 8, 12)
    timer_dict[pyb.Pin.board.Y9] = (2)
    timer_dict[pyb.Pin.board.Y10] = (2)
    timer_dict[pyb.Pin.board.Y11] = (1, 8)
    timer_dict[pyb.Pin.board.Y12] = (1, 8)

    timer_dict[pyb.Pin.board.X1] = (2, 5)
    timer_dict[pyb.Pin.board.X2] = (2, 5)
    timer_dict[pyb.Pin.board.X3] = (2, 5, 9)
    timer_dict[pyb.Pin.board.X4] = (2, 5, 9)
    timer_dict[pyb.Pin.board.X5] = None
    timer_dict[pyb.Pin.board.X6] = (2, 8)
    timer_dict[pyb.Pin.board.X7] = (13)
    timer_dict[pyb.Pin.board.X8] = (1, 8, 14)
    timer_dict[pyb.Pin.board.X9] = (4)
    timer_dict[pyb.Pin.board.X10] = (4)
    timer_dict[pyb.Pin.board.X11] = None
    timer_dict[pyb.Pin.board.X12] = None
    timer_dict[pyb.Pin.board.X17] = None
    timer_dict[pyb.Pin.board.X18] = None
    timer_dict[pyb.Pin.board.X19] = None
    timer_dict[pyb.Pin.board.X20] = None
    timer_dict[pyb.Pin.board.X21] = None
    timer_dict[pyb.Pin.board.X22] = None

    timer_dict[pyb.Pin.board.P2] = None
    timer_dict[pyb.Pin.board.P3] = None
    timer_dict[pyb.Pin.board.P4] = None
    timer_dict[pyb.Pin.board.P5] = None

    """
    channel_dict: class varible for storing all the possible channel selections based upon pin
    due to it being a class varible, this dictionary is only created once upon the first
    instantiation of this class.
    """
    channel_dict = {}
    channel_dict[pyb.Pin.board.Y1] = (1)
    channel_dict[pyb.Pin.board.Y2] = (2)
    channel_dict[pyb.Pin.board.Y3] = (3, 1)
    channel_dict[pyb.Pin.board.Y4] = (4, 1)
    channel_dict[pyb.Pin.board.Y5] = None
    channel_dict[pyb.Pin.board.Y6] = (1)
    channel_dict[pyb.Pin.board.Y7] = (2, 2, 1)
    channel_dict[pyb.Pin.board.Y8] = (3, 3, 2)
    channel_dict[pyb.Pin.board.Y9] = (3)
    channel_dict[pyb.Pin.board.Y10] = (4)
    channel_dict[pyb.Pin.board.Y11] = (2, 2)
    channel_dict[pyb.Pin.board.Y12] = (3, 3)

    channel_dict[pyb.Pin.board.X1] = (1, 1)
    channel_dict[pyb.Pin.board.X2] = (2, 2)
    channel_dict[pyb.Pin.board.X3] = (3, 3, 1)
    channel_dict[pyb.Pin.board.X4] = (4, 4, 2)
    channel_dict[pyb.Pin.board.X5] = None
    channel_dict[pyb.Pin.board.X6] = (1, 1)
    channel_dict[pyb.Pin.board.X7] = (1)
    channel_dict[pyb.Pin.board.X8] = (1, 1, 1)
    channel_dict[pyb.Pin.board.X9] = (1)
    channel_dict[pyb.Pin.board.X10] = (2)
    channel_dict[pyb.Pin.board.X11] = None
    channel_dict[pyb.Pin.board.X12] = None
    channel_dict[pyb.Pin.board.X17] = None
    channel_dict[pyb.Pin.board.X18] = None
    channel_dict[pyb.Pin.board.X19] = None
    channel_dict[pyb.Pin.board.X20] = None
    channel_dict[pyb.Pin.board.X21] = None
    channel_dict[pyb.Pin.board.X22] = None

    channel_dict[pyb.Pin.board.P2] = None
    channel_dict[pyb.Pin.board.P3] = None
    channel_dict[pyb.Pin.board.P4] = None
    channel_dict[pyb.Pin.board.P5] = None

    # A dictionary to keep track of the timers that are available?
    timer_avail = {}

    def get_timer(self, pin, index=0):
        try:
            timer_number = TimerHelper.timer_dict[pin][index]
            timer_channel_number = TimerHelper.timer_channel[pin][index]
        except TypeError:
            timer_number = TimerHelper.timer_dict[pin]
            timer_channel_number = TimerHelper.timer_channel[pin]

        return (timer_number, timer_channel_number)