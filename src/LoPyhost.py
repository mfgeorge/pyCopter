#!/usr/bin/python3           # This is server.py file
import socket
from network import WLAN
import time


def socket_test():
    # create a socket object
    serversocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    wl = WLAN()
    host = wl.ifconfig()[0]

    port = 9999

    # bind to the port
    print('testing')
    serversocket.bind((host, port))

    # queue up to 5 requests
    serversocket.listen(5)

        # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    msg='Thank you for connecting'+ "\r\n"
    clientsocket.send(msg.encode('ascii'))
    while True:
        recieved = clientsocket.recv(1024)
        print(recieved)
        time.sleep(.2)