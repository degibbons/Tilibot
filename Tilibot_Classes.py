## Tilibot Classes

import os
from Tilibot_Constants import *
from Tilibot_Functions import *
# import yaml
from dynamixel_sdk import *
import numpy as np
import pandas as pd
import copy as cp
import time
# import RPi.GPIO as GPIO
import math
import sys
# import dynamixel_functions as dynamixel  
import csv

class Servo:
    def __init__(self,IDnum,Positions,Speeds,MaxMinMov,digital_only=None):
        self.ID = IDnum
        if digital_only == None:
            self.digital_only == False
        self.Positions = Positions
        self.Speeds = Speeds
        self.MaxMin = MaxMinMov
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

    def InitialSetup(self,portHandler): 
        if self.digital_only == False:
            #Set drive mode to velocity based
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_DRIVE_MODE, DRIVE_MODE_VEL_BASED)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Drive mode set to: %03d" %(self.ID, DRIVE_MODE_VEL_BASED))

            # time.sleep(PreferedDelay)

            #Set operating mode to joint/position control mode
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_OPERATING_MODE, OPERATING_JOINT_POSITION_MODE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Operating mode set to: %03d" %(self.ID, OPERATING_JOINT_POSITION_MODE))

            # time.sleep(PreferedDelay)

            #Set acceleration limit 
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_ACCELERATION_LIMIT, ACCELERATION_LIMIT_M)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Acceleration limit set to: %03d" %(self.ID, ACCELERATION_LIMIT_M))

            # time.sleep(PreferedDelay)

            #Set max position limit
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_MAX_POSITION_LIMIT, self.MaxMin[0])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Max position limit set to: %03d" %(self.ID, self.MaxMin[0]))

            # time.sleep(PreferedDelay)

            #Set min position limit
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_MIN_POSITION_LIMIT, self.MaxMin[1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Min position limit set to: %03d" %(self.ID, self.MaxMin[1]))

            # time.sleep(PreferedDelay)

            #Set moving threshold
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_MOVING_THRESHOLD, MOVING_THRESHOLD_ACCURACY_H)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Moving accuracy set to high: %03d" %(self.ID, MOVING_THRESHOLD_ACCURACY_H))

            # time.sleep(PreferedDelay)

    def ToggleTorque(self,OnOrOff,portHandler):
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_PRO_TORQUE_ENABLE, OnOrOff)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            if (OnOrOff == 1):
                print("Dynamixel#%d torque on" % self.ID)
            elif (OnOrOff == 0):
                print("Dynamixel#%d torque off" % self.ID)

    def SetServoVelocity(self,InVelocity,portHandler):
        print(InVelocity)
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_PROFILE_VELOCITY,int(InVelocity))
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Velocity limit set to: %03d" %(self.ID, InVelocity))

    def MoveServo(self,InPosition,portHandler):
         # Write goal position
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_PRO_GOAL_POSITION, InPosition)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Goal Position set to: %03d" %(self.ID, InPosition))

    def MoveHome(self,homespeed):
        self.SetServoVelocity(homespeed)
        self.MoveServo(self.Positions[0])

    def ContinuousMove(self,portHandler,stride_numbers,record_array,start_time):
        for stride_count in range(stride_numbers[0]):
            for position_count in range(stride_numbers[1]):
                self.SetServoVelocity(self.Speeds[stride_count])
                self.MoveServo(self.Positions[stride_count])
                out_data = []
                while 1: # Check if servo is moving
                    dxl_mov, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(portHandler, self.ID, ADDR_MOVING)
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                    elif dxl_error != 0:
                        print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                    if dxl_mov == 1:
                        pass
                    else:
                        break
                if record_array[0] == True:
                    servo_data_array = [self.ID]
                    if record_array[1] == True:
                        pos_out = self.Positions[position_count]
                        servo_data_array.append(pos_out)
                        # Record Position / self.Positions[stride_count]
                    if record_array[2] == True:
                        vel_out = self.Speeds[position_count]
                        servo_data_array.append(vel_out)
                        # Record Speed / self.Speeds[stride_count]
                    if record_array[3] == True:
                        record_time = time.time()
                        end_time = record_time = start_time
                        servo_data_array.append(end_time)
                        # Record Time / record_time - start_time
                    if record_array[4] == True:
                        pos_count = position_count
                        servo_data_array.append(pos_count)
                        # Record Position Index / position_count
                    if record_array[5] == True:
                        strd_count = stride_count
                        servo_data_array.append(strd_count)
                        # Record Stride Count / stride_count
                    if record_array[6] == True:
                        pass # Record Current / 42:126 - 2
                        dxl_current, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(portHandler, self.ID, AddrDict[42])
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                        elif dxl_error != 0:
                            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                        else:
                            servo_data_array.append(dxl_current)
                    if record_array[7] == True:
                        pass # Record Voltage / 47:144 - 2
                        dxl_voltage, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(portHandler, self.ID, AddrDict[47])
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                        elif dxl_error != 0:
                            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                        else:
                            servo_data_array.append(dxl_voltage)
                    if record_array[8] == True:
                        pass # Record Temperature / 48:146 - 1
                        dxl_temp, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(portHandler, self.ID, AddrDict[48])
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                        elif dxl_error != 0:
                            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                        else:
                            servo_data_array.append(dxl_temp)
                    out_data.append(servo_data_array)
                else:
                    pass
        return out_data

    def RebootServo(self,portHandler,packetHandler):
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

        # # Open port
        # if portHandler.openPort():
        #     print("Succeeded to open the port")
        # else:
        #     print("Failed to open the port")
        #     print("Press any key to terminate...")
        #     getch()
        #     return

        # # Set port baudrate
        # if portHandler.setBaudRate(BAUDRATE):
        #     print("Succeeded to change the baudrate")
        # else:
        #     print("Failed to change the baudrate")
        #     print("Press any key to terminate...")
        #     getch()
        #     return

        # # Trigger
        # print("Press any key to reboot")
        # getch()

        print("See the Dynamixel LED flickering")
        # Try reboot
        # Dynamixel LED will flicker while it reboots
        dxl_comm_result, dxl_error = packetHandler.reboot(portHandler, self.ID)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] reboot Succeeded\n" % self.ID)


        # Close port
        #portHandler.closePort()

    def ResetServo(self,portHandler):
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

                           # Uses DYNAMIXEL SDK library

        # Initialize PortHandler Structs
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        port_num = dynamixel.portHandler(DEVICENAME_1)

        # Initialize PacketHandler Structs
        dynamixel.packetHandler()

        dxl_comm_result = COMM_TX_FAIL                              # Communication result

        dxl_error = 0                                               # Dynamixel error
        dxl_baudnum_read = 0                                        # Read baudnum

        # Open port
        if dynamixel.openPort(port_num):
            print("Succeeded to open the port!")
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            return

        # Set port baudrate
        if dynamixel.setBaudRate(port_num, BAUDRATE):
            print("Succeeded to change the baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            return

        # Read present baudrate of the controller
        print("Now the controller baudrate is : %d" % (dynamixel.getBaudRate(port_num)))

        # Try factoryreset
        print("[ID:%03d] Try factoryreset : " % (self.ID))
        dynamixel.factoryReset(port_num, PROTOCOL_VERSION, self.ID, OPERATION_MODE)
        if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
            print("Aborted")
            dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
            return
        elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
            dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))


        # Wait for reset
        print("Wait for reset...")
        time.sleep(2)

        print("[ID:%03d] factoryReset Success!" % (self.ID))

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
          print("[ID:%03d] Dynamixel baudnum is now : %d" % (self.ID, dxl_baudnum_read))

        # Write new baudnum
        dynamixel.write1ByteTxRx(port_num, PROTOCOL_VERSION, self.ID, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
        if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
            dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
        elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
            dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
        else:
          print("[ID:%03d] Set Dynamixel baudnum to : %d" % (self.ID, NEW_BAUDNUM))

        # Set port baudrate to BAUDRATE
        if dynamixel.setBaudRate(port_num, BAUDRATE):
            print("Succeed to change the controller baudrate to : %d" % (BAUDRATE))
        else:
            print("Failed to change the controller baudrate")
            getch()
            return

        time.sleep(0.2)

        # Read Dynamixel baudnum
        dxl_baudnum_read = dynamixel.read1ByteTxRx(port_num, PROTOCOL_VERSION, self.ID, ADDR_PRO_BAUDRATE)
        if dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION) != COMM_SUCCESS:
            dynamixel.printTxRxResult(PROTOCOL_VERSION, dynamixel.getLastTxRxResult(port_num, PROTOCOL_VERSION))
        elif dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION) != 0:
            dynamixel.printRxPacketError(PROTOCOL_VERSION, dynamixel.getLastRxPacketError(port_num, PROTOCOL_VERSION))
        else:
          print("[ID:%03d] Dynamixel baudnum is now : %d" % (self.ID, dxl_baudnum_read))


        # Close port
        dynamixel.closePort(port_num)

    def CleanUp(self):
        pass

    def __del__(self):
        pass

class Limb:
    def __init__(self,limbnum,servo_dict):
        self.LimbNumber = limbnum
        self.ServoDict = servo_dict
    
    def InitialSetup(self,port_hand_list):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.InitialSetup(port_hand_list[CorrectPortHandler(each_servo)])
        return

    #Turn into group sync function
    def ToggleTorque(self,OnOrOff,port_hand_list):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.ToggleTorque(OnOrOff,port_hand_list[CorrectPortHandler(each_servo)])
        return

    # def SetLimbVelocity(self,InVelocity,port_hand_list):
    #     for each_servo, each_servo_obj in self.ServoDict.items():
    #         each_servo_obj.SetServoVelocity(InVelocity,port_hand_list[CorrectPortHandler(each_servo)])
    #     return

    def DetermineVelocities(self,speed_index,home_speed=50): # 50 for default home speed may be changed
        speed_list = []
        if speed_index == -1:
            for _ in self.ServoDict:
                speed_list.append(home_speed)
        else:
            for servo_obj in self.ServoDict.values():
                speed_list.append(servo_obj.Speeds[speed_index])
        return speed_list

    def SetLimbVelocity(self,speed_list,port_hand_list,packet_handler):
        if (self.LimbNumber == 1) or (self.LimbNumber == 2):
            port_handler = port_hand_list[0]
        elif (self.LimbNumber == 3) or (self.LimbNumber == 4):
            port_handler = port_hand_list[1]
        elif (self.LimbNumber == 5) or (self.LimbNumber == 6) or (self.LimbNumber == 7):
            port_handler = port_hand_list[2]

        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL = GroupSyncWrite(port_handler, packet_handler, AddrDict[36], 4)
        
        GoalVelocity = []
        for count,servo_obj in enumerate(self.ServoDict.values()):
            GoalVelocity.append(FormatSendData(int(speed_list[count])))
            dxl_addparam_result = groupSyncWriteVEL.addParam(servo_obj.ID,GoalVelocity[count])
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % servo_obj.ID)
                return
        
        # Syncwrite goal velocity
        dxl_comm_result = groupSyncWriteVEL.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

        # Clear syncwrite parameter storage
        groupSyncWriteVEL.clearParam()
        return

    def MoveLimb(self,position_index,port_hand_list,packet_handler):

        if (self.LimbNumber == 1) or (self.LimbNumber == 2):
            port_handler = port_hand_list[0]
        elif (self.LimbNumber == 3) or (self.LimbNumber == 4):
            port_handler = port_hand_list[1]
        elif (self.LimbNumber == 5) or (self.LimbNumber == 6) or (self.LimbNumber == 7):
            port_handler = port_hand_list[2]

        # Initialize GroupSyncWrite instance
        groupSyncWritePOS = GroupSyncWrite(port_handler, packet_handler, AddrDict[37], 4)

        GoalPosition = []

        for servo_obj in self.ServoDict.values(): # Dictionaries ordered in Python 3.6 and later, so viable. Sorted by order of item insertion in Python 3.7 and later
            GoalPosition.append(FormatSendData(servo_obj.Positions[position_index]))

        for count, servo_obj in self.ServoDict.values():
            FormattedPos = self.GoalPosition[count]
            dxl_addparam_result = groupSyncWritePOS.addParam(servo_obj.ID,FormattedPos)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % servo_obj.ID)
                return

        # Syncwrite goal position
        dxl_comm_result = groupSyncWritePOS.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

        # Clear syncwrite parameter storage
        groupSyncWritePOS.clearParam()
        return

    def MoveHome(self,home_speed,port_hand_list,packet_handler):
        speed_list = self.DetermineVelocities(-1,home_speed)
        self.SetLimbVelocity(speed_list,port_hand_list,packet_handler)
        self.MoveLimb(0,port_hand_list,packet_handler)
        print(f"Limb #{self.LimbNumber} Moved To Home Position\n")

class Leg(Limb):
    def __init__(self,limbnum,servo_dict):
        super().__init__(limbnum,servo_dict)

    def ContinuousMove(self,port_hand_list,packet_handler,stride_numbers, record_array, start_time):
        if (self.LimbNumber == 1) or (self.LimbNumber == 2):
            port_handler = port_hand_list[0]
        elif (self.LimbNumber == 3) or (self.LimbNumber == 4):
            port_handler = port_hand_list[1]
        elif (self.LimbNumber == 5) or (self.LimbNumber == 6) or (self.LimbNumber == 7):
            port_handler = port_hand_list[2]
        out_data = []
        # Initialize GroupSyncRead instace for Moving designation
        groupSyncRead_Moving = GroupSyncRead(port_handler,packet_handler,AddrDict[39],1)
        readers_exist = False
        for stride_count in range(stride_numbers[0]):
            for position_index in range(stride_numbers[1]):
                isStopped = [0] * len(self.ServoDict)
                if (stride_count == 0) and (position_index == 0): # Skip the first position, this is Home Position
                    continue
                if (position_index == 0):
                    speed_index = stride_numbers[1] - 1
                else:
                    speed_index = position_index - 1
                speed_list = self.DetermineVelocities(speed_index)
                self.SetLimbVelocity(speed_list,port_hand_list,packet_handler)
                self.MoveLimb(position_index,port_hand_list,packet_handler)
                for each_servo in self.ServoDict.keys():
                    groupSyncRead_Moving.addParam(each_servo)
                while 1:
                    # Syncread Moving Value
                    dxl_comm_result = groupSyncRead_Moving.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                    for count,each_servo in enumerate(self.ServoDict.keys()):
                        # Get Dynamixel present Moving value
                        dxl_mov = groupSyncRead_Moving.getData(each_servo, AddrDict[39],1)               
                        if (dxl_mov == 0) and (isStopped[count] == 0):
                            isStopped[count] = 1
                    if 0 in isStopped:
                        pass
                    else:
                        groupSyncRead_Moving.clearParam()
                        if record_array[0] == True:
                            if readers_exist == False:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current = GroupSyncRead(port_handler,packet_handler,AddrDict[42],2)
                                    port_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage = GroupSyncRead(port_handler,packet_handler,AddrDict[47],2)
                                    port_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature = GroupSyncRead(port_handler,packet_handler,AddrDict[48],1)
                                    port_Temperature = []
                                    readers_exist = True
                            if readers_exist == True:
                                for each_servo in self.ServoDict.keys():
                                    if record_array[6] == True:
                                        groupSyncRead_Current.addParam(each_servo)
                                    if record_array[7] == True:
                                        groupSyncRead_Voltage.addParam(each_servo)
                                    if record_array[8] == True:
                                        groupSyncRead_Temperature.addParam(each_servo)
                            if readers_exist == True:
                                if record_array[6] == True:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_servo in self.ServoDict.keys():
                                        # Check if groupsyncread data of Dynamixel is available
                                        dxl_getdata_result = groupSyncRead_Current.isAvailable(each_servo, AddrDict[42], 2)
                                        if dxl_getdata_result != True:
                                            print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                            quit()
                                        # Get Dynamixel present current value
                                        port_Current.append(groupSyncRead_Current.getData(each_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current.clearParam()
                                if record_array[7] == True:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_servo in self.ServoDict.keys():
                                        # Check if groupsyncread data of Dynamixel is available
                                        dxl_getdata_result = groupSyncRead_Voltage.isAvailable(each_servo, AddrDict[47], 2)
                                        if dxl_getdata_result != True:
                                            print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                            quit()
                                        # Get Dynamixel present voltage value
                                        port_Voltage.append(groupSyncRead_Voltage.getData(each_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current.clearParam()
                                if record_array[8] == True:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_servo in self.ServoDict.keys():
                                        # Check if groupsyncread data of Dynamixel is available
                                        dxl_getdata_result = groupSyncRead_Temperature.isAvailable(each_servo, AddrDict[48], 1)
                                        if dxl_getdata_result != True:
                                            print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                            quit()
                                        # Get Dynamixel present temperature value
                                        port_Temperature.append(groupSyncRead_Temperature.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature.clearParam()
                            if readers_exist == True:
                                for list_index,each_servo in enumerate(self.ServoDict.keys()):
                                    servo_data_array = [each_servo]
                                    if record_array[1] == True:
                                        pos_out = self.ServoDict[each_servo].Positions[position_index]
                                        servo_data_array.append(pos_out)
                                        # Record Position / self.Positions[stride_count]
                                    if record_array[2] == True:
                                        vel_out = self.ServoDict[each_servo].Speeds[stride_count]
                                        servo_data_array.append(vel_out)
                                        # Record Speed / self.Speeds[stride_count]
                                    if record_array[3] == True:
                                        record_time = time.time()
                                        end_time = record_time = start_time
                                        servo_data_array.append(end_time)
                                        # Record Time / record_time - start_time
                                    if record_array[4] == True:
                                        pos_count = position_index
                                        servo_data_array.append(pos_count)
                                        # Record Position Index / position_count
                                    if record_array[5] == True:
                                        strd_count = stride_count
                                        servo_data_array.append(strd_count)
                                        # Record Stride Count / stride_count
                                    if record_array[6] == True:
                                        servo_data_array.append(port_Current[list_index])
                                    if record_array[7] == True:
                                        servo_data_array.append(port_Voltage[list_index])
                                    if record_array[8] == True:   
                                        servo_data_array.append(port_Temperature[list_index])
                                    out_data.append(servo_data_array)
                        break
        return out_data        

    def __del__(self):
            pass        


class Neck(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def StayStraight(self,port_handler,packet_handler):
            
        return

    def __del__(self):
        pass  

class Spine(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def StayStraight(self,port_handler,packet_handler):

        return

    def __del__(self):
        pass  

class Tail(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def StayStraight(self,port_handler,packet_handler):

        return

    def __del__(self):
        pass  

class Body:
    def __init__(self,LimbDictionary,ServoDictionary): #limbs should be a list
        self.LimbDict = LimbDictionary
        self.ServoDict = ServoDictionary
        
    def InitialSetup(self,port_hand_list):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.InitialSetup(port_hand_list[CorrectPortHandler(each_servo)])
        return

    #Turn into group sync function
    def ToggleTorque(self,OnOrOff,port_hand_list):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.ToggleTorque(OnOrOff,port_hand_list[CorrectPortHandler(each_servo)])
        return

    def DetermineVelocities(self,speed_index,home_speed=50): # 50 for default home speed may be changed
        speed_list = []
        if speed_index == -1:
            for _ in self.ServoDict:
                speed_list.append(home_speed)
        else:
            for servo_obj in self.ServoDict.values():
                speed_list.append(servo_obj.Speeds[speed_index])
        return speed_list

    def SetLimbVelocity(self,speed_list,port_hand_list,packet_handler):

        # Initialize GroupSyncWrite instances
        groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[36], 4)
        groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[36], 4)
        groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[36], 4)

        GoalVelocity = []
        for count,servo_obj in enumerate(self.ServoDict.values()):
            GoalVelocity.append(FormatSendData(int(speed_list[count])))
            if servo_obj.ID in FRONT_ARMS:
                dxl_addparam_result = groupSyncWriteVEL_1.addParam(servo_obj.ID,GoalVelocity[count])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam failed" % servo_obj.ID)
                    return
            elif servo_obj.ID in BACK_ARMS:
                dxl_addparam_result = groupSyncWriteVEL_2.addParam(servo_obj.ID,GoalVelocity[count])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam failed" % servo_obj.ID)
                    return
            elif servo_obj.ID in BODY_LENGTH:
                dxl_addparam_result = groupSyncWriteVEL_3.addParam(servo_obj.ID,GoalVelocity[count])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam failed" % servo_obj.ID)
                    return
            else:
                print("Error, servo ID does not match existing limb. Please fix and try again.")
            
        # Syncwrite goal velocity
        dxl_comm_result = groupSyncWriteVEL_1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        dxl_comm_result = groupSyncWriteVEL_2.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        dxl_comm_result = groupSyncWriteVEL_3.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

        # Clear syncwrite parameter storage
        groupSyncWriteVEL_1.clearParam()
        groupSyncWriteVEL_2.clearParam()
        groupSyncWriteVEL_3.clearParam()
        return

    def MoveLegs(self,position_index,port_hand_list,packet_handler):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[37], 4)
        
        
        GoalPosition_1 = []
        GoalPosition_2 = []
        
        for servo_obj in self.ServoDict.values(): # Dictionaries ordered in Python 3.6 and later, so viable. Sorted by order of item insertion in Python 3.7 and later
            if servo_obj.ID in FRONT_ARMS:
                GoalPosition_1.append(FormatSendData(servo_obj.Positions[position_index]))
                dxl_addparam_result = groupSyncWritePOS_1.addParam(servo_obj.ID,GoalPosition_1[-1])
                if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam velocity failed" % servo_obj.ID)
                        return
            elif servo_obj.ID in BACK_ARMS:
                GoalPosition_2.append(FormatSendData(servo_obj.Positions[position_index]))
                dxl_addparam_result = groupSyncWritePOS_2.addParam(servo_obj.ID,GoalPosition_2[-1])
                if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam velocity failed" % servo_obj.ID)
                        return

        # Syncwrite goal position
        dxl_comm_result = groupSyncWritePOS_1.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        dxl_comm_result = groupSyncWritePOS_2.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
        
        # Clear syncwrite parameter storage
        groupSyncWritePOS_1.clearParam()
        groupSyncWritePOS_2.clearParam()
        return

    def MoveSpine(self,position_index,port_hand_list,packet_handler):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[37], 4)

        GoalPosition_3 = []
        
        for servo_obj in self.ServoDict.values(): # Dictionaries ordered in Python 3.6 and later, so viable. Sorted by order of item insertion in Python 3.7 and later
            if servo_obj.ID in BODY_LENGTH:
                if position_index == -1:
                    # Orient Spine straight
                    GoalPosition_3.append(FormatSendData(2048))
                    dxl_addparam_result = groupSyncWritePOS_3.addParam(servo_obj.ID,GoalPosition_3[-1])
                    if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % servo_obj.ID)
                            return
                else: 
                    # Orient Spine at a home position
                    GoalPosition_3.append(FormatSendData(servo_obj.Positions[position_index]))
                    dxl_addparam_result = groupSyncWritePOS_3.addParam(servo_obj.ID,GoalPosition_3[-1])
                    if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % servo_obj.ID)
                            return

        # Syncwrite goal position
        dxl_comm_result = groupSyncWritePOS_3.txPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

        groupSyncWritePOS_3.clearParam()    
        return

    def MoveLegsHome(self,home_speed,port_hand_list,packet_handler):
        self.MoveLegs(0,port_hand_list,packet_handler)
        print("All limbs Moved to Home Position\n")

    def MoveSpineHome(self,home_speed,port_hand_list,packet_handler):
        self.MoveSpine(-1,port_hand_list,packet_handler)
        print("All Spine servos have been moved to Home Position")
        return

    def ContinuousLegsMove(self,port_hand_list,packet_handler,stride_numbers, record_array, start_time):
        out_data = []
        # Initialize GroupSyncRead instace for Moving designation
        groupSyncRead_Moving = GroupSyncRead(port_handler,packet_handler,AddrDict[39],1)
        readers_exist = False
        for stride_count in range(stride_numbers[0]):
            for position_index in range(stride_numbers[1]):
                isStopped = [0] * 16
                if (stride_count == 0) and (position_index == 0): # Skip the first position, this is Home Position
                    continue
                if (position_index == 0):
                    speed_index = stride_numbers[1] - 1
                else:
                    speed_index = position_index - 1
        return

    def __del__(self):
            pass
