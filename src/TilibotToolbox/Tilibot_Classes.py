## Tilibot Classes

from Tilibot_Constants import *
# from Tilibot_Functions import *
from Tilibot_Universal_Functions import *
from dynamixel_sdk import *
import time



class Servo:
    def __init__(self,IDnum,port_used,Positions,Speeds,MaxMinMov,digital_only=None):
        self.ID = IDnum
        self.digital_only = False
        if digital_only == None:
            self.digital_only == False
        self.Positions = Positions
        self.Speeds = Speeds
        self.MaxMin = MaxMinMov
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.port_used = port_used
        self.position_fixing = False

    def InitialSetup(self,portHandler,silenceYesNo): 
        print("#############################################################")
        print("Servo #%0.3d" %(self.ID))
        if self.digital_only == False:
            portHandler.openPort()
            #Set drive mode to velocity based
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_DRIVE_MODE, DRIVE_MODE_VEL_BASED)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Drive mode set to: %03d" %(self.ID, DRIVE_MODE_VEL_BASED))

            # time.sleep(PreferedDelay)

            #Set operating mode to joint/position control mode
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_OPERATING_MODE, OPERATING_JOINT_POSITION_MODE)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Operating mode set to: %03d" %(self.ID, OPERATING_JOINT_POSITION_MODE))

            # time.sleep(PreferedDelay)

            #Set acceleration limit 
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_ACCELERATION_LIMIT, ACCELERATION_LIMIT_M)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Acceleration limit set to: %03d" %(self.ID, ACCELERATION_LIMIT_M))

            # time.sleep(PreferedDelay)

            #Set max position limit
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_MAX_POSITION_LIMIT, self.MaxMin[0])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Max position limit set to: %03d" %(self.ID, self.MaxMin[0]))

            # time.sleep(PreferedDelay)

            #Set min position limit
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, ADDR_MIN_POSITION_LIMIT, self.MaxMin[1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Min position limit set to: %03d" %(self.ID, self.MaxMin[1]))

            # time.sleep(PreferedDelay)

            #Set moving threshold
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, AddrDict[11], MOVING_THRESHOLD_ACCURACY)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if silenceYesNo == False:
                    print("[ID:%03d] Moving accuracy set to high: %03d" %(self.ID, MOVING_THRESHOLD_ACCURACY))

            # time.sleep(PreferedDelay)
        elif self.digital_only == True:
            print("[ID:%03d] Digital Only Port set to Open" %(self.ID))

    def ToggleTorque(self,OnOrOff,portHandler):
        if self.digital_only == False:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(portHandler, self.ID, AddrDict[22], OnOrOff)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                if (OnOrOff == 1):
                    print("Dynamixel#%d torque on" % self.ID)
                elif (OnOrOff == 0):
                    print("Dynamixel#%d torque off" % self.ID)
        elif self.digital_only == True:
            if (OnOrOff == 1):
                print("[ID:%03d] Digital Only Torque set to On" %(self.ID))
            elif (OnOrOff == 0):
                print("[ID:%03d] Digital Only Torque set to Off" %(self.ID))
             


    def SetServoVelocity(self,InVelocity,portHandler):
        if self.digital_only == False:
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, AddrDict[34], int(InVelocity))
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Velocity limit set to: %03d" %(self.ID, InVelocity))
        elif self.digital_only == True:
            print("[ID:%03d] Digital Only Velocity set." %(self.ID))

    def MoveServo(self,InPosition,portHandler):
        if self.digital_only == False:
             # Write goal position
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(portHandler, self.ID, AddrDict[37], InPosition)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("[ID:%03d] Goal Position set to: %03d" %(self.ID, InPosition))
        elif self.digital_only == True:
            print("[ID:%03d] Digital Only Position set." %(self.ID))

    def MoveHome(self,homespeed,portHandler):
        self.SetServoVelocity(homespeed,portHandler)
        self.MoveServo(self.Positions[0],portHandler)
        print("#############################################################")


    def ContinuousMove(self,portHandler,stride_numbers,record_array,start_time):
        for stride_count in range(stride_numbers[0]):
            for position_count in range(stride_numbers[1]):
                if self.digital_only == False:
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
                            end_time = record_time - start_time
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
                elif self.digital_only == True:
                    print("[ID:%03d] Digital Only Velocity set." %(self.ID))
                    print("[ID:%03d] Digital Only Position set." %(self.ID))
                    if record_array[0] == True:
                        print("#############################################################")
                        if record_array[1] == True:
                            pos_out = self.Positions[position_count]
                            print("[ID:%03d] Digital Only Position is %d." %(self.ID,self.Positions[stride_count]))
                        if record_array[2] == True:
                            print("[ID:%03d] Digital Only Speed is %d." %(self.ID,self.Speeds[stride_count]))
                        if record_array[3] == True:
                            record_time = time.time()
                            end_time = record_time - start_time
                            print("[ID:%03d] Digital Only Time is %f." %(self.ID,end_time))
                        if record_array[4] == True:
                            print("[ID:%03d] Digital Only Position Index is %d." %(self.ID,position_count))
                        if record_array[5] == True:
                            print("[ID:%03d] Digital Only Position Stride Count is %d." %(self.ID,stride_count))
                        if record_array[6] == True:
                            print("[ID:%03d] Digital Only Position Current - Not Available." %(self.ID))
                        if record_array[7] == True:
                            print("[ID:%03d] Digital Only Position Voltage - Not Available." %(self.ID))
                        if record_array[8] == True:
                            print("[ID:%03d] Digital Only Position Temperature - Not Available." %(self.ID))
                        print("#############################################################")
        return out_data

    def CleanUp(self):
        pass

    def __del__(self):
        pass

class Limb:
    def __init__(self,limbnum,servo_dict):
        self.LimbNumber = limbnum
        self.ServoDict = servo_dict
    
    def InitialSetup(self,port_servo_dict):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.InitialSetup(port_servo_dict[each_servo])
        return

    def ToggleTorque(self,OnOrOff,port_servo_dict):
        for each_servo, each_servo_obj in self.ServoDict.items():
            each_servo_obj.ToggleTorque(OnOrOff,port_servo_dict[each_servo])
        return

class Leg(Limb):
    def __init__(self,limbnum,servo_dict):
        super().__init__(limbnum,servo_dict)

    def __del__(self):
            pass        


class Neck(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def __del__(self):
        pass  

class Spine(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def __del__(self):
        pass  

class Tail(Limb):
    def __init__(self,limbnum,servolist):
        super().__init__(limbnum,servolist)

    def __del__(self):
        pass  

class Body:
    def __init__(self,LimbDictionary,ServoDictionary): #limbs should be a list
        self.LimbDict = LimbDictionary
        self.ServoDict = ServoDictionary
        
    def InitialSetup(self,port_hand_list):
        for each_servo_obj in self.ServoDict.values():
            each_servo_obj.InitialSetup(port_hand_list[each_servo_obj.port_used])
        return

    #Turn into group sync function
    def ToggleTorque(self,OnOrOff,port_hand_list):
        for each_servo_obj in self.ServoDict.values():
            each_servo_obj.ToggleTorque(OnOrOff,port_hand_list[each_servo_obj.port_used])
        return

    def __del__(self):
            pass
