"""
main.py
*******
pyCopter - the micropython quadcopter main file
Chad Bickel
Oscar Ruiz
Michael George

In this file you will find the main code which makes use of the libraries and tasks that we have written to run the
quadcopter. It is from this file that the all of the task objects are made and the task_manager is ran.

TODO:
=====
    * Test the new task scheme with while loop
    * Test the new task scheme using task_manager
    * Implement a bmp180 task/ or add to imu_task? see task diagram
    * Implement a GPS sensor query task 
        -> add the GPS sensor queries as inputs to the PID task
    * Implement a ground control task

"""

# All of the required libraries:
import micropython
from machine import I2C
import sys
from bmp180 import BMP180
import time

bus = I2C(0, baudrate=100000)  
# ----------------------------------------------------------------------
def main():
    """
    Function which contains the main code to run and from which all subsequent processes will branch from.
    """
    # Instantiate the necessary sensors required for quadcopter control
    # Pressure Sensor
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    while True:

        temp = bmp180.temperature
        p = bmp180.pressure
        altitude = bmp180.altitude
        print(temp, p, altitude)
	time.sleep(500)



if __name__ == '__main__':
    main()
