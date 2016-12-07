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
            pitch = bno.get_pitch()
            print("Pitch from sensor: ", pitch)
            utime.sleep_ms(100)
    except KeyboardInterrupt:
        print("Ending BNO UART Test Program")
        pass

    return bno

if __name__ == '__main__':
    bno  = main()
