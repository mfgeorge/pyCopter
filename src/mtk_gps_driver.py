from micropyGPS.micropyGPS import MicropyGPS
from MTK_commands import mtk

class MTKGPS:
    """
    Task for the adafruit ultimate gps featherWing module. This class is instantiated with a UART object that is
    configured for the correct UART bus that the GPS is connected to. It wraps the implementation of MtkCommandRx so
    that it supplies characters to this class, letting the class perform the error checking and sentence generation.
    Subsequently, this class will utilize microPyGPS to interpret the sentence and return position data.
    """
    def __init__(self, uart_object):
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
        if self.uart.any():
            self.sentence_type = self.interpretter.update(chr(self.uart.readchar()))

    def get_latitude(self):
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.latitude
        else:
            return None

    def get_longitude(self):
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.longitude
        else:
            return None

    def get_heading(self):
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.course
        else:
            return None

    def get_altitude(self):
        # Check that a sentence has been received at least
        if self.sentence_type:
            return self.interpretter.altitude
        else:
            return None

    def get_fix(self):
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
