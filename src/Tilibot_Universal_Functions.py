## Tilibot Universal Functions

# Intended to prevent circular referencing

from dynamixel_sdk import *
from Tilibot_Constants import *
import os

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

def FormatSendData(rawData):
    return [DXL_LOBYTE(DXL_LOWORD(rawData)), DXL_HIBYTE(DXL_LOWORD(rawData)), DXL_LOBYTE(DXL_HIWORD(rawData)), DXL_HIBYTE(DXL_HIWORD(rawData))]

def Packet_Port_Setup(config_array):
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    ports_used = [0, 0, 0, 0] # Create ports used list and port handlers to edit

    portHandler_1 = PortHandler(DEVICENAME_1)
    portHandler_2 = PortHandler(DEVICENAME_2)
    portHandler_3 = PortHandler(DEVICENAME_3)
    portHandler_4 = PortHandler(DEVICENAME_4)

    try: 
        portHandler_1.openPort()
        print("Succeeded to open the port (#1) - CHECK")
        ports_used[0] = 1
        portHandler_1.closePort()
        print("Port (#1) now closed.")
    except:
        print("Port (#1) is not able to be opened.")
    try: 
        portHandler_2.openPort()
        print("Succeeded to open the port (#2) - CHECK")
        ports_used[1] = 1
        portHandler_2.closePort()
        print("Port (#2) now closed.")
    except:
        print("Port (#2) is not able to be opened.")
    try: 
        portHandler_3.openPort()
        print("Succeeded to open the port (#3) - CHECK")
        ports_used[2] = 1
        portHandler_3.closePort()
        print("Port (#3) now closed.")
    except:
        print("Port (#3) is not able to be opened.")
    portHandler_4 = 0
    if ports_used[0] == 1:
        if portHandler_1.openPort():
            print("Succeeded to open the port (#1) - ACTUAL")
            if portHandler_1.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 1")
            else:
                print("Failed to change the baudrate - 1")
                print("Press any key to terminate...")
                getch() 
        else:
            print("Failed to open the port - 1")
            print("Press any key to terminate...")
            getch() 
    if ports_used[1] == 1:
        if portHandler_2.openPort():
            print("Succeeded to open the port (#2) - ACTUAL")
            if portHandler_2.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 2")
            else:
                print("Failed to change the baudrate - 2")
                print("Press any key to terminate...")
                getch() 
        else:
            print("Failed to open the port - 2")
            print("Press any key to terminate...")
            getch() 
    if ports_used[2] == 1:
        if portHandler_3.openPort():
            print("Succeeded to open the port (#3) - ACTUAL")
            if portHandler_3.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 3")
            else:
                print("Failed to change the baudrate - 3")
                print("Press any key to terminate...")
                getch()    
        else:
            print("Failed to open the port - 3")
            print("Press any key to terminate...")
            getch()
    if 1 not in ports_used:
        print("No ports appear to be accessed. Please check the connection and try again...")
        exit()

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    return portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler

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
    print("\nFrom Port (#1):")
    for dxl_id in dxl_data_list_1:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_1.get(dxl_id)[0], dxl_data_list_1.get(dxl_id)[1]))
    print("\nFrom Port (#2):")
    for dxl_id in dxl_data_list_2:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_2.get(dxl_id)[0], dxl_data_list_2.get(dxl_id)[1]))
    print("\nFrom Port (#3):")
    for dxl_id in dxl_data_list_3:
        print("[ID:%03d] Detected" % (dxl_id))
        print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_3.get(dxl_id)[0], dxl_data_list_3.get(dxl_id)[1]))
    
    dxl_data_list = {**dxl_data_list_1, **dxl_data_list_2, **dxl_data_list_3}
    return dxl_data_list

def Port_Servo_Assign(dxl_data_list,port_hand_list):
    port_servo_dict = {}   
    for servo in dxl_data_list[0]:
        port_servo_dict[servo] = port_hand_list[0]
    for servo in dxl_data_list[1]:
        port_servo_dict[servo] = port_hand_list[1]
    for servo in dxl_data_list[2]:
        port_servo_dict[servo] = port_hand_list[2]

def CorrectPortHandler(servoID):
    out_port_handler = None
    if (servoID == 1) or (servoID == 2) or (servoID == 3) or (servoID == 4): # Limb #1
        out_port_handler = 0
    elif (servoID == 5) or (servoID == 6) or (servoID == 7) or (servoID == 8): # Limb #2
        out_port_handler = 0
    elif (servoID == 9) or (servoID == 10) or (servoID == 11) or (servoID == 12): # Limb #3
        out_port_handler = 1
    elif (servoID == 13) or (servoID == 14) or (servoID == 15) or (servoID == 16): # Limb #4
        out_port_handler = 1
    elif (servoID == 17) or (servoID == 18): # Limb #5
        out_port_handler = 2
    elif (servoID == 19) or (servoID == 20) or (servoID == 21) or (servoID == 22): # Limb #6
        out_port_handler = 2
    elif (servoID == 23) or (servoID == 24): # Limb #7
        out_port_handler = 2
    else:
        print("The correct port handler can not be identified because the servo ID isn't recognized. Please fix and try again.")
    return out_port_handler
