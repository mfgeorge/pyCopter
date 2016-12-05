#! /bin/python
"""
ground-socket-test.py
*********************
Michael George 12/4/16

A test script used to generate test command strings to the drone


"""
import socket
import time

def main():

    # address parameters of socket
    host = "192.168.43.15"
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

    print("Sending Messages to emmulate ground control connection...")
    print("Press crtl-c to end")

    # thrust profile to send to drone
    profile = MotionProfile(ramp_profile)
    try:
        while True:
            message = profile.get_profile()
            drone_socket.send(message)
            time.sleep(timing)
    except KeyboardInterrupt:
        message = b'p_0;r_0;t_0;y_0;'
        drone_socket.send(message)
        print("ending ground control communication")
        drone_socket.close()

class MotionProfile:
    def __init__(self, profile_callback):
        self.current_time = time.time()
        self.start_time = self.current_time
        self.profile_callback = profile_callback

    def get_profile(self):
        self.current_time = time.time()
        thrust = self.profile_callback(self.current_time - self.start_time)
        if thrust > 1:
            self.start_time = self.current_time
            thrust = self.profile_callback(self.current_time - self.start_time)

        print("Thrust: ", '%0.3f' % (thrust*180), end='\r')
        profile_out = "p_0;r_0;y_0;t_" + '%0.3f' % thrust + ";"
        return profile_out.encode("ascii")


def ramp_profile(the_time):
    return 20/180*the_time


if __name__ == "__main__":
    main()