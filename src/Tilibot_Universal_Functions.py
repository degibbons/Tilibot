## Tilibot Universal Functions

# Intended to prevent circular referencing

from dynamixel_sdk import *

def FormatSendData(rawData):
    return [DXL_LOBYTE(DXL_LOWORD(rawData)), DXL_HIBYTE(DXL_LOWORD(rawData)), DXL_LOBYTE(DXL_HIWORD(rawData)), DXL_HIBYTE(DXL_HIWORD(rawData))]

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