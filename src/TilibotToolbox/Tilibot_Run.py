## Tilibot Run

import os
import numpy as np
import time
import pandas as pd
from Tilibot_Constants import *
from Tilibot_Functions import *
from Tilibot_Classes import *
from dynamixel_sdk import *
# from threading import Thread

GUI_or_TERMINAL = 1 # -1 for GUI, +1 for Terminal

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

config_array = read_config_file("Tilibot_Configuration_File.yml")
[invalidate_value, confirmed_action] = check_config_file(config_array,GUI_or_TERMINAL)
record_array = RecordPreferences(config_array)
stride_numbers = (config_array[4], config_array[2],config_array[3]) # Stride amount and positions per stride

if invalidate_value == True:
    print("Shutting Down Tilibot...")
    exit()

if config_array[32] == True:
    # DigitalSetup(config_array)
    pass
elif config_array[32] == False:
    portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler = Packet_Port_Setup(config_array[0])
    port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]
    dxl_data_list = PingServos(port_hand_list,packetHandler)
    port_servo_dict, port_used_dict = Port_Servo_Assign(dxl_data_list,port_hand_list)
else:
    print("Error in run option. Please fix and try again.")

preprocessed_positions = ReadServoAngles(config_array[1])
print("Angle .CSV data read.")
PositionsMatrix = PostProcessPositions(preprocessed_positions)
print("Positions Matrix Created.")
SpeedMatrix = DetermineSpeeds(config_array[3],PositionsMatrix,config_array[2],config_array)
print("Speeds Calculated.")

Obj_list = []
ServosDictionary = Create_DigitalServos(config_array,port_used_dict,PositionsMatrix,SpeedMatrix)
Obj_list.append(ServosDictionary)

# Limb Objects may not be necessary 
if any(config_array[6]):
    LimbDictionary = Create_DigitalLimbs(config_array[6],ServosDictionary)
    Obj_list.append(LimbDictionary)

# Body Object may not be necessary
#if all(limb_present == True for limb_present in config_array[7]):
#    TilibotBody = Create_DigitalBody(LimbDictionary)
#    Obj_list.append(TilibotBody)

if confirmed_action[0] == 1: # Move Single Servo
    servo_to_move = ServosDictionary[confirmed_action[1]]
    servo_to_move.InitialSetup(port_servo_dict[servo_to_move.ID],config_array[31])
    servo_to_move.ToggleTorque(1,port_servo_dict[servo_to_move.ID])
    servo_to_move.MoveHome(config_array[17],port_servo_dict[servo_to_move.ID])
    print("Servo has been moved to Home Position.")
    print("Please press enter when you are ready to begin.")
    getch()
    start_time = time.time()
    out_data = servo_to_move.ContinuousMove(port_servo_dict[servo_to_move.ID], stride_numbers, record_array, start_time)
    if config_array[32] == False:
        if record_array[0] == True:
            Write_Doc(record_array,out_data)
elif confirmed_action[0] == 2: # Move Numerous Servos
    while 1:
        if (config_array[28] == True):
            for each_spine_servo in list(set(ServosDictionary.keys()).intersection(set(NECK))):
                ServosDictionary[each_spine_servo].InitialSetup(port_servo_dict[each_spine_servo],config_array[31])
                ServosDictionary[each_spine_servo].ToggleTorque(1,port_servo_dict[each_spine_servo])
        if (config_array[29] == True):
            for each_spine_servo in list(set(ServosDictionary.keys()).intersection(set(SPINE))):
                ServosDictionary[each_spine_servo].InitialSetup(port_servo_dict[each_spine_servo],config_array[31])
                ServosDictionary[each_spine_servo].ToggleTorque(1,port_servo_dict[each_spine_servo])
        if (config_array[30] == True):
            for each_spine_servo in list(set(ServosDictionary.keys()).intersection(set(TAIL))):
                ServosDictionary[each_spine_servo].InitialSetup(port_servo_dict[each_spine_servo],config_array[31])
                ServosDictionary[each_spine_servo].ToggleTorque(1,port_servo_dict[each_spine_servo])
        print("#############################################################")
        print("\nStraightening Spine - ")
        StraightenSpine(ServosDictionary,port_hand_list,packetHandler,config_array[32])
        print("Spine Straightened. Moving to Legs.\n")
        for each_servo in confirmed_action[1]:
            ServosDictionary[each_servo].InitialSetup(port_servo_dict[each_servo],config_array[31])
            ServosDictionary[each_servo].ToggleTorque(1,port_servo_dict[each_servo])
    # Move Servo to Spider Stance
    # Move Servos to Floor and Push Up
        Move_Spider_Up(confirmed_action[1], ServosDictionary, port_hand_list, port_servo_dict, packetHandler,config_array[17],config_array[32])
        time.sleep(2)
        Move_Spider_Down(confirmed_action[1], ServosDictionary, port_hand_list, port_servo_dict, packetHandler,config_array[17], config_array[32])
        time.sleep(2)
        for each_servo in confirmed_action[1]:
            ServosDictionary[each_servo].MoveHome(config_array[17],port_servo_dict[each_servo])
        print("Servos have been moved to Home Position.")
        print("Please press enter when you are ready to begin.\n")
        getch()
        print("*********************************************************")
        start_time = time.time()
        out_data = MoveNumerousServos(confirmed_action[1],ServosDictionary,port_hand_list,port_servo_dict,
            packetHandler,stride_numbers,record_array, start_time,config_array[32])
        record_time = time.time()
        end_time = record_time - start_time
        print("\n*********************************************************")
        print("End Time: %f" %(end_time))
        print("*********************************************************\n")
        if config_array[32] == False:
            if record_array[0] == True:
                Write_Doc(record_array,out_data)
        break_var = 0
        while break_var == 0:        
            run_again = input("Run again?(Y/n)")
            if run_again.lower() == "y" or run_again.lower() == "yes":
                break_var = 1
                break
            elif (run_again.lower() == "n" or run_again.lower() == "no"):
                break_var = -1
                break
            else:
                print("Not a recognized option. Please try again.\n")
        if break_var == 1:
            continue
        elif break_var == -1:
            break
print("Shutting down Tilibot. Please press enter.")
getch()
CleanUp(ServosDictionary,port_hand_list)
ShutDown()
