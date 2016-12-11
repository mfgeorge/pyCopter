#!/bin/python
"""
Miscillaneous file for classes that help get things done.
"""

# Handle the case where we aren't in micropython for documentation
# generation
try:
    import pyb
    import utime
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries import utime, pyb

class TimerHelper:
    'A simple class for helping pick timers and channels based upon pin number'

    #: class varible for storing all the possible timer selections based upon pin
    #: due to it being a class varible, this dictionary is only created once upon the first
    #: instantiation of this class.
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


    #: class varible for storing all the possible channel selections based upon pin
    #: due to it being a class varible, this dictionary is only created once upon the first
    #: instantiation of this class.
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

    #: A dictionary to keep track of the timers that are available
    timer_avail = {}

    def get_timer(self, pin, index=0):
        """
        A method to get a timer connected to a pin.

        :param pin: Pin that timer should be connected to
        :param index: the index of the timer on that pin (for the
            case of multiple timers connected to one pin).
        :return: The timer number and channel associated with that pin.
        """
        try:
            timer_number = TimerHelper.timer_dict[str(pin)][index]
            timer_channel_number = TimerHelper.channel_dict[str(pin)][index]
        except TypeError:
            timer_number = TimerHelper.timer_dict[str(pin)]
            timer_channel_number = TimerHelper.channel_dict[str(pin)]

        return (timer_number, timer_channel_number)


def timed_function(f, *args, **kwargs):
    """
    Obtained from the micropython documentation.
    A function decorator which will time the function that was decorated.
    """
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_ms()
        result = f(*args, **kwargs)
        delta = utime.ticks_ms() - t
        print('Function {} Time = {:6.3f}ms'.format(myname, delta))
        return result
    return new_func