"""
main.py - in BNO-test
*********************
Michael George

A main file to test the BNO055 sensor library

"""

#from BNO055_lib import BNO055
import machine
import time
import sys

def main(baud):
    i2c = machine.I2C(0, baudrate=baud)
    print("addresses on i2c bus: ", i2c.scan())
    bno = BNO055(i2c)

    try:
        while True:
            print("Pitch: %0.3f" % bno.get_pitch(), "\t Roll: %0.3f" % bno.get_roll(), end = '\r')
            time.sleep(.2)
            sys.stdout.write("\033[K")  # Clear the old text
    except KeyboardInterrupt:
        print("\n\nEnding Program! ")

if __name__ == '__main__':
    baud = 50000
    print("Running with baud = ", baud)
    main(baud)

