#!/bin/python
import pyb
import time
"""
Miscillaneous file for classes that help get things done.
"""

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


def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = time.ticks_us()
        result = f(*args, **kwargs)
        delta = time.ticks_diff(t, time.ticks_us())
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func