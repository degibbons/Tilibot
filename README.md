# Tilibot Toolbox

Welcome to Tilibot Toolbox!

Tilibot Toolbox is a toolbox created with the intention of emulating biomechanics of the Tiliqua genus  
using servo motors.

Tilibot toolbox is written in Python 3.
Tilibot toolbox is intended to be run on a Raspberry Pi but may be edited to run on other machines.  
Tilibot was developed utilizing Dynamixel MX-64AT servos and using the DynamixelSDK python distribution.  
Tilibot_Reference.pdf will explain all parts of Tilibot in detail. 

In order to download and install, you may follow one of two options below:
### Non-Tech Savvy
1. Download the zip file on the GitHub page
2. Unpack the folder
3. Open the command prompt
4. Change your directory to the location of the now extracted Tilibot Toolbox. For example - 
> C:\Users\daneg> cd C:\Users\daneg\Documents\TilibotToolbox
5. Then, change your directory to the src\ folder
> C:\Users\daneg> cd src
6. Run the following:
> C:\Users\daneg> python3 Tilibot_Intro.py

This should walk you through introduction, installation, and any other requirements Tilibot Toolbox may require.
For further instructions, please read the Tilibot_Reference.pdf in the Tilibot root folder.

### Tech Savvy
1. Open the command prompt
2. Navigate to the destination directory you'd like to clone the Tilibot repository to.
3. Run the following:
> git clone https://github.com/degibbons/Tilibot/
> 4. As above, for the Non-Tech Savvy individuals, you may execute instructions 5 and 6, that is:  
>  * Change the directory to the src\ folder
>  * Run Tilibot_Intro.py
5. For simplification purposes, you may also simply run the following:
> python3 setup.py install --user

It is highly recommended to run Tilibot_Install.py however.

pip install -r requirements.txt