## Tilibot Display

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
# from Tilibot_Functions import *

if os.name == 'nt':
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




print("Welcome to Tilibot Display!")
print("Tilibot Display is a visual representation of the digital operations that")
print("take place in Tilibot modules. Press enter to continue!\n")
getch()
print("                   (HEAD)")
print("                     mm")
print("                    [{:02d}]".format(DXL17_ID))
print("                    [{:02d}]".format(DXL18_ID))
print("   <[{:02d}][{:02d}][{:02d}][{:02d}]    [{:02d}][{:02d}][{:02d}][{:02d}]>".format(DXL8_ID,DXL7_ID,DXL6_ID,DXL5_ID,DXL1_ID,DXL2_ID,DXL3_ID,DXL4_ID))
print("                    [{:02d}]".format(DXL19_ID))
print("                    [{:02d}]".format(DXL20_ID))
print("                    [{:02d}]".format(DXL21_ID))
print("                    [{:02d}]".format(DXL22_ID))
print("   <[{:02d}][{:02d}][{:02d}][{:02d}]    [{:02d}][{:02d}][{:02d}][{:02d}]>".format(DXL16_ID,DXL15_ID,DXL14_ID,DXL13_ID,DXL9_ID,DXL10_ID,DXL11_ID,DXL12_ID))
print("                    [{:02d}]".format(DXL23_ID))
print("                    [{:02d}]".format(DXL24_ID))
print("                     \/")
print("                   (TAIL)")
print("\n")
print("This is the digital layout of Tilibot, matched up with the physical placement of") 
print("the servos in real life. Press enter to continue!\n")
getch()
print("The layout will begin like this:\n")
print("                   (HEAD)")
print("                     mm")
print("                    [{:02d}]".format(0))
print("                    [{:02d}]".format(0))
print("   <[{:02d}][{:02d}][{:02d}][{:02d}]    [{:02d}][{:02d}][{:02d}][{:02d}]>".format(0,0,0,0,0,0,0,0))
print("                    [{:02d}]".format(0))
print("                    [{:02d}]".format(0))
print("                    [{:02d}]".format(0))
print("                    [{:02d}]".format(0))
print("   <[{:02d}][{:02d}][{:02d}][{:02d}]    [{:02d}][{:02d}][{:02d}][{:02d}]>".format(0,0,0,0,0,0,0,0))
print("                    [{:02d}]".format(0))
print("                    [{:02d}]".format(0))
print("                     \/")
print("                   (TAIL)")
print("\n")
# Program responsiveness to update visual layout when servos are detected and such.
print("Servos will visually update when they are detected or being used.\n")
print("")
