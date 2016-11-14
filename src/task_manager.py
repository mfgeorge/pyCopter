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
    Class to facilitate thread safe variables of primitive data type.
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
        Method to lock protected data and return it's value
        :return: the protected data
        """
        with self.lock:
            return self.data

    def putData(self, new_data):
        """
        Method to lock protected data and reassign it's data
        :param new_data: the new data to reassign
        """
        with self.lock:
            self.data = new_data
            return new_data

    # Container operator definition so that using container data types is easy
    def __getitem__(self, key):
        """
        Gets the item located at key in the dictionary
        :param key: the index or key of the item to get
        :return: the item at the specified key
        """
        with self.lock:
            return self.data[key]


    def __setitem__(self, key, value):
        """
        Sets the item located at key to the value specified
        :param key: the index or key of the item to set
        :param value: the value to set the item to
        :return: self so that object is preserved
        """
        with self.lock:
            self.data[key] = value
            return self

    def append(self, value):
        with self.lock:
            self.data.append(value)

    # Numeric Operator definition so using primitive numeric data types is easy
    def __eq__(self, other):
        """
        Test that the other value is equal to the data
        :param other: other value to compare with
        :return: boolean if data matches
        """
        return self.getData() == other

    def __iadd__(self, other):
        """
        Perform inline addition on the data present
        :param other: the value to add to the existing data
        :return: self so that the object is preserved
        """
        with self.lock:
            self.data += other
            return self

    def __lt__(self, other):
        """
        Perform less than comparison with data
        :param other: value to compare data with
        :return: boolean of the comparison
        """
        return self.getData() < other

    def ___le__(self, other):
        """
        Perform less than/ equal to comparison with data
        :param other: value to compare data with
        :return: boolean of the comparison
        """
        return self.getData() <= other

    def __ne__(self, other):
        """
        Perform not equal comparison with data
        :param other: value to compare data with
        :return: boolean of the comparison
        """
        return self.getData() != other

    def __gt__(self, other):
        """
        Perform greater than comparison with data
        :param other: value to compare data with
        :return: boolean of the comparison
        """
        return self.getData() > other

    def __ge__(self, other):
        """
        Perform greater than/equal to comparison with data
        :param other: value to compare data with
        :return: boolean of the comparison
        """
        return self.getData() >= other

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
        """
        Enum meant to be used with the thread_dict to keep track of placement
        """
        task = 0
        runs = 1
        timing = 2
        exit = 3

    def __init__(self):
        # Each entry has task name as key and a list of [task_object, run_count, timing, exit flag]
        self.thread_dict = {}

    def add_new_task(self, task_name, timing, task_object):
        """
        Adds a new Task object to the TaskManager, and starts it's thread.
        :param task_name: Name to identify the task with
        :param timing: The timing that the task must run at
        :param task_object: The previously defined task object whose .run() method will be called
        """
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
        """
        A wrapped callback for the task threads to use which facilitate using the correct exit_flag, incrementing runs,
        and the timing required.
        :param task_name: The name to identify the task by
        """
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

    def get_thread_dict(self):
        """
        A method for getting the thread dictionary that the TaskManager uses
        :return: the task manager thread_dict
        """
        return self.thread_dict

    def end_task(self, task_name):
        """
        Ends a specific task as identified by it's task_name
        :param task_name: the string name of the task to end
        """
        self.thread_dict[task_name][3].putData(True)

    def get_runs(self, task_name):
        """
        Gets the number of runs that a specific task has ran as identified by it's task_name
        :param task_name: the string name of the task whose runs to get
        :return:
        """
        return self.thread_dict[task_name][1].getData()

    def kill_all_tasks(self):
        """
        A method for killing all of the tasks being managed by the TaskManager
        """
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
    # Create a task class that extends Task
    class add_by_1_task(Task):
        def __init__(self, protected_number):
            self.number = protected_number
            self.number.append(0)
        def run(self):
            self.number[0] += 1
            # new_number = self.number.getData()
            # new_number += 1
            # self.number.putData(new_number)

    # list to house the number
    list = []
    # Create a number that will be used by the add_by_1_task
    shared_number = ProtectedData(list)
    # Instantiate the task
    task_1 = add_by_1_task(shared_number)
    # Instantiate a TaskManager to manage tasks
    task_manager = TaskManager()
    # Add the add_by_1_task to the TaskManager
    task_manager.add_new_task("add by 1", .1, task_1)
    # Print the dictionary of the TaskManager to see what it contains
    print(task_manager.get_thread_dict())
    # Run a main thread loop which simply reports stats about the add_by_1_task
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


