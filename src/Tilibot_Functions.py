## Tilibot Functions

from Tilibot_Constants import *
from Tilibot_Classes import Servo, Leg, Neck, Spine, Tail, Body
import os
import yaml
from dynamixel_sdk import *
import numpy as np
import pandas as pd
import copy as cp
import time
import sys
import csv

if os.name == 'nt': # nt for windows, posix for mac and linux
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



def read_config_file(Config_Yaml_File): # Read the configuration yaml file and export data in an array
    with open(Config_Yaml_File, "r") as stream:
        config_data = yaml.safe_load(stream)
        baudrate = config_data['Baud-Rate']                             #0
        positions_file = config_data['Position-Angle-File']             #1
        position_amount = config_data['Positions-Per-Stride']           #2
        stride_time = config_data["Stride-Time"]                        #3
        stride_amount = config_data['Stride-Amount']                    #4
        connected_servos = config_data['Servos-Connected']              #5
        connected_limbs = config_data['Limbs-Connected']                #6
        connected_body = config_data['Whole-Body-Connected']            #7
        move_body_act = config_data['Move-Body']                        #8
        move_one_limb_act = config_data['Move-Single-Limb']             #9
        single_limb_to_move = config_data['Single-Limb-To-Move']        #10
        move_multi_limb_act = config_data['Move-Multiple-Limbs']        #11
        limbs_to_move = config_data['Limbs-To-Move']                    #12
        move_one_servo_act = config_data['Move-Single-Servo']           #13
        single_servo_to_move = config_data['Single-Servo-To-Move']      #14
        move_multi_servo_act = config_data['Move-Multiple-Servos']      #15
        servos_to_move = config_data['Servos-To-Move']                  #16
        home_speed = config_data['Home-Speed']                          #17
        out_file_name = config_data['Output-File-Name']                 #18
        out_file_dir = config_data['Output-File-Directory']             #19
        position_write = config_data['Position']                        #20
        speed_write = config_data['Speed']                              #21
        time_write = config_data['Time']                                #22
        posindex_write = config_data['Position-Index']                  #23
        stridecount_write = config_data['Stride-Count']                 #24
        current_write = config_data['Current']                          #25
        voltage_write = config_data['Voltage']                          #26
        temp_write = config_data['Temperature']                         #27
        neck_straight = config_data['Neck-Straight']                    #28
        spine_straight = config_data['Spine-Straight']                  #29
        tail_straight = config_data['Tail-Straight']                    #30
        silence_ext_ouput = config_data['Silence-Extraneous-Output']    #31
        run_digital_only = config_data['Run-Digital-Only']              #32

    config_array = [baudrate, positions_file, position_amount, stride_time, stride_amount, 
    connected_servos, connected_limbs, connected_body, move_body_act, move_one_limb_act, single_limb_to_move,
    move_multi_limb_act, limbs_to_move, move_one_servo_act, single_servo_to_move, move_multi_servo_act, 
    servos_to_move, home_speed, out_file_name, out_file_dir, position_write, speed_write, time_write, 
    posindex_write, stridecount_write, current_write, voltage_write, temp_write, neck_straight, spine_straight,
    tail_straight, silence_ext_ouput, run_digital_only]

    return config_array

def check_config_file(config_array):
    print("Confirming configuration file is properly written...")
    invalidate_value = False
    # Check that Configuration File is filled out correctly
    # That only one action is picked, its corresponding array is filled
    # and every field in the file is filled out correctly
    servo_count = len(config_array[5])
    limb_count = len(config_array[6])
    servo_all_bool = True
    limb_all_bool = True
    for x in config_array[5]:
        if not isinstance(x,bool):
            servo_all_bool = False
    for y in config_array[6]:
        if not isinstance(y,bool):
            limb_all_bool = False
    move_limb_number = len(config_array[12])
    move_servo_number = len(config_array[16])
    limbs_proper_ints = True
    servos_proper_ints = True
    if move_limb_number > 0:
        for a in move_limb_number:
            if (not isinstance(a, int)) or (a <= 0):
                limbs_proper_ints = False
    if move_servo_number > 0:
        for b in move_limb_number:
            if (not isinstance(a, int)) or (b <= 0):
                servos_proper_ints = False
    valid_home_speed = True
    if (not isinstance(config_array[17],int)):
        valid_home_speed = False
    elif (config_array[17] > 1023) or (config_array[17] < 0):
        valid_home_speed = False
    
    if (not isinstance(config_array[0],int)) or (config_array[0] <= 0):
        print("Baud-Rate input is incorrect format. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[1],str)) or (os.path.isfile(config_array[1])):
        print("Position-Angle-File is not a valid String or is not a valid file. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[2],int)) or (config_array[2] <= 0):
        print("Positions-Per-Stride is not a valid Integer number, or not the correct format. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[3],float)) or (config_array[3] <= 0):
        print("Stride-Time is not a valid Float number, or not the correct format. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[4],int)) or (config_array[0] <= 0):
        print("Stride-Amount is not a valid Integer number, or not the correct format.. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[5],list)) or (servo_count != 24) or (servo_all_bool == False):
        print("Servos-Connected is not a correct list, not 24 in length, or one of the elements is not a Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[6],list)) or (limb_count != 7) or (limb_all_bool == False):
        print("Limbs-Connected . Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[7],int)) or (config_array[7] <= 0):
        print("Whole-Body-Connected is not a correct list, not 7 in length, or one of the elements is not a Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[8],bool)):
        print("Move-Body is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[9],bool)):
        print("Move-Single-Limb is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[10],int)) or (config_array[10] <= 0):
        print("Single-Limb-To-Move is not a valid Integer. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[11],bool)):
        print("Move-Multiple-Limbs is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[12],list)) or (limbs_proper_ints == False):
        print("Limbs-To-Move is not a valid list or not all elements in it are Integers. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[13],bool)) :
        print("Move-Single-Servo is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[14],int)) or (config_array[14] <= 0):
        print("Single-Servo-To-Move is not a valid Integer. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[15],bool)):
        print("Move-Multiple-Servos is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[16],list)) or (servos_proper_ints == False):
        print("Servos-To-Move is not a valid list or not all elements in it are Integers. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[17],int)) or (valid_home_speed == False):
        print("Home-Speed is not a valid Integer between 0-1023. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[18],str)):
        print("Output-File-Name is not a valid String value. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[19],str)) or (os.path.isdir(config_array[19])):
        print("Output-File-Directory is not a valid String or not a valid Directory. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[20],int)) or (config_array[20] <= 0):
        print("Position is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[21],bool)):
        print("Speed is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[22],bool)):
        print("Time is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[23],bool)):
        print("Position-Index is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[24],bool)):
        print("Stride-Count is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[25],bool)):
        print("Current is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[26],bool)):
        print("Voltage is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[27],bool)):
        print("Temperature is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[28],bool)):
        print("Silence-Extraneous-Output is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[29],bool)):
        print("Neck-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[30],bool)):
        print("Spine-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[31],bool)):
        print("Tail-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True
    elif (not isinstance(config_array[32],bool)):
        print("Run-Digital-Only is not a valid Boolean. Please fix and try again.")
        invalidate_value = True

    if not any(config_array[5]):
        print("No Servos are marked as connected. Please fix and try again.")
        invalidate_value = True
    
    confirmed_action = [0, 0]
    action_currently_selected = False
    action_array = [config_array[8], config_array[9], config_array[10], config_array[11],
        config_array[12], config_array[13], config_array[14], config_array[15], config_array[16]]
    if action_array[0] == True:
        confirmed_action = [1, 0]
        if action_currently_selected == True:
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True
        action_currently_selected = True
    if action_array[1] == True:
        confirmed_action = [2, action_array[2]]
        if action_currently_selected == True:
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True
        action_currently_selected = True
    if action_array[3] == True:
        confirmed_action = [3, action_array[4]]
        if action_currently_selected == True:
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True
        action_currently_selected = True
    if action_array[5] == True:
        confirmed_action = [4, action_array[6]]
        if action_currently_selected == True:
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True
        action_currently_selected = True
    if action_array[7] == True:
        confirmed_action = [5, action_array[8]]
        if action_currently_selected == True:
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True
        action_currently_selected = True

    if (action_currently_selected == False):
        print("No action selected. Please fix and try again.")
        invalidate_value = True
    
    return invalidate_value, confirmed_action

def RecordPreferences(config_array):
    record_fields = [config_array[20], config_array[21], config_array[22], config_array[23], config_array[24],
                    config_array[25], config_array[26], config_array[27]]
    record_yesno = None
    if any(record_fields):
        record_yesno = True
    else:
        record_yesno = False
    # Consider using bit array for information
    record_fields.insert(0,record_yesno)
    new_path = os.path.join(config_array[19],config_array[18])
    outfile_whole = os.path.normpath(new_path)
    record_fields.append(outfile_whole)
    return record_fields

def Packet_Port_Setup(config_array):
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    ports_used = [0, 0, 0, 0]
    portHandler_1 = 0
    portHandler_2 = 0
    portHandler_3 = 0
    portHandler_4 = 0
    if (config_array[7]==True):
        portHandler_1 = PortHandler(DEVICENAME_1)
        # Open port
        if portHandler_1.openPort():
            print("Succeeded to open the port (#1)")
            if portHandler_1.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 1")
            else:
                print("Failed to change the baudrate")
                print("Press any key to terminate...")
                getch() # pylint: disable=undefined-variable
                return
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch() # pylint: disable=undefined-variable
            return
        portHandler_2 = PortHandler(DEVICENAME_2)
        if portHandler_2.openPort():
            print("Succeeded to open the port (#2)")
            if portHandler_2.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 2")
            else:
                print("Failed to change the baudrate")
                print("Press any key to terminate...")
                getch() # pylint: disable=undefined-variable
                return
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch() # pylint: disable=undefined-variable
            return
        portHandler_3 = PortHandler(DEVICENAME_3)
        if portHandler_3.openPort():
            print("Succeeded to open the port (#3)")
            if portHandler_3.setBaudRate(config_array[0]):
                print("Succeeded to change the baudrate for port 3")
            else:
                print("Failed to change the baudrate")
                print("Press any key to terminate...")
                getch() # pylint: disable=undefined-variable
                return
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch() # pylint: disable=undefined-variable
            return
        # portHandler_4 = PortHandler(DEVICENAME_4)
        # if portHandler_4.openPort():
        #     print("Succeeded to open the port (#4")
        #     # Set port baudrate
        #     if portHandler_4.setBaudRate(config_array[0]):
        #         print("Succeeded to change the baudrate for port 4")
        #     else:
        #         print("Failed to change the baudrate")
        #         print("Press any key to terminate...")
        #         getch() # pylint: disable=undefined-variable
        #         return
        # else:
        #     print("Failed to open the port")
        #     print("Press any key to terminate...")
        #     getch() # pylint: disable=undefined-variable
        #     return
        portHandler_4 = 0
        ports_used = [1, 1, 1, 1]
    elif (config_array[7]==False):
        if True in config_array[6]:
            count = 0
            for connected_limb in config_array[6]:
                if (connected_limb == True) and (count == 0 or count == 1):
                    ports_used[0] = 1
                elif (connected_limb == True) and (count == 2 or count == 3):
                    ports_used[1] = 1
                elif (connected_limb == True) and (count == 4 or count == 5 or count == 6):
                    ports_used[2] = 1
                elif (connected_limb == False):
                    pass
                count += 1
            if True in ports_used:
                pass
            else:
                print("No ports appear to be accessed. Please check the configuration file and try again...")
                exit()
            for count_2, accesed_port in enumerate(ports_used):
                if (accesed_port == 1) and (count_2 == 0):
                    portHandler_1 = PortHandler(DEVICENAME_1)
                    # Open port
                    if portHandler_1.openPort():
                        print("Succeeded to open the port (#1)")
                        if portHandler_1.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 1")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return
                elif (accesed_port == 1) and (count_2 == 1):
                    portHandler_2 = PortHandler(DEVICENAME_2)
                    if portHandler_2.openPort():
                        print("Succeeded to open the port (#2)")
                        if portHandler_2.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 2")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return
                elif (accesed_port == 1) and (count_2 == 2):
                    portHandler_3 = PortHandler(DEVICENAME_3)
                    if portHandler_3.openPort():
                        print("Succeeded to open the port (#3)")
                        if portHandler_3.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 3")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return                    
                elif (accesed_port == 1) and (count_2 == 3):
                    # portHandler_4 = PortHandler(DEVICENAME_4)
                    # if portHandler_4.openPort():
                    #     print("Succeeded to open the port (#4")
                    #     # Set port baudrate
                    #     if portHandler_4.setBaudRate(config_array[0]):
                    #         print("Succeeded to change the baudrate for port 4")
                    #     else:
                    #         print("Failed to change the baudrate")
                    #         print("Press any key to terminate...")
                    #         getch() # pylint: disable=undefined-variable
                    #         return
                    # else:
                    #     print("Failed to open the port")
                    #     print("Press any key to terminate...")
                    #     getch() # pylint: disable=undefined-variable
                    #     return
                    portHandler_4 = 0
                else:
                    pass 
        else:
            for count, connected_servo in enumerate(config_array[5]):
                if connected_servo == True:
                    if (count >= 1) and (count <=8):
                        ports_used[0] = 1
                    elif (count >= 9) and (count <= 16):
                        ports_used[1] = 1
                    elif (count >= 17) and (count <= 24):
                        ports_used[2] = 1
                    else:
                        pass
            for count_2, port_used in enumerate(ports_used):
                if (count_2 == 0) and (port_used == 1):
                    portHandler_1 = PortHandler(DEVICENAME_1)
                     # Open port
                    if portHandler_1.openPort():
                        print("Succeeded to open the port (#1)")
                        # Set port baudrate
                        if portHandler_1.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 1")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return
                elif (count_2 == 1) and (port_used == 1):
                    portHandler_2 = PortHandler(DEVICENAME_2)
                    if portHandler_2.openPort():
                        print("Succeeded to open the port (#2)")
                        # Set port baudrate
                        if portHandler_2.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 2")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return
                elif (count_2 == 2) and (port_used == 1):
                    portHandler_3 = PortHandler(DEVICENAME_3)
                    # Open port
                    if portHandler_3.openPort():
                        print("Succeeded to open the port (#3)")
                        # Set port baudrate
                        if portHandler_3.setBaudRate(config_array[0]):
                            print("Succeeded to change the baudrate for port 3")
                        else:
                            print("Failed to change the baudrate")
                            print("Press any key to terminate...")
                            getch() # pylint: disable=undefined-variable
                            return
                    else:
                        print("Failed to open the port")
                        print("Press any key to terminate...")
                        getch() # pylint: disable=undefined-variable
                        return    
                elif (count_2 == 3) and (port_used == 1):
                    # portHandler_4 = PortHandler(DEVICENAME_4)
                    # if portHandler_4.openPort():
                    #     print("Succeeded to open the port (#4")
                    #     # Set port baudrate
                    #     if portHandler_4.setBaudRate(config_array[0]):
                    #         print("Succeeded to change the baudrate for port 4")
                    #     else:
                    #         print("Failed to change the baudrate")
                    #         print("Press any key to terminate...")
                    #         getch() # pylint: disable=undefined-variable
                    #         return
                    # else:
                    #     print("Failed to open the port")
                    #     print("Press any key to terminate...")
                    #     getch() # pylint: disable=undefined-variable
                    #     return
                    portHandler_4 = 0
                else:
                    print("No ports appear to be accessed. Please check the configuration file and try again...")
                    exit()
    else: 
        print("No ports appear to be accessed. Please check the configuration file and try again...")
        exit()

    # Initialize PacketHandler instance
    # Set the protocol version
    # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    return portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler

def DigitalSetup(config_array):

    return


def gcd(a, b): 
    if b == 0: 
        return a 
    else: 
        return gcd(b, a%b) 

def RotatePositionArray(inArray,shiftNum,arrayLength):
    for i in range(gcd(shiftNum,arrayLength)):  
        temp = inArray[i] 
        j = i 
        while 1: 
            k = j + shiftNum 
            if k >= arrayLength: 
                k = k - arrayLength 
            if k == i: 
                break
            inArray[j] = inArray[k] 
            j = k 
        inArray[j] = temp
    return inArray

def DataAddrConversion(DesiredData):
    DataAddr = -1
    # Get the address of the desired data trait, used in conjuction with ReturnRelevantData and ChangeSpecificTrait
    if (DesiredData >= 1 and DesiredData <= 48):
        DataAddr = AddrDict[DesiredData]
    else:
        print("That's not a recognized trait selection, please try again!\n")
    return DataAddr if DataAddr != -1 else -1

def FormatSendData(rawData):
    return [DXL_LOBYTE(DXL_LOWORD(rawData)), DXL_HIBYTE(DXL_LOWORD(rawData)), DXL_LOBYTE(DXL_HIWORD(rawData)), DXL_HIBYTE(DXL_HIWORD(rawData))]

def ReadServoAngles(positionsFile):

    old_df = pd.read_csv(positionsFile)
    old_df = old_df.values[:][:]

    FL_ST_R_1 = old_df[:,0]
    FL_ST_R_2 = old_df[:,1]
    FL_ST_R_3 = old_df[:,2]
    FL_ST_R_4 = old_df[:,3]

    FL_SW_R_1 = old_df[:,4]
    FL_SW_R_2 = old_df[:,5]
    FL_SW_R_3 = old_df[:,6]
    FL_SW_R_4 = old_df[:,7]

    FL_TOT_R_1 = np.concatenate((FL_ST_R_1, FL_SW_R_1),axis=0)
    FL_TOT_R_2 = np.concatenate((FL_ST_R_2, FL_SW_R_2),axis=0)
    FL_TOT_R_3 = np.concatenate((FL_ST_R_3, FL_SW_R_3),axis=0)
    FL_TOT_R_4 = np.concatenate((FL_ST_R_4, FL_SW_R_4),axis=0)

    FL_ST_L_1 = old_df[:,0]
    FL_ST_L_2 = old_df[:,1]
    FL_ST_L_3 = old_df[:,2]
    FL_ST_L_4 = old_df[:,3]

    FL_SW_L_1 = old_df[:,4]
    FL_SW_L_2 = old_df[:,5]
    FL_SW_L_3 = old_df[:,6]
    FL_SW_L_4 = old_df[:,7]

    FL_TOT_L_1 = np.concatenate((FL_ST_L_1, FL_SW_L_1),axis=0)
    FL_TOT_L_2 = np.concatenate((FL_ST_L_2, FL_SW_L_2),axis=0)
    FL_TOT_L_3 = np.concatenate((FL_ST_L_3, FL_SW_L_3),axis=0)
    FL_TOT_L_4 = np.concatenate((FL_ST_L_4, FL_SW_L_4),axis=0)

    HL_ST_R_1 = old_df[:,8]
    HL_ST_R_2 = old_df[:,9]
    HL_ST_R_3 = old_df[:,10]
    HL_ST_R_4 = old_df[:,11]

    HL_SW_R_1 = old_df[:,12]
    HL_SW_R_2 = old_df[:,13]
    HL_SW_R_3 = old_df[:,14]
    HL_SW_R_4 = old_df[:,15]

    HL_TOT_R_1 = np.concatenate((HL_ST_R_1, HL_SW_R_1),axis=0)
    HL_TOT_R_2 = np.concatenate((HL_ST_R_2, HL_SW_R_2),axis=0)
    HL_TOT_R_3 = np.concatenate((HL_ST_R_3, HL_SW_R_3),axis=0)
    HL_TOT_R_4 = np.concatenate((HL_ST_R_4, HL_SW_R_4),axis=0)

    HL_ST_L_1 = old_df[:,8]
    HL_ST_L_2 = old_df[:,9]
    HL_ST_L_3 = old_df[:,10]
    HL_ST_L_4 = old_df[:,11]

    HL_SW_L_1 = old_df[:,12]
    HL_SW_L_2 = old_df[:,13]
    HL_SW_L_3 = old_df[:,14]
    HL_SW_L_4 = old_df[:,15]

    HL_TOT_L_1 = np.concatenate((HL_ST_L_1, HL_SW_L_1),axis=0)
    HL_TOT_L_2 = np.concatenate((HL_ST_L_2, HL_SW_L_2),axis=0)
    HL_TOT_L_3 = np.concatenate((HL_ST_L_3, HL_SW_L_3),axis=0)
    HL_TOT_L_4 = np.concatenate((HL_ST_L_4, HL_SW_L_4),axis=0)

    dyn_con = 4096/360

    j = 0
    for i in FL_TOT_R_1:    # Right Forelimb Servo #1
        FL_TOT_R_1[j] = 2048 - (i * dyn_con)
        j += 1
    FL_TOT_R_1 = FL_TOT_R_1.round()
    FL_TOT_R_1 = list(map(int,FL_TOT_R_1))
    j = 0
    for i in FL_TOT_R_2:    # Right Forelimb Servo #2
        FL_TOT_R_2[j] = 2048 + (i * dyn_con)
        j += 1
    FL_TOT_R_2 = FL_TOT_R_2.round()
    FL_TOT_R_2 = list(map(int,FL_TOT_R_2))
    j = 0
    for i in FL_TOT_R_3:    # Right Forelimb Servo #3
        FL_TOT_R_3[j] = 2048 + (i * dyn_con)
        j += 1
    FL_TOT_R_3 = FL_TOT_R_3.round()
    FL_TOT_R_3 = list(map(int,FL_TOT_R_3))
    j = 0
    for i in FL_TOT_R_4:    # Right Forelimb Servo #4
        FL_TOT_R_4[j] = 2048 + (i * dyn_con)
        j += 1
    FL_TOT_R_4 = FL_TOT_R_4.round()
    FL_TOT_R_4 = list(map(int,FL_TOT_R_4))
    j = 0
    for i in FL_TOT_L_1:    # Left Forelimb Servo #5
        FL_TOT_L_1[j] = 2048 + ( i * dyn_con)
        j += 1
    FL_TOT_L_1 = FL_TOT_L_1.round()
    FL_TOT_L_1 = list(map(int,FL_TOT_L_1))
    j = 0
    for i in FL_TOT_L_2:    # Left Forelimb Servo #6
        FL_TOT_L_2[j] = 2048 + (i * dyn_con)
        j += 1
    FL_TOT_L_2 = FL_TOT_L_2.round()
    FL_TOT_L_2 = list(map(int,FL_TOT_L_2))
    j = 0
    for i in FL_TOT_L_3:    # Left Forelimb Servo #7
        FL_TOT_L_3[j] = 2048 - (i * dyn_con)
        j += 1
    FL_TOT_L_3 = FL_TOT_L_3.round()
    FL_TOT_L_3 = list(map(int,FL_TOT_L_3))
    j = 0
    for i in FL_TOT_L_4:    # Left Forelimb Servo #8
        FL_TOT_L_4[j] = 2048 + (i * dyn_con)
        j += 1
    FL_TOT_L_4 = FL_TOT_L_4.round()
    FL_TOT_L_4 = list(map(int,FL_TOT_L_4))
    j = 0
    for i in HL_TOT_R_1:    # Right Hindlimb Servo #9
        HL_TOT_R_1[j] = 2048 - (i * dyn_con)
        j += 1
    HL_TOT_R_1 = HL_TOT_R_1.round()
    HL_TOT_R_1 = list(map(int,HL_TOT_R_1))
    j = 0
    for i in HL_TOT_R_2:    # Right Hindlimb Servo #10
        HL_TOT_R_2[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_R_2 = HL_TOT_R_2.round()
    HL_TOT_R_2 = list(map(int,HL_TOT_R_2))
    j = 0
    for i in HL_TOT_R_3:    # Right Hindlimb Servo #11
        HL_TOT_R_3[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_R_3 = HL_TOT_R_3.round()
    HL_TOT_R_3 = list(map(int,HL_TOT_R_3))
    j = 0
    for i in HL_TOT_R_4:    # Right Hindlimb Servo #12
        HL_TOT_R_4[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_R_4 = HL_TOT_R_4.round()
    HL_TOT_R_4 = list(map(int,HL_TOT_R_4))
    j = 0
    for i in HL_TOT_L_1:    # Left Hindlimb Servo #13
        HL_TOT_L_1[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_L_1 = HL_TOT_L_1.round()
    HL_TOT_L_1 = list(map(int,HL_TOT_L_1))
    j = 0
    for i in HL_TOT_L_2:    # Left Hindlimb Servo #14
        HL_TOT_L_2[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_L_2 = HL_TOT_L_2.round()
    HL_TOT_L_2 = list(map(int,HL_TOT_L_2))
    j = 0
    for i in HL_TOT_L_3:    # Left Hindlimb Servo #15
        HL_TOT_L_3[j] = 2048 - (i * dyn_con)
        j += 1
    HL_TOT_L_3 = HL_TOT_L_3.round()
    HL_TOT_L_3 = list(map(int,HL_TOT_L_3))
    j = 0
    for i in HL_TOT_L_4:    # Left Hindlimb Servo #16
        HL_TOT_L_4[j] = 2048 + (i * dyn_con)
        j += 1
    HL_TOT_L_4 = HL_TOT_L_4.round()
    HL_TOT_L_4 = list(map(int,HL_TOT_L_4))

    return [FL_TOT_R_1, FL_TOT_R_2, FL_TOT_R_3, FL_TOT_R_4, FL_TOT_L_1, 
    FL_TOT_L_2, FL_TOT_L_3, FL_TOT_L_4, HL_TOT_R_1, HL_TOT_R_2, HL_TOT_R_3, 
    HL_TOT_R_4, HL_TOT_L_1, HL_TOT_L_2, HL_TOT_L_3, HL_TOT_L_4]

def PostProcessPositions(inPositions):
    ServoPos1 = RotatePositionArray(inPositions[0],1,len(inPositions[0]))
    ServoPos2 = RotatePositionArray(inPositions[1],1,len(inPositions[1]))
    ServoPos3 = RotatePositionArray(inPositions[2],1,len(inPositions[2]))
    ServoPos4 = RotatePositionArray(inPositions[3],1,len(inPositions[3]))

    ServoPos5 = RotatePositionArray(inPositions[4],9,len(inPositions[4]))
    ServoPos6 = RotatePositionArray(inPositions[5],9,len(inPositions[5]))
    ServoPos7 = RotatePositionArray(inPositions[6],9,len(inPositions[6]))
    ServoPos8 = RotatePositionArray([7],9,len(inPositions[7]))

    ServoPos9 = RotatePositionArray(inPositions[8],8,len(inPositions[8]))
    ServoPos10 = RotatePositionArray(inPositions[9],8,len(inPositions[9]))
    ServoPos11 = RotatePositionArray(inPositions[10],8,len(inPositions[10]))
    ServoPos12 = RotatePositionArray(inPositions[11],8,len(inPositions[11]))

    # Does Not Need to be Rotated, starts exactly at zero (0)
    ServoPos13 = inPositions[12]
    ServoPos14 = inPositions[13]
    ServoPos15 = inPositions[14]
    ServoPos16 = inPositions[15]

    ServoPos1 = np.array(ServoPos1)
    ServoPos2 = np.array(ServoPos2)
    ServoPos3 = np.array(ServoPos3)
    ServoPos4 = np.array(ServoPos4)

    ServoPos5 = np.array(ServoPos5)
    ServoPos6 = np.array(ServoPos6)
    ServoPos7 = np.array(ServoPos7)
    ServoPos8 = np.array(ServoPos8)

    ServoPos9 = np.array(ServoPos9)
    ServoPos10 = np.array(ServoPos10)
    ServoPos11 = np.array(ServoPos11)
    ServoPos12 = np.array(ServoPos12)

    ServoPos13 = np.array(ServoPos13)
    ServoPos14 = np.array(ServoPos14)
    ServoPos15 = np.array(ServoPos15)
    ServoPos16 = np.array(ServoPos16)

    return [ServoPos1, ServoPos2, ServoPos3, ServoPos4, 
    ServoPos5, ServoPos6, ServoPos7, ServoPos8, 
    ServoPos9, ServoPos10, ServoPos11, ServoPos12, 
    ServoPos13, ServoPos14, ServoPos15, ServoPos16]

def DetermineSpeeds(tspan,PositionsMatrix):
    #Import position points as a data frame (df)
    #old_df = pd.read_csv(positionsFile)
    #old_df = old_df.values[:][:]
    #Make a copy of the dataframe with the same dimensions for the speeds
    speeds = cp.copy(PositionsMatrix)
    h_stance = 4.892994
    h_swing = 3.347006
    f_stance = 5.211718
    f_swing = 3.028282
    h_st_per = h_stance / 8.24
    h_sw_per = h_swing / 8.24
    f_st_per = f_stance / 8.24
    f_sw_per = f_swing / 8.24
    #Starting % index for each limb
    L_hl = 0
    L_fl = 9 # 90% Approximately
    R_hl = 8 # 80% Approximately
    R_fl = 1 # 10% Approximately
    #Points per Phase
    pointsPerPhase = 11
    speeds = np.array(speeds)
    b = speeds.shape
    cLength = int(b[1]/2)
    cWidth = int(b[0])
    MoveIndex = np.linspace(1,int(b[1]),int(b[1]))
    servos = list(range(1,cWidth+1))
    MoveIndex = MoveIndex.astype(int).tolist()
    newSpeeds = []
    #t1 = np.zeros(b[1])
    for i in np.linspace(1,cWidth,cWidth):
        newSpeeds.append(np.zeros(b[1]))
    for i in servos:
        for j in MoveIndex: 
            if (i == 1 or i == 2 or i == 3 or i == 4 ):
                if (j==b[1]):
                    rotations = abs(speeds[i-1][0]-speeds[i-1][j-1])/4096
                else:
                    rotations = abs(speeds[i-1][j]-speeds[i-1][j-1])/4096
                if ((j-1) >= (pointsPerPhase - R_fl) and (j-1)<=(pointsPerPhase - R_fl + 10)):
                    movementTime = (tspan*f_sw_per/cLength)/60
                else:
                    movementTime = (tspan*f_st_per/cLength)/60
                movementSpeed = (rotations / movementTime) / 0.114
                newSpeeds[i-1][j-1] = round(movementSpeed)
            elif (i == 5 or i == 6 or i == 7 or i == 8): 
                if (j==b[1]):
                    rotations = abs(speeds[i-1][0]-speeds[i-1][j-1])/4096
                else:
                    rotations = abs(speeds[i-1][j]-speeds[i-1][j-1])/4096
                if ((j-1) >= (pointsPerPhase - L_fl) and (j-1)<=(pointsPerPhase - L_fl + 10)):
                    movementTime = (tspan*f_sw_per/cLength)/60
                else:
                    movementTime = (tspan*f_st_per/cLength)/60
                movementSpeed = (rotations / movementTime) / 0.114
                newSpeeds[i-1][j-1] = round(movementSpeed)
            elif (i == 9 or i == 10 or i == 11 or i == 12 ):
                if (j==b[1]):
                    rotations = abs(speeds[i-1][0]-speeds[i-1][j-1])/4096
                else:
                    rotations = abs(speeds[i-1][j]-speeds[i-1][j-1])/4096
                if ((j-1) >= (pointsPerPhase - R_hl) and (j-1)<=(pointsPerPhase - R_hl + 10)):
                    movementTime = (tspan*h_sw_per/cLength)/60
                else:
                    movementTime = (tspan*h_st_per/cLength)/60
                movementSpeed = (rotations / movementTime) / 0.114
                newSpeeds[i-1][j-1] = round(movementSpeed)
            elif (i == 13 or i == 14 or i == 15 or i == 16 ):
                if (j==b[1]):
                    rotations = abs(speeds[i-1][0]-speeds[i-1][j-1])/4096
                else:
                    rotations = abs(speeds[i-1][j]-speeds[i-1][j-1])/4096
                if ((j-1) >= (pointsPerPhase - L_hl) and (j-1)<=(pointsPerPhase - L_hl + 10)):
                    movementTime = (tspan*h_sw_per/cLength)/60
                else:
                    movementTime = (tspan*h_st_per/cLength)/60
                movementSpeed = (rotations / movementTime) / 0.114
                newSpeeds[i-1][j-1] = round(movementSpeed)
    for i in servos:
        newSpeeds[i-1] = newSpeeds[i-1].astype(int)
    for j in servos:
        newSpeeds[j-1][newSpeeds[j-1] > 1023] = 1023
        newSpeeds[j-1][newSpeeds[j-1] == 0] = 1

    return newSpeeds
    
def Create_DigitalServos(config_array, PositionsMatrix, SpeedMatrix):
    ServoDictionary = {}
    for ID, connected_servo in enumerate(config_array[5]):
        if connected_servo == True:
            ID += 1
            if (ID == 1) or (ID == 5) or (ID == 9) or (ID == 13):
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
            elif (ID == 2) or (ID == 6) or (ID == 10) or (ID == 14):
                Max_Position_Limit = 2620
                Min_Position_Limit = 1024
            elif (ID == 3) or (ID == 7) or (ID == 11) or (ID == 15):
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
            elif (ID == 4) or (ID == 8) or (ID == 12) or (ID == 16):
                Max_Position_Limit = 2820
                Min_Position_Limit = 1024
            elif (ID == 17) or (ID == 18): # Needs to be checked
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
                if config_array[28] == True:
                    pass
            elif (ID == 19) or (ID == 20) or (ID == 21) or (ID == 22): # Needs to be checked
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
                if config_array[29] == True:
                    pass
            elif (ID == 23) or (ID == 24): # Needs to be checked
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
                if config_array[30] == True:
                    pass
            else:
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
            MaxMinLimit = (Max_Position_Limit, Min_Position_Limit)
            
            NewServo = Servo(ID,PositionsMatrix[ID-1][:], SpeedMatrix[:][ID-1], MaxMinLimit)
            print("Servo #%d has been digitally created." % (NewServo.ID))
            ServoDictionary[ID] = NewServo
    return ServoDictionary 

def Create_DigitalLimbs(config_array,ServoDictionary):
    LimbDictionary = {}
    servo_limb_dic = {}
    for Limb_ID, connected_limb in enumerate(config_array[6]):
        if connected_limb == True:
            entire_limb_not_present = False
            for servo in BODY[Limb_ID]:
                if ServoDictionary.has_key(servo):
                    servo_limb_dic[ServoDictionary[servo].ID] = ServoDictionary[servo]
                else:
                    entire_limb_not_present = True
            if entire_limb_not_present == True:
                print("Corresponding Servos for the indicated connected limbs are not present. Please fix and try again.")
                exit()
            elif entire_limb_not_present == False:
                Limb_ID += 1
                if (Limb_ID >= 1) and (Limb_ID <= 4):
                    NewLimb = Leg(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.ID))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 5):
                    NewLimb = Neck(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.ID))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 6):
                    NewLimb = Spine(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.ID))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 7):
                    NewLimb = Tail(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.ID))
                    LimbDictionary[Limb_ID] = NewLimb
            servo_limb_dic = {}
    return LimbDictionary

def Create_DigitalBody(LimbDictionary):
    all_limbs_present = True
    for Limb_ID in BODY_LIMB_IDS:
        if LimbDictionary.has_keys(Limb_ID):
            pass
        else:
            all_limbs_present = False
    if all_limbs_present == True:
        WholeBody = Body(LimbDictionary)
        print("Whole Body digitally created.")
    else:
        print("Not all limbs are registered as being connected. Body can not be digitally assembled. Please fix and try again.")
    return WholeBody

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

def MoveNumerousServos(servo_list, ServosDictionary, port_hand_list, packet_handler, stride_numbers, record_array, start_time):
    ports_used = [0, 0, 0]
    if any(x in servo_list for x in FRONT_ARMS):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[36], 4)
        groupSyncRead_Moving_1 = GroupSyncRead(port_hand_list[0],packet_handler, AddrDict[39], 1)
        ports_used[0] = 1
    if any(x in servo_list for x in BACK_ARMS):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[36], 4)
        groupSyncRead_Moving_2 = GroupSyncRead(port_hand_list[1],packet_handler, AddrDict[39], 1)
        ports_used[1] = 1
    if any(x in servo_list for x in BODY_LENGTH):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[36], 4)
        groupSyncRead_Moving_3 = GroupSyncRead(port_hand_list[2],packet_handler, AddrDict[39], 1)
        ports_used[2] = 1
    
    front_servo_count = 0
    back_servo_count = 0
    bodylength_servo_count = 0
    for each_servo in servo_list:
        if each_servo in FRONT_ARMS:
            front_servo_count += 1
        elif each_servo in BACK_ARMS:
            back_servo_count += 1
        elif each_servo in BODY_LENGTH: 
            bodylength_servo_count += 1

    GoalVelocity = []
    GoalPosition = []
    
    out_data = []
    readers_exist = False
    for stride_count in range(stride_numbers[0]):
        for position_index in range(stride_numbers[1]):
            if ports_used[0] == 1:
                isStopped_1 = [0] * front_servo_count
            if ports_used[1] == 1:
                isStopped_2 = [0] * back_servo_count
            if ports_used[2] == 1:
                isStopped_3 = [0] * bodylength_servo_count
            if (stride_count == 0) and (position_index == 0): # Skip the first position, this is Home Position
                continue
            if (position_index == 0):
                speed_index = stride_numbers[1] - 1
            else:
                speed_index = position_index - 1
            for index, each_servo in enumerate(servo_list):
                GoalVelocity.append(FormatSendData(int(ServosDictionary[each_servo].Speeds[speed_index])))
                GoalPosition.append(FormatSendData(ServosDictionary[each_servo].Positions[position_index]))
                if each_servo in FRONT_ARMS:
                    dxl_addparam_result = groupSyncWriteVEL_1.addParam(each_servo,GoalVelocity[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                        return
                    dxl_addparam_result = groupSyncWritePOS_1.addParam(each_servo,GoalPosition[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                        return
                elif each_servo in BACK_ARMS:
                    dxl_addparam_result = groupSyncWriteVEL_2.addParam(each_servo,GoalVelocity[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                        return
                    dxl_addparam_result = groupSyncWritePOS_2.addParam(each_servo,GoalPosition[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                        return
                elif each_servo in BODY_LENGTH:
                    dxl_addparam_result = groupSyncWriteVEL_3.addParam(each_servo,GoalVelocity[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                        return
                    dxl_addparam_result = groupSyncWritePOS_3.addParam(each_servo,GoalPosition[index])
                    if dxl_addparam_result != True:
                        print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                        return
                else:
                    print('Error in servo list. Please fix and try again.')
            if ports_used[0] == 1:
                # Syncwrite goal velocity
                dxl_comm_result = groupSyncWriteVEL_1.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWriteVEL_1.clearParam()
            if ports_used[1] == 1:
                # Syncwrite goal velocity
                dxl_comm_result = groupSyncWriteVEL_2.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWriteVEL_2.clearParam()
            if ports_used[2] == 1:
                # Syncwrite goal velocity
                dxl_comm_result = groupSyncWriteVEL_3.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWriteVEL_3.clearParam()
            if ports_used[0] == 1:
                # Syncwrite goal position
                dxl_comm_result = groupSyncWritePOS_1.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWritePOS_1.clearParam()
            if ports_used[1] == 1:
                # Syncwrite goal position
                dxl_comm_result = groupSyncWritePOS_2.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWritePOS_2.clearParam()
            if ports_used[2] == 1:
                # Syncwrite goal position
                dxl_comm_result = groupSyncWritePOS_3.txPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                # Clear syncwrite parameter storage
                groupSyncWritePOS_3.clearParam()
            for each_servo in ServosDictionary.keys():
                if each_servo in FRONT_ARMS:
                    groupSyncRead_Moving_1.addParam(each_servo)
                elif each_servo in BACK_ARMS:
                    groupSyncRead_Moving_2.addParam(each_servo)
                elif each_servo in BODY_LENGTH:
                    groupSyncRead_Moving_3.addParam(each_servo)
            while 1:
                # Syncread Moving Value
                if ports_used[0] == 1:
                    dxl_comm_result = groupSyncRead_Moving_1.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                if ports_used[1] == 1:
                    dxl_comm_result = groupSyncRead_Moving_2.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                if ports_used[2] == 1:
                    dxl_comm_result = groupSyncRead_Moving_3.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))

                for index,each_servo in enumerate(ServosDictionary.keys()):
                    # Get Dynamixel present Moving value
                    if each_servo in FRONT_ARMS:
                        dxl_mov = groupSyncRead_Moving_1.getData(each_servo, AddrDict[39],1)
                        if (dxl_mov == 0) and (isStopped_1[index] == 0):
                            isStopped_1[index] = 1
                    if each_servo in BACK_ARMS:
                        dxl_mov = groupSyncRead_Moving_2.getData(each_servo, AddrDict[39],1)
                        if (dxl_mov == 0) and (isStopped_2[index-front_servo_count] == 0):
                            isStopped_2[index] = 1
                    if each_servo in BODY_LENGTH:
                        dxl_mov = groupSyncRead_Moving_3.getData(each_servo, AddrDict[39],1)
                        if (dxl_mov == 0) and (isStopped_3[index-(front_servo_count + back_servo_count)] == 0):
                            isStopped_3[index] = 1
                if (0 in isStopped_1) or (0 in isStopped_2) or (0 in isStopped_3):
                    pass
                else:
                    groupSyncRead_Moving_1.clearParam()
                    groupSyncRead_Moving_2.clearParam()
                    groupSyncRead_Moving_3.clearParam()
                    if record_array[0] == True:
                        if readers_exist == False:
                            if ports_used[0] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[42],2)
                                    port_1_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[47],2)
                                    port_1_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[48],1)
                                    port_1_Temperature = []
                                    readers_exist = True
                            if ports_used[1] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[42],2)
                                    port_2_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[47],2)
                                    port_2_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[48],1)
                                    port_2_Temperature = []
                                    readers_exist = True
                            if ports_used[2] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[42],2)
                                    port_3_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[47],2)
                                    port_3_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[48],1)
                                    port_3_Temperature = []
                                    readers_exist = True
                        if readers_exist == True:
                            for each_servo in servo_list:
                                if record_array[6] == True:
                                    if ports_used[0] == 1:
                                        groupSyncRead_Current_1.addParam(each_servo)
                                    if ports_used[1] == 1:
                                        groupSyncRead_Current_2.addParam(each_servo)
                                    if ports_used[2] == 1:
                                        groupSyncRead_Current_3.addParam(each_servo)
                                if record_array[7] == True:
                                    if ports_used[0] == 1:
                                        groupSyncRead_Voltage_1.addParam(each_servo)
                                    if ports_used[1] == 1:
                                        groupSyncRead_Voltage_2.addParam(each_servo)
                                    if ports_used[2] == 1:
                                        groupSyncRead_Voltage_3.addParam(each_servo)
                                if record_array[8] == True:
                                    if ports_used[0] == 1:
                                        groupSyncRead_Temperature_1.addParam(each_servo)
                                    if ports_used[1] == 1:
                                        groupSyncRead_Temperature_2.addParam(each_servo)
                                    if ports_used[2] == 1:
                                        groupSyncRead_Temperature_3.addParam(each_servo)
                        if readers_exist == True:
                            if record_array[6] == True:
                                if ports_used[0] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_1.isAvailable(each_front_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_front_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_1_Current.append(groupSyncRead_Current_1.getData(each_front_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_2.isAvailable(each_back_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_back_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_2_Current.append(groupSyncRead_Current_2.getData(each_back_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_3.isAvailable(each_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_3_Current.append(groupSyncRead_Current_3.getData(each_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_3.clearParam()
                            if record_array[7] == True:
                                if ports_used[0] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_1.isAvailable(each_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_1_Voltage.append(groupSyncRead_Voltage_1.getData(each_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_2.isAvailable(each_back_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_back_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_2_Voltage.append(groupSyncRead_Voltage_2.getData(each_back_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Voltage_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_3.isAvailable(each_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_3_Voltage.append(groupSyncRead_Voltage_3.getData(each_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Voltage_3.clearParam()
                            if record_array[8] == True:
                                if ports_used[0] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_1.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_1_Temperature.append(groupSyncRead_Temperature_1.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_2.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_2_Temperature.append(groupSyncRead_Temperature_2.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_3.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_3_Temperature.append(groupSyncRead_Temperature_3.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_3.clearParam()
                        if readers_exist == True:
                            for list_index,each_servo in enumerate(servo_list):
                                servo_data_array = [each_servo]
                                if record_array[1] == True:
                                    pos_out = ServosDictionary[each_servo].Positions[position_index]
                                    servo_data_array.append(pos_out)
                                    # Record Position / self.Positions[stride_count]
                                if record_array[2] == True:
                                    vel_out = ServosDictionary[each_servo].Speeds[stride_count]
                                    servo_data_array.append(vel_out)
                                    # Record Speed / self.Speeds[stride_count]
                                if record_array[3] == True:
                                    record_time = time.time()
                                    end_time = record_time - start_time
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
                                    if each_servo in FRONT_ARMS:
                                        dxl_current = port_1_Current[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_current = port_2_Current[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_current = port_3_Current[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_current)
                                if record_array[7] == True:
                                    if each_servo in FRONT_ARMS:
                                        dxl_voltage = port_1_Voltage[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_voltage = port_2_Voltage[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_voltage = port_3_Voltage[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_voltage)
                                if record_array[8] == True:
                                    if each_servo in FRONT_ARMS:
                                        dxl_temp = port_1_Temperature[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_temp = port_2_Temperature[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_temp = port_3_Temperature[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_temp)
                                out_data.append(servo_data_array)
                    if record_array[6] == True:
                        if ports_used[0] == 1:
                            port_1_Current = []
                        if ports_used[1] == 1:
                            port_2_Current = []
                        if ports_used[2] == 1:
                            port_3_Current = []
                    if record_array[7] == True:
                        if ports_used[0] == 1:
                            port_1_Voltage = []
                        if ports_used[1] == 1:
                            port_2_Voltage = []
                        if ports_used[2] == 1:
                            port_3_Voltage = []
                    if record_array[8] == True:
                        if ports_used[0] == 1:
                            port_1_Temperature = []
                        if ports_used[1] == 1:
                            port_2_Temperature = []
                        if ports_used[2] == 1:
                            port_3_Temperature = []
                    GoalVelocity = []
                    GoalPosition = []
                    break
    return out_data

def MoveNumerousLimbs(limb_list,LimbDictionary,ServosDictionary,port_hand_list,packet_handler,stride_numbers,record_array,start_time):
    ports_used = [0, 0, 0]
    servo_list = []
    for each_limb in LimbDictionary.values():
        for each_servo in each_limb.ServoDict.keys():
            servo_list.append(each_servo)
    front_servo_count = 0
    back_servo_count = 0
    bodylength_servo_count = 0
    for each_servo in servo_list:
        if each_servo in FRONT_ARMS:
            front_servo_count += 1
        elif each_servo in BACK_ARMS:
            back_servo_count += 1
        elif each_servo in BODY_LENGTH: 
            bodylength_servo_count += 1
    if any(x in limb_list for x in LEG_LIMB_IDS_FRONT):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packet_handler, AddrDict[36], 4)
        # Initialize GroupSyncRead instace for Moving designation
        groupSyncRead_Moving_1 = GroupSyncRead(port_hand_list[0],packet_handler, AddrDict[39], 1)
        ports_used[0] = 1
    if any(x in limb_list for x in LEG_LIMB_IDS_BACK):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packet_handler, AddrDict[36], 4)
        # Initialize GroupSyncRead instace for Moving designation
        groupSyncRead_Moving_2 = GroupSyncRead(port_hand_list[1],packet_handler, AddrDict[39], 1)
        ports_used[1] = 1
    if any(x in limb_list for x in BODY_LENGTH_LIMB_IDS):
        # Initialize GroupSyncWrite instance
        groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[37], 4)
        # Initialize GroupSyncWrite instance
        groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packet_handler, AddrDict[36], 4)
        # Initialize GroupSyncRead instace for Moving designation
        groupSyncRead_Moving_3 = GroupSyncRead(port_hand_list[2],packet_handler, AddrDict[39], 1)
        ports_used[2] = 1
    out_data = []
    readers_exist = False
    number_of_servos = 0
    for each_limb in LimbDictionary.values():
        for each_servo in each_limb.ServoDict.keys():
            number_of_servos += 1
    for stride_count in range(stride_numbers[0]):
        for position_index in range(stride_numbers[1]):
            if (stride_count == 0) and (position_index == 0): # Skip the first position, this is Home Position
                continue
            if (position_index == 0):
                speed_index = stride_numbers[1] - 1
            else:
                speed_index = position_index - 1
            for each_limb,limb_obj in LimbDictionary.items():
                if ports_used[0] == 1:
                    GoalVelocity_1 = []
                    GoalPosition_1 = []
                if ports_used[1] == 1:
                    GoalVelocity_2 = []
                    GoalPosition_2 = []
                if ports_used[2] == 1:
                    GoalVelocity_3 = []
                    GoalPosition_3 = []
                speed_list = limb_obj.DetermineVelocities(speed_index)
                if (each_limb == 1) or (each_limb == 2):
                    for count,servo_obj in enumerate(limb_obj.ServoDict.values()):
                        GoalVelocity_1.append(FormatSendData(int(speed_list[count])))
                        GoalPosition_1.append(FormatSendData(servo_obj.Positions[position_index]))
                        groupSyncWriteVEL_1.addParam(each_servo, GoalVelocity_1[count])
                        groupSyncWritePOS_1.addParam(each_servo, GoalPosition_1[count])
                        groupSyncRead_Moving_1.addParam(servo_obj.ID)
                elif (each_limb == 3) or (each_limb == 4):
                    for count,servo_obj in enumerate(limb_obj.ServoDict.values()):
                        GoalVelocity_2.append(FormatSendData(int(speed_list[count])))
                        GoalPosition_2.append(FormatSendData(servo_obj.Positions[position_index]))
                        groupSyncWriteVEL_2.addParam(each_servo, GoalVelocity_2[count])
                        groupSyncWritePOS_2.addParam(each_servo, GoalPosition_2[count])
                        groupSyncRead_Moving_2.addParam(servo_obj.ID)
                elif (each_limb == 5) or (each_limb == 6) or (each_limb == 7):
                    for count,servo_obj in enumerate(limb_obj.ServoDict.values()):
                        GoalVelocity_3.append(FormatSendData(int(speed_list[count])))
                        GoalPosition_3.append(FormatSendData(servo_obj.Positions[position_index]))
                        groupSyncWriteVEL_3.addParam(each_servo, GoalVelocity_3[count])
                        groupSyncWritePOS_3.addParam(each_servo, GoalPosition_3[count])
                        groupSyncRead_Moving_3.addParam(servo_obj.ID)
            # Write Speeds
            if ports_used[0] == 1:
                groupSyncWriteVEL_1.txPacket()
                groupSyncWriteVEL_1.clearParam()
            if ports_used[1] == 1:
                groupSyncWriteVEL_2.txPacket()
                groupSyncWriteVEL_2.clearParam()
            if ports_used[2] == 1:
                groupSyncWriteVEL_3.txPacket()
                groupSyncWriteVEL_3.clearParam()
            # Write Positions
            if ports_used[0] == 1:
                groupSyncWritePOS_1.txPacket()
                groupSyncWritePOS_1.clearParam()
            if ports_used[1] == 1:
                groupSyncWritePOS_2.txPacket()
                groupSyncWritePOS_2.clearParam()
            if ports_used[2] == 1:
                groupSyncWritePOS_3.txPacket()
                groupSyncWritePOS_3.clearParam()

            while 1:
                moving_YesNo = []
                if ports_used[0] == 1:
                    # Syncread Moving Value
                    dxl_comm_result = groupSyncRead_Moving_1.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                    for each_limb in limb_list:
                        if each_limb in LEG_LIMB_IDS_FRONT:
                            for each_servo in LimbDictionary[each_limb].ServoDict.values():
                                # Get Dynamixel present Moving value
                                dxl_mov = groupSyncRead_Moving_1.getData(each_servo.ID, AddrDict[39],1)
                                moving_YesNo.append(dxl_mov)
                        else:
                            continue
                if ports_used[1] == 1:
                    # Syncread Moving Value
                    dxl_comm_result = groupSyncRead_Moving_2.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                    for each_limb in limb_list:
                        if each_limb in LEG_LIMB_IDS_BACK:
                            for each_servo in LimbDictionary[each_limb].ServoDict.values():
                                # Get Dynamixel present Moving value
                                dxl_mov = groupSyncRead_Moving_2.getData(each_servo.ID, AddrDict[39],1)
                                moving_YesNo.append(dxl_mov)
                        else:
                            continue
                if ports_used[2] == 1:
                    # Syncread Moving Value
                    dxl_comm_result = groupSyncRead_Moving_3.txRxPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                    for each_limb in limb_list:
                        if each_limb in BODY_LENGTH_LIMB_IDS:
                            for each_servo in LimbDictionary[each_limb].ServoDict.values():
                                # Get Dynamixel present Moving value
                                dxl_mov = groupSyncRead_Moving_3.getData(each_servo.ID, AddrDict[39],1)
                                moving_YesNo.append(dxl_mov)
                        else:
                            continue
                if 1 in moving_YesNo:
                    pass
                else:
                    if ports_used[0] == 1:
                        groupSyncRead_Moving_1.clearParam()
                    if ports_used[1] == 1:
                        groupSyncRead_Moving_2.clearParam()
                    if ports_used[2] == 1:
                       groupSyncRead_Moving_3.clearParam()
                    if record_array[0] == True:
                        if readers_exist == False:
                            if ports_used[0] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[42],2)
                                    port_1_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[47],2)
                                    port_1_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_1 = GroupSyncRead(port_hand_list[0],packet_handler,AddrDict[48],1)
                                    port_1_Temperature = []
                                    readers_exist = True
                            if ports_used[1] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[42],2)
                                    port_2_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[47],2)
                                    port_2_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_2 = GroupSyncRead(port_hand_list[1],packet_handler,AddrDict[48],1)
                                    port_2_Temperature = []
                                    readers_exist = True
                            if ports_used[2] == 1:
                                if record_array[6] == True:
                                    # Create Current Reader
                                    groupSyncRead_Current_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[42],2)
                                    port_3_Current = []
                                    readers_exist = True
                                if record_array[7] == True:
                                    # Create Voltage Reader
                                    groupSyncRead_Voltage_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[47],2)
                                    port_3_Voltage = []
                                    readers_exist = True
                                if record_array[8] == True:
                                    # Create Temperature Reader
                                    groupSyncRead_Temperature_3 = GroupSyncRead(port_hand_list[2],packet_handler,AddrDict[48],1)
                                    port_3_Temperature = []
                                    readers_exist = True
                        if readers_exist == True:
                            for each_limb in LimbDictionary.values():
                                for each_servo in each_limb.ServoDict.keys():
                                    if record_array[6] == True:
                                        if ports_used[0] == 1:
                                            groupSyncRead_Current_1.addParam(each_servo)
                                        if ports_used[1] == 1:
                                            groupSyncRead_Current_2.addParam(each_servo)
                                        if ports_used[2] == 1:
                                            groupSyncRead_Current_3.addParam(each_servo)
                                    if record_array[7] == True:
                                        if ports_used[0] == 1:
                                            groupSyncRead_Voltage_1.addParam(each_servo)
                                        if ports_used[1] == 1:
                                            groupSyncRead_Voltage_2.addParam(each_servo)
                                        if ports_used[2] == 1:
                                            groupSyncRead_Voltage_3.addParam(each_servo)
                                    if record_array[8] == True:
                                        if ports_used[0] == 1:
                                            groupSyncRead_Temperature_1.addParam(each_servo)
                                        if ports_used[1] == 1:
                                            groupSyncRead_Temperature_2.addParam(each_servo)
                                        if ports_used[2] == 1:
                                            groupSyncRead_Temperature_3.addParam(each_servo)
                        if readers_exist == True:
                            if record_array[6] == True:
                                if ports_used[0] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_1.isAvailable(each_front_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_front_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_1_Current.append(groupSyncRead_Current_1.getData(each_front_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_2.isAvailable(each_back_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_back_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_2_Current.append(groupSyncRead_Current_2.getData(each_back_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present current
                                    dxl_comm_result = groupSyncRead_Current_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Current_3.isAvailable(each_servo, AddrDict[42], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present current value
                                            port_3_Current.append(groupSyncRead_Current_3.getData(each_servo, AddrDict[42], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_3.clearParam()
                            if record_array[7] == True:
                                if ports_used[0] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_1.isAvailable(each_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_1_Voltage.append(groupSyncRead_Voltage_1.getData(each_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Current_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_2.isAvailable(each_back_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_back_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_2_Voltage.append(groupSyncRead_Voltage_2.getData(each_back_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Voltage_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present voltage
                                    dxl_comm_result = groupSyncRead_Voltage_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Voltage_3.isAvailable(each_servo, AddrDict[47], 2)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present voltage value
                                            port_3_Voltage.append(groupSyncRead_Voltage_3.getData(each_servo, AddrDict[47], 2))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Voltage_3.clearParam()
                            if record_array[8] == True:
                                if ports_used[0] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_1.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_front_servo in FRONT_ARMS:
                                        if each_front_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_1.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_1_Temperature.append(groupSyncRead_Temperature_1.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_1.clearParam()
                                if ports_used[1] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_2.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_back_servo in BACK_ARMS:
                                        if each_back_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_2.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_2_Temperature.append(groupSyncRead_Temperature_2.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_2.clearParam()
                                if ports_used[2] == 1:
                                    # Syncread present temperature
                                    dxl_comm_result = groupSyncRead_Temperature_3.txRxPacket()
                                    if dxl_comm_result != COMM_SUCCESS:
                                        print("%s" % packet_handler.getTxRxResult(dxl_comm_result))
                                    for each_bodyln_servo in BODY_LENGTH:
                                        if each_bodyln_servo in servo_list:
                                            # Check if groupsyncread data of Dynamixel is available
                                            dxl_getdata_result = groupSyncRead_Temperature_3.isAvailable(each_servo, AddrDict[48], 1)
                                            if dxl_getdata_result != True:
                                                print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                quit()
                                            # Get Dynamixel present temperature value
                                            port_3_Temperature.append(groupSyncRead_Temperature_3.getData(each_servo, AddrDict[48], 1))
                                    # Clear syncread parameter storage
                                    groupSyncRead_Temperature_3.clearParam()
                        if readers_exist == True:
                            for list_index,each_servo in enumerate(servo_list):
                                servo_data_array = [each_servo]
                                if record_array[1] == True:
                                    pos_out = ServosDictionary[each_servo].Positions[position_index]
                                    servo_data_array.append(pos_out)
                                    # Record Position / self.Positions[stride_count]
                                if record_array[2] == True:
                                    vel_out = ServosDictionary[each_servo].Speeds[stride_count]
                                    servo_data_array.append(vel_out)
                                    # Record Speed / self.Speeds[stride_count]
                                if record_array[3] == True:
                                    record_time = time.time()
                                    end_time = record_time - start_time
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
                                    if each_servo in FRONT_ARMS:
                                        dxl_current = port_1_Current[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_current = port_2_Current[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_current = port_3_Current[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_current)
                                if record_array[7] == True:
                                    if each_servo in FRONT_ARMS:
                                        dxl_voltage = port_1_Voltage[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_voltage = port_2_Voltage[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_voltage = port_3_Voltage[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_voltage)
                                if record_array[8] == True:
                                    if each_servo in FRONT_ARMS:
                                        dxl_temp = port_1_Temperature[list_index]
                                    elif each_servo in BACK_ARMS:
                                        dxl_temp = port_2_Temperature[list_index-(front_servo_count)]
                                    elif each_servo in BODY_LENGTH:
                                        dxl_temp = port_3_Temperature[list_index-(front_servo_count+back_servo_count)]
                                    servo_data_array.append(dxl_temp)
                                out_data.append(servo_data_array)
                    if record_array[6] == True:
                        if ports_used[0] == 1:
                            port_1_Current = []
                        if ports_used[1] == 1:
                            port_2_Current = []
                        if ports_used[2] == 1:
                            port_3_Current = []
                    if record_array[7] == True:
                        if ports_used[0] == 1:
                            port_1_Voltage = []
                        if ports_used[1] == 1:
                            port_2_Voltage = []
                        if ports_used[2] == 1:
                            port_3_Voltage = []
                    if record_array[8] == True:
                        if ports_used[0] == 1:
                            port_1_Temperature = []
                        if ports_used[1] == 1:
                            port_2_Temperature = []
                        if ports_used[2] == 1:
                            port_3_Temperature = []
                    break            

    return out_data

def Write_Doc(record_array, out_data):
    if record_array[0] == True:
        with open(record_array[-1], 'w', newline='') as csvfile:
            DocWriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)    
            header_line = []
            if record_array[1] == True:
                header_line.append("Position")
            if record_array[2] == True:
                header_line.append("Speed")
            if record_array[3] == True:
                header_line.append("Time")
            if record_array[4] == True:
                header_line.append("Position Index")
            if record_array[5] == True:
                header_line.append("Stride Count")
            if record_array[6] == True:
                header_line.append("Current")
            if record_array[7] == True:
                header_line.append("Voltage")
            if record_array[8] == True:
                header_line.append("Temperature")
            DocWriter.writerow(header_line)
            for each_line in out_data:
                DocWriter.writerow(each_line)
        print("Data Finished Recording.")
    else:
        print("Data Not Recorded.")
    return

def CleanUp(Obj_list,port_hand_list,packetHandler):
    for each_servo in Obj_list[0].values():
        if (each_servo.ID >=1) and (each_servo.ID<=8):
            each_servo.ToggleTorque(0,port_hand_list[0],packetHandler)
        elif (each_servo.ID >=9) and (each_servo.ID <= 16):
            each_servo.ToggleTorque(0,port_hand_list[1],packetHandler)
        elif (each_servo.ID >= 17) and (each_servo.ID <= 24):
            each_servo.ToggleTorque(0,port_hand_list[2],packetHandler)
    if len(Obj_list) == 3:
        Obj_list[2].__del__()
        for each_limb in Obj_list[1].values():
            each_limb.__del__()
        for each_servo in Obj_list[0].values():
            each_servo.__del__()
    elif len(Obj_list) == 2:
        for each_limb in Obj_list[1].values():
            each_limb.__del__()
        for each_servo in Obj_list[0].values():
            each_servo.__del__()
    elif len(Obj_list) == 1:
        for each_servo in Obj_list[0].values():
            each_servo.__del__()
    for each_port_obj in port_hand_list:
        if each_port_obj != 0:
            each_port_obj.closePort()
    
def ShutDown():
    print("Shutting down system.\n")
    # Turn off power to external boards and other systems
    print("Thank you for using Tilibot!")

