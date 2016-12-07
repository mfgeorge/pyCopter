"""
main.py - in BNO-test
*********************
Michael George

A main file to test the BNO055 sensor library

"""

from BNO055_lib import BNO055
from pyb import UART
import time
import sys

def main():
    uart = UART(3, 9600)                         # init with given baudrate
    uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

    try:
        bno = BNO055()

        while True:
            print("Pitch: %0.3f" % bno.get_pitch(), "\t Roll: %0.3f" % bno.get_roll(), end = '\r')
            
            buff = 'p_' + "%0.3f" % bno.get_pitch()+ ';' + "r_" + "%0.3f" % bno.get_roll() + ";" + "y_" + "%0.3f" % bno.get_yaw() + ";"

            uart.write(buff) 
            time.sleep_ms(10)
            sys.stdout.write("\033[K")  # Clear the old text

    except OSError:
        
        

if __name__ == '__main__':
    main()

