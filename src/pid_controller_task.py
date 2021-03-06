"""
..  module: imu_task
    :platform: Pycom LoPy
    :synopsis: Task for gaining imu data

..  topic:: Authors

    | Michael George
    | Chad Bickel
    | Oscar Ruiz

A task to execute all of the PID control loops, and fuse their output together.

..  topic:: TODO

    * Add logic to only engage control once throttle is at a minimum value (no stabilization while on ground)
    * Add altitude control
    * Add GPS control
"""

import PID_lib
from task_manager import Task
import time
# from misc import timed_function

class PIDControlTask(Task):
    """
    A class to run the PID control for the quadcopter. This class houses all the controllers for stabilizing flight and
    manages them by updating their control loop. This task has specific timing requirements
    """
    def __init__(self, gain_dict, sensor_reading_dict, set_point_dict, output_list, time_log, val_log):
        """
        Constructor for the PID control class.
        :param gain_dict: A ProtectedData dictionary containing the key values "roll","pitch","yaw", and "thrust"
                            which have sub-dictionaries containing keys "P","I", "D", "windup_guard", and
                            "sample_time" which contain the gain values.
                            Using the **gain_dict["roll"] as the argument to a PID constructor
                            will shove the P, I, and D values into the constructor appropriately since P, I, and D
                            are the argument names taken by the constructor.
        :param sensor_reading_dict: a ProtectedData dictionary containing keys pitch, roll, yaw, ect for each sub-controller
                                    with feedback values for each sub-controller
        :param set_point_dict: a fused_output = [0,0,0,0]ProtectedData dictionary containing keys pitch, roll, yaw, ect for each sub-controller
                                    with set-point values for each sub-controller.

        """
        # Store the needed dictionaries
        self.gain_dict = gain_dict
        self.sensor_reading_dict = sensor_reading_dict
        self.set_point_dict = set_point_dict

        # Store the log arrays
        self.time_log = time_log
        self.val_log = val_log

        # Instantiate the needed controllers
        self.pitch_controller = PID_lib.PID()
        self.roll_controller = PID_lib.PID()
        self.yaw_controller = PID_lib.PID()

        # same as: pitch_controller.setMemberData(gain_dict["pitch"]["P"], gain_dict["pitch"][I], gain_dict["pitch"]["D"])
        self.pitch_controller.setMemberData(**gain_dict["pitch"])
        self.roll_controller.setMemberData(**gain_dict["roll"])
        self.yaw_controller.setMemberData(**gain_dict["yaw"])

        self.output_list = output_list

    def run(self):
        """
        Function to run the PIDControlTask task managing all the sub-PID controllers

        :return fused_output: A list of fused output of all the sub-controllers
        """
        # update the setpoint of each controller
        temp_set_point_dict = self.set_point_dict.getData()

        # print("Setpoint from PID ctl: ", temp_set_point_dict)

        self.pitch_controller.SetPoint = temp_set_point_dict["pitch"]
        self.roll_controller.SetPoint = temp_set_point_dict["roll"]
        self.yaw_controller.SetPoint = temp_set_point_dict["yaw"]


        # update the feedback values of each controller
        temp_sensor_reading_dict = self.sensor_reading_dict.getData()

        # print("Sensor dict in task pid: ", temp_sensor_reading_dict)

        self.pitch_controller.update(temp_sensor_reading_dict["pitch"])
        self.roll_controller.update(-1*temp_sensor_reading_dict["roll"])
        self.yaw_controller.update(temp_sensor_reading_dict["yaw"])

        # fuse all the outputs of the controllers together and return it in a length 4 list
        output_list = [self.pitch_controller.output - self.roll_controller.output - self.yaw_controller.output,
                        self.pitch_controller.output + self.roll_controller.output + self.yaw_controller.output,
                        -self.pitch_controller.output + self.roll_controller.output - self.yaw_controller.output,
                        -self.pitch_controller.output - self.roll_controller.output + self.yaw_controller.output]

        # add thrust on top of everything
        output_list = [output + temp_set_point_dict["thrust"] for output in output_list]

        # Saturate everything to 180 and 0
        for index, output in enumerate(output_list):
            if output > 180:
                output_list[index] = 180
            elif output < 0:
                output_list[index] = 0
        #print("Output list is: ", output_list)

        self.output_list.putData(output_list)

        # log some data
        self.time_log.append(time.ticks_ms())
        self.val_log.append(temp_sensor_reading_dict["pitch"])

    def update_gain_dict(self, gain_dict):
        """
        Function to update the the member data of all the sub-controllers due to the shared gain_dict changing.
        The plan is to call this method after obtaining a dictionary generated by a json config file containing
        all of our controller parameters.

        :param gain_dict: A dict containing all sub-controller parameters to update to
        """
        # Grab the new shared gain dictionary
        gain_dict = self.gain_dict.getData().copy()
        self.pitch_controller.setMemberData(**gain_dict["pitch"])
        self.roll_controller.setMemberData(**gain_dict["roll"])
        self.yaw_controller.setMemberData(**gain_dict["yaw"])
        # set the member data of other controllers also