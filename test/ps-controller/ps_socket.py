#!/bin/python
"""
..  module:: ps-socket
    :platform: Linux
    :synopsis: Task for sending joystick data to the quadcopter

..  topic:: Authors

    | Michael George


A script for connecting to pyCopter and sending it commands
based upon a playstation controller's input.
The ZD-V+ is being used for our specific application.
"""

from __future__ import print_function
import pygame
import time
import sys
import socket

class Controller:
    """
    Class for managing the outputs of the controller and translating
    them into outputs that the LoPy can process
    Depends on pygame.

    :param controller_object: a pygame joystick object
                                ie. a pygame.joystick.Joystick(i) object
    :param axis_map: a map of the controller joystick axis to
                    the value that is will effect in the output
                    to the LoPy. ie the axis mapped to "t" will
                    send its value to the LoPy as "t_value"
    """
    def __init__(self, controller_object, axis_map={"t":1, "r":3, "p":4, "y":0}):
        """
        Constructor for the Controller class.
        """
        # Make sure that pygame is initialized
        pygame.init()
        # Store the controller
        self.controller = controller_object
        # Store the axis map
        self.axis_map = axis_map
        # Check that it is initialized
        if not self.controller.get_init():
            # if not, then initialize the controller
            self.controller.init()
        # Store the number of axes available
        self.num_axes = self.controller.get_numaxes()
        # Store the number of buttons available
        self.num_buttons = self.controller.get_numbuttons()
        # Store the number of hats available
        self.num_hats = self.controller.get_numhats()

    def print_joysticks_loop(self):
        """
        A function to print all of the joystick values of the controller
        in a loop. Useful for debugging.

        :return: none - simply print messages to stdout
        """
        self._print_controller_input_loop(self.controller.get_axis, self.num_axes)

    def print_buttons_loop(self):
        """
        A function to print all of the button values of the controller
        in a loop. Useful for debugging.

        :return: none - simply print messages to stdout
        """
        self._print_controller_input_loop(self.controller.get_button, self.num_buttons)

    def print_hats_loop(self):
        """
        A function to print all of the hat values of the controller in a
        loop. Useful for debugging.

        :return: none - simply print messages to stdout
        """
        self._print_controller_input_loop(self.controller.get_hat, self.num_hats)

    def make_output_string(self):
        """
        A function to construct the output string to send to the LoPy
        based upon the position of the joysticks that are mapped in the
        axis_map.

        :return: the output string to be sent to the quadcopter
        """
        # pump the event so that the most up to date information is present
        pygame.event.pump()
        profile_out = "p_" + '%0.3f' % (self.controller.get_axis(self.axis_map["p"])) + ";"\
                      "r_" + '%0.3f' % (self.controller.get_axis(self.axis_map["r"])*-1) + ";"\
                      "y_" + '%0.3f' % self.controller.get_axis(self.axis_map["y"]) + ";"\
                      "t_" + '%0.3f' % (self.controller.get_axis(self.axis_map["t"])*-1) + ";"
        return profile_out.encode("ascii")

    def _print_controller_input_loop(self, input_callback, num_inputs):
        """
        Print the results of an input callback for all inputs of that
        type up to num_inputs in a loop. Press crtl-c to exit. Protected
        meant to be used within in this class only.

        :param input_callback: callback that returns position of an input
        :param num_inputs: the number of inputs associated with the callback
        """
        count = 0
        print("Printing inputs, press crtl-c to exit...")
        try:
            while True:
                pygame.event.pump()
                print(count, end=' ')
                for index in range(num_inputs):
                    print("input", index, "=", input_callback(index), end=" | ")
                time.sleep(.01)
                count += 1
                sys.stdout.write("\r")
                sys.stdout.write("\033[K")
        except KeyboardInterrupt:
            pass

    def _print_controller_input(self, input_callback, num_inputs):
        """
        Print the inputs for a controller input once.

        :param input_callback: the callback that will return the input position
        :param num_inputs: the number of inputs that the callback can be called on
        """
        # pump the event so that the most up to date information is present
        pygame.event.pump()
        for index in range(num_inputs):
            print("input", index, "=", input_callback(index), end=" | ")

    def deinit(self):
        """
        Deinitialize pygame and the joysticks
        """
        self.controller.quit()
        pygame.joystick.quit()
        pygame.quit()

def main():
    """
    Main code for runnig the ground control socket communication.
    This function creates a client socket and tries to connect to
    the LoPy server socket. Once it does, it grabs the position of
    the joysticks on the ps2 controller, and send them over the socket
    to the drone.
    """
    # address parameters of socket
    host = "192.168.4.1"
    port = 9999

    # 0 message to send to the drone
    # message = b'p_0;r_0;t_0;y_0;'

    # timing for sending the messages
    timing = 0.04

    # make a socket to communicate with the drone
    drone_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the drone
    print("waiting for connection...")
    drone_socket.connect((host, port))

    # print the handshake
    print(drone_socket.recv(1024))

    print("Sending Messages to pyCopter...")
    print("Press crtl-c to end")

    # Initialize the pygame joystick module
    pygame.joystick.init()
    # Grab the first joystick controller
    joystick_controller = pygame.joystick.Joystick(0)
    # Make a controller object
    controller = Controller(joystick_controller)

    # Print out the output being sent
    try:
        while True:
            # Grab the output string from the controller
            message = controller.make_output_string()
            # Send the drone the command over socket
            drone_socket.send(message)
            # Print message to user
            print(message, end='\r')
            # pause so we don't kill the buffer on the LoPy
            time.sleep(timing)
    except KeyboardInterrupt:
        # Set all motors to zero
        message = b'p_0;r_0;t_0;y_0;'
        # send the final message
        drone_socket.send(message)
        # Notify that communication is ending
        print("ending ground control communication")
        # close socket
        drone_socket.close()

    # Deinitialize the controller
    controller.deinit()


if __name__ == '__main__':
    main()
