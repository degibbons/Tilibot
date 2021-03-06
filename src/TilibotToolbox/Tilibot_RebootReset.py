## Tilibot Reboot / Reset

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

def RebootServo(servo_num,port_hand_list,port_used_dict,packetHandler):

    # Trigger
    print("Press any key to reboot")
    getch()

    if port_used_dict[servo_num] == 0:
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
            quit()
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packetHandler.reboot(port_hand_list[0], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)
    elif port_used_dict[servo_num] == 1:
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
            quit()
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packetHandler.reboot(port_hand_list[1], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)
    elif port_used_dict[servo_num] == 2:
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
            quit()
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packetHandler.reboot(port_hand_list[2], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)

    # Close port
    if port_used_dict[servo_num] == 0:
        port_hand_list[0].closePort()
    elif port_used_dict[servo_num] == 1:
        port_hand_list[1].closePort()
    elif port_used_dict[servo_num] == 2:
        port_hand_list[2].closePort()

def ResetServo(servo_num,port_hand_list,port_used_dict,packetHandler,config_array,reset_value):
    #resets settings of Dynamixel to default values. The Factoryreset function has three operation modes:
    #0xFF : reset all values (ID to 1, baudrate to 57600)
    #0x01 : reset all values except ID (baudrate to 57600)
    #0x02 : reset all values except ID and baudrate.

    if reset_value == 1:
        OPERATION_MODE = 0xFF
    elif reset_value == 2:
        OPERATION_MODE = 0x01
    elif reset_value == 3:
        OPERATION_MODE = 0x02
    else:
        print("Reset value not recognized. Please fix and try again.")
        quit()

    if port_used_dict[servo_num] == 0:
        # Try factoryreset
        print("[ID:%03d] Try factoryreset : " % (servo_num))
        dxl_comm_result, dxl_error = packetHandler.factoryReset(port_hand_list[0], servo_num, OPERATION_MODE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Aborted")
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            quit()
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
    elif port_used_dict[servo_num] == 1:
       # Try factoryreset
        print("[ID:%03d] Try factoryreset : " % (servo_num))
        dxl_comm_result, dxl_error = packetHandler.factoryReset(port_hand_list[1], servo_num, OPERATION_MODE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Aborted")
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            quit()
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
    elif port_used_dict[servo_num] == 2:
       # Try factoryreset
        print("[ID:%03d] Try factoryreset : " % (servo_num))
        dxl_comm_result, dxl_error = packetHandler.factoryReset(port_hand_list[2], servo_num, OPERATION_MODE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Aborted")
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            quit()
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
    


    # Wait for reset
    print("Wait for reset...")
    sleep(2.0)
    print("[ID:%03d] factoryReset Success!" % (servo_num))

    if port_used_dict[servo_num] == 0:
        # Set controller baudrate to Dynamixel default baudrate
        if port_hand_list[0].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
            print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))

        # Write new baudnum
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))

        # Set port baudrate to BAUDRATE
        if port_hand_list[0].setBaudRate(config_array[0]):
            print("Succeeded to change the controller baudrate to : %d" % config_array[0])
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        sleep(0.2)

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
    elif port_used_dict[servo_num] == 1:
        # Set controller baudrate to Dynamixel default baudrate
        if port_hand_list[1].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
            print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))

        # Write new baudnum
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))

        # Set port baudrate to BAUDRATE
        if port_hand_list[1].setBaudRate(config_array[0]):
            print("Succeeded to change the controller baudrate to : %d" % config_array[0])
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        sleep(0.2)

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
    elif port_used_dict[servo_num] == 2:
        # Set controller baudrate to Dynamixel default baudrate
        if port_hand_list[0].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
            print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))

        # Write new baudnum
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))

        # Set port baudrate to BAUDRATE
        if port_hand_list[2].setBaudRate(config_array[0]):
            print("Succeeded to change the controller baudrate to : %d" % config_array[0])
        else:
            print("Failed to change the controller baudrate")
            print("Press any key to terminate...")
            quit()

        sleep(0.2)

        # Read Dynamixel baudnum
        dxl_baudnum_read, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))

    if port_used_dict[servo_num] == 0:
        # Close port
        port_hand_list[0].closePort()
    elif port_used_dict[servo_num] == 1:
        # Close port
        port_hand_list[1].closePort()
    elif port_used_dict[servo_num] == 2:
        # Close port
        port_hand_list[2].closePort()

print("Welcome to Tilibot Reboot/Reset!")
print("Press any key to continue.")
getch()
config_array = read_config_file("Tilibot_Configuration_File.yml")
[portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler] = Packet_Port_Setup(config_array)
port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]
dxl_data_list = PingServos(port_hand_list,packetHandler)
port_servo_dict, port_used_dict = Port_Servo_Assign(dxl_data_list,port_hand_list)
print("Take note: Reboot and Reset are fundamentally different processes.")
print("Reboot - Turn the servo off and then on.")
print("Reset - Factory Resets all servo trait values to default values.")
print("Reset modes are as follows:")
print("1 : reset all values (ID to 1, baudrate to 57600")
print("2 : reset all values except ID (baudrate to 57600)")
print("3 : reset all values except ID and baudrate.")

while 1:
    selection_1 = int(input("Please select what option you want Reboot(1), Reset(2), Quit(0): "))
    if selection_1 == 1:
        servo_num = int(input("Please indicate the servo number (ID) you wish to reboot: "))
        RebootServo(servo_num,port_hand_list,port_used_dict,packetHandler)
    elif selection_1 == 2:
        servo_num = int(input("Please indicate the servo number (ID) you wish to reset: "))
        reset_mode = int(input("Please indicate the reset mode you wish to use as indicated above: "))
        ResetServo(servo_num,port_hand_list,port_used_dict,packetHandler,config_array,reset_mode)
    elif selection_1 == 0:
        print("Quitting Reboot/Reset program.")
        break
    else:
        print("That is not a recognized option. Please fix and try again.")
        quit()