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
from pyb import Servo, millis, I2C  # ****** To change as we port to the LoPy
from motor_control_task import MotorControlTask
from BNO055_lib import BNO055
import time
from rfComm import SpektrumController, ServoPulse
from pid_controller_task import PIDControlTask
from imu_task import IMUTask
import sys
import json
from bmp180 import BMP180
from task_manager import TaskManager, ProtectedData


# ----------------------------------------------------------------------
def load_config_file(config_file):
    """
    A function to load a .json configuration file, parse the json entries, and return a python
    dictionary with all of the .json entries.
    :param config_file: String, the path to the config file to open
    :return: The config dictionary parsed from the .json file
    """
    with open(config_file, mode='r') as file:
        try:
            config_dict = json.loads(file.read())
        except json.JSONDecodeError:
            print("ERROR: Invalid Configuration File '" + str(file) +"'")
            return None
        return config_dict

# ----------------------------------------------------------------------
def main():
    """
    Function which contains the main code to run and from which all subsequent processes will branch from.
    """

    # Instantiate servo objects which are connected to the ESCs that control the electric motors that
    # generate thrust for the quadcopter
    servo1 = pyb.Servo(1)
    servo2 = pyb.Servo(2)
    servo3 = pyb.Servo(3)
    servo4 = pyb.Servo(4)

    # Instantiate the protected data classes for data that will be shared between tasks
    # Load in the initial configuration data
    gain_dict = ProtectedData(load_config_file("gain_config.json"))
    sensor_reading_dict = ProtectedData({})
    set_point_dict = ProtectedData({})
    speed_list = ProtectedData([0, 0, 0, 0])

    # Instantiate the necessary sensors required for quadcopter control
    # Pressure Sensor
    bmp180 = BMP180()
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

    # 9 DOF IMU sensor for craft attitude readings
    try:
        imu = BNO055()
    except OSError as e:
        print("Communication Error with the BNO055. \n")
        print("Exception: OSError ", e)
        time.sleep(2)
        sys.exit()

    # Instantiate the tasks:
    # Instantiate the IMUSensorTask which will update the sensor_reading_dict
    imu_task = IMUTask(imu, sensor_reading_dict)
    # Instantiate the Motor Control Task which will be responsible for updating the output to the motors
    motor_task = MotorControlTask(servo1, servo2, servo3, servo4, speed_list)
    # Instantiate the PID control task which will update the outputs to the motors
    pid_task = PIDControlTask(gain_dict, sensor_reading_dict, set_point_dict, speed_list)

    # Make a task manager to add tasks to
    task_manager = TaskManager()
    # Add all of the tasks to the task_manager
    # task_manager.add_new_task("imu task", .005, imu_task)
    # task_manager.add_new_task("motor task", .01, motor_task)
    # task_manager.add_new_task("pid task", .005, pid_task)
    try:
        while True:
            t = time.ticks_us()

            imu_task.run()

            # Set setpoint to 0 for tests
            set_point_dict["pitch"] = 0
            set_point_dict["roll"] = 0
            set_point_dict["yaw"] = 0
            set_point_dict["thrust"] = 0

            pid_task.run()

            # temp = bmp180.temperature
            # p = bmp180.pressure
            # altitude = bmp180.altitude
            # print(temp, p, altitude)

            motor_task.run()

            # print ("Pitch: ", sensor_reading_dict["pitch"], "\tRoll: ", sensor_reading_dict["roll"])
            delta = time.ticks_diff(t, time.ticks_us())
            #print("delta = ", delta/1000, " ms")
    except:
        task_manager.kill_all_tasks()
        # Make sure to kill motors at zero speed
        speed_list.putData([0, 0, 0, 0])
        # Run the motor task a last time to output 0 speed to motors
        motor_task.run()
        # Deinitialize the IMU so that the i2c bus doesn't get messed up
        IMU.deinit_i2c()
        # Re-raise the exception for debugging purposes
        raise


if __name__ == '__main__':
    main()
