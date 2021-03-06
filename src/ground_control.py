#!/usr/bin/python3
"""
..  module: ground_control
    :platform: Pycom LoPy
    :synopsis: Contains the task for ground control communication via Wifi sockets

..  topic:: Authors

    | Michael George
    | Oscar Ruiz

Module for hosting connections to ground control on the LoPy
The scheme for incoming commands to be parsed is as follows::

    incoming = b'p_val1;r_val2;y_val3;t_val4'

where incoming is then parsed and the letters *p, r, y, and t* indicate
to stick the *val* that follows into the pitch, roll, yaw, or thrust
set-point respectively. Commands can also be added dynamically during
run-time or start up using the
:func:`~ground_control.GroundControlSocketTask.add_command` method.


"""
import socket
import time
import task_manager
import sys

# Handle the case where we aren't in micropython for documentation
# generation
try:
    from network import WLAN
except ImportError:
    import sys
    # Add some dummy libraries
    sys.path.insert(0, '../dummy_libraries')
    from dummy_libraries.network import WLAN


class GroundControlSocketTask(task_manager.Task):
    """
    Class for hosting a server socket and communicating to
    a ground control client socket

    :param shared_setpoint_dict: Dictionary to put received set-points in
    :param setpoint_map: Map of command letters to keys of setpoint_dict

    """
    def __init__(self, shared_setpoint_dict, setpoint_map):
        """
        Constructor for the Ground Control Task

        :param shared_setpoint_dict: Dictionary to put received set-points in
        :param setpoint_map: Map of command letters to keys of setpoint_dict
        """

        # make sure that the setpoint dict is a ProtectedData object
        assert type(shared_setpoint_dict) == task_manager.ProtectedData
        # store the setpoint dict
        self.setpoint_dict = shared_setpoint_dict

        # store map of command letters to keys in setpoint dict
        self.setpoint_map = setpoint_map

        # Create a command dictionary
        self.command_dict = {}

        # Start the socket server and wait for connections
        self.open_socket()

        # store a last time for time profiling the receipt of commands
        self.last_time = time.ticks_ms()

    def run(self):
        """
        Function called by the task manager repeatedly for this task
        to run.
        """
        try:

                self.command_string_in = self.clientsocket.recv(200)               # self.now = time.ticks_ms()
                # print("time difference: " + str(self.now-self.last_time))
                # self.last_time = now
                self.parse_command_string()

                self.store_basic_setpoints()

                self.call_other_commands()
        except:
            self.serversocket.close()


    def open_socket(self):
        """
        open a socket connection with ground control
        """
        # create a socket object
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        # get local machine ip address by asking the WLAN library
        wl = WLAN()
        host = wl.ifconfig()[0]

        # port for the socket connection to occur over
        port = 9999

        # bind to the port
        print('Waiting for ground control socket connection...')
        self.serversocket.bind((host, port))

        # queue 1 request
        try:
            self.serversocket.listen(1)
        except:
            print("Ground control socket error")
            self.serversocket.close()
            sys.exit()

        # establish an incoming connection
        self.clientsocket, self.addr = self.serversocket.accept()

        # Notify that a ground control connection was received
        print("Ground control connection from %s" % str(self.addr))

        # Print a handshake message to the client
        msg = 'pyCopter Ground Control handshake. ' + "\r\n"
        self.clientsocket.send(msg.encode('ascii'))

    def close_socket(self):
        """
        Close the socket that was opened with ground control as well
        as the server socket
        """
        self.clientsocket.close()
        self.serversocket.close()

    def parse_command_string(self):
        """
        method for parsing the command string received from ground control
        the in_command_dict will be filled by this method, where the keys are
        the command letter, and the value is the argument for the command letter
        """
        # convert the command string from a byte string to a normal
        # one so that string operations can be performed on it
        command_string = str(self.command_string_in, 'utf-8')

        # print the command string for debugging
        # print(command_string)

        # separate all the commands by the ; deliminator
        command_list = command_string.split(';')

        # Pop off the empty element on the end
        command_list.remove('')

        # clear the in_command_dict
        self.in_command_dict = {}

        # iterate through the separated commands
        for command in command_list:
            # separate the command letter from argument
            command = command.split('_')
            # store the command and argument in the in_command_dict
            self.in_command_dict[command[0]] = command[1]

        # print the in_command_dict for debugging
        #print("in_command_dict: ", self.in_command_dict)

    def add_command(self, command_letter, command_callback):
        """
        Method for adding a command to the command_dict so that
        a received command letter has a callback it is mapped to.

        :param command_letter: the command letter that will be received from ground control
        :param command_callback: the callback associated with the letter

        ..  warning:: *command_callback* needs to take exactly one parameter
            to work with the parsing scheme.
        """

        # Check that the command letter is not already in the command_dict
        if command_letter not in self.command_dict.keys():
            # store it if it is not yet
            self.command_dict[command_letter] = command_callback
        else:
            # notify the user if it is
            print("Conflicting command letter '", command_letter,
                  "' in attempt in to add command: ", command_callback)

    def store_basic_setpoints(self):
        """
        method to use for quickly storing the basic set-points needed
        to fly the drone
        """

        # iterate through all of the command letters received
        for letter in self.in_command_dict.keys():
            # Check if the command letter is used in setpoint dict
            if letter in self.setpoint_map.keys():
                # Store the value to the mapped setpoint key index
                # and remove the letter from the command_dict
                self.setpoint_dict[self.setpoint_map[letter]] = float(self.in_command_dict.pop(letter))*180

    def call_other_commands(self):
        """
        method to use for calling the other command callbacks that
        were added
        """

        # check that there are items still left in the in_command_dict
        if len(self.in_command_dict) > 0:
            # Iterate through the letters still left
            for letter in self.in_command_dict:
                # check if the letter is mapped to a command to call
                if letter in self.command_dict.keys():
                    # call the command with the argument
                    self.command_dict[letter](self.in_command_dict.pop(letter))