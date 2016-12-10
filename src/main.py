"""
..  module:: main.py
    : platform: Pycom LoPy
    :synopsis: pyCopter - the micropython quadcopter main file

..  topic:: Authors

    | Chad Bickel
    | Oscar Ruiz
    | Michael George


In this file you will find the main code which makes use of the libraries and tasks that we have written to run the
quadcopter. It is from this file that the all of the task objects are made and the task_manager is ran.

..  topic:: TODO/BUGS

    * Speed up implementation by switching many datatypes from dict to array
    * Implement many Enums for cases where dictionaries were being used
    * Speed up ground control socket by popping backwards till all setpoints are good.

"""

# All of the required libraries:
try:
    import micropython
    # from pyb import Servo, millis#, I2C  # ****** To change as we port to the LoPy
    from machine import I2C,PWM,Pin
    from servo_lib import Servo
    from motor_control_task import MotorControlTask
    from BNO055_lib import BNO055
    import time
    # from rfComm import SpektrumController, ServoPulse
    from pid_controller_task import PIDControlTask
    from imu_task import IMUTask
    import sys
    import json
    from bmp180 import BMP180
    from task_manager import TaskManager, ProtectedData
    from ground_control import GroundControlSocketTask
    import gc
except ImportError:
    print("ImportError: Are you in uPy? ")
    pass


# Set debugging to true for a lot of printing and waiting for input
global debugging
global calibrate_esc
debugging = True
calibrate_esc = False

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
    global debugging
    global calibrate_esc

    # Enable garbage collection
    gc.enable()

    if debugging:
        # for debugging, wait till a user hits enter
        input("Press any key to continue main")

    # Instantiate servo objects which are connected to the ESCs that control the electric motors that
    # generate thrust for the quadcopter
    # Had to swap servo 1 and 3 different from thier labels on the PCB due
    # to mismatches.
    servo1 = Servo('P23')
    servo2 = Servo('P20')
    servo3 = Servo('P19')
    servo4 = Servo('P22')

    # Instantiate the protected data classes for data that will be shared between tasks
    # Load in the initial configuration data
    gain_dict = ProtectedData(load_config_file("gain_config.json"))
    sensor_reading_dict = ProtectedData({})
    set_point_dict = ProtectedData({"pitch": 0, "roll":0, "yaw":0, "thrust":0})
    speed_list = ProtectedData([0, 0, 0, 0])

    # Instantiate the necessary sensors required for quadcopter control
    # Pressure Sensor
    i2c_bus = I2C(0)
    bmp180 = BMP180(i2c_bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325


    # 9 DOF IMU sensor for craft attitude readings
    uart_bus = machine.UART(1, 115200)
    imu = BNO055(uart_bus)

    # Instantiate the tasks:
    # Instantiate the IMUSensorTask which will update the sensor_reading_dict
    imu_task = IMUTask(imu, sensor_reading_dict)
    # Instantiate the Motor Control Task which will be responsible for updating the output to the motors
    motor_task = MotorControlTask(servo1, servo2, servo3, servo4, speed_list, calibrate=calibrate_esc)
    # Instantiate the PID control task which will update the outputs to the motors
    pid_task = PIDControlTask(gain_dict, sensor_reading_dict, set_point_dict, speed_list)
    # Instantiate the ground control socket task
    setpoint_command_map = {"p": "pitch", "r": "roll", "y": "yaw", "t": "thrust"}
    ground_control_task = GroundControlSocketTask(set_point_dict, setpoint_command_map)
    # Make a task manager to add tasks to
    task_manager = TaskManager()
    # Add all of the tasks to the task_manager
    # task_manager.add_new_task("imu task", .005, imu_task)
    # task_manager.add_new_task("motor task", .01, motor_task)
    # task_manager.add_new_task("pid task", .005, pid_task)

    runs = 0
    last_runs = 0
    try:
        while True:
            t = utime.ticks_ms()

            imu_task.run()

            ground_control_task.run()

            # if debugging:
            #     print("Set-point from main: ",  set_point_dict.getData())

            pid_task.run()

            # temp = bmp180.temperature
            # p = bmp180.pressure
            # altitude = bmp180.altitude
            # print(temp, p, altitude)

            motor_task.run()
            # if debugging:
                # print("Speeds: ", speed_list.getData())
                # print ("Pitch: ", sensor_reading_dict["pitch"], "\tRoll: ", sensor_reading_dict["roll"],
                #       "Yaw: ", sensor_reading_dict["yaw"])
                # delta = time.ticks_diff(t, time.ticks_us())
                #print("delta = ", delta/1000, " ms")

            runs += 1
            if runs - last_runs >10:
                print("Loop time diff: ", utime.ticks_ms() - t, "ms")
                print(set_point_dict.getData())
                print(sensor_reading_dict.getData())
                print("Memory Allocated: ", gc.mem_alloc(),
                      "  Memory Free: ", gc.mem_free())
                last_runs = runs
                gc.collect()

    except:
        task_manager.kill_all_tasks()
        # Make sure to kill motors at zero speed
        speed_list.putData([0, 0, 0, 0])
        # Run the motor task a last time to output 0 speed to motors
        motor_task.run()
        # Deinitialize the IMU so that the i2c bus doesn't get messed up
        # imu.deinit_i2c()

        # Close the ground control sockets
        ground_control_task.close_socket()

        # if debugging:
        #     # wait for user input so that bug is printed to user
        #     input("Press any button for error")

        # Re-raise the exception for debugging purposes
        raise


if __name__ == '__main__':
    main()
