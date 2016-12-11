"""
..  module:: mtk_gps_driver
    :platform: Pycom LoPy
    :synopsis: Driver for getting gps data from the gps

..  topic:: Author

    Michael George

A module for housing the MTKGPS driver which will obtain readings from the
GPS and implement function calls for retrieving the most up to date version
of those readings.
"""

from micropyGPS import MicropyGPS
import mtk

class MTKGPS:
    """
    Task for the adafruit ultimate gps featherWing module. This class is instantiated with a UART object that is
    configured for the correct UART bus that the GPS is connected to. It wraps the implementation of MtkCommandRx so
    that it supplies characters to this class, letting the class perform the error checking and sentence generation.
    Subsequently, this class will utilize microPyGPS to interpret the sentence and return position data.

    :param uart_object: a pre-initialized uart bus object at 9600 baudrate,
        No parity, no stop bit.
    """
    def __init__(self, uart_object):
        """
        Constructor for MTKGPS class
        """
        # Set up and store all objects needed by task
        self.uart = uart_object
        self.mtk_checker = mtk.MtkCommandRx()
        self.interpretter = MicropyGPS()

        # Configure the GPS module for GPRMC and GPGGA
        self.uart.write(mtk.update_sentences(en_rmc=True, en_gga=True, en_gsv=False,
                                             en_gsa=False, en_vtg=False, en_gll=False))
        # Confirm that command was received
        self.check_command_success()

        # Set Update Rate to 10Hz
        self.uart.write(mtk.update_nmea_rate(10))
        # Check for Confirmation of Command
        self.check_command_success()

        # Initialize a place to store interpreted sentence type
        self.sentence_type = None


    def get_next_sentence_char(self):
        """
        gets the next character from the uart bus and updates the interpretter
        with it.
        """
        if self.uart.any():
            self.sentence_type = self.interpretter.update(chr(self.uart.readchar()))

    def get_latitude(self):
        """
        Method for obtaining the latitude position of the GPS

        :return: Latitude GPS position
        """
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.latitude
        else:
            return None

    def get_longitude(self):
        """
        Method for obtaining the longitude position of the GPS

        :return: Longitude GPS position
        """
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.longitude
        else:
            return None

    def get_heading(self):
        """
        Method for getting the heading according to the GPS.

        :return: Heading direction in degrees
        """
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.course
        else:
            return None

    def get_altitude(self):
        """
        Gets the altitude based upon the GPS satellite triangulation.

        :return: altitude in meters
        """
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.altitude
        else:
            return None

    def get_fix(self):
        """
        Reports whether or not the GPS has obtained a fix.

        :return: number of satellites the GPS has a fix on
        """
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.fix_type
        else:
            return None

    def check_command_success(self):
        """
        To be ran after a command is sent to the MTK board to indicate success

        :return: True for success, False if Timeout reached
        """
        result = None
        while not result:
            while self.uart.any():
                result = self.mtk_checker.update(chr(self.uart.readchar()))
                if result:
                    if result[-4] == '3':
                        print('Command Succeeded:', result)
                        return False
                    else:
                        return False
        return False
