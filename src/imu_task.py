"""
imu_task.py
***********
Michael George
Chad Bickel
Oscar Ruiz

A Task to update the shared sensor reading dictionary with the imu readings
"""

from task_manager import Task

class IMUTask(Task):
    def __init__(self, imu, sensor_reading_dict):
        self.imu = imu
        self.sensor_reading_dict = sensor_reading_dict

    def run(self):
        self.sensor_reading_dict["pitch"] = self.imu.get_pitch()
        self.sensor_reading_dict["roll"] = self.imu.get_roll()
        self.sensor_reading_dict["yaw"] = self.imu.get_yaw_rate()