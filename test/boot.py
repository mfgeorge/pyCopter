import machine
import network
import time
import os
from network import WLAN
from network import Server


known_nets = {
    # SSID : PSK (passphrase)
    'Google Fiber': 'ifuckinglovetacos'
} # change this dict to match your WiFi settings

# Do not change these two lines
uart = machine.UART(0, 115200)
os.dupterm(uart)

custom_ssid = 'pyCopter Dev 1'
custom_auth = (WLAN.WPA2, 'calpoly123')

# test needed to avoid losing connection after a soft reboot
if machine.reset_cause() != machine.SOFT_RESET: 
    wl = WLAN()
    server = Server()
    server.deinit()
    server.init(login=('pycopter', 'calpoly123'), timeout=600)
    # save the default ssid and auth
    original_ssid = wl.ssid()
    original_auth = wl.auth()

    wl.mode(WLAN.STA)

    for ssid, bssid, sec, channel, rssi in wl.scan():
        # Note: could choose priority by rssi if desired
        try:
            wl.connect(ssid, (sec, known_nets[ssid]), timeout=10000)
            break
        except KeyError:
            pass # unknown SSID
    else:
        # if there are no known SSIDs available, then make one 
        print("No Known SSIDs available. Hosting own WLAN connection")
        wl.init(mode=WLAN.AP, ssid=custom_ssid, auth=custom_auth, channel=6, antenna=WLAN.INT_ANT)
        # Reiterate the settings, for some reason does not always work with init
        # wl.ssid(custom_ssid)
        # wl.auth(custom_auth)
        print("SSID: ", wl.ssid())
        print("PASS: ", wl.auth())