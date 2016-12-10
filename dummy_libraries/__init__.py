"""
..  module:: dummy_libraries.py
    :platform: None
    :synopsis: A file for housing micropython dummy libraries

..  topic:: Author
    Michael George

A Module for housing micropython libraries that are not available in
normal python.
"""

class utime:

    @staticmethod
    def ticks_ms(*args):
        pass

    @staticmethod
    def sleep_ms(*args):
        pass

    @staticmethod
    def sleep_us(*args):
        pass