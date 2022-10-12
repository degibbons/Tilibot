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

def Packet_Port_Setup(baud_rate_in):
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    ports_used = [0, 0, 0, 0, 0, 0] # Create ports used list and port handlers to edit

    portHandler_1 = PortHandler(DEVICENAME_1)
    portHandler_2 = PortHandler(DEVICENAME_2)
    portHandler_3 = PortHandler(DEVICENAME_3)
    portHandler_4 = PortHandler(DEVICENAME_4)
    portHandler_5 = PortHandler(DEVICENAME_5)
    portHandler_6 = PortHandler(DEVICENAME_6)

    try: 
        portHandler_1.openPort()
        print("Succeeded to open the port (#1) - CHECK")
        ports_used[0] = 1
        portHandler_1.closePort()
        print("Port (#1) now closed.")
    except:
        print("Port (#1) is not able to be opened.")
        portHandler_1 = 0
    try: 
        portHandler_2.openPort()
        print("Succeeded to open the port (#2) - CHECK")
        ports_used[1] = 1
        portHandler_2.closePort()
        print("Port (#2) now closed.")
    except:
        print("Port (#2) is not able to be opened.")
        portHandler_2 = 0
    try: 
        portHandler_3.openPort()
        print("Succeeded to open the port (#3) - CHECK")
        ports_used[2] = 1
        portHandler_3.closePort()
        print("Port (#3) now closed.")
    except:
        print("Port (#3) is not able to be opened.")
        portHandler_3 = 0
    try: 
        portHandler_4.openPort()
        print("Succeeded to open the port (#4) - CHECK")
        ports_used[3] = 1
        portHandler_4.closePort()
        print("Port (#4) now closed.")
    except:
        print("Port (#4) is not able to be opened.")
        portHandler_4 = 0
    try: 
        portHandler_5.openPort()
        print("Succeeded to open the port (#5) - CHECK")
        ports_used[4] = 1
        portHandler_5.closePort()
        print("Port (#5) now closed.")
    except:
        print("Port (#5) is not able to be opened.")
        portHandler_5 = 0
    try: 
        portHandler_6.openPort()
        print("Succeeded to open the port (#6) - CHECK")
        ports_used[5] = 1
        portHandler_6.closePort()
        print("Port (#6) now closed.")
    except:
        print("Port (#6) is not able to be opened.")
        portHandler_6 = 0
    

    if ports_used[0] == 1:
        if portHandler_1.openPort():
            print("Succeeded to open the port (#1) - ACTUAL")
            if portHandler_1.setBaudRate(baud_rate_in):
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
            if portHandler_2.setBaudRate(baud_rate_in):
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
            if portHandler_3.setBaudRate(baud_rate_in):
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

    if ports_used[3] == 1:
        if portHandler_4.openPort():
            print("Succeeded to open the port (#4) - ACTUAL")
            if portHandler_4.setBaudRate(baud_rate_in):
                print("Succeeded to change the baudrate for port 4")
            else:
                print("Failed to change the baudrate - 4")
                print("Press any key to terminate...")
                getch()     
        else:
            print("Failed to open the port - 4")
            print("Press any key to terminate...")
            getch() 
        
    if ports_used[4] == 1:
        if portHandler_5.openPort():
            print("Succeeded to open the port (#5) - ACTUAL")
            if portHandler_5.setBaudRate(baud_rate_in):
                print("Succeeded to change the baudrate for port 5")
            else:
                print("Failed to change the baudrate - 5")
                print("Press any key to terminate...")
                getch()  
        else:
            print("Failed to open the port - 5")
            print("Press any key to terminate...")
            getch() 

    if ports_used[5] == 1:
        if portHandler_6.openPort():
            print("Succeeded to open the port (#6) - ACTUAL")
            if portHandler_6.setBaudRate(baud_rate_in):
                print("Succeeded to change the baudrate for port 6")
            else:
                print("Failed to change the baudrate - 6")
                print("Press any key to terminate...")
                getch()     
        else:
            print("Failed to open the port - 6")
            print("Press any key to terminate...")
            getch()
    if 1 not in ports_used:
        print("No ports appear to be accessed. Please check the connection and try again...")
        exit()


    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    return portHandler_1, portHandler_2, portHandler_3, portHandler_4, portHandler_5, portHandler_6, packetHandler

def PingServos(port_hand_list,packetHandler):
    dxl_port_list_1 = []
    dxl_port_list_2 = []
    dxl_port_list_3 = []
    dxl_port_list_4 = []
    dxl_port_list_5 = []
    dxl_port_list_6 = []
    if port_hand_list[0] != 0:
        port_hand_list[0].openPort()
        # Try to broadcast ping the Dynamixel
        print("Pinging Port #1")
        dxl_data_list_1, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[0])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #1")
        time.sleep(1)
        # Close port
        port_hand_list[0].closePort() 
    if port_hand_list[1] != 0:
        port_hand_list[1].openPort()
        print("Pinging Port #2")
        dxl_data_list_2, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[1])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #2")
        time.sleep(1)
        # Close port
        port_hand_list[1].closePort()
    if port_hand_list[2] != 0:
        port_hand_list[2].openPort()
        print("Pinging Port #3")
        dxl_data_list_3, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[2])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #3")
        time.sleep(1)
        # Close port
        port_hand_list[2].closePort()
    if port_hand_list[3] != 0:
        port_hand_list[3].openPort()
        # Try to broadcast ping the Dynamixel
        print("Pinging Port #4")
        dxl_data_list_4, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[3])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #4")
        time.sleep(1)
        # Close port
        port_hand_list[3].closePort() 
    if port_hand_list[4] != 0:
        port_hand_list[4].openPort()
        print("Pinging Port #5")
        dxl_data_list_5, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[4])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #5")
        time.sleep(1)
        # Close port
        port_hand_list[4].closePort()
    if port_hand_list[5] != 0:
        port_hand_list[5].openPort()
        print("Pinging Port #6")
        dxl_data_list_6, dxl_comm_result = packetHandler.broadcastPing(port_hand_list[5])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Broadcast Issue for Port #6")
        time.sleep(1)
        # Close port
        port_hand_list[5].closePort()

    if port_hand_list[0] != 0:
        print("\nFrom Port (#1):")
        for dxl_id in dxl_data_list_1:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_1.get(dxl_id)[0], dxl_data_list_1.get(dxl_id)[1]))
            dxl_port_list_1.append(dxl_id)
    if port_hand_list[1] != 0:
        print("\nFrom Port (#2):")
        for dxl_id in dxl_data_list_2:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_2.get(dxl_id)[0], dxl_data_list_2.get(dxl_id)[1]))
            dxl_port_list_2.append(dxl_id)
    if port_hand_list[2] != 0:
        print("\nFrom Port (#3):")
        for dxl_id in dxl_data_list_3:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_3.get(dxl_id)[0], dxl_data_list_3.get(dxl_id)[1]))
            dxl_port_list_3.append(dxl_id)
    if port_hand_list[3] != 0:
        print("\nFrom Port (#4):")
        for dxl_id in dxl_data_list_4:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_4.get(dxl_id)[0], dxl_data_list_4.get(dxl_id)[1]))
            dxl_port_list_4.append(dxl_id)
    if port_hand_list[4] != 0:
        print("\nFrom Port (#5):")
        for dxl_id in dxl_data_list_5:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_5.get(dxl_id)[0], dxl_data_list_5.get(dxl_id)[1]))
            dxl_port_list_5.append(dxl_id)
    if port_hand_list[5] != 0:
        print("\nFrom Port (#6):")
        for dxl_id in dxl_data_list_6:
            print("[ID:%03d] Detected" % (dxl_id))
            print("[ID:%03d] model version : %d | firmware version : %d" % (dxl_id, dxl_data_list_6.get(dxl_id)[0], dxl_data_list_6.get(dxl_id)[1]))
            dxl_port_list_6.append(dxl_id)

    dxl_data_list = [dxl_port_list_1, dxl_port_list_2, dxl_port_list_3,dxl_port_list_4, dxl_port_list_5, dxl_port_list_6]
    return dxl_data_list

def Port_Servo_Assign(dxl_data_list,port_hand_list):
    port_servo_dict = {}
    port_used_dict = {}
    for servo in dxl_data_list[0]:
        port_servo_dict[servo] = port_hand_list[0]
        port_used_dict[servo] = 0
    for servo in dxl_data_list[1]:
        port_servo_dict[servo] = port_hand_list[1]
        port_used_dict[servo] = 1
    for servo in dxl_data_list[2]:
        port_servo_dict[servo] = port_hand_list[2]
        port_used_dict[servo] = 2
    for servo in dxl_data_list[3]:
        port_servo_dict[servo] = port_hand_list[3]
        port_used_dict[servo] = 3
    for servo in dxl_data_list[4]:
        port_servo_dict[servo] = port_hand_list[4]
        port_used_dict[servo] = 4
    for servo in dxl_data_list[5]:
        port_servo_dict[servo] = port_hand_list[5]
        port_used_dict[servo] = 5
    return port_servo_dict, port_used_dict
