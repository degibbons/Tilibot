## Tilibot Functions

from Tilibot_Constants import *
from Tilibot_Classes import Servo, Leg, Neck, Spine, Tail, Body
import os
import yaml
from dynamixel_sdk import *
from Tilibot_Universal_Functions import *
import numpy as np
import pandas as pd
import copy as cp
import time
import sys
import csv
import math

if os.name == 'nt': # nt for windows, posix for mac and linux, Defines getch for user control, makes hitting enter to continue possible
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
    with open(Config_Yaml_File, "r") as stream: # Open configuration file in read mode
        config_data = yaml.safe_load(stream)
        baudrate = config_data['Baud-Rate']                             #0       Read Baud Rate
        positions_file = config_data['Position-Angle-File']             #1       Read in the name of the Position Angle File
        position_amount = config_data['Positions-Per-Stride']           #2       Read the amount of positions present in one whole stride
        stride_time = config_data["Stride-Time"]                        #3       Read the amount of time 1 stride should take
        stride_amount = config_data['Stride-Amount']                    #4       Read the amount of desired strides one run should make
        connected_servos = config_data['Servos-Connected']              #5       Read in as a list which servos are connected
        connected_limbs = config_data['Limbs-Connected']                #6       Read in as a list which limbs are connected
        connected_sensors = config_data['Body-Sensors-Connected']       #7       Read in if the body sensors are connected or not
        forelimb_stance_time = config_data['Forelimb-Stance']           #8       Read in the time duration for stance in the forelimbs
        forelimb_swing_time = config_data['Forelimb-Swing']             #9       Read in the time duration for swing in the forelimbs
        hindlimb_stance_time = config_data['Hindlimb-Stance']           #10      Read in the time duration for stance in the hindlimbs
        hindlimb_swing_time = config_data['Hindlimb-Swing']             #11      Read in the time duration for swing in the forelimbs
        stance_swing_ratio_time = config_data['Ratio-Time']             #12      Read in the time duration relative to the previous durations for a single stride
        move_one_servo_act = config_data['Move-Single-Servo']           #13      Read in if one servo should be moved or not
        single_servo_to_move = config_data['Single-Servo-To-Move']      #14      Read in which servo should be moved if one is to be moved
        move_multi_servo_act = config_data['Move-Multiple-Servos']      #15      Read in if multiple servos should be moved or not
        servos_to_move = config_data['Servos-To-Move']                  #16      Read in which servos are to be moved if multiple are to be moved
        home_speed = config_data['Home-Speed']                          #17      Read in home speed
        out_file_name = config_data['Output-File-Name']                 #18      Read in what the output file name should be if output is desired
        out_file_dir = config_data['Output-File-Directory']             #19      Read in what the output file directory location should be
        position_write = config_data['Position']                        #20      Read in if you want "position" to be recorded
        speed_write = config_data['Speed']                              #21      Read in if you want "speed" to be recorded
        time_write = config_data['Time']                                #22      Read in if you want "time" to be recorded
        posindex_write = config_data['Position-Index']                  #23      Read in if you want "position index" to be recorded
        stridecount_write = config_data['Stride-Count']                 #24      Read in if you want "stride count" to be recorded
        current_write = config_data['Current']                          #25      Read in if you want "current" to be recorded
        voltage_write = config_data['Voltage']                          #26      Read in if you want "voltage" to be recorded
        temp_write = config_data['Temperature']                         #27      Read in if you want "temperature" to be recorded
        neck_straight = config_data['Neck-Straight']                    #28      Read in if you want to keep the neck straight or move according to instructions
        spine_straight = config_data['Spine-Straight']                  #29      Read in if you want to keep the spine straight or move according to instructions
        tail_straight = config_data['Tail-Straight']                    #30      Read in if you want to keep the tail straight or move according to instructions
        silence_ext_ouput = config_data['Silence-Extraneous-Output']    #31      Read in if you want to silence extraneous outputs
        run_digital_only = config_data['Run-Digital-Only']              #32      Read in if you want to run this program digitally without a physical body

    config_array = [baudrate, positions_file, position_amount, stride_time, stride_amount,                      # Assemble output array of all field options for return
    connected_servos, connected_limbs, connected_sensors, forelimb_stance_time, forelimb_swing_time, hindlimb_stance_time,
    hindlimb_swing_time, stance_swing_ratio_time, move_one_servo_act, single_servo_to_move, move_multi_servo_act, 
    servos_to_move, home_speed, out_file_name, out_file_dir, position_write, speed_write, time_write, 
    posindex_write, stridecount_write, current_write, voltage_write, temp_write, neck_straight, spine_straight,
    tail_straight, silence_ext_ouput, run_digital_only]

    return config_array

def check_config_file(config_array,GUI_or_TERMINAL):
    print("Confirming configuration file is properly written...")
    invalidate_value = False
    # Check that Configuration File is filled out correctly
    # That only one action is picked, its corresponding array is filled
    # and every field in the file is filled out correctly
    servo_count = len(config_array[5]) # Get the amount of servos from the length of the array of connected servos
    limb_count = len(config_array[6]) # Get the amount of limbs connected from the length of the array of connected limbs
    servo_all_bool = True # Indicator that all servos in list are booleans and no other type of variable
    limb_all_bool = True # Indicator that all limbs in list are booleans and no other variable type
    for x in config_array[5]: # Check if all servos have booleans assigned as their values
        if not isinstance(x,bool):
            servo_all_bool = False # Change the value of the check variable if this is not the case
    for y in config_array[6]: # Check if all limbs have booleans assigned as their values
        if not isinstance(y,bool):
            limb_all_bool = False # Change the value of the check variable if this is not the case
    move_servo_number = len(config_array[16]) # Get the amount of servos intended to move from 
    servos_proper_ints = True # Indicator that all moving servos are integers and no other variable type
    if move_servo_number > 0: # If the amount of moving servos is greater than 0
        for b in config_array[16]:
            if (not isinstance(b, int)) or (b <= 0): # If the value is not an integer or it's not greater than 0
                servos_proper_ints = False # Change the value of the check variable if this is not the case
    valid_home_speed = True # Indicator if the home speed value is an integer and within the valid range
    if (not isinstance(config_array[17],int)): # If the value is not an int
        valid_home_speed = False # Change the value of the check variable if this is not the case
    elif (config_array[17] > 1023) or (config_array[17] < 0): # Check if the value of the variable is within the Dynamixel-established Speed Range
        valid_home_speed = False # Change the value of the check variable if this is not the case
    
    if (not isinstance(config_array[0],int)) or (config_array[0] <= 0): # Check if baud rate is integer and less than or equal to 0
        print("Baud-Rate input is incorrect format. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[1],str)) or (not os.path.isfile(config_array[1])): # Check if Position Angle File is string and proper file
        print("Position-Angle-File is not a valid String or is not a valid file. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[2],int)) or (config_array[2] <= 0): # Check if Positions per Stride is integer and less than or equal to 0
        print("Positions-Per-Stride is not a valid Integer number, or not the correct format. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[3],float)) or (config_array[3] <= 0): # Check if Stride Time is float and less than or equal to 0
        print("Stride-Time is not a valid Float number, or not the correct format. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[4],int)) or (config_array[0] <= 0): # Check if Stride Amount is integer and less than or equal to 0
        print("Stride-Amount is not a valid Integer number, or not the correct format.. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[5],list)) or (servo_count != 24) or (servo_all_bool == False): # Check if Servos Connected is proper list, not 24 in length, or any of the servos is not a boolean
        print("Servos-Connected is not a correct list, not 24 in length, or one of the elements is not a Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[6],list)) or (limb_count != 7) or (limb_all_bool == False): # Check if Limbs Connected is proper list, not 7 in length, or any of the limbs is not a boolean
        print("Limbs-Connected . Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[7],bool)): # Check if External Sensors Connected is boolean
        print("Body-Sensors-Connected is not a Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[8],float)): # Check if Move Body is boolean
        print("Forelimb-Stance is not a valid Float. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[9],float)): # Check if Move Single Limb is boolean
        print("Forelimb-Swing is not a valid Float. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[10],float)) or (config_array[10] < 0): # Check if Single Limb to Move is integer and not less than 0
        print("Hindlimb-Stance is not a valid Float. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[11],float)): # Check if Move Multiple Limbs is boolean
        print("Hindlimb-Swing is not a valid Float. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[12],float)): # Check if Ratio Time is proper float
        print("Ratio-Time is not a valid Float. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[13],bool)) : # Check if Move Single Servo is boolean
        print("Move-Single-Servo is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[14],int)) or (config_array[14] < 0): # Check if Single Servo to Move is integer and not less than 0
        print("Single-Servo-To-Move is not a valid Integer. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[15],bool)): # Check if Move Multiple Servos is proper booelans
        print("Move-Multiple-Servos is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[16],list)) or (servos_proper_ints == False): # Check if servos to move is proper list and all servos are integers
        print("Servos-To-Move is not a valid list or not all elements in it are Integers. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[17],int)) or (valid_home_speed == False): # Check if Home Speed is integer and between 0 and 1023
        print("Home-Speed is not a valid Integer between 0-1023. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[18],str)): # Check if Output File Name is valid string
        print("Output-File-Name is not a valid String value. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[19],str)) or (not os.path.isdir(config_array[19])): # Check if Output File Directoy is valid string and proper directory
        print("Output-File-Directory is not a valid String or not a valid Directory. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[20],bool)): # Check if Position Record is proper boolean 
        print("Position is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[21],bool)): # Check if Speed Record is proper boolean
        print("Speed is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[22],bool)): # Check if Time Record is proper boolean
        print("Time is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[23],bool)): # Check Position Index Record is proper boolean
        print("Position-Index is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[24],bool)): # Check if Stride Count Record is proper boolean
        print("Stride-Count is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[25],bool)): # Check if Current Record is proper boolean
        print("Current is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[26],bool)): # Check if Voltage Record is proper boolean
        print("Voltage is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[27],bool)): # Check if Temperature Record is proper boolean
        print("Temperature is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[28],bool)): # Check if Neck Straight is proper boolean
        print("Neck-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[29],bool)): # Check if Spine Straight is proper boolean
        print("Spine-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[30],bool)): # Check if Tail Straight is proper boolean
        print("Tail-Straight is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[31],bool)): # Check if Silence Extraneous Output is proper boolean
        print("Silence-Extraneous-Output is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    elif (not isinstance(config_array[32],bool)): # Check if Run Digital Only is proper boolean
        print("Run-Digital-Only is not a valid Boolean. Please fix and try again.")
        invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    if GUI_or_TERMINAL == -1: # If being used through the GUI, do not check if servos have already been established, the GUI will do this for you after detecting
        pass
    elif GUI_or_TERMINAL == 1:
        if not any(config_array[5]): # If using the terminal, moving servos should already be established in the file
            print("No Servos are marked as connected. Please fix and try again.")
            invalidate_value = True # If this is not the case, change the indicator value to reflect there is a problem
    confirmed_action = [0, 0] # Create a list for actions to populate
    action_currently_selected = False # Change when an action is selected
    action_array = [config_array[13], config_array[14], config_array[15], config_array[16]] # Assemble an action array detailing if a single or multiple servos are to move, and which servos will perform that
    if action_array[0] == True: # If one servo is to move
        confirmed_action = [1, action_array[1]]
        if action_currently_selected == True: # If an action was already selected, there is more than one acion present, and this is a problem
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True # If this is the case, change the indicator value to reflect there is a problem
        action_currently_selected = True
    if action_array[2] == True: # If multiple servos are to move
        confirmed_action = [2, action_array[3]]
        if action_currently_selected == True: # If an action was already selected, there is more than one acion present, and this is a problem
            print("More than one action selected. Please fix and try again.")
            invalidate_value = True # If this is the case, change the indicator value to reflect there is a problem
        action_currently_selected = True
    if (action_currently_selected == False): # If there's no action selected
        print("No action selected. Please fix and try again.")
        invalidate_value = True # If this is the case, change the indicator value to reflect there is a problem
    return invalidate_value, confirmed_action

def RecordPreferences(config_array): # Check if any of the record fields are set to True for recording purposes
    record_fields = [config_array[20], config_array[21], config_array[22], config_array[23], config_array[24],
                    config_array[25], config_array[26], config_array[27]]
    record_yesno = None
    if any(record_fields):
        record_yesno = True
    else:
        record_yesno = False
    record_fields.insert(0,record_yesno)
    if record_yesno == True:
        new_path = os.path.join(config_array[19],config_array[18])
        outfile_whole = os.path.normpath(new_path)
        record_fields.append(outfile_whole)
    return record_fields

def DigitalSetup(config_array):
    print("Digital Setup Selected. Setting up digital Tilibot without physical connected apparatus.")
    print("Extraneous Output is set to {s}".format(config_array[31]))
    return

def ErrorChecker(ErrorIn): 
    byteError = ErrorIn
    InputVoltageError = False
    InputVoltageError_msg = "Input Voltage exceeds the configured operating voltage"
    OverheatingError = False
    OverheatingError_msg = "Internal temperature exceeds the configured operating temperature"
    MotorEncoderError = False
    MotorEncoderError_msg = "Malfunction of the motor encoder detected"
    ElectricalShockError = False
    ElectricalShockError_msg = "Electrical shock on the circuit or insufficient power to operate the motor"
    OverloadError = False
    OverloadError_msg = "Persistent load detected that exceeds the maximum output"
    Error_Message_print = ""
    if byteError in [1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61]:
        InputVoltageError = True
    if byteError in [4,5,12,13,20,21,28,29,36,37,44,45,52,53,60,61]:
        OverheatingError = True
    if byteError in [8,9,12,13,24,25,28,29,40,41,44,45,56,57,60,61]:
        MoterEncoderError = True
    if byteError in [16,17,20,21,24,25,28,29,48,49,52,53,56,57,60,61]:
        ElectricalShockError = True
    if byteError in [32,33,36,37,40,41,44,45,48,49,52,53,56,57,60,61]:
        OverloadError = True
    errorArray = [InputVoltageError, OverheatingError, MotorEncoderError, ElectricalShockError, OverloadError]
    if True in errorArray:
        if InputVoltageError == True:
            if Error_Message_print == "":
                Error_Message_print = Error_Message_print + InputVoltageError_msg
            else:
                Error_Message_print = Error_Message_print + "\n" + InputVoltageError_msg
        if OverheatingError == True:
            if Error_Message_print == "":
                Error_Message_print = Error_Message_print + OverheatingError_msg
            else:
                Error_Message_print = Error_Message_print + "\n" + OverheatingError_msg
        if MotorEncoderError == True:
            if Error_Message_print == "":
                Error_Message_print = Error_Message_print + MotorEncoderError_msg
            else:
                Error_Message_print = Error_Message_print + "\n" + MotorEncoderError_msg
        if ElectricalShockError == True:
            if Error_Message_print == "":
                Error_Message_print = Error_Message_print + ElectricalShockError_msg
            else:
                Error_Message_print = Error_Message_print + "\n" + ElectricalShockError_msg
        if OverloadError == True:
            if Error_Message_print == "":
                Error_Message_print = Error_Message_print + OverloadError_msg
            else:
                Error_Message_print = Error_Message_print + "\n" + OverloadError_msg
    return Error_Message_print

def RotatePositionArray(inArray,shiftNum,arrayLength):
    for i in range(math.gcd(arrayLength,shiftNum)):  # Use the juggling algorithm to rotate the position array, using the greatest common divisor
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

def ReadServoAngles(positionsFile):
    old_df = pd.read_csv(positionsFile) # Read in Positions File as dataframe
    old_df = old_df.values[:][:] # Change dataframe into matrix

    FL_ST_R_1 = old_df[:,0] # Break up matrix into single arrays
    FL_ST_R_2 = old_df[:,1]
    FL_ST_R_3 = old_df[:,2]
    FL_ST_R_4 = old_df[:,3]

    FL_SW_R_1 = old_df[:,4] # Break up matrix into single arrays
    FL_SW_R_2 = old_df[:,5]
    FL_SW_R_3 = old_df[:,6]
    FL_SW_R_4 = old_df[:,7]

    FL_TOT_R_1 = np.concatenate((FL_ST_R_1, FL_SW_R_1),axis=0) # Attach Swing phase to end of Stance phase as single array
    FL_TOT_R_2 = np.concatenate((FL_ST_R_2, FL_SW_R_2),axis=0)
    FL_TOT_R_3 = np.concatenate((FL_ST_R_3, FL_SW_R_3),axis=0)
    FL_TOT_R_4 = np.concatenate((FL_ST_R_4, FL_SW_R_4),axis=0)

    FL_ST_L_1 = old_df[:,0] # Break up matrix into single arrays
    FL_ST_L_2 = old_df[:,1]
    FL_ST_L_3 = old_df[:,2]
    FL_ST_L_4 = old_df[:,3]

    FL_SW_L_1 = old_df[:,4] # Break up matrix into single arrays
    FL_SW_L_2 = old_df[:,5]
    FL_SW_L_3 = old_df[:,6]
    FL_SW_L_4 = old_df[:,7]

    FL_TOT_L_1 = np.concatenate((FL_ST_L_1, FL_SW_L_1),axis=0) # Attach Swing phase to end of Stance phase as single array
    FL_TOT_L_2 = np.concatenate((FL_ST_L_2, FL_SW_L_2),axis=0)
    FL_TOT_L_3 = np.concatenate((FL_ST_L_3, FL_SW_L_3),axis=0)
    FL_TOT_L_4 = np.concatenate((FL_ST_L_4, FL_SW_L_4),axis=0)

    HL_ST_R_1 = old_df[:,8] # Break up matrix into single arrays
    HL_ST_R_2 = old_df[:,9]
    HL_ST_R_3 = old_df[:,10]
    HL_ST_R_4 = old_df[:,11]

    HL_SW_R_1 = old_df[:,12] # Break up matrix into single arrays
    HL_SW_R_2 = old_df[:,13]
    HL_SW_R_3 = old_df[:,14]
    HL_SW_R_4 = old_df[:,15]

    HL_TOT_R_1 = np.concatenate((HL_ST_R_1, HL_SW_R_1),axis=0) # Attach Swing phase to end of Stance phase as single array
    HL_TOT_R_2 = np.concatenate((HL_ST_R_2, HL_SW_R_2),axis=0)
    HL_TOT_R_3 = np.concatenate((HL_ST_R_3, HL_SW_R_3),axis=0)
    HL_TOT_R_4 = np.concatenate((HL_ST_R_4, HL_SW_R_4),axis=0)

    HL_ST_L_1 = old_df[:,8] # Break up matrix into single arrays
    HL_ST_L_2 = old_df[:,9]
    HL_ST_L_3 = old_df[:,10]
    HL_ST_L_4 = old_df[:,11]

    HL_SW_L_1 = old_df[:,12] # Break up matrix into single arrays
    HL_SW_L_2 = old_df[:,13]
    HL_SW_L_3 = old_df[:,14]
    HL_SW_L_4 = old_df[:,15]

    HL_TOT_L_1 = np.concatenate((HL_ST_L_1, HL_SW_L_1),axis=0) # Attach Swing phase to end of Stance phase as single array
    HL_TOT_L_2 = np.concatenate((HL_ST_L_2, HL_SW_L_2),axis=0)
    HL_TOT_L_3 = np.concatenate((HL_ST_L_3, HL_SW_L_3),axis=0)
    HL_TOT_L_4 = np.concatenate((HL_ST_L_4, HL_SW_L_4),axis=0)

    dyn_con = 4096/360

    index = 0
    for i in FL_TOT_R_1:    # Right Forelimb Servo #1
        FL_TOT_R_1[index] = 2048 - (i * dyn_con)
        index += 1
    FL_TOT_R_1 = FL_TOT_R_1.round()
    FL_TOT_R_1 = list(map(int,FL_TOT_R_1))
    index = 0
    for i in FL_TOT_R_2:    # Right Forelimb Servo #2
        FL_TOT_R_2[index] = 2048 + (i * dyn_con)
        index += 1
    FL_TOT_R_2 = FL_TOT_R_2.round()
    FL_TOT_R_2 = list(map(int,FL_TOT_R_2))
    index = 0
    for i in FL_TOT_R_3:    # Right Forelimb Servo #3
        FL_TOT_R_3[index] = 2048 + (i * dyn_con)
        index += 1
    FL_TOT_R_3 = FL_TOT_R_3.round()
    FL_TOT_R_3 = list(map(int,FL_TOT_R_3))
    index = 0
    for i in FL_TOT_R_4:    # Right Forelimb Servo #4
        FL_TOT_R_4[index] = 2048 + (i * dyn_con)
        index += 1
    FL_TOT_R_4 = FL_TOT_R_4.round()
    FL_TOT_R_4 = list(map(int,FL_TOT_R_4))
    index = 0
    for i in FL_TOT_L_1:    # Left Forelimb Servo #5
        FL_TOT_L_1[index] = 2048 + ( i * dyn_con)
        index += 1
    FL_TOT_L_1 = FL_TOT_L_1.round()
    FL_TOT_L_1 = list(map(int,FL_TOT_L_1))
    index = 0
    for i in FL_TOT_L_2:    # Left Forelimb Servo #6
        FL_TOT_L_2[index] = 2048 + (i * dyn_con)
        index += 1
    FL_TOT_L_2 = FL_TOT_L_2.round()
    FL_TOT_L_2 = list(map(int,FL_TOT_L_2))
    index = 0
    for i in FL_TOT_L_3:    # Left Forelimb Servo #7
        FL_TOT_L_3[index] = 2048 - (i * dyn_con)
        index += 1
    FL_TOT_L_3 = FL_TOT_L_3.round()
    FL_TOT_L_3 = list(map(int,FL_TOT_L_3))
    index = 0
    for i in FL_TOT_L_4:    # Left Forelimb Servo #8
        FL_TOT_L_4[index] = 2048 + (i * dyn_con)
        index += 1
    FL_TOT_L_4 = FL_TOT_L_4.round()
    FL_TOT_L_4 = list(map(int,FL_TOT_L_4))
    index = 0
    for i in HL_TOT_R_1:    # Right Hindlimb Servo #9
        HL_TOT_R_1[index] = 2048 - (i * dyn_con)
        index += 1
    HL_TOT_R_1 = HL_TOT_R_1.round()
    HL_TOT_R_1 = list(map(int,HL_TOT_R_1))
    index = 0
    for i in HL_TOT_R_2:    # Right Hindlimb Servo #10
        HL_TOT_R_2[index] = 2048 + (i * dyn_con)
        index += 1
    HL_TOT_R_2 = HL_TOT_R_2.round()
    HL_TOT_R_2 = list(map(int,HL_TOT_R_2))
    index = 0
    for i in HL_TOT_R_3:    # Right Hindlimb Servo #11
        HL_TOT_R_3[index] = 2048 + (i * dyn_con)
        index += 1
    HL_TOT_R_3 = HL_TOT_R_3.round()
    HL_TOT_R_3 = list(map(int,HL_TOT_R_3))
    index = 0
    for i in HL_TOT_R_4:    # Right Hindlimb Servo #12
        HL_TOT_R_4[index] = 2048 + (i * dyn_con)
        index += 1
    HL_TOT_R_4 = HL_TOT_R_4.round()
    HL_TOT_R_4 = list(map(int,HL_TOT_R_4))
    index = 0
    for i in HL_TOT_L_1:    # Left Hindlimb Servo #13
        HL_TOT_L_1[index] = 2048 + (i * dyn_con)
        index += 1
    HL_TOT_L_1 = HL_TOT_L_1.round()
    HL_TOT_L_1 = list(map(int,HL_TOT_L_1))
    index = 0
    for i in HL_TOT_L_2:    # Left Hindlimb Servo #14
        HL_TOT_L_2[index] = 2048 + (i * dyn_con)
        index += 1
    HL_TOT_L_2 = HL_TOT_L_2.round()
    HL_TOT_L_2 = list(map(int,HL_TOT_L_2))
    index = 0
    for i in HL_TOT_L_3:    # Left Hindlimb Servo #15
        HL_TOT_L_3[index] = 2048 - (i * dyn_con)
        index += 1
    HL_TOT_L_3 = HL_TOT_L_3.round()
    HL_TOT_L_3 = list(map(int,HL_TOT_L_3))
    index = 0
    for i in HL_TOT_L_4:    # Left Hindlimb Servo #16
        HL_TOT_L_4[index] = 2048 + (i * dyn_con)
        index += 1
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
    ServoPos8 = RotatePositionArray(inPositions[7],9,len(inPositions[7]))

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

def DetermineSpeeds(tspan,PositionsMatrix,points_per_stride,config_array):
    #Make a copy of the dataframe with the same dimensions for the speeds
    speeds = cp.copy(PositionsMatrix)
    h_stance = config_array[10]
    h_swing = config_array[11]
    f_stance = config_array[8]
    f_swing = config_array[9]
    print("determine speeds - " + str(config_array[12]))
    h_st_per = h_stance / config_array[12]
    h_sw_per = h_swing / config_array[12]
    f_st_per = f_stance / config_array[12]
    f_sw_per = f_swing / config_array[12]
    #Starting % index of stride for each limb
    L_hl = 0 # Left Hindlimb
    L_fl = 9 # Left Forelimb 90% Approximately
    R_hl = 8 # Right Hindlimb 80% Approximately
    R_fl = 1 # Right Forelimb 10% Approximately
    #Points per Phase
    pointsPerPhase = points_per_stride/2
    speeds = np.array(speeds)
    b = speeds.shape
    phase_length = int(b[1]/2)
    cLength = int(b[1])
    cWidth = int(b[0])
    MoveIndex = np.linspace(1,int(cLength),int(cLength))
    servos = list(range(1,cWidth+1))
    MoveIndex = MoveIndex.astype(int).tolist()
    newSpeeds = []
    #t1 = np.zeros(b[1])
    for i in np.linspace(1,cWidth,cWidth):
        newSpeeds.append(np.zeros(cLength))
    for each_servo in servos:
        for stride_index in MoveIndex: #0.114 rpm given by https://emanual.robotis.com/docs/en/dxl/mx/mx-64/
            if (each_servo == 1 or each_servo == 2 or each_servo == 3 or each_servo == 4 ):
                if (stride_index==cLength):
                    rotations = abs(speeds[each_servo-1][0]-speeds[each_servo-1][stride_index-1])/4096
                else:
                    rotations = abs(speeds[each_servo-1][stride_index]-speeds[each_servo-1][stride_index-1])/4096
                if ((stride_index-1) >= (pointsPerPhase - R_fl) and (stride_index-1)<=(pointsPerPhase - R_fl + 10)):
                    movementTime = (tspan*f_sw_per/phase_length)/60
                else:
                    movementTime = (tspan*f_st_per/phase_length)/60
                movementSpeed = (rotations / movementTime) / DYNAMIXEL_SPEED_CONSTANT
                newSpeeds[each_servo-1][stride_index-1] = round(movementSpeed)
            elif (each_servo == 5 or each_servo == 6 or each_servo == 7 or each_servo == 8): 
                if (stride_index==cLength):
                    rotations = abs(speeds[each_servo-1][0]-speeds[each_servo-1][stride_index-1])/4096
                else:
                    rotations = abs(speeds[each_servo-1][stride_index]-speeds[each_servo-1][stride_index-1])/4096
                if ((stride_index-1) >= (pointsPerPhase - L_fl) and (stride_index-1)<=(pointsPerPhase - L_fl + 10)):
                    movementTime = (tspan*f_sw_per/phase_length)/60
                else:
                    movementTime = (tspan*f_st_per/phase_length)/60
                movementSpeed = (rotations / movementTime) / DYNAMIXEL_SPEED_CONSTANT
                newSpeeds[each_servo-1][stride_index-1] = round(movementSpeed)
            elif (each_servo == 9 or each_servo == 10 or each_servo == 11 or each_servo == 12 ):
                if (stride_index==cLength):
                    rotations = abs(speeds[each_servo-1][0]-speeds[each_servo-1][stride_index-1])/4096
                else:
                    rotations = abs(speeds[each_servo-1][stride_index]-speeds[each_servo-1][stride_index-1])/4096
                if ((stride_index-1) >= (pointsPerPhase - R_hl) and (stride_index-1)<=(pointsPerPhase - R_hl + 10)):
                    movementTime = (tspan*h_sw_per/phase_length)/60
                else:
                    movementTime = (tspan*h_st_per/phase_length)/60
                movementSpeed = (rotations / movementTime) / DYNAMIXEL_SPEED_CONSTANT
                newSpeeds[each_servo-1][stride_index-1] = round(movementSpeed)
            elif (each_servo == 13 or each_servo == 14 or each_servo == 15 or each_servo == 16 ):
                if (stride_index==cLength):
                    rotations = abs(speeds[each_servo-1][0]-speeds[each_servo-1][stride_index-1])/4096
                else:
                    rotations = abs(speeds[each_servo-1][stride_index]-speeds[each_servo-1][stride_index-1])/4096
                if ((stride_index-1) >= (pointsPerPhase - L_hl) and (stride_index-1)<=(pointsPerPhase - L_hl + 10)):
                    movementTime = (tspan*h_sw_per/phase_length)/60
                else:
                    movementTime = (tspan*h_st_per/phase_length)/60
                movementSpeed = (rotations / movementTime) / DYNAMIXEL_SPEED_CONSTANT
                newSpeeds[each_servo-1][stride_index-1] = round(movementSpeed)
            else:
                print("Program not set up to calculate speeds for spine yet. Exiting now.")
                exit()
    for each_servo in servos:
        for stride_index in MoveIndex:
            newSpeeds[each_servo-1][stride_index-1] = newSpeeds[each_servo-1][stride_index-1].astype(int)
        newSpeeds[each_servo-1][newSpeeds[each_servo-1] > 1023] = 1023 # For Joint Mode/Multi-turn Mode, 0-1023 is the range for speeds
        newSpeeds[each_servo-1][newSpeeds[each_servo-1] == 0] = 1 # 0 sets the speed to the fastest possible, NOT the slowest
    return newSpeeds
    
def Create_DigitalServos(config_array,port_used_dict,PositionsMatrix,SpeedMatrix):
    ServoDictionary = {}
    DigitalOnly = config_array[32]
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
            elif (ID == 17) or (ID == 18): 
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
                if config_array[28] == True:
                    pass
            elif (ID == 19) or (ID == 20) or (ID == 21) or (ID == 22): 
                if (ID == 19):
                    Max_Position_Limit = 3072
                    Min_Position_Limit = 1024
                elif (ID == 20):
                    Max_Position_Limit = 2800
                    Min_Position_Limit = 1350
                elif (ID == 21):
                    Max_Position_Limit = 2800
                    Min_Position_Limit = 1350
                elif (ID == 22):
                    Max_Position_Limit = 3072
                    Min_Position_Limit = 1024
                if config_array[29] == True:
                    pass
            elif (ID == 23) or (ID == 24):
                if (ID == 23):
                    Max_Position_Limit = 3072
                    Min_Position_Limit = 1024
                elif (ID==24):
                    Max_Position_Limit = 2700
                    Min_Position_Limit = 1400
                if config_array[30] == True:
                    pass
            else:
                Max_Position_Limit = 3072
                Min_Position_Limit = 1024
            MaxMinLimit = (Max_Position_Limit, Min_Position_Limit)
            if DigitalOnly == True:
                port_used = None
            elif DigitalOnly == False:
                port_used = port_used_dict[ID]
            if (ID >= 1) and (ID <= 16):
                NewServo = Servo(ID,port_used,PositionsMatrix[ID-1][:],SpeedMatrix[ID-1][:],MaxMinLimit)
            elif (ID >= 17) and (ID <= 24):
                NewServo = Servo(ID,port_used,2048,config_array[17],MaxMinLimit)
            print("Servo #%d has been digitally created." % (NewServo.ID))
            ServoDictionary[ID] = NewServo
    return ServoDictionary 

def Create_DigitalLimbs(limb_list,ServoDictionary):
    LimbDictionary = {}
    servo_limb_dic = {}
    for Limb_ID, connected_limb in enumerate(limb_list):
        if connected_limb == True:
            entire_limb_not_present = False
            for servo in BODY[Limb_ID]:
                if servo in ServoDictionary:
                    servo_limb_dic[ServoDictionary[servo].ID] = ServoDictionary[servo]
                else:
                    entire_limb_not_present = True
            if entire_limb_not_present == True:
                # print("Corresponding Servos for the indicated connected limbs are not present. Please fix and try again.")
                pass
            elif entire_limb_not_present == False:
                Limb_ID += 1
                if (Limb_ID >= 1) and (Limb_ID <= 4):
                    NewLimb = Leg(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.LimbNumber))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 5):
                    NewLimb = Neck(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.LimbNumber))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 6):
                    NewLimb = Spine(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.LimbNumber))
                    LimbDictionary[Limb_ID] = NewLimb
                elif (Limb_ID == 7):
                    NewLimb = Tail(Limb_ID, servo_limb_dic)
                    print("Limb #%d has been digitally created" % (NewLimb.LimbNumber))
                    LimbDictionary[Limb_ID] = NewLimb
            servo_limb_dic = {}
    return LimbDictionary

def Create_DigitalBody(LimbDictionary):
    all_limbs_present = True
    for Limb_ID in BODY_LIMB_IDS:
        if Limb_ID in LimbDictionary:
            pass
        else:
            all_limbs_present = False
    if all_limbs_present == True:
        WholeBody = Body(LimbDictionary)
        print("Whole Body digitally created.")
    else:
        print("Not all limbs are registered as being connected. Body can not be digitally assembled. Please fix and try again.")
    return WholeBody

def StraightenSpine(ServosDictionary,port_hand_list,packetHandler,DigitalOnly):
    if DigitalOnly == True:
        pass
    elif DigitalOnly == False:
        port_0_count = 0
        port_0_list = []
        port_1_count = 0
        port_1_list = []
        port_2_count = 0
        port_2_list = []
        port_3_count = 0
        port_3_list = []
        port_4_count = 0
        port_4_list = []
        port_5_count = 0
        port_5_list = []
        ports_used = [0, 0, 0, 0, 0, 0]
        try: 
            port_hand_list[0].openPort()
        except:
            pass
        try:
            port_hand_list[1].openPort()
        except:
            pass
        try:
            port_hand_list[2].openPort()
        except:
            pass
        try:
            port_hand_list[3].openPort()
        except:
            pass
        try:
            port_hand_list[4].openPort()
        except:
            pass
        try:
            port_hand_list[5].openPort()
        except:
            pass
        body_length_connected = []
        for each_servo in BODY_LENGTH:
            if each_servo in ServosDictionary:
                if (ServosDictionary[each_servo].port_used == 0):
                    port_0_count += 1
                    port_0_list.append(each_servo)
                    ports_used[0] = 1
                elif (ServosDictionary[each_servo].port_used == 1):
                    port_1_count += 1
                    port_1_list.append(each_servo)
                    ports_used[1] = 1
                elif (ServosDictionary[each_servo].port_used == 2):
                    port_2_count += 1
                    port_2_list.append(each_servo)
                    ports_used[2] = 1
                elif (ServosDictionary[each_servo].port_used == 3):
                    port_3_count += 1
                    port_3_list.append(each_servo)
                    ports_used[3] = 1
                elif (ServosDictionary[each_servo].port_used == 4):
                    port_4_count += 1
                    port_4_list.append(each_servo)
                    ports_used[4] = 1
                elif (ServosDictionary[each_servo].port_used == 5):
                    port_5_count += 1
                    port_5_list.append(each_servo)
                    ports_used[5] = 1
                body_length_connected.append(each_servo)
        if port_0_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[36], 4)
        if port_1_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[36], 4)
        if port_2_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[36], 4)
        if port_3_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[36], 4)
        if port_4_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[36], 4)
        if port_5_count > 0:
            # Initialize GroupSyncWrite instance
            groupSyncWritePOS_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[37], 4)
            # Initialize GroupSyncWrite instance
            groupSyncWriteVEL_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[36], 4)
        GoalVelocity = []
        GoalPosition = []
        # Add parameters for Velocity and Position change commands
        for index, each_servo in enumerate(body_length_connected):
            GoalVelocity.append(FormatSendData(int(ServosDictionary[each_servo].Speeds)))
            GoalPosition.append(FormatSendData(ServosDictionary[each_servo].Positions))
            if each_servo in port_0_list:
                dxl_addparam_result = groupSyncWriteVEL_1.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_1.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif each_servo in port_1_list:
                dxl_addparam_result = groupSyncWriteVEL_2.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_2.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif each_servo in port_2_list:
                dxl_addparam_result = groupSyncWriteVEL_3.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_3.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif each_servo in port_3_list:
                dxl_addparam_result = groupSyncWriteVEL_4.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_4.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif each_servo in port_4_list:
                dxl_addparam_result = groupSyncWriteVEL_5.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_5.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif each_servo in port_5_list:
                dxl_addparam_result = groupSyncWriteVEL_6.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                    return each_servo
                dxl_addparam_result = groupSyncWritePOS_6.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                    return each_servo
            elif (each_servo in ServosDictionary) and (each_servo not in port_0_list) and (each_servo not in port_1_list) and (each_servo not in port_2_list):
                print("Servo #%03d not included in stay straight protocol" % each_servo)
            else:
                print('Error in servo list. Please fix and try again.')

        if ports_used[0] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 1")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 2")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 3")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 4")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 5")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Velocity:Port 6")
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_6.clearParam()

        if ports_used[0] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 1")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 2")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 3")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 4")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 5")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                print("Position:Port 6")
            # Clear syncwrite parameter storage
            groupSyncWritePOS_6.clearParam()
    return 0

def DetermineProfileAccceleration(profileVelocity,changeInPosition,endMoveTime):
    print("Profile Velocity: " + str(profileVelocity))
    print("Change in Position: " + str(changeInPosition))
    print("End Move Time: " + str(endMoveTime))
    prof_acc = int(((64 * profileVelocity) / endMoveTime - ((64 * changeInPosition) / profileVelocity)).round())
    print("Profile Acceleration: " + str(prof_acc))
    print("===============================")
    return prof_acc

def MoveNumerousServos(TilibotGUI, servo_list, ServosDictionary, port_hand_list, port_servo_dict, packetHandler, stride_numbers, record_array, start_time, move_smooth, DigitalOnly):
    if DigitalOnly == True:
        pass
    elif DigitalOnly == False:
        ports_used = [0, 0, 0, 0, 0, 0]
        for x in servo_list:
            if any(port_servo_dict[x] == port_hand_list[0] for x in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_1 = GroupSyncWrite(port_hand_list[0],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_1 = GroupSyncWrite(port_hand_list[0],packetHandler, AddrDict[36], 4)
                ports_used[0] = 1
            if any(port_servo_dict[x] == port_hand_list[1] for x in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_2 = GroupSyncWrite(port_hand_list[1],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_2 = GroupSyncWrite(port_hand_list[1],packetHandler, AddrDict[36], 4)
                ports_used[1] = 1
            if any(port_servo_dict[x] == port_hand_list[2] for x in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_3 = GroupSyncWrite(port_hand_list[2],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_3 = GroupSyncWrite(port_hand_list[2],packetHandler, AddrDict[36], 4)
                ports_used[2] = 1
            if any(port_servo_dict[x] == port_hand_list[3] for x in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_4 = GroupSyncWrite(port_hand_list[3],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_4 = GroupSyncWrite(port_hand_list[3],packetHandler, AddrDict[36], 4)
                ports_used[3] = 1
            if any(port_servo_dict[x] == port_hand_list[4] for x in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_5 = GroupSyncWrite(port_hand_list[4],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_5 = GroupSyncWrite(port_hand_list[4],packetHandler, AddrDict[36], 4)
                ports_used[4] = 1
            if any(port_servo_dict[x] == port_hand_list[5] for x in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[26], 1)
                groupSyncRead_Position_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[44], 4)
                if move_smooth == 1:
                    groupSyncWriteProfileAcc_6 = GroupSyncWrite(port_hand_list[5],packetHandler, AddrDict[35], 4)
                    groupSyncWriteProfileVel_6 = GroupSyncWrite(port_hand_list[5],packetHandler, AddrDict[36], 4)
                ports_used[5] = 1
        port_0_count = 0
        port_0_list = []
        port_1_count = 0
        port_1_list = []
        port_2_count = 0
        port_2_list = []
        port_3_count = 0
        port_3_list = []
        port_4_count = 0
        port_4_list = []
        port_5_count = 0
        port_5_list = []
        for each_servo in servo_list:
            if (ServosDictionary[each_servo].port_used == 0):
                port_0_count += 1
                port_0_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 1):
                port_1_count += 1
                port_1_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 2):
                port_2_count += 1
                port_2_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 3):
                port_3_count += 1
                port_3_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 4):
                port_4_count += 1
                port_4_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 5):
                port_5_count += 1
                port_5_list.append(each_servo)
        GoalVelocity = []
        GoalPosition = []
        Original_GoalPosition = []
        out_data = []
        readers_exist = False
        for stride_count in range(stride_numbers[0]):
            for position_index in range(stride_numbers[1]):
                if (stride_count == 0) and (position_index == 0): # Skip the first position, this is Home Position
                    continue
                if (stride_count != 0) and (position_index == 0):
                    speed_index = stride_numbers[1] - 1
                else:
                    speed_index = position_index - 1
                if ports_used[0] == 1:
                    isStopped_0 = [0] * port_0_count
                    isInThreshold_0 = [0] * port_0_count
                else:
                    isStopped_0 = []
                    isInThreshold_0 = []
                if ports_used[1] == 1:
                    isStopped_1 = [0] * port_1_count
                    isInThreshold_1 = [0] * port_1_count
                else:
                    isStopped_1 = []
                    isInThreshold_1 = []
                if ports_used[2] == 1:
                    isStopped_2 = [0] * port_2_count
                    isInThreshold_2 = [0] * port_2_count
                else:
                    isStopped_2 = []
                    isInThreshold_2 = []
                if ports_used[3] == 1:
                    isStopped_3 = [0] * port_3_count
                    isInThreshold_3 = [0] * port_3_count
                else:
                    isStopped_3 = []
                    isInThreshold_3 = []
                if ports_used[4] == 1:
                    isStopped_4 = [0] * port_4_count
                    isInThreshold_4 = [0] * port_0_count
                else:
                    isStopped_4 = []
                    isInThreshold_4 = []
                if ports_used[5] == 1:
                    isStopped_5 = [0] * port_5_count
                    isInThreshold_5 = [0] * port_5_count
                else:
                    isStopped_5 = []
                    isInThreshold_5 = []
                # Add parameters for Velocity and Position change commands
                for index, each_servo in enumerate(servo_list):
                    GoalVelocity.append(FormatSendData(int(ServosDictionary[each_servo].Speeds[speed_index])))
                    Original_GoalPosition.append(ServosDictionary[each_servo].Positions[position_index])
                    GoalPosition.append(FormatSendData(ServosDictionary[each_servo].Positions[position_index]))
                    if each_servo in port_0_list:
                        dxl_addparam_result = groupSyncWriteVEL_1.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_1.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_1.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_1.addParam(each_servo,GoalVelocity[index])  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    elif each_servo in port_1_list:
                        dxl_addparam_result = groupSyncWriteVEL_2.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_2.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_2.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_2.addParam(each_servo,GoalVelocity[index]) 
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    elif each_servo in port_2_list:
                        dxl_addparam_result = groupSyncWriteVEL_3.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_3.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_3.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_3.addParam(each_servo,GoalVelocity[index]) # Possibly needs to be just number
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    if each_servo in port_3_list:
                        dxl_addparam_result = groupSyncWriteVEL_4.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_4.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_4.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_4.addParam(each_servo,GoalVelocity[index]) # Possibly needs to be just number
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    elif each_servo in port_4_list:
                        dxl_addparam_result = groupSyncWriteVEL_5.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_5.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_5.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))  
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_5.addParam(each_servo,GoalVelocity[index]) 
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    elif each_servo in port_5_list:
                        dxl_addparam_result = groupSyncWriteVEL_6.addParam(each_servo,GoalVelocity[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam velocity failed" % each_servo)
                            return
                        dxl_addparam_result = groupSyncWritePOS_6.addParam(each_servo,GoalPosition[index])
                        if dxl_addparam_result != True:
                            print("[ID:%03d] groupSyncWrite addparam position failed" % each_servo)
                            return
                        # # Determine position difference for use in determining profile acceleration
                        if (position_index != 0):
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[position_index-1])
                        else:
                            pos_difference = abs(ServosDictionary[each_servo].Positions[position_index] - ServosDictionary[each_servo].Positions[-1])
                        if move_smooth == 1:
                            dxl_addparam_result = groupSyncWriteProfileAcc_6.addParam(each_servo,FormatSendData(DetermineProfileAccceleration(int(ServosDictionary[each_servo].Speeds[speed_index]),pos_difference,stride_numbers[2]/stride_numbers[1])))   
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile acceleration failed" % each_servo)
                                return
                            dxl_addparam_result = groupSyncWriteProfileVel_6.addParam(each_servo,GoalVelocity[index]) 
                            if dxl_addparam_result != True:
                                print("[ID:%03d] groupSyncWrite addparam profile velocity failed" % each_servo)
                                return
                    else:
                        print('Error in servo list. Please fix and try again.')
                        
                # Write Velocity Profile, Acceleration Profile, and Velocity values
                if ports_used[0] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_1.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_1.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_1.clearParam()
                        groupSyncWriteProfileVel_1.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_1.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_1.clearParam()

                if ports_used[1] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_2.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_2.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_2.clearParam()
                        groupSyncWriteProfileVel_2.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_2.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_2.clearParam()

                if ports_used[2] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_3.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_3.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_3.clearParam()
                        groupSyncWriteProfileVel_3.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_3.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_3.clearParam()

                if ports_used[3] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_4.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_4.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_4.clearParam()
                        groupSyncWriteProfileVel_4.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_4.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_4.clearParam()

                if ports_used[4] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_5.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_5.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_5.clearParam()
                        groupSyncWriteProfileVel_5.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_5.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_5.clearParam()

                if ports_used[5] == 1:
                    if move_smooth == 1:
                        # Syncwrite Velocity and Acceleration profiles for trapezoidal Velocity Profile
                        dxl_comm_result = groupSyncWriteProfileAcc_3.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Acceleration Profile:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncWriteProfileVel_6.txPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Velocity Profile:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                        groupSyncWriteProfileAcc_6.clearParam()
                        groupSyncWriteProfileVel_6.clearParam()
                    # Syncwrite goal velocity
                    dxl_comm_result = groupSyncWriteVEL_6.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Velocity:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWriteVEL_6.clearParam()
                    
                # Write Position Values
                if ports_used[0] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_1.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_1.clearParam()
                if ports_used[1] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_2.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_2.clearParam()
                if ports_used[2] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_3.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_3.clearParam()
                if ports_used[3] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_4.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_4.clearParam()
                if ports_used[4] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_5.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_5.clearParam()
                if ports_used[5] == 1:
                    # Syncwrite goal position
                    dxl_comm_result = groupSyncWritePOS_6.txPacket()
                    if dxl_comm_result != COMM_SUCCESS:
                        print("%s - Position:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                    # Clear syncwrite parameter storage
                    groupSyncWritePOS_6.clearParam()

                for each_servo in ServosDictionary.keys():
                    if each_servo in port_0_list:
                        groupSyncRead_Moving_1.addParam(each_servo)
                        groupSyncRead_Error_1.addParam(each_servo)
                        groupSyncRead_Position_1.addParam(each_servo)
                    elif each_servo in port_1_list:
                        groupSyncRead_Moving_2.addParam(each_servo)
                        groupSyncRead_Error_2.addParam(each_servo)
                        groupSyncRead_Position_2.addParam(each_servo)
                    elif each_servo in port_2_list:
                        groupSyncRead_Moving_3.addParam(each_servo)
                        groupSyncRead_Error_3.addParam(each_servo)
                        groupSyncRead_Position_3.addParam(each_servo)
                    elif each_servo in port_3_list:
                        groupSyncRead_Moving_4.addParam(each_servo)
                        groupSyncRead_Error_4.addParam(each_servo)
                        groupSyncRead_Position_4.addParam(each_servo)
                    elif each_servo in port_4_list:
                        groupSyncRead_Moving_5.addParam(each_servo)
                        groupSyncRead_Error_5.addParam(each_servo)
                        groupSyncRead_Position_5.addParam(each_servo)
                    elif each_servo in port_5_list:
                        groupSyncRead_Moving_6.addParam(each_servo)
                        groupSyncRead_Error_6.addParam(each_servo)
                        groupSyncRead_Position_6.addParam(each_servo)
                while 1:
                    # Syncread Moving Value, Hardware Error Value, and Position Value
                    if ports_used[0] == 1:
                        dxl_comm_result = groupSyncRead_Moving_1.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_1.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_1.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                    if ports_used[1] == 1:
                        dxl_comm_result = groupSyncRead_Moving_2.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_2.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_2.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                    if ports_used[2] == 1:
                        dxl_comm_result = groupSyncRead_Moving_3.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_3.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_3.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                    if ports_used[3] == 1:
                        dxl_comm_result = groupSyncRead_Moving_4.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_4.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_4.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                    if ports_used[4] == 1:
                        dxl_comm_result = groupSyncRead_Moving_5.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_5.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_5.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                    if ports_used[5] == 1:
                        dxl_comm_result = groupSyncRead_Moving_6.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Moving Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Error_6.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Hardware Error Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                        dxl_comm_result = groupSyncRead_Position_6.txRxPacket()
                        if dxl_comm_result != COMM_SUCCESS:
                            print("%s - Position Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                    index_1 = 0
                    index_2 = 0
                    index_3 = 0
                    index_4 = 0
                    index_5 = 0
                    index_6 = 0 
                    print("\n+-+-+-+ Cycle Stride #{0} / Move #{1} +-+-+-+".format(stride_count,position_index))
                    for each_servo in ServosDictionary.keys():
                        # Get Error Code if Present. Change color on schematic if present.
                        # Get Dynamixel present Moving value
                        if (each_servo in port_0_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_1.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_1.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_1.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_0[index_1] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_0[index_1] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_0[index_1] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_0[index_1] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_0[index_1] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass 
                            elif (dxl_mov == 0) and (isStopped_0[index_1] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_0[index_1] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_0[index_1] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_0[index_1] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_0[index_1] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_1 += 1
                        if (each_servo in port_1_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_2.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_2.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_2.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_1[index_2] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_1[index_1] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_1[index_2] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_1[index_2] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_1[index_2] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 0) and (isStopped_1[index_2] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_1[index_2] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_1[index_2] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_1[index_2] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_1[index_1] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_2 += 1
                        if (each_servo in port_2_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_3.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_3.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_3.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_2[index_3] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_2[index_3] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_2[index_3] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_2[index_3] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_2[index_3] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 0) and (isStopped_2[index_3] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_2[index_3] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_2[index_3] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_2[index_3] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_2[index_3] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_3 += 1
                        if (each_servo in port_3_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_4.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_4.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_4.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_3[index_4] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_3[index_4] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_3[index_4] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_3[index_4] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_3[index_4] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 0) and (isStopped_3[index_4] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_3[index_4] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_3[index_4] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_3[index_4] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_3[index_4] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_4 += 1
                        if (each_servo in port_4_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_5.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_5.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_5.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_4[index_5] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_4[index_5] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_4[index_5] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_4[index_5] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_4[index_5] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 0) and (isStopped_4[index_5] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_4[index_5] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_4[index_5] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_4[index_5] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_4[index_5] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_5 += 1
                        if (each_servo in port_5_list) and (each_servo in LIMBS_ONLY):
                            dxl_error = groupSyncRead_Error_6.getData(each_servo, AddrDict[26],1)
                            if (dxl_error == 0):
                                pass
                            else:
                                print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                                print(ErrorChecker(dxl_error))
                                TilibotGUI.change_servo_color(each_servo,"blue")
                            dxl_mov = groupSyncRead_Moving_6.getData(each_servo, AddrDict[39],1)
                            dxl_pos = groupSyncRead_Position_6.getData(each_servo, AddrDict[44],4)
                            if (dxl_mov == 0) and (isStopped_5[index_6] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo has stopped moving, and is housed within the correct location threshold but has not been marked as finished, so that must be changed.
                                isStopped_5[index_6] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            elif (dxl_mov == 1) and (isStopped_5[index_6] == 0) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving to desired position. Let it continue moving.
                                pass 
                            elif (dxl_mov == 0) and (isStopped_5[index_6] == 0) and not ((dxl_pos >=(Original_GoalPosition [position_index]- MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold and has not registered as reaching its destination. Send move command again until servo is in correct place.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                pass
                            elif (dxl_mov == 1) and (isStopped_5[index_6] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is moving but has already registered as reaching its destination but is not within the move threshold. Send the move command to hopefully send it back to the proper position. 
                                if ServosDictionary[each_servo].position_fixing == False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 0) and (isStopped_5[index_6] == 1) and not ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is not moving but is not within the location threshold but has reached its destination. Send move command again until servo is in correct place. 
                                if ServosDictionary[each_servo].position_fixing = False:
                                    list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                    ServosDictionary[each_servo].position_fixing = True
                                    ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                else:
                                    pass
                            elif (dxl_mov == 1) and (isStopped_5[index_6] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but has reached its destination and is within the move threshold. Send move command again so servo can hopefully stop moving.
                                list_index = servo_list.index(ServosDictionary[each_servo].ID)
                                # ServosDictionary[each_servo].MoveServo(Original_GoalPosition[list_index],port_hand_list[ServosDictionary[each_servo].port_used])
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 0) and (isStopped_5[index_6] == 1) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is where it needs to be and has registered as such. No further action required. 
                                ServosDictionary[each_servo].position_fixing = False
                                pass
                            elif (dxl_mov == 1) and (isStopped_5[index_6] == 0) and ((dxl_pos >=(Original_GoalPosition[position_index] - MOVING_THRESHOLD_ACCURACY)) and (dxl_pos <= (Original_GoalPosition[position_index] + MOVING_THRESHOLD_ACCURACY))):
                                # Servo is still moving but is within the move threshold but has not been marked as reaching its destination. Mark the servo as having done so.
                                isStopped_5[index_6] = 1
                                ServosDictionary[each_servo].position_fixing = False
                            else:
                                pass
                            index_6 += 1
                    if (0 in isStopped_0) or (0 in isStopped_1) or (0 in isStopped_2) or (0 in isStopped_3) or (0 in isStopped_4) or (0 in isStopped_5):
                        pass
                    else:
                        if ports_used[0] == 1:
                            groupSyncRead_Moving_1.clearParam()
                            groupSyncRead_Error_1.clearParam()
                        if ports_used[1] == 1:
                            groupSyncRead_Moving_2.clearParam()
                            groupSyncRead_Error_2.clearParam()
                        if ports_used[2] == 1:
                            groupSyncRead_Moving_3.clearParam()
                            groupSyncRead_Error_3.clearParam()
                        if ports_used[3] == 1:
                            groupSyncRead_Moving_4.clearParam()
                            groupSyncRead_Error_4.clearParam()
                        if ports_used[4] == 1:
                            groupSyncRead_Moving_5.clearParam()
                            groupSyncRead_Error_5.clearParam()
                        if ports_used[5] == 1:
                            groupSyncRead_Moving_6.clearParam()
                            groupSyncRead_Error_6.clearParam()
                        if record_array[0] == True:
                            if readers_exist == False:
                                if ports_used[0] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_1 = GroupSyncRead(port_hand_list[0],packetHandler,AddrDict[42],2)
                                        port_1_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_1 = GroupSyncRead(port_hand_list[0],packetHandler,AddrDict[47],2)
                                        port_1_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_1 = GroupSyncRead(port_hand_list[0],packetHandler,AddrDict[48],1)
                                        port_1_Temperature = []
                                        readers_exist = True
                                if ports_used[1] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_2 = GroupSyncRead(port_hand_list[1],packetHandler,AddrDict[42],2)
                                        port_2_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_2 = GroupSyncRead(port_hand_list[1],packetHandler,AddrDict[47],2)
                                        port_2_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_2 = GroupSyncRead(port_hand_list[1],packetHandler,AddrDict[48],1)
                                        port_2_Temperature = []
                                        readers_exist = True
                                if ports_used[2] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_3 = GroupSyncRead(port_hand_list[2],packetHandler,AddrDict[42],2)
                                        port_3_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_3 = GroupSyncRead(port_hand_list[2],packetHandler,AddrDict[47],2)
                                        port_3_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_3 = GroupSyncRead(port_hand_list[2],packetHandler,AddrDict[48],1)
                                        port_3_Temperature = []
                                        readers_exist = True
                                if ports_used[3] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_4 = GroupSyncRead(port_hand_list[3],packetHandler,AddrDict[42],2)
                                        port_4_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_4 = GroupSyncRead(port_hand_list[3],packetHandler,AddrDict[47],2)
                                        port_4_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_4 = GroupSyncRead(port_hand_list[3],packetHandler,AddrDict[48],1)
                                        port_4_Temperature = []
                                        readers_exist = True
                                if ports_used[4] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_5 = GroupSyncRead(port_hand_list[4],packetHandler,AddrDict[42],2)
                                        port_5_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_5 = GroupSyncRead(port_hand_list[4],packetHandler,AddrDict[47],2)
                                        port_5_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_5 = GroupSyncRead(port_hand_list[4],packetHandler,AddrDict[48],1)
                                        port_5_Temperature = []
                                        readers_exist = True
                                if ports_used[5] == 1:
                                    if record_array[6] == True:
                                        # Create Current Reader
                                        groupSyncRead_Current_6 = GroupSyncRead(port_hand_list[5],packetHandler,AddrDict[42],2)
                                        port_6_Current = []
                                        readers_exist = True
                                    if record_array[7] == True:
                                        # Create Voltage Reader
                                        groupSyncRead_Voltage_6 = GroupSyncRead(port_hand_list[5],packetHandler,AddrDict[47],2)
                                        port_6_Voltage = []
                                        readers_exist = True
                                    if record_array[8] == True:
                                        # Create Temperature Reader
                                        groupSyncRead_Temperature_6 = GroupSyncRead(port_hand_list[5],packetHandler,AddrDict[48],1)
                                        port_6_Temperature = []
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
                                        if ports_used[3] == 1:
                                            groupSyncRead_Current_4.addParam(each_servo)
                                        if ports_used[4] == 1:
                                            groupSyncRead_Current_5.addParam(each_servo)
                                        if ports_used[5] == 1:
                                            groupSyncRead_Current_6.addParam(each_servo)
                                    if record_array[7] == True:
                                        if ports_used[0] == 1:
                                            groupSyncRead_Voltage_1.addParam(each_servo)
                                        if ports_used[1] == 1:
                                            groupSyncRead_Voltage_2.addParam(each_servo)
                                        if ports_used[2] == 1:
                                            groupSyncRead_Voltage_3.addParam(each_servo)
                                        if ports_used[3] == 1:
                                            groupSyncRead_Voltage_4.addParam(each_servo)
                                        if ports_used[4] == 1:
                                            groupSyncRead_Voltage_5.addParam(each_servo)
                                        if ports_used[5] == 1:
                                            groupSyncRead_Voltage_6.addParam(each_servo)
                                    if record_array[8] == True:
                                        if ports_used[0] == 1:
                                            groupSyncRead_Temperature_1.addParam(each_servo)
                                        if ports_used[1] == 1:
                                            groupSyncRead_Temperature_2.addParam(each_servo)
                                        if ports_used[2] == 1:
                                            groupSyncRead_Temperature_3.addParam(each_servo)
                                        if ports_used[3] == 1:
                                            groupSyncRead_Temperature_4.addParam(each_servo)
                                        if ports_used[4] == 1:
                                            groupSyncRead_Temperature_5.addParam(each_servo)
                                        if ports_used[5] == 1:
                                            groupSyncRead_Temperature_6.addParam(each_servo)
                            if readers_exist == True:
                                if record_array[6] == True:
                                    if ports_used[0] == 1:
                                        # Syncread present current
                                        dxl_comm_result = groupSyncRead_Current_1.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_front_servo in port_0_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_back_servo in port_1_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_bodyln_servo in port_2_list:
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
                                    if ports_used[3] == 1:
                                        # Syncread present current
                                        dxl_comm_result = groupSyncRead_Current_4.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_front_servo in port_3_list:
                                            if each_front_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Current_4.isAvailable(each_front_servo, AddrDict[42], 2)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_front_servo)
                                                    quit()
                                                # Get Dynamixel present current value
                                                port_4_Current.append(groupSyncRead_Current_4.getData(each_front_servo, AddrDict[42], 2))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Current_4.clearParam()
                                    if ports_used[4] == 1:
                                        # Syncread present current
                                        dxl_comm_result = groupSyncRead_Current_5.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_back_servo in port_4_list:
                                            if each_back_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Current_5.isAvailable(each_back_servo, AddrDict[42], 2)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_back_servo)
                                                    quit()
                                                # Get Dynamixel present current value
                                                port_5_Current.append(groupSyncRead_Current_5.getData(each_back_servo, AddrDict[42], 2))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Current_5.clearParam()
                                    if ports_used[5] == 1:
                                        # Syncread present current
                                        dxl_comm_result = groupSyncRead_Current_6.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_bodyln_servo in port_5_list:
                                            if each_bodyln_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Current_6.isAvailable(each_servo, AddrDict[42], 2)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                    quit()
                                                # Get Dynamixel present current value
                                                port_6_Current.append(groupSyncRead_Current_6.getData(each_servo, AddrDict[42], 2))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Current_6.clearParam()
                                if record_array[7] == True:
                                    if ports_used[0] == 1:
                                        # Syncread present voltage
                                        dxl_comm_result = groupSyncRead_Voltage_1.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_front_servo in port_0_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_back_servo in port_1_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_bodyln_servo in port_2_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_front_servo in port_0_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_back_servo in port_1_list:
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
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_bodyln_servo in port_2_list:
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
                                    if ports_used[3] == 1:
                                        # Syncread present temperature
                                        dxl_comm_result = groupSyncRead_Temperature_4.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_front_servo in port_3_list:
                                            if each_front_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Temperature_4.isAvailable(each_servo, AddrDict[48], 1)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                    quit()
                                                # Get Dynamixel present temperature value
                                                port_4_Temperature.append(groupSyncRead_Temperature_4.getData(each_servo, AddrDict[48], 1))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Temperature_4.clearParam()
                                    if ports_used[4] == 1:
                                        # Syncread present temperature
                                        dxl_comm_result = groupSyncRead_Temperature_5.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_back_servo in port_4_list:
                                            if each_back_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Temperature_5.isAvailable(each_servo, AddrDict[48], 1)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                    quit()
                                                # Get Dynamixel present temperature value
                                                port_5_Temperature.append(groupSyncRead_Temperature_5.getData(each_servo, AddrDict[48], 1))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Temperature_5.clearParam()
                                    if ports_used[5] == 1:
                                        # Syncread present temperature
                                        dxl_comm_result = groupSyncRead_Temperature_6.txRxPacket()
                                        if dxl_comm_result != COMM_SUCCESS:
                                            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
                                        for each_bodyln_servo in port_5_list:
                                            if each_bodyln_servo in servo_list:
                                                # Check if groupsyncread data of Dynamixel is available
                                                dxl_getdata_result = groupSyncRead_Temperature_6.isAvailable(each_servo, AddrDict[48], 1)
                                                if dxl_getdata_result != True:
                                                    print("[ID:%03d] groupSyncRead getdata failed" % each_servo)
                                                    quit()
                                                # Get Dynamixel present temperature value
                                                port_6_Temperature.append(groupSyncRead_Temperature_6.getData(each_servo, AddrDict[48], 1))
                                        # Clear syncread parameter storage
                                        groupSyncRead_Temperature_6.clearParam()
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
                                        if each_servo in port_0_list:
                                            dxl_current = port_1_Current[list_index]
                                        elif each_servo in port_1_list:
                                            dxl_current = port_2_Current[list_index-(port_0_count)]
                                        elif each_servo in port_2_list:
                                            dxl_current = port_3_Current[list_index-(port_0_count+port_1_count)]
                                        elif each_servo in port_3_list:
                                            dxl_current = port_4_Current[list_index-(port_0_count+port_1_count+port_2_count)]
                                        elif each_servo in port_4_list:
                                            dxl_current = port_5_Current[list_index-(port_0_count+port_1_count+port_2_count+port_3_count)]
                                        elif each_servo in port_5_list:
                                            dxl_current = port_6_Current[list_index-(port_0_count+port_1_count+port_2_count+port_3_count+port_4_count)]
                                        servo_data_array.append(dxl_current)
                                    if record_array[7] == True:
                                        if each_servo in port_0_list:
                                            dxl_voltage = port_1_Voltage[list_index]
                                        elif each_servo in port_1_list:
                                            dxl_voltage = port_2_Voltage[list_index-(port_0_count)]
                                        elif each_servo in port_2_list:
                                            dxl_voltage = port_3_Voltage[list_index-(port_0_count+port_1_count)]
                                        elif each_servo in port_3_list:
                                            dxl_voltage = port_4_Voltage[list_index-(port_0_count+port_1_count+port_2_count)]
                                        elif each_servo in port_4_list:
                                            dxl_voltage = port_5_Voltage[list_index-(port_0_count+port_1_count+port_2_count+port_3_count)]
                                        elif each_servo in port_5_list:
                                            dxl_voltage = port_6_Voltage[list_index-(port_0_count+port_1_count+port_2_count+port_3_count+port_4_count)]
                                        servo_data_array.append(dxl_voltage)
                                    if record_array[8] == True:
                                        if each_servo in port_0_list:
                                            dxl_temp = port_1_Temperature[list_index]
                                        elif each_servo in port_1_list:
                                            dxl_temp = port_2_Temperature[list_index-(port_0_count)]
                                        elif each_servo in port_2_list:
                                            dxl_temp = port_3_Temperature[list_index-(port_0_count+port_1_count)]
                                        elif each_servo in port_3_list:
                                            dxl_temp = port_4_Temperature[list_index-(port_0_count+port_1_count+port_2_count)]
                                        elif each_servo in port_4_list:
                                            dxl_temp = port_5_Temperature[list_index-(port_0_count+port_1_count+port_2_count+port_3_count)]
                                        elif each_servo in port_5_list:
                                            dxl_temp = port_6_Temperature[list_index-(port_0_count+port_1_count+port_2_count+port_3_count+port_4_count)]
                                        servo_data_array.append(dxl_temp)
                                    out_data.append(servo_data_array)
                            if record_array[6] == True:
                                if ports_used[0] == 1:
                                    port_1_Current = []
                                if ports_used[1] == 1:
                                    port_2_Current = []
                                if ports_used[2] == 1:
                                    port_3_Current = []
                                if ports_used[3] == 1:
                                    port_4_Current = []
                                if ports_used[4] == 1:
                                    port_5_Current = []
                                if ports_used[5] == 1:
                                    port_6_Current = []
                            if record_array[7] == True:
                                if ports_used[0] == 1:
                                    port_1_Voltage = []
                                if ports_used[1] == 1:
                                    port_2_Voltage = []
                                if ports_used[2] == 1:
                                    port_3_Voltage = []
                                if ports_used[3] == 1:
                                    port_4_Voltage = []
                                if ports_used[4] == 1:
                                    port_5_Voltage = []
                                if ports_used[5] == 1:
                                    port_6_Voltage = []
                            if record_array[8] == True:
                                if ports_used[0] == 1:
                                    port_1_Temperature = []
                                if ports_used[1] == 1:
                                    port_2_Temperature = []
                                if ports_used[2] == 1:
                                    port_3_Temperature = []
                                if ports_used[3] == 1:
                                    port_4_Temperature = []
                                if ports_used[4] == 1:
                                    port_5_Temperature = []
                                if ports_used[5] == 1:
                                    port_6_Temperature = []
                        GoalVelocity = []
                        GoalPosition = []
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

def Move_Spider_Up(TilibotGUI, servo_list, ServosDictionary, port_hand_list, port_servo_dict, packetHandler, in_home_speed, DigitalOnly):
    if DigitalOnly == True:
        pass
    elif DigitalOnly == False:
        ports_used = [0, 0, 0, 0, 0, 0]
        for used_servo in servo_list:
            if any(port_servo_dict[used_servo] == port_hand_list[0] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[26], 1)
                ports_used[0] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[1] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[26], 1)
                ports_used[1] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[2] for used_servo in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[26], 1)
                ports_used[2] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[3] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[26], 1)
                ports_used[3] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[4] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[26], 1)
                ports_used[4] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[5] for used_servo in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[26], 1)
                ports_used[5] = 1
            else:
                pass
        port_0_count = 0
        port_0_list = []
        port_1_count = 0
        port_1_list = []
        port_2_count = 0
        port_2_list = []
        port_3_count = 0
        port_3_list = []
        port_4_count = 0
        port_4_list = []
        port_5_count = 0
        port_5_list = []
        for each_servo in servo_list:
            if (ServosDictionary[each_servo].port_used == 0):
                port_0_count += 1
                port_0_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 1):
                port_1_count += 1
                port_1_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 2):
                port_2_count += 1
                port_2_list.append(each_servo)
            if (ServosDictionary[each_servo].port_used == 3):
                port_3_count += 1
                port_3_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 4):
                port_4_count += 1
                port_4_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 5):
                port_5_count += 1
                port_5_list.append(each_servo)
    
        GoalVelocity = []
        GoalPosition = []

        if ports_used[0] == 1:
            isStopped_0 = [0] * port_0_count
        else:
            isStopped_0 = []
        if ports_used[1] == 1:
            isStopped_1 = [0] * port_1_count
        else:
            isStopped_1 = []
        if ports_used[2] == 1:
            isStopped_2 = [0] * port_2_count
        else:
            isStopped_2 = []
        if ports_used[3] == 1:
            isStopped_3 = [0] * port_3_count
        else:
            isStopped_3 = []
        if ports_used[4] == 1:
            isStopped_4 = [0] * port_4_count
        else:
            isStopped_4 = []
        if ports_used[5] == 1:
            isStopped_5 = [0] * port_5_count
        else:
            isStopped_5 = []

        for index, each_servo in enumerate(servo_list):
            GoalVelocity.append(FormatSendData(int(in_home_speed)))
            GoalPosition.append(FormatSendData(SPIDER_UP[each_servo]))
            if each_servo in port_0_list:
                dxl_addparam_result = groupSyncWriteVEL_1.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_1.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            elif each_servo in port_1_list:
                dxl_addparam_result = groupSyncWriteVEL_2.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_2.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            elif each_servo in port_2_list:
                dxl_addparam_result = groupSyncWriteVEL_3.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_3.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            elif each_servo in port_3_list:
                dxl_addparam_result = groupSyncWriteVEL_4.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_4.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            elif each_servo in port_4_list:
                dxl_addparam_result = groupSyncWriteVEL_5.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_5.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            elif each_servo in port_5_list:
                dxl_addparam_result = groupSyncWriteVEL_6.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_6.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-UP addparam position failed" % each_servo)
                    return
            else:
                print('Error in servo list. Please fix and try again.')
        if ports_used[0] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Veloctiy:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Velocity:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Velocity:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Veloctiy:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Velocity:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Velocity:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_6.clearParam()

        if ports_used[0] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-UP Position:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_6.clearParam()
        for each_servo in ServosDictionary.keys():
            if each_servo in port_0_list:
                groupSyncRead_Moving_1.addParam(each_servo)
                groupSyncRead_Error_1.addParam(each_servo)
            elif each_servo in port_1_list:
                groupSyncRead_Moving_2.addParam(each_servo)
                groupSyncRead_Error_2.addParam(each_servo)
            elif each_servo in port_2_list:
                groupSyncRead_Moving_3.addParam(each_servo)
                groupSyncRead_Error_3.addParam(each_servo)
            elif each_servo in port_3_list:
                groupSyncRead_Moving_4.addParam(each_servo)
                groupSyncRead_Error_4.addParam(each_servo)
            elif each_servo in port_4_list:
                groupSyncRead_Moving_5.addParam(each_servo)
                groupSyncRead_Error_5.addParam(each_servo)
            elif each_servo in port_5_list:
                groupSyncRead_Moving_6.addParam(each_servo)
                groupSyncRead_Error_6.addParam(each_servo)
        while 1:
            # Syncread Moving Value
            if ports_used[0] == 1:
                dxl_comm_result = groupSyncRead_Moving_1.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_1.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[1] == 1:
                dxl_comm_result = groupSyncRead_Moving_2.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_2.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[2] == 1:
                dxl_comm_result = groupSyncRead_Moving_3.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_3.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))    
            if ports_used[3] == 1:
                dxl_comm_result = groupSyncRead_Moving_4.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_4.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[4] == 1:
                dxl_comm_result = groupSyncRead_Moving_5.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_5.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[5] == 1:
                dxl_comm_result = groupSyncRead_Moving_6.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-UP Moving Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_6.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            index_1 = 0
            index_2 = 0
            index_3 = 0
            index_4 = 0
            index_5 = 0
            index_6 = 0 
            for each_servo in ServosDictionary.keys():
                # Get Dynamixel present Moving value
                if each_servo in port_0_list:
                    dxl_error = groupSyncRead_Error_1.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_1.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_0[index_1] == 0):
                        isStopped_0[index_1] = 1
                    index_1 += 1
                if each_servo in port_1_list:
                    dxl_error = groupSyncRead_Error_2.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_2.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_1[index_2] == 0):
                        isStopped_1[index_2] = 1
                    index_2 += 1
                if each_servo in port_2_list:
                    dxl_error = groupSyncRead_Error_3.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_3.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_2[index_3] == 0):
                        isStopped_2[index_3] = 1
                    index_3 += 1
                if each_servo in port_3_list:
                    dxl_error = groupSyncRead_Error_4.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_4.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_3[index_4] == 0):
                        isStopped_3[index_4] = 1
                    index_4 += 1
                if each_servo in port_4_list:
                    dxl_error = groupSyncRead_Error_5.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_5.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_4[index_5] == 0):
                        isStopped_4[index_5] = 1
                    index_5 += 1
                if each_servo in port_5_list:
                    dxl_error = groupSyncRead_Error_6.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_6.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_5[index_6] == 0):
                        isStopped_5[index_6] = 1
                    index_6 += 1
            if (0 in isStopped_0) or (0 in isStopped_1) or (0 in isStopped_2) or (0 in isStopped_3) or (0 in isStopped_4) or (0 in isStopped_5):
                if ports_used[0] == 1:
                    groupSyncRead_Moving_1.clearParam()
                    groupSyncRead_Error_1.clearParam()
                if ports_used[1] == 1:
                    groupSyncRead_Moving_2.clearParam()
                    groupSyncRead_Error_2.clearParam()
                if ports_used[2] == 1:
                    groupSyncRead_Moving_3.clearParam()
                    groupSyncRead_Error_3.clearParam()
                if ports_used[3] == 1:
                    groupSyncRead_Moving_4.clearParam()
                    groupSyncRead_Error_4.clearParam()
                if ports_used[4] == 1:
                    groupSyncRead_Moving_5.clearParam()
                    groupSyncRead_Error_5.clearParam()
                if ports_used[5] == 1:
                    groupSyncRead_Moving_6.clearParam()
                    groupSyncRead_Error_6.clearParam()
                for each_servo in ServosDictionary.keys():
                    if each_servo in port_0_list:
                        groupSyncRead_Moving_1.addParam(each_servo)
                        groupSyncRead_Error_1.addParam(each_servo)
                    elif each_servo in port_1_list:
                        groupSyncRead_Moving_2.addParam(each_servo)
                        groupSyncRead_Error_2.addParam(each_servo)
                    elif each_servo in port_2_list:
                        groupSyncRead_Moving_3.addParam(each_servo)
                        groupSyncRead_Error_3.addParam(each_servo)
                    elif each_servo in port_3_list:
                        groupSyncRead_Moving_4.addParam(each_servo)
                        groupSyncRead_Error_4.addParam(each_servo)
                    elif each_servo in port_4_list:
                        groupSyncRead_Moving_5.addParam(each_servo)
                        groupSyncRead_Error_5.addParam(each_servo)
                    elif each_servo in port_5_list:
                        groupSyncRead_Moving_6.addParam(each_servo)
                        groupSyncRead_Error_6.addParam(each_servo)
            else:
                break
                
def Move_Spider_Down(TilibotGUI, servo_list, ServosDictionary, port_hand_list, port_servo_dict, packetHandler, in_home_speed, DigitalOnly):
    if DigitalOnly == True:
        pass
    elif DigitalOnly == False:
        ports_used = [0, 0, 0, 0, 0, 0]
        for used_servo in servo_list:
            if any(port_servo_dict[used_servo] == port_hand_list[0] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_1 = GroupSyncWrite(port_hand_list[0], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_1 = GroupSyncRead(port_hand_list[0],packetHandler, AddrDict[26], 1)
                ports_used[0] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[1] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_2 = GroupSyncWrite(port_hand_list[1], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_2 = GroupSyncRead(port_hand_list[1],packetHandler, AddrDict[26], 1)
                ports_used[1] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[2] for used_servo in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_3 = GroupSyncWrite(port_hand_list[2], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_3 = GroupSyncRead(port_hand_list[2],packetHandler, AddrDict[26], 1)
                ports_used[2] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[3] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_4 = GroupSyncWrite(port_hand_list[3], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_4 = GroupSyncRead(port_hand_list[3],packetHandler, AddrDict[26], 1)
                ports_used[3] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[4] for used_servo in servo_list):
                 # Initialize GroupSyncWrite instance
                groupSyncWritePOS_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_5 = GroupSyncWrite(port_hand_list[4], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_5 = GroupSyncRead(port_hand_list[4],packetHandler, AddrDict[26], 1)
                ports_used[4] = 1
            else:
                pass
            if any(port_servo_dict[used_servo] == port_hand_list[5] for used_servo in servo_list):
                # Initialize GroupSyncWrite instance
                groupSyncWritePOS_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[37], 4)
                # Initialize GroupSyncWrite instance
                groupSyncWriteVEL_6 = GroupSyncWrite(port_hand_list[5], packetHandler, AddrDict[36], 4)
                groupSyncRead_Moving_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[39], 1)
                groupSyncRead_Error_6 = GroupSyncRead(port_hand_list[5],packetHandler, AddrDict[26], 1)
                ports_used[5] = 1
            else:
                pass
        port_0_count = 0
        port_0_list = []
        port_1_count = 0
        port_1_list = []
        port_2_count = 0
        port_2_list = []
        port_3_count = 0
        port_3_list = []
        port_4_count = 0
        port_4_list = []
        port_5_count = 0
        port_5_list = []
        for each_servo in servo_list:
            if (ServosDictionary[each_servo].port_used == 0):
                port_0_count += 1
                port_0_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 1):
                port_1_count += 1
                port_1_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 2):
                port_2_count += 1
                port_2_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 3):
                port_3_count += 1
                port_3_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 4):
                port_4_count += 1
                port_4_list.append(each_servo)
            elif (ServosDictionary[each_servo].port_used == 5):
                port_5_count += 1
                port_5_list.append(each_servo)
        GoalVelocity = []
        GoalPosition = []
        if ports_used[0] == 1:
            isStopped_0 = [0] * port_0_count
        else:
            isStopped_0 = []
            
        if ports_used[1] == 1:
            isStopped_1 = [0] * port_1_count
        else:
            isStopped_1 = []
            
        if ports_used[2] == 1:
            isStopped_2 = [0] * port_2_count
        else:
            isStopped_2 = []
            
        if ports_used[3] == 1:
            isStopped_3 = [0] * port_3_count
        else:
            isStopped_3 = []
            
        if ports_used[4] == 1:
            isStopped_4 = [0] * port_4_count
        else:
            isStopped_4 = []
            
        if ports_used[5] == 1:
            isStopped_5 = [0] * port_5_count
        else:
            isStopped_5 = []
            
        for index, each_servo in enumerate(servo_list):
            GoalVelocity.append(FormatSendData(int(in_home_speed)))
            GoalPosition.append(FormatSendData(SPIDER_DOWN[each_servo]))
            if each_servo in port_0_list:
                dxl_addparam_result = groupSyncWriteVEL_1.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_1.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            elif each_servo in port_1_list:
                dxl_addparam_result = groupSyncWriteVEL_2.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_2.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            elif each_servo in port_2_list:
                dxl_addparam_result = groupSyncWriteVEL_3.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_3.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            elif each_servo in port_3_list:
                dxl_addparam_result = groupSyncWriteVEL_4.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_4.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            elif each_servo in port_4_list:
                dxl_addparam_result = groupSyncWriteVEL_5.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_5.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            elif each_servo in port_5_list:
                dxl_addparam_result = groupSyncWriteVEL_6.addParam(each_servo,GoalVelocity[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam velocity failed" % each_servo)
                    return
                dxl_addparam_result = groupSyncWritePOS_6.addParam(each_servo,GoalPosition[index])
                if dxl_addparam_result != True:
                    print("[ID:%03d] groupSyncWrite SPIDER-DOWN addparam position failed" % each_servo)
                    return
            else:
                print('Error in servo list. Please fix and try again.')
        if ports_used[0] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Veloctiy:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Velocity:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Velocity:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Veloctiy:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Velocity:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal velocity
            dxl_comm_result = groupSyncWriteVEL_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Velocity:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWriteVEL_6.clearParam()

        if ports_used[0] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_1.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_1.clearParam()
        if ports_used[1] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_2.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_2.clearParam()
        if ports_used[2] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_3.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_3.clearParam()
        if ports_used[3] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_4.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_4.clearParam()
        if ports_used[4] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_5.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_5.clearParam()
        if ports_used[5] == 1:
            # Syncwrite goal position
            dxl_comm_result = groupSyncWritePOS_6.txPacket()
            if dxl_comm_result != COMM_SUCCESS:
                print("%s - SPIDER-DOWN Position:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            # Clear syncwrite parameter storage
            groupSyncWritePOS_6.clearParam()

        for each_servo in ServosDictionary.keys():
            if each_servo in port_0_list:
                groupSyncRead_Moving_1.addParam(each_servo)
                groupSyncRead_Error_1.addParam(each_servo)
            elif each_servo in port_1_list:
                groupSyncRead_Moving_2.addParam(each_servo)
                groupSyncRead_Error_2.addParam(each_servo)
            elif each_servo in port_2_list:
                groupSyncRead_Moving_3.addParam(each_servo)
                groupSyncRead_Error_3.addParam(each_servo)
            if each_servo in port_3_list:
                groupSyncRead_Moving_4.addParam(each_servo)
                groupSyncRead_Error_4.addParam(each_servo)
            elif each_servo in port_4_list:
                groupSyncRead_Moving_5.addParam(each_servo)
                groupSyncRead_Error_5.addParam(each_servo)
            elif each_servo in port_5_list:
                groupSyncRead_Moving_6.addParam(each_servo)
                groupSyncRead_Error_6.addParam(each_servo)
        while 1:
            # Syncread Moving Value
            if ports_used[0] == 1:
                dxl_comm_result = groupSyncRead_Moving_1.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_1.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 1" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[1] == 1:
                dxl_comm_result = groupSyncRead_Moving_2.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_2.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 2" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[2] == 1:
                dxl_comm_result = groupSyncRead_Moving_3.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_3.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 3" % packetHandler.getTxRxResult(dxl_comm_result))    
            if ports_used[3] == 1:
                dxl_comm_result = groupSyncRead_Moving_4.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_4.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 4" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[4] == 1:
                dxl_comm_result = groupSyncRead_Moving_5.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_5.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 5" % packetHandler.getTxRxResult(dxl_comm_result))
            if ports_used[5] == 1:
                dxl_comm_result = groupSyncRead_Moving_6.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - SPIDER-DOWN Moving Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
                dxl_comm_result = groupSyncRead_Error_6.txRxPacket()
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s - Hardware Error Value:Port 6" % packetHandler.getTxRxResult(dxl_comm_result))
            index_1 = 0
            index_2 = 0
            index_3 = 0 
            index_4 = 0
            index_5 = 0
            index_6 = 0 
            for each_servo in ServosDictionary.keys():
                # Get Dynamixel present Moving value
                if each_servo in port_0_list:
                    dxl_error = groupSyncRead_Error_1.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_1.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_0[index_1] == 0):
                        isStopped_0[index_1] = 1
                    index_1 += 1
                if each_servo in port_1_list:
                    dxl_error = groupSyncRead_Error_2.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_2.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_1[index_2] == 0):
                        isStopped_1[index_2] = 1
                    index_2 += 1
                if each_servo in port_2_list:
                    dxl_error = groupSyncRead_Error_3.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_3.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_2[index_3] == 0):
                        isStopped_2[index_3] = 1
                    index_3 += 1
                if each_servo in port_3_list:
                    dxl_error = groupSyncRead_Error_4.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_4.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_3[index_4] == 0):
                        isStopped_3[index_4] = 1
                    index_4 += 1
                if each_servo in port_4_list:
                    dxl_error = groupSyncRead_Error_5.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_5.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_4[index_5] == 0):
                        isStopped_4[index_5] = 1
                    index_5 += 1
                if each_servo in port_5_list:
                    dxl_error = groupSyncRead_Error_6.getData(each_servo, AddrDict[26],1)
                    if (dxl_error == 0):
                        pass
                    else:
                        print('servo ' + str(each_servo) + ' error value: ' + str(dxl_error))
                        print(ErrorChecker(dxl_error))
                        TilibotGUI.change_servo_color(each_servo,"blue")
                    dxl_mov = groupSyncRead_Moving_6.getData(each_servo, AddrDict[39],1)
                    if (dxl_mov == 0) and (isStopped_5[index_6] == 0):
                        isStopped_5[index_6] = 1
                    index_6 += 1
            if (0 in isStopped_0) or (0 in isStopped_1) or (0 in isStopped_2):
                if ports_used[0] == 1:
                    groupSyncRead_Moving_1.clearParam()
                    groupSyncRead_Error_1.clearParam()
                if ports_used[1] == 1:
                    groupSyncRead_Moving_2.clearParam()
                    groupSyncRead_Error_2.clearParam()
                if ports_used[2] == 1:
                    groupSyncRead_Moving_3.clearParam()
                    groupSyncRead_Error_3.clearParam()
                if ports_used[3] == 1:
                    groupSyncRead_Moving_4.clearParam()
                    groupSyncRead_Error_4.clearParam()
                if ports_used[4] == 1:
                    groupSyncRead_Moving_5.clearParam()
                    groupSyncRead_Error_5.clearParam()
                if ports_used[5] == 1:
                    groupSyncRead_Moving_6.clearParam()
                    groupSyncRead_Error_6.clearParam()
                for each_servo in ServosDictionary.keys():
                    if each_servo in port_0_list:
                        groupSyncRead_Moving_1.addParam(each_servo)
                        groupSyncRead_Error_1.addParam(each_servo)
                    elif each_servo in port_1_list:
                        groupSyncRead_Moving_2.addParam(each_servo)
                        groupSyncRead_Error_2.addParam(each_servo)
                    elif each_servo in port_2_list:
                        groupSyncRead_Moving_3.addParam(each_servo)
                        groupSyncRead_Error_3.addParam(each_servo)
                    elif each_servo in port_3_list:
                        groupSyncRead_Moving_4.addParam(each_servo)
                        groupSyncRead_Error_4.addParam(each_servo)
                    elif each_servo in port_4_list:
                        groupSyncRead_Moving_5.addParam(each_servo)
                        groupSyncRead_Error_5.addParam(each_servo)
                    elif each_servo in port_5_list:
                        groupSyncRead_Moving_6.addParam(each_servo)
                        groupSyncRead_Error_6.addParam(each_servo)
            else:
                break

def Write_Settings_Doc(Config_Dictionary,filename_for_save):
    with open(filename_for_save, 'w') as file:
        yaml.dump(Config_Dictionary, file)

def CleanUp(ServosDictionary,port_hand_list):
    for each_servo in ServosDictionary.values():
        if (each_servo.port_used == 0):
            each_servo.ToggleTorque(0,port_hand_list[0])
        elif (each_servo.port_used == 1):
            each_servo.ToggleTorque(0,port_hand_list[1])
        elif (each_servo.port_used == 2):
            each_servo.ToggleTorque(0,port_hand_list[2])
        elif (each_servo.port_used == 3):
            each_servo.ToggleTorque(0,port_hand_list[3])
        elif (each_servo.port_used == 4):
            each_servo.ToggleTorque(0,port_hand_list[4])
        elif (each_servo.port_used == 5):
            each_servo.ToggleTorque(0,port_hand_list[5])
        each_servo.__del__()
    for each_port_obj in port_hand_list:
        if each_port_obj != 0:
            each_port_obj.closePort()

def Reset_For_Run(ServosDictionary,port_hand_list):
    for each_servo in ServosDictionary.values():
        if (each_servo.port_used == 0):
            each_servo.ToggleTorque(0,port_hand_list[0])
        elif (each_servo.port_used == 1):
            each_servo.ToggleTorque(0,port_hand_list[1])
        elif (each_servo.port_used == 2):
            each_servo.ToggleTorque(0,port_hand_list[2])
        elif (each_servo.port_used == 3):
            each_servo.ToggleTorque(0,port_hand_list[3])
        elif (each_servo.port_used == 4):
            each_servo.ToggleTorque(0,port_hand_list[4])
        elif (each_servo.port_used == 5):
            each_servo.ToggleTorque(0,port_hand_list[5])
    
def ShutDown():
    print("+-+-+-+-+Shutting down system.+-+-+-+-+\n")
    # Turn off power to external boards and other systems
    print("Thank you for using Tilibot!\n")

## Tilibot Functions
