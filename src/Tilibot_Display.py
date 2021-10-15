## Tilibot Display

import os, sys
from dynamixel_sdk import *
from Tilibot_Constants import *
from Tilibot_Functions import *

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
print("take place in Tilibot modules. Press enter to continue!")
getch()

print("                   (HEAD)")
print("                     mm")
print("                    [17]")
print("                    [18]")
print("   <[08][07][06][05]    [01][02][03][04]>")
print("                    [19]")
print("                    [20]")
print("                    [21]")
print("                    [22]")
print("   <[16][15][14][13]    [09][10][11][12]>")
print("                    [23]")
print("                    [24]")
print("                     \/")
print("                   (TAIL)")

print("This is the digital layout of Tilibot, matched up with the physical placement of the servos in real life. ")

# Program responsiveness to update visual layout when servos are detected and such.
print("Servos will visually update when they are detected or being used.")
print("")
