## Tilibot Torque Reset

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *
from time import sleep

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios # pylint: disable=import-error
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

print("Welcome to Tilibot Torque Reset!")
print("Press any key to continue.")
getch()

config_array = read_config_file("Tilibot_Configuration_File.yml")
[portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler] = Packet_Port_Setup(config_array)
port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]
dxl_data_list = PingServos(port_hand_list,packetHandler)
port_servo_dict, port_used_dict = Port_Servo_Assign(dxl_data_list,port_hand_list)

print("\nServos have been identified and digitally recreated. Press enter to turn the torque off on all of them.")
getch()
preprocessed_positions = ReadServoAngles(config_array[1])

PositionsMatrix = PostProcessPositions(preprocessed_positions)

SpeedMatrix = DetermineSpeeds(config_array[3],PositionsMatrix,config_array[2],config_array)


ServosDictionary = Create_DigitalServos(config_array,port_used_dict,PositionsMatrix,SpeedMatrix,config_array[32])
for each_servo,each_servo_obj in ServosDictionary.items():
    each_servo_obj.ToggleTorque(0,port_used_dict[each_servo])

print("\nFinished Toggling Torque off.")