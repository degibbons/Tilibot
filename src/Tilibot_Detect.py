## Tilibot Detect

# For detecting and displaying what servos are currently plugged into the current raspberry pi

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *
from Tilibot_Universal_Functions import *

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios 
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch



print("Welcome to Tilibot Detect.")
print("Press any key to begin detect process.")
getch()

config_array = read_config_file("Tilibot_Configuration_File.yml")
[portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler] = Packet_Port_Setup(config_array)
port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]

print("Ports tested. Please press enter to begin pinging servos.")
getch()

dxl_data_list = PingServos(port_hand_list,packetHandler)

print("\nFinished Detecting.")