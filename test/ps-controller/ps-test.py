#!/bin/python
import pygame
import time
import sys

def main():
    # Initialize pygame
    pygame.init()

    # Initialize the joystick module
    pygame.joystick.init()
    # Make a list of all of the joystick objects available
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    # Print them out
    print("Available Joysticks: ", joysticks)

    # Grab the controller at index 0
    ps_controller = joysticks[0]

    # Print out the name of the controller being used
    print("Using joystick: ", ps_controller.get_name())

    # Initialize the controller so information about the
    # controller can be obtained
    ps_controller.init()

    print("Controller initialized: ", ps_controller.get_init())
    # Print out the number of axis available
    num_axis_available = ps_controller.get_numaxes()
    print("Number of axis: ", num_axis_available)

    # Print out the number of buttons available
    num_buttons_available = ps_controller.get_numbuttons()
    print("Number of buttons: ", num_buttons_available)

    # Print the number of hats available
    num_hats_available = ps_controller.get_numhats()
    print("Number of hats: ", num_hats_available)

    # Print the number of balls available
    num_balls_available = ps_controller.get_numballs()
    print("Number of balls: ", num_balls_available)

    # Print out information from the axis
    def print_joystick_input(input_callback, num_inputs):
        count = 0
        while True:
            pygame.event.pump()
            try:
                print(count, end=' ')
                for index in range(num_inputs):
                    print("input", index, "=", input_callback(index), end=" | ")
                time.sleep(.01)
                count += 1
                sys.stdout.write("\r")
                sys.stdout.write("\033[K")
            except KeyboardInterrupt:
                break

    print_joystick_input(ps_controller.get_axis, num_axis_available)

    # Deinitialize the playstation controller
    ps_controller.quit()
    # Deinitialize the joystick module
    pygame.joystick.quit()
    # Deinitialize pygame
    pygame.quit()

if __name__ == "__main__":
    main()
