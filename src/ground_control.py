#!/usr/bin/python3           # This is server.py file
import socket
from network import WLAN
import time
import task_manager
import sys


class GroundControlSocketTask(task_manager.Task):
    def __init__(self, shared_setpoint_string):

        assert type(shared_setpoint_string) == task_manager.ProtectedData
        self.shared_setpoint_string = shared_setpoint_string

        # create a socket object
        self.serversocket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        wl = WLAN()
        host = wl.ifconfig()[0]

        port = 9999

        # bind to the port
        print('testing')
        self.serversocket.bind((host, port))

        # queue up to 5 requests
        try:
            self.serversocket.listen(5)
        except:
            print("socket error")
            self.serversocket.close()
            sys.exit()

        # establish a connection
        self.clientsocket,self.addr = self.serversocket.accept()

        print("Got a connection from %s" % str(self.addr))

        msg='Thank you for connecting'+ "\r\n"
        self.clientsocket.send(msg.encode('ascii'))
        self.last_time = time.ticks_ms()
    def run(self):
        try:
                self.shared_setpoint_string.putData(self.clientsocket.recv(1024))
                # print(recieved)
                # now = time.ticks_ms()
                # print("time difference: " + str(now-last_time))
                # last_time = now
        except:
            self.serversocket.close()