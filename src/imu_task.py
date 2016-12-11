"""
..  module: imu_task
    :platform: Pycom LoPy
    :synopsis: Task for gaining imu data

..  topic: Authors

    | Michael George
    | Chad Bickel
    | Oscar Ruiz

Module for housing the IMUTask which updates the sensor readings
"""

from task_manager import Task


class IMUTask(Task):
    """
    A Task to update the shared sensor reading dictionary with the imu readings

    :param imu: :class:`BNO055_lib.BNO055` object to get readings from
    :param sensor_reading_dict: the shared :class:`task_manager.ProtectedData`
        dictionary which will contain sensor readings.
    """
    def __init__(self, imu, sensor_reading_dict):
        """
        Constructor for IMUTask
        """
        self.imu = imu
        self.sensor_reading_dict = sensor_reading_dict

    def run(self):
        """
        Run method of this class will update the *sensor_reading_dict*
        with fresh readings.
        """
        self.sensor_reading_dict["pitch"] = self.imu.get_pitch()
        self.sensor_reading_dict["roll"] = self.imu.get_roll()
        self.sensor_reading_dict["yaw"] = self.imu.get_yaw_rate()