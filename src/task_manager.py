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
                my_manager.addTask(some_task, some_task_timing_ms)

"""

import _thread
import time


class ProtectedData:
   def __init__(self, data):
      self.data = data
      self.lock = _thread.allocate_lock()

   def getData(self):
      with self.lock:
         return self.data

   def putData(self, new_data):
      with self.lock:
         self.data = new_data

class Task:
    def __init__(self):
        raise NotImplementedError("Individual (children) tasks must implement task constructor")

    def run(self):
        raise NotImplementedError("Individual (children) tasks must implement run method")



class TaskManager:
   thread_dict = {}
   def __init__(self, name, timing, task_callback, callback_arguments = [None]):
      if name not in TaskManager.thread_dict.keys():
         self.name = name
         print("Task Create Named: ", self.name)
         self.task_callback = task_callback
         self.callback_arguments = callback_arguments
         self.exit_flag = ProtectedData(False)
         self.timing = timing
         TaskManager.thread_dict[name] = self.exit_flag
         self.task_runs = ProtectedData(0)
         _thread.start_new_thread(self.wrapped_callback, tuple())
      else:
         print("Task name: ", name, " already in use")
         print("please alter to have a unique name")

   def wrapped_callback(self):
      print("Starting thread for Task: ", self.name)
      while not self.exit_flag.getData():
         self.task_callback(*self.callback_arguments)
         runs = self.task_runs.getData()
         runs += 1
         self.task_runs.putData(runs)
         time.sleep(self.timing)
      print("Ending thread for Task: ", self.name)

   def end_task(self):
      self.exit_flag.putData(True)

   def get_runs(self):
      return self.task_runs.getData()

   @staticmethod
   def kill_all_tasks():
      for exit_flag in TaskManager.thread_dict.values():
         exit_flag.putData(True)
      print("All tasks were flagged to end")


def add_by_1_task(number):
   number += 1

number = 0
task1 = TaskManager("Add By 1", 3, add_by_1_task, [number])