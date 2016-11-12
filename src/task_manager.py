"""
task_manager.py
***************
Michael George
11/10/16

A module for micropython which utilizes the primitive _thread module to schedule tasks, and keep track of their
exit flag.

The ProtectedData class should be used by any class that needs to share any data between threads/ other tasks
        example: shared_int = ProtectedData(some_integer)
                Access in tasks using:
                        shared_int.putData(new_int)
                        current_shared_int = shared_int.getData()

The Task class should be extended by all classes which are classified as tasks. The task class is a pure virtual task,
meaning that it only lays out the methods that need to be defined and overriden in order for the Task to be called
by the task manager. This consists of:
                    * The constructor
                    * The .run() method
        minimum example: my_task_class(Task):
                            def __init__(self, *args):
                                # Some unique initialization specific to that task
                            def run(self):
                                # The code that will be performed upon each call of the task
                                # DO NOT PLACE ANY BLOCKING CODE HERE OR ANYTHING THAT SLEEPS, THIS CODE MUST
                                # BE INTENDED TO BE USED IN A COOPERATIVE MULTITASKING ENVIRONMENT (YES, EVEN THOUGH
                                # THREADING IS BEING USED). THE TASK MANAGER WILL CONTROL THE TIMING AND SLEEP CALLS.

The TaskManager class should be used (preferably only one constructed for the project) to manage all of the tasks.
Most importantly, the TaskManager is in control of the timing of each task, and calls each task's .run() method
It stores exit flags so that tasks can be ended if necessary, as well as keeps track of the amount of calls that a
task has received. The task manager is also able to kill all tasks if necessary.
        example:
                some_task = SomeTaskConstructor(*args)
                my_manager = TaskManager()
                my_manager.addTask("Some Task Name", some_task, some_task_timing_ms)

"""

import _thread
import time
from enum import Enum


class ProtectedData:
    """
    Class to facilitate thread safe variables.
    """
    def __init__(self, data):
        """
        Constructor for the ProtectedData class
        :param data: The data that needs protecting.
                    Note** That objects will be a reference to the constructed one, while primitive data types
                    will be copies!
        """
        self.data = data
        self.lock = _thread.allocate_lock()

    def getData(self):
        """

        :param self:
        :return:
        """
        with self.lock:
            return self.data

    def putData(self, new_data):
        """

        :param self:
        :param new_data:
        :return:
        """
        with self.lock:
            self.data = new_data

class Task:
    """
    Pure Virtual Class to extend for each class. Each child task can then be added to TaskManager for running.
    """
    def __init__(self, *args):
        # Some unique initialization specific to that task
        raise NotImplementedError("Individual (children) tasks must implement task constructor")

    def run(self):
        # The code that will be performed upon each call of the task
        # DO NOT PLACE ANY BLOCKING CODE HERE OR ANYTHING THAT SLEEPS, THIS CODE MUST
        # BE INTENDED TO BE USED IN A COOPERATIVE MULTITASKING ENVIRONMENT (YES, EVEN THOUGH
        # THREADING IS BEING USED). THE TASK MANAGER WILL CONTROL THE TIMING AND SLEEP CALLS.
        raise NotImplementedError("Individual (children) tasks must implement run method")



class TaskManager:
    """
    Class to manage task's timing, exit flags, and thread instantiation.
    """
    class info(Enum):
        task = 0
        runs = 1
        timing = 2
        exit = 3
    def __init__(self):
        # Each entry has task name as key and a list of [task_object, run_count, timing, exit flag]
        self.thread_dict = {}



    def add_new_task(self, task_name, timing, task_object):
        if task_name not in self.thread_dict.keys():
            exit_flag = ProtectedData(False)
            run_count = ProtectedData(0)
            self.thread_dict[task_name] = (task_object, run_count, timing, exit_flag)
            print("Task ", task_name, " added to TaskManager")
            _thread.start_new_thread(self.wrapped_callback, (task_name, ))
        else:
            print("Task name: ", task_name, " already in use")
            print("please alter to have a unique name")

    def wrapped_callback(self, task_name):
        task = self.thread_dict[task_name][0]
        run_count = self.thread_dict[task_name][1]
        timing = self.thread_dict[task_name][2]
        exit_flag = self.thread_dict[task_name][3]
        print("Starting thread for Task: ", task_name)
        while not exit_flag.getData():
            task.run()
            runs = run_count.getData()
            runs += 1
            run_count.putData(runs)
            time.sleep(timing)
        print("Ending thread for Task: ", task_name)

    def end_task(self, task_name):
        self.thread_dict[task_name][3].putData(True)

    def get_runs(self, task_name):
        return self.thread_dict[task_name][1].getData()

    def kill_all_tasks(self):
        for exit_flag in self.thread_dict.values():
            exit_flag[3].putData(True)
        print("All tasks were flagged to end")




"""
task_manager Tests
==================
The test function below illustrates a simple example of how this module should be used as well
as tests its functionality
"""
def test():
    class add_by_1_task(Task):
        def __init__(self, protected_number):
            self.number = protected_number
        def run(self):
            number = self.number.getData()
            number += 1
            self.number.putData(number)

    shared_number = ProtectedData(0)
    task_1 = add_by_1_task(shared_number)
    task_manager = TaskManager()
    task_manager.add_new_task("add by 1", .1, task_1)
    while True:
        try:
            time.sleep(1)
            print("Runs: ", task_manager.get_runs("add by 1"))
            print("Number is: ", shared_number.getData())
        except KeyboardInterrupt:
            task_manager.kill_all_tasks()
            time.sleep(3)
            break
    print("Goodbye!")


if __name__ == "__main__":
    test()


