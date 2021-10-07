## Tilibot Detect

# For detecting and displaying what servos are currently plugged into the current raspberry pi

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *

def PingServos(port_hand_list,packet_handler):
    import os

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
    #Initialize PortHandler instance
    #Set the port path
    #Get methods and members of PortHandlerLinux or PortHandlerWindows
    # portHandler1 = PortHandler(DEVICENAME_1)
    # portHandler2 = PortHandler(DEVICENAME_2)
    # portHandler3 = PortHandler(DEVICENAME_3)

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    # packetHandler = PacketHandler(PROTOCOL_VERSION)

    # # Open port
    # if portHandler1.openPort():
    #     print("Succeeded to open the port")
    # else:
    #     print("Failed to open the port")
    #     print("Press any key to terminate...")
    #     getch()
    #     return


    # # Set port baudrate
    # if portHandler1.setBaudRate(BAUDRATE):
    #     print("Succeeded to change the baudrate")
    # else:
    #     print("Failed to change the baudrate")
    #     print("Press any key to terminate...")
    #     getch()
    #     return

    # # Open port
    # if portHandler2.openPort():
    #     print("Succeeded to open the port")
    # else:
    #     print("Failed to open the port")
    #     print("Press any key to terminate...")
    #     getch()
    #     return


    # # Set port baudrate
    # if portHandler2.setBaudRate(BAUDRATE):
    #     print("Succeeded to change the baudrate")
    # else:
    #     print("Failed to change the baudrate")
    #     print("Press any key to terminate...")
    #     getch()
    #     return

    # # Open port
    # if portHandler3.openPort():
    #     print("Succeeded to open the port")
    # else:
    #     print("Failed to open the port")
    #     print("Press any key to terminate...")
    #     getch()
    #     return


    # # Set port baudrate
    # if portHandler3.setBaudRate(BAUDRATE):
    #     print("Succeeded to change the baudrate")
    # else:
    #     print("Failed to change the baudrate")
    #     print("Press any key to terminate...")
    #     getch()
    #     return

    # Try to broadcast ping the Dynamixel
    dxl_data_list_1, dxl_comm_result = packetHandler.broadcastPing(portHandler1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Broadcast Issue for Port #1")
    time.sleep(1)
    dxl_data_list_2, dxl_comm_result = packetHandler.broadcastPing(portHandler2)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Broadcast Issue for Port #2")
    time.sleep(1)
    dxl_data_list_3, dxl_comm_result = packetHandler.broadcastPing(portHandler3)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        print("Broadcast Issue for Port #3")
    time.sleep(1)
    print("Detected Dynamixel :")
    for dxl_id in dxl_data_list_1:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_1.get(dxl_id)[0], dxl_data_list_1.get(dxl_id)[1]))
    for dxl_id in dxl_data_list_2:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_2.get(dxl_id)[0], dxl_data_list_2.get(dxl_id)[1]))
    for dxl_id in dxl_data_list_3:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_3.get(dxl_id)[0], dxl_data_list_3.get(dxl_id)[1]))
    # Close port
    # portHandler1.closePort() 
    # portHandler2.closePort() 
    # portHandler3.closePort() 
    dxl_data_list = {**dxl_data_list_1, **dxl_data_list_2, **dxl_data_list_3}
    return dxl_data_list