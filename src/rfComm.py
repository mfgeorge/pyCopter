#!/bin/python
import pyb

"""
Parent Class for any rf controller available 
Lays out what needs to be implemented so that all controllers 
will implement the same methods, no matter what type they are.
"""

class RFController6CH:
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

class SpektrumController(RFController6CH):
    'A class for a specific 6 channel Spektrum radio module.'

    def __init__(self, thro_pin, aile_pin, elev_pin, rudd_pin, gear_pin, aux1_pin):
        self.thro_pulse = ServoPulse(thro_pin)
        self.aile_pulse = ServoPulse(aile_pin)
        self.elev_pulse = ServoPulse(elev_pin)
        self.rudd_pulse = ServoPulse(rudd_pin)
        self.gear_pulse = ServoPulse(gear_pin)
        self.aux1_pulse = ServoPulse(aux1_pin)

    def get_thrust(self):
        return (self.thro_pulse.get_width() - 1048)/(1933 - 1048)*50

    def get_roll(self):
        return (self.aile_pulse.get_width() - 1094)/(1893 - 1094)*50

    def get_pitch(self):
        return (self.elev_pulse.get_width() - 1077)/(1876 - 1077)*50

    def get_yaw(self):
        return (self.rudd_pulse.get_width() - 1086)/(1876 - 1086)*50

    def get_switch1(self):
        ret = 1 if self.gear_pulse.get_width() > 1500 else 0
        return ret

    def get_switch2(self):
        ret = 1 if self.aux1_pulse.get_width() > 1500 else 0
        return ret

"""
A servo_pulse Class written by wagnerc4 on github and modified by michael george for our
purposes
"""
class ServoPulse:
    start = width = last_width = 0

    def __init__(self, pin, index=0):
        timer_dict = TimerHelper()
        timer_number, timer_channel_number = timer_dict.get_timer(pin,index)
        print("Timer: ", timer_number, "\t Channel: ", timer_channel_number)
        input("Any key to continue")
        timer = pyb.Timer(timer_number, prescaler=83, period=0x0fffffff)
        self.pin = pin
        self.channel = timer.channel(timer_channel_number,
                                    pyb.Timer.IC,
                                    pin=self.pin,
                                    polarity=pyb.Timer.BOTH)
        self.channel.callback(self.callback)

    def callback(self, timer):
        #print("interrupt")
        if self.pin.value(): 
            #print("HI")
            self.start = self.channel.capture()
        else: 
            #print("LO")
            self.width = (self.channel.capture() - self.start) & 0x0fffffff

    def get_width(self):
        w = self.width
        # print(w)
        self.last_width = w if w > 950 and w < 1950 else self.last_width
        return self.last_width

    def __del__(self):
        self.timer.deinit()


class TimerHelper:
    'A simple class for helping pick timers and channels based upon pin number'
    """
    timer_dict: class varible for storing all the possible timer selections based upon pin
    due to it being a class varible, this dictionary is only created once upon the first
    instantiation of this class.
    """
    timer_dict = {}
    timer_dict[str(pyb.Pin.board.Y1)] = (8)
    timer_dict[str(pyb.Pin.board.Y2)] = (8)
    timer_dict[str(pyb.Pin.board.Y3)] = (4, 10)
    timer_dict[str(pyb.Pin.board.Y4)] = (4, 11)
    timer_dict[str(pyb.Pin.board.Y5)] = None
    timer_dict[str(pyb.Pin.board.Y6)] = (1)
    timer_dict[str(pyb.Pin.board.Y7)] = (1, 8, 12)
    timer_dict[str(pyb.Pin.board.Y8)] = (1, 8, 12)
    timer_dict[str(pyb.Pin.board.Y9)] = (2)
    timer_dict[str(pyb.Pin.board.Y10)] = (2)
    timer_dict[str(pyb.Pin.board.Y11)] = (1, 8)
    timer_dict[str(pyb.Pin.board.Y12)] = (1, 8)

    timer_dict[str(pyb.Pin.board.X1)] = (2, 5)
    timer_dict[str(pyb.Pin.board.X2)] = (2, 5)
    timer_dict[str(pyb.Pin.board.X3)] = (2, 5, 9)
    timer_dict[str(pyb.Pin.board.X4)] = (2, 5, 9)
    timer_dict[str(pyb.Pin.board.X5)] = None
    timer_dict[str(pyb.Pin.board.X6)] = (2, 8)
    timer_dict[str(pyb.Pin.board.X7)] = (13)
    timer_dict[str(pyb.Pin.board.X8)] = (1, 8, 14)
    timer_dict[str(pyb.Pin.board.X9)] = (4)
    timer_dict[str(pyb.Pin.board.X10)] = (4)
    timer_dict[str(pyb.Pin.board.X11)] = None
    timer_dict[str(pyb.Pin.board.X12)] = None
    timer_dict[str(pyb.Pin.board.X17)] = None
    timer_dict[str(pyb.Pin.board.X18)] = None
    timer_dict[str(pyb.Pin.board.X19)] = None
    timer_dict[str(pyb.Pin.board.X20)] = None
    timer_dict[str(pyb.Pin.board.X21)] = None
    timer_dict[str(pyb.Pin.board.X22)] = None

    # timer_dict[str(pyb.Pin.board.P2)] = None
    # timer_dict[str(pyb.Pin.board.P3)] = None
    # timer_dict[str(pyb.Pin.board.P4)] = None
    # timer_dict[str(pyb.Pin.board.P5)] = None

    """
    channel_dict: class varible for storing all the possible channel selections based upon pin
    due to it being a class varible, this dictionary is only created once upon the first
    instantiation of this class.
    """
    channel_dict = {}
    channel_dict[str(pyb.Pin.board.Y1)] = (1)
    channel_dict[str(pyb.Pin.board.Y2)] = (2)
    channel_dict[str(pyb.Pin.board.Y3)] = (3, 1)
    channel_dict[str(pyb.Pin.board.Y4)] = (4, 1)
    channel_dict[str(pyb.Pin.board.Y5)] = None
    channel_dict[str(pyb.Pin.board.Y6)] = (1)
    channel_dict[str(pyb.Pin.board.Y7)] = (2, 2, 1)
    channel_dict[str(pyb.Pin.board.Y8)] = (3, 3, 2)
    channel_dict[str(pyb.Pin.board.Y9)] = (3)
    channel_dict[str(pyb.Pin.board.Y10)] = (4)
    channel_dict[str(pyb.Pin.board.Y11)] = (2, 2)
    channel_dict[str(pyb.Pin.board.Y12)] = (3, 3)

    channel_dict[str(pyb.Pin.board.X1)] = (1, 1)
    channel_dict[str(pyb.Pin.board.X2)] = (2, 2)
    channel_dict[str(pyb.Pin.board.X3)] = (3, 3, 1)
    channel_dict[str(pyb.Pin.board.X4)] = (4, 4, 2)
    channel_dict[str(pyb.Pin.board.X5)] = None
    channel_dict[str(pyb.Pin.board.X6)] = (1, 1)
    channel_dict[str(pyb.Pin.board.X7)] = (1)
    channel_dict[str(pyb.Pin.board.X8)] = (1, 1, 1)
    channel_dict[str(pyb.Pin.board.X9)] = (1)
    channel_dict[str(pyb.Pin.board.X10)] = (2)
    channel_dict[str(pyb.Pin.board.X11)] = None
    channel_dict[str(pyb.Pin.board.X12)] = None
    channel_dict[str(pyb.Pin.board.X17)] = None
    channel_dict[str(pyb.Pin.board.X18)] = None
    channel_dict[str(pyb.Pin.board.X19)] = None
    channel_dict[str(pyb.Pin.board.X20)] = None
    channel_dict[str(pyb.Pin.board.X21)] = None
    channel_dict[str(pyb.Pin.board.X22)] = None

    # channel_dict[str(pyb.Pin.board.P2)] = None
    # channel_dict[str(pyb.Pin.board.P3)] = None
    # channel_dict[str(pyb.Pin.board.P4)] = None
    # channel_dict[str(pyb.Pin.board.P5)] = None

    # A dictionary to keep track of the timers that are available?
    timer_avail = {}

    def get_timer(self, pin, index=0):
        try:
            timer_number = TimerHelper.timer_dict[str(pin)][index]
            timer_channel_number = TimerHelper.channel_dict[str(pin)][index]
        except TypeError:
            timer_number = TimerHelper.timer_dict[str(pin)]
            timer_channel_number = TimerHelper.channel_dict[str(pin)]

        return (timer_number, timer_channel_number)