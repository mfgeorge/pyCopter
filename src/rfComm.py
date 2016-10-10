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

    def __init__(self, thro_pin, aile_pin, elev_pin, rudd_pin, gear_pin, aux1_pin, smoothing_factor=1):
        self.thro_pulse = ServoPulse(thro_pin)
        self.aile_pulse = ServoPulse(aile_pin)
        self.elev_pulse = ServoPulse(elev_pin)
        self.rudd_pulse = ServoPulse(rudd_pin)
        self.gear_pulse = ServoPulse(gear_pin)
        self.aux1_pulse = ServoPulse(aux1_pin)
        self.smoothing_factor = smoothing_factor
        self.last_thrust = 0
        self.last_roll = 0
        self.last_yaw = 0
        self.last_pitch = 0

    def get_thrust(self):
        value = (self.thro_pulse.get_width() - 1048)/(1933 - 1048)*50
        self.last_thrust = value
        return value

    def get_roll(self):
        value = (self.aile_pulse.get_width() - 1094)/(1893 - 1094)*50-25
        self.last_roll = value
        return value 

    def get_pitch(self):
        value = (self.elev_pulse.get_width() - 1077)/(1876 - 1077)*50-25
        self.last_pitch = value
        return value 

    def get_yaw(self):
        value = (self.rudd_pulse.get_width() - 1086)/(1876 - 1086)*50-25
        self.last_yaw = value
        return value 

    def get_switch1(self):
        value = 1 if self.gear_pulse.get_width() > 1500 else 0
        return value

    def get_switch2(self):
        value = 1 if self.aux1_pulse.get_width() > 1500 else 0
        return value

"""
A servo_pulse Class written by wagnerc4 on github and modified by michael george for our
purposes
"""
class ServoPulse:
    start = width = last_width = 0

    def __init__(self, pin, timer=pyb.Timer(8, prescaler=83, period=0xffff)):
        self.pulseCounter = timer
        self.tickConversion = 1e6/(self.pulseCounter.freq()*self.pulseCounter.period())
        # input("Any key to continue configuring external interrupts")
        self.pin = pin
        self.interrupt = pyb.ExtInt(self.pin, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_NONE, self.callback)
        self.interrupt.enable()
        print("External Interrupt Set up on Line: ", self.interrupt.line())

    def callback(self, line):
        now = self.pulseCounter.counter()
        if self.pin.value(): 
            self.start = now
        else: 
            self.width = (now - self.start) & 0xffff

    def get_width(self):
        w = self.width*self.tickConversion
        # print(w)
        self.last_width = w if w > 950 and w < 1950 else self.last_width
        return self.last_width

    def __del__(self):
        self.timer.deinit()
        self.interrupt.disable()

