## Tilibot Tinker

# For manually moving servos and limbs
# and for tweaking variables for test runs

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *

def DisplayServoTraits():
    print("========Servo Traits:========\n")
    print("1: Model Number")
    print("2: Model Information")
    print("3: Firmware Version")
    print("4: ID")
    print("5: Baud Rate")
    print("6: Return Delay Time")
    print("7: Drive Mode")
    print("8: Operating Mode")
    print("9: Protocol Type")
    print("10: Homing Offset")
    print("11: Moving Threshold")
    print("12: Temperature Limit")
    print("13: Max Voltage Limit")
    print("14: Min Voltage Limit")
    print("15: PWM Limit")
    print("16: Current Limit")
    print("17: Acceleration Limit")
    print("18: Velocity Limit")
    print("19: Max Position Limit")
    print("20: Min Position Limit")
    print("21: Shutdown")
    print("22: Torque Toggle")
    print("23: LED")
    print("24: Status Return Level")
    print("25: Registered Instruction")
    print("26: Hardware Error Status")
    print("27: Velocity I Gain")
    print("28: Velocity P Gain")
    print("29: Position D Gain")
    print("30: Position I Gain")
    print("31: Position P Gain")
    print("32: Goal PWM")
    print("33: Goal Current")
    print("34: Goal Velocity")
    print("35: Profile Acceleration")
    print("36: Profile Velocity")
    print("37: Goal Position")
    print("38: Realtime Tick")
    print("39: Moving")
    print("40: Moving Status")
    print("41: Present PWM")
    print("42: Present Current")
    print("43: Present Velocity")
    print("44: Present Position")
    print("45: Velocity Trajectory")
    print("46: Position Trajectory")
    print("47: Present Input Voltage")
    print("48: Present Temperature\n")

def DataAddrConversion(DesiredData):
    DataAddr = -1
    # Get the address of the desired data trait, used in conjuction with ReadTrait and WriteTrait
    if (DesiredData >= 1 and DesiredData <= 48):
        DataAddr = AddrDict[DesiredData]
    else:
        print("That's not a recognized trait selection, please try again!\n")
    return DataAddr if DataAddr is not -1 else -1

def ReadTraitData(DesiredData,DesiredServo,portHandler,packetHandler):
    # Obtain from the desired servo the desired trait data


    DataAddr = DataAddrConversion(DesiredData)

    if (DesiredData == 1):
        ModelNumber, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Model Number: %03d" % (DesiredServo, ModelNumber))
    elif (DesiredData == 2):
        ModelInfo, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Model Information: %03d" % (DesiredServo, ModelInfo))
    elif (DesiredData == 3):
        FirmwareVer, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Firmware Version: %03d" % (DesiredServo, FirmwareVer))
    elif (DesiredData == 4):
        IDnum, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] ID Number: %03d" % (DesiredServo, IDnum))
    elif (DesiredData == 5):
        BaudRate, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Baud Rate: %03d" % (DesiredServo, BaudRate))
    elif (DesiredData == 6):
        RetDelayTime, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Return Delay Time: %03d" % (DesiredServo, RetDelayTime))
    elif (DesiredData == 7):
        DriveMode, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Drive Mode: %03d" % (DesiredServo, DriveMode))
    elif (DesiredData == 8):
        OperateMode, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Operating Mode: %03d" % (DesiredServo, OperateMode))
    elif (DesiredData == 9):
        ProtocType, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Protocol Type: %03d" % (DesiredServo, ProtocType))
    elif (DesiredData == 10):
        HomeOffset, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Homing Offset: %03d" % (DesiredServo, HomeOffset))
    elif (DesiredData == 11):
        MoveThreshold, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Threshold: %03d" % (DesiredServo, MoveThreshold))
    elif (DesiredData == 12):
        TempLimit, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Temperature Limit: %03d" % (DesiredServo, TempLimit))
    elif (DesiredData == 13):
        MaxVoltLimit, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Max Voltage Limit: %03d" % (DesiredServo, MaxVoltLimit))
    elif (DesiredData == 14):
        MinVoltLimit, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Min Voltage Limit: %03d" % (DesiredServo, MinVoltLimit))
    elif (DesiredData == 15):
        PWMlimit, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] PWM Limit: %03d" % (DesiredServo, PWMlimit))
    elif (DesiredData == 16):
        CurrLimit, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Current Limit: %03d" % (DesiredServo, CurrLimit))
    elif (DesiredData == 17):
        AccLimit, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Acceleration Limit: %03d" % (DesiredServo, AccLimit))
    elif (DesiredData == 18):
        VelLimit, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity Limit: %03d" % (DesiredServo, VelLimit))
    elif (DesiredData == 19):
        MaxPosLimit, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Max Position Limit: %03d" % (DesiredServo, MaxPosLimit))
    elif (DesiredData == 20):
        MinPosLimit, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Min Position Limit: %03d" % (DesiredServo, MinPosLimit))
    elif (DesiredData == 21):
        ShutdownVal, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Shutdown Value: %03d" % (DesiredServo, ShutdownVal))
    elif (DesiredData == 22):
        TorqToggle, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Torque Toggle Value: %03d" % (DesiredServo, TorqToggle))
    elif (DesiredData == 23):
        LEDtoggle, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] LED Toggle Value: %03d" % (DesiredServo, LEDtoggle))
    elif (DesiredData == 24):
        StatusRetLevel, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Status Return Level: %03d" % (DesiredServo, StatusRetLevel))
    elif (DesiredData == 25):
        RegInstruction, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Registered Instruction: %03d" % (DesiredServo, RegInstruction))
    elif (DesiredData == 26):
        HardErrStat, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Hardware Error Status: %03d" % (DesiredServo, HardErrStat))
    elif (DesiredData == 27):
        VelIgain, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity I Gain: %03d" % (DesiredServo, VelIgain))
    elif (DesiredData == 28):
        VelPgain, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity P Gain: %03d" % (DesiredServo, VelPgain))
    elif (DesiredData == 29):
        PosDgain, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position D Gain: %03d" % (DesiredServo, PosDgain))
    elif (DesiredData == 30):
        PosIgain, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position I Gain: %03d" % (DesiredServo, PosIgain))
    elif (DesiredData == 31):
        PosPgain, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position P Gain: %03d" % (DesiredServo, PosPgain))
    elif (DesiredData == 32):
        GoalPWM, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal PWM: %03d" % (DesiredServo, GoalPWM))
    elif (DesiredData == 33):
        GoalCurr, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Current: %03d" % (DesiredServo, GoalCurr))
    elif (DesiredData == 34):
        GoalVel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Velocity: %03d" % (DesiredServo, GoalVel))
    elif (DesiredData == 35):
        ProfAccel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Profile Acceleration: %03d" % (DesiredServo, ProfAccel))
    elif (DesiredData == 36):
        ProfVel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Profile Velocity: %03d" % (DesiredServo, ProfVel))
    elif (DesiredData == 37):
        GoalPos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Position: %03d" % (DesiredServo, GoalPos))
    elif (DesiredData == 38):
        RealtimeTick, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Realtime Tick: %03d" % (DesiredServo, RealtimeTick))
    elif (DesiredData == 39):
        MovingVal, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Value: %03d" % (DesiredServo, MovingVal))
    elif (DesiredData == 40):
        MovingStat, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Status: %03d" % (DesiredServo, MovingStat))
    elif (DesiredData == 41):
        PresentPWM, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present PWM: %03d" % (DesiredServo, PresentPWM))
    elif (DesiredData == 42):
        PresentCurr, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Current: %03d" % (DesiredServo, PresentCurr))
    elif (DesiredData == 43):
        PresentVel, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Velocity: %03d" % (DesiredServo, PresentVel))
    elif (DesiredData == 44):
        PresentPos, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Position: %03d" % (DesiredServo, PresentPos))
    elif (DesiredData == 45):
        VelTraj, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity Trajectory: %03d" % (DesiredServo, VelTraj))
    elif (DesiredData == 46):
        PosTraj, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position Trajectory: %03d" % (DesiredServo, PosTraj))
    elif (DesiredData == 47):
        PresInVoltage, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Input Voltage: %03d" % (DesiredServo, PresInVoltage))
    elif (DesiredData == 48):
        PresTemp, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DesiredServo, DataAddr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Temperature: %03d" % (DesiredServo, PresTemp))
    else:
        print("Data does not have a matchable address")
    # Close port
    portHandler.closePort()

def WriteTraitData(DesiredData,DesiredValue,DesiredServo,portHandler,packetHandler):
    # Change the desired trait data of the desired servo

    DataAddr = DataAddrConversion(DesiredData)

    if (DesiredData == 1):
        ModelNumber = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, ModelNumber)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Model Number Changed To: %03d" % (DesiredServo, ModelNumber))
    elif (DesiredData == 2):
        ModelInfo = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, ModelInfo)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Model Information Changed To: %03d" % (DesiredServo, ModelInfo))
    elif (DesiredData == 3):
        FirmwareVer = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, FirmwareVer)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Firmware Version Changed To: %03d" % (DesiredServo, FirmwareVer))
    elif (DesiredData == 4):
        IDnum = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, IDnum)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] ID Number Changed To: %03d" % (DesiredServo, IDnum))
    elif (DesiredData == 5):
        BaudRate = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, BaudRate)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Baud Rate Changed To: %03d" % (DesiredServo, BaudRate))
    elif (DesiredData == 6):
        RetDelayTime = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, RetDelayTime)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Return Delay Time Changed To: %03d" % (DesiredServo, RetDelayTime))
    elif (DesiredData == 7):
        DriveMode = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, DriveMode)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Drive Mode Changed To: %03d" % (DesiredServo, DriveMode))
    elif (DesiredData == 8):
        OperateMode = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, OperateMode)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Operating Mode Changed To: %03d" % (DesiredServo, OperateMode))
    elif (DesiredData == 9):
        ProtocType = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, ProtocType)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Protocol Type Changed To: %03d" % (DesiredServo, ProtocType))
    elif (DesiredData == 10):
        HomeOffset = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, HomeOffset)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Homing Offset Changed To: %03d" % (DesiredServo, HomeOffset))
    elif (DesiredData == 11):
        MoveThreshold = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, MoveThreshold)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Threshold Changed To: %03d" % (DesiredServo, MoveThreshold))
    elif (DesiredData == 12):
        TempLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, TempLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Temperature Limit Changed To: %03d" % (DesiredServo, TempLimit))
    elif (DesiredData == 13):
        MaxVoltLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, MaxVoltLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Max Voltage Limit Changed To: %03d" % (DesiredServo, MaxVoltLimit))
    elif (DesiredData == 14):
        MinVoltLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, MinVoltLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Min Voltage Limit Changed To: %03d" % (DesiredServo, MinVoltLimit))
    elif (DesiredData == 15):
        PWMlimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PWMlimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] PWM Limit Changed To: %03d" % (DesiredServo, PWMlimit))
    elif (DesiredData == 16):
        CurrLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, CurrLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Current Limit Changed To: %03d" % (DesiredServo, CurrLimit))
    elif (DesiredData == 17):
        AccLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, AccLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Acceleration Limit Changed To: %03d" % (DesiredServo, AccLimit))
    elif (DesiredData == 18):
        VelLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, VelLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity Limit Changed To: %03d" % (DesiredServo, VelLimit))
    elif (DesiredData == 19):
        MaxPosLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, MaxPosLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Max Position Limit Changed To: %03d" % (DesiredServo, MaxPosLimit))
    elif (DesiredData == 20):
        MinPosLimit = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, MinPosLimit)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Min Position Limit Changed To: %03d" % (DesiredServo, MinPosLimit))
    elif (DesiredData == 21):
        ShutdownVal = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, ShutdownVal)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Shutdown Value Changed To: %03d" % (DesiredServo, ShutdownVal))
    elif (DesiredData == 22):
        TorqToggle = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, TorqToggle)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Torque Toggle Value Changed To: %03d" % (DesiredServo, TorqToggle))
    elif (DesiredData == 23):
        LEDtoggle = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, LEDtoggle)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] LED Toggle Value Changed To: %03d" % (DesiredServo, LEDtoggle))
    elif (DesiredData == 24):
        StatusRetLevel = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, StatusRetLevel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Status Return Level Changed To: %03d" % (DesiredServo, StatusRetLevel))
    elif (DesiredData == 25):
        RegInstruction = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, RegInstruction)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Registered Instruction Changed To: %03d" % (DesiredServo, RegInstruction))
    elif (DesiredData == 26):
        HardErrStat = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, HardErrStat)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Hardware Error Status Changed To: %03d" % (DesiredServo, HardErrStat))
    elif (DesiredData == 27):
        VelIgain = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, VelIgain)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity I Gain Changed To: %03d" % (DesiredServo, VelIgain))
    elif (DesiredData == 28):
        VelPgain = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, VelPgain)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity P Gain Changed To: %03d" % (DesiredServo, VelPgain))
    elif (DesiredData == 29):
        PosDgain = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PosDgain)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position D Gain Changed To: %03d" % (DesiredServo, PosDgain))
    elif (DesiredData == 30):
        PosIgain = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PosIgain)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position I Gain Changed To: %03d" % (DesiredServo, PosIgain))
    elif (DesiredData == 31):
        PosPgain = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PosPgain)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position P Gain Changed To: %03d" % (DesiredServo, PosPgain))
    elif (DesiredData == 32):
        GoalPWM = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, GoalPWM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal PWM Changed To: %03d" % (DesiredServo, GoalPWM))
    elif (DesiredData == 33):
        GoalCurr = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, GoalCurr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Current Changed To: %03d" % (DesiredServo, GoalCurr))
    elif (DesiredData == 34):
        GoalVel = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, GoalVel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Velocity Changed To: %03d" % (DesiredServo, GoalVel))
    elif (DesiredData == 35):
        ProfAccel = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, ProfAccel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Profile Acceleration Changed To: %03d" % (DesiredServo, ProfAccel))
    elif (DesiredData == 36):
        ProfVel = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, ProfVel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Profile Velocity Changed To: %03d" % (DesiredServo, ProfVel))
    elif (DesiredData == 37):
        GoalPos = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, GoalPos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Goal Position Changed To: %03d" % (DesiredServo, GoalPos))
    elif (DesiredData == 38):
        RealtimeTick = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, RealtimeTick)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Realtime Tick Changed To: %03d" % (DesiredServo, RealtimeTick))
    elif (DesiredData == 39):
        MovingVal = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, MovingVal)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Value Changed To: %03d" % (DesiredServo, MovingVal))
    elif (DesiredData == 40):
        MovingStat = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, MovingStat)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Moving Status Changed To: %03d" % (DesiredServo, MovingStat))
    elif (DesiredData == 41):
        PresentPWM = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PresentPWM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present PWM Changed To: %03d" % (DesiredServo, PresentPWM))
    elif (DesiredData == 42):
        PresentCurr = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PresentCurr)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Current Changed To: %03d" % (DesiredServo, PresentCurr))
    elif (DesiredData == 43):
        PresentVel = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, PresentVel)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Velocity Changed To: %03d" % (DesiredServo, PresentVel))
    elif (DesiredData == 44):
        PresentPos = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, PresentPos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Position Changed To: %03d" % (DesiredServo, PresentPos))
    elif (DesiredData == 45):
        VelTraj = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, VelTraj)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Velocity Trajectory Changed To: %03d" % (DesiredServo, VelTraj))
    elif (DesiredData == 46):
        PosTraj = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DesiredServo, DataAddr, PosTraj)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Position Trajectory Changed To: %03d" % (DesiredServo, PosTraj))
    elif (DesiredData == 47):
        PresInVoltage = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DesiredServo, DataAddr, PresInVoltage)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Input Voltage Changed To: %03d" % (DesiredServo, PresInVoltage))
    elif (DesiredData == 48):
        PresTemp = DesiredValue
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DesiredServo, DataAddr, PresTemp)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        print("[ID:%03d] Present Temperature Changed To: %03d" % (DesiredServo, PresTemp))
    else:
        print("Data does not have a matchable address")

    # Close port
    portHandler.closePort()

print("Welcome to Tilibot Tinker.")
print("Here you can tweak servo traits and move servos to desired positions manually.")
print("Press any key to begin Tinkering.")
getch()
config_array = read_config_file("Tilibot_Configuration_File.yml")
[portHandler_1, portHandler_2, portHandler_3, portHandler_4, packetHandler] = Packet_Port_Setup(config_array)
port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4]
dxl_data_list = PingServos(port_hand_list,packetHandler)
port_servo_dict, port_used_dict = Port_Servo_Assign(dxl_data_list,port_hand_list)
while 1:
    ReadOrWrite = int(input("Would you like to read(1), write(2), or exit(0)?: "))
    if ReadOrWrite == 1:
        print("ENTERING READ MODE\n")
        print("The servo traits you can read are as follows: ")
        DisplayServoTraits()
        Selection1 = int(input("Enter the Trait Number you'd like to extract: "))
        Selection2 = int(input("Enter the Servo you'd like to extract the Trait from: "))
        # Need Error checking for both
        if port_used_dict[Selection2] == 0:
            ReadTraitData(Selection1,Selection2,port_hand_list[0],packetHandler)
        elif port_used_dict[Selection2] == 1:
            ReadTraitData(Selection1,Selection2,port_hand_list[1],packetHandler)
        elif port_used_dict[Selection2] == 2:
            ReadTraitData(Selection1,Selection2,port_hand_list[2],packetHandler)
        else:
            print("Not a recognized or connected servo number. Please fix and try again.")
            quit()
        print("Trait Read Finished\n")
    elif ReadOrWrite == 2:
        print("ENTERING WRITE MODE\n")
        print("The servo traits you can write are as follows: ")
        DisplayServoTraits()
        Selection1 = int(input("Enter the Trait Number you'd like to edit: "))
        Selection3 = int(input("Enter the Value you'd like to change the trait to: "))
        Selection2 = int(input("Enter the Servo you'd like to edit the Trait for: "))
        # Need Error checking for all 3
        if port_used_dict[Selection2] == 0:
            WriteTraitData(Selection1,Selection3,Selection2,port_hand_list[0],packetHandler)
        elif port_used_dict[Selection2] == 1:
            WriteTraitData(Selection1,Selection3,Selection2,port_hand_list[1],packetHandler)
        elif port_used_dict[Selection2] == 2:
            WriteTraitData(Selection1,Selection3,Selection2,port_hand_list[2],packetHandler)
        else:
            print("Not a recognized or connected servo number. Please fix and try again.")
            quit()
        print("Trait Edit Finished\n")
    elif ReadOrWrite == 0:
        print("Exiting Tilibot Tinker.")
        break
    else:
        print("That is not a valid option, please try again.")
print("Thank you for using Tilibot Tinker!")





