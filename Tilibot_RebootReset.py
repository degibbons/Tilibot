## Tilibot Reboot / Reset

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *

def RebootServo(servo_num,port_hand_list,packet_handler):
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

    if servo_num in FRONT_ARMS:
        # Open port
        if port_hand_list[0].openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[0].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            return
    elif servo_num in BACK_ARMS:
        # Open port
        if port_hand_list[1].openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[1].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            return
    elif servo_num in BODY_LENGTH:
        # Open port
        if port_hand_list[2].openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[2].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            return

    # Trigger
    print("Press any key to reboot")
    getch()


    if servo_num in FRONT_ARMS:
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packet_handler.reboot(port_hand_list[0], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packet_handler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)
    elif servo_num in BACK_ARMS:
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packet_handler.reboot(port_hand_list[1], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packet_handler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)
    elif servo_num in BODY_LENGTH:
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packet_handler.reboot(port_hand_list[2], servo_num)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packet_handler.getRxPacketError(dxl_error))
        print("[ID:%03d] reboot Succeeded\n" % servo_num)


    # Close port
    if servo_num in FRONT_ARMS:
        port_hand_list[0].closePort()
    elif servo_num in BACK_ARMS:
        port_hand_list[0].closePort()
    elif servo_num in BODY_LENGTH:
        port_hand_list[0].closePort()

def ResetServo(servo_num,port_hand_list,packet_handler):
    #resets settings of Dynamixel to default values. The Factoryreset function has three operation modes:
    #0xFF : reset all values (ID to 1, baudrate to 57600)
    #0x01 : reset all values except ID (baudrate to 57600)
    #0x02 : reset all values except ID and baudrate.

    import os, sys

    if os.name == 'nt':
        import msvcrt
        def getch():
            return msvcrt.getch().decode()
    else:
        import tty, termios # pylint: disable=import-error
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        def getch():
            return sys.stdin.read(1)

    os.sys.path.append('../dynamixel_functions_py')             # Path setting

    # from time import sleep
    # import dynamixel_functions as dynamixel                     # Uses DYNAMIXEL SDK library

    # Initialize PortHandler Structs
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    # port_num = dynamixel.portHandler(DEVICENAME_1)

    # Initialize PacketHandler Structs
    # dynamixel.packetHandler()

    dxl_comm_result = COMM_TX_FAIL                              # Communication result

    dxl_error = 0                                               # Dynamixel error
    dxl_baudnum_read = 0                                        # Read baudnum

    if servo_num in FRONT_ARMS:
        # Open port
        if port_hand_list[0].openPort():
            print("Succeeded to open the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[0].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            return
    elif servo_num in BACK_ARMS:
        # Open port
        if port_hand_list[1].openPort():
            print("Succeeded to open the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[1].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            return
    elif servo_num in BODY_LENGTH:
        # Open port
        if port_hand_list[2].openPort():
            print("Succeeded to open the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            return
        # Set port baudrate
        if port_hand_list[2].setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            return

    if servo_num in FRONT_ARMS:
        # Read present baudrate of the controller
        print("Now the controller baudrate is : %d" % (port_hand_list[0].getBaudRate()))
    elif servo_num in BACK_ARMS:
        # Read present baudrate of the controller
        print("Now the controller baudrate is : %d" % (port_hand_list[1].getBaudRate()))
    elif servo_num in BODY_LENGTH:
        # Read present baudrate of the controller
        print("Now the controller baudrate is : %d" % (port_hand_list[2].getBaudRate()))

    # Try factoryreset
    print("[ID:%03d] Try factoryreset : " % (servo_num))
    port_hand_list[0].factoryReset(PROTOCOL_VERSION, servo_num, OPERATION_MODE)
    if port_hand_list[0].getLastTxRxResult(PROTOCOL_VERSION) != COMM_SUCCESS:
        print("Aborted")
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
        return
    elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))


    # Wait for reset
    print("Wait for reset...")
    time.sleep(2)

    print("[ID:%03d] factoryReset Success!" % (servo_num))

    # Set controller baudrate to dxl default baudrate
    if dynamixel.setBaudRate(port_num, FACTORYRST_DEFAULTBAUDRATE):
        print("Succeed to change the controller baudrate to : %d" % (FACTORYRST_DEFAULTBAUDRATE))
    else:
        print("Failed to change the controller baudrate")
        getch()
        return

    # Read Dynamixel baudnum
    dxl_baudnum_read = dynamixel.read1ByteTxRx(port_num, PROTOCOL_VERSION, self.ID, ADDR_PRO_BAUDRATE)
    if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
    elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
    else:
      print("[ID:%03d] Dynamixel baudnum is now : %d" % (servo_num, dxl_baudnum_read))

    # Write new baudnum
    dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
    if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
    elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
    else:
      print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))

    # Set port baudrate to BAUDRATE
    if dynamixel.setBaudRate(port_num, BAUDRATE):
        print("Succeed to change the controller baudrate to : %d" % (BAUDRATE))
    else:
        print("Failed to change the controller baudrate")
        getch()
        return

    time.sleep(0.2)

    # Read Dynamixel baudnum
    dxl_baudnum_read = dynamixel.read1ByteTxRx(port_num, PROTOCOL_VERSION, servo_num, ADDR_PRO_BAUDRATE)
    if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
        dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
    elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
        dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
    else:
      print("[ID:%03d] Dynamixel baudnum is now : %d" % (servo_num, dxl_baudnum_read))


    if servo_num in FRONT_ARMS:
        # Close port
        port_hand_list[0].closePort()
    elif servo_num in BACK_ARMS:
        # Close port
        port_hand_list[0].closePort()
    elif servo_num in BODY_LENGTH:
        # Close port
        port_hand_list[0].closePort()
