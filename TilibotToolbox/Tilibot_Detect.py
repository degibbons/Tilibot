## Tilibot Detect

# For detecting and displaying what servos are currently plugged into the current raspberry pi

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *

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

def PingServos(port_hand_list,packet_handler):

    if port_hand_list[0] != 0:
        # Try to broadcast ping the Dynamixel
        dxl_data_list_1, dxl_comm_result = packet_handler.broadcastPing(port_hand_list[0])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #1")
        time.sleep(1)
        # Close port
        port_hand_list[0].closePort() 
    if port_hand_list[1] != 0:
        dxl_data_list_2, dxl_comm_result = packet_handler.broadcastPing(port_hand_list[1])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #2")
        time.sleep(1)
        # Close port
        port_hand_list[1].closePort()
    if port_hand_list[2] != 0:
        dxl_data_list_3, dxl_comm_result = packet_handler.broadcastPing(port_hand_list[2])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #3")
        time.sleep(1)
        # Close port
        port_hand_list[2].closePort()
    for dxl_id in dxl_data_list_1:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_1.get(dxl_id)[0], dxl_data_list_1.get(dxl_id)[1]))
    for dxl_id in dxl_data_list_2:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_2.get(dxl_id)[0], dxl_data_list_2.get(dxl_id)[1]))
    for dxl_id in dxl_data_list_3:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_3.get(dxl_id)[0], dxl_data_list_3.get(dxl_id)[1]))
    
    dxl_data_list = {**dxl_data_list_1, **dxl_data_list_2, **dxl_data_list_3}
    return dxl_data_list

print("Welcome to Tilibot Detect.")
print("Press any key to begin detect process.")
getch()

config_array = read_config_file("Tilibot_Configuration_File.yml")
[portHandler_1, portHandler_2, portHandler_3, portHandler_4, packet_handler] = Packet_Port_Setup(config_array)
port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]

dxl_data_list = PingServos(port_hand_list,packet_handler)

print("\nFinished Detecting.")