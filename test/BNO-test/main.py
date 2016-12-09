"""
main.py - in BNO-test
*********************
Michael George

A main file to test the BNO055 sensor library

"""

from BNO055_lib import BNO055
import machine
import utime
import sys

def main():
    print("Starting BNO UART Test Program")

    uart_bus = machine.UART(1, 115200)

    bno = BNO055(uart_bus)

    try:
        while True:
            print("Pitch: %0.3f" % bno.get_pitch(), "\t Roll: %0.3f" % bno.get_roll())
            utime.sleep_ms(200)
            sys.stdout.write("\033[F\033[K")  # Clear the old text
    except KeyboardInterrupt:
        print("Ending BNO UART Test Program")
        pass

    return bno

if __name__ == '__main__':
    bno  = main()
