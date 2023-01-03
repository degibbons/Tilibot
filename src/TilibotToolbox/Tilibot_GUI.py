from cProfile import run
from cgitb import text
from configparser import ConfigParser
from doctest import master
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdlg
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import ImageTk,Image 
import time
from Tilibot_Constants import *

# from Tilibot_Functions import *

# from Tilibot_Functions_noThres2 import *
from Tilibot_Functions_debug1 import *

from Tilibot_Classes import *
from Tilibot_Universal_Functions import *
from dynamixel_sdk import *
import sys
import os
# import dynamixel_functions as dynamixel

GUI_or_TERMINAL = -1 # -1 for GUI, +1 for Terminal
Step_Progressor = 0

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.packetHandler = None # The PacketHandler used to move information to, from, and between servos
        self.move_list = [] # Lists to Assemble from detection - These are the Servos that SHOULD move - Limbs
        self.dont_move_list = [] #These are the servos that should NOT move - Spine
        self.port_hand_list = None # List of port-handlers 
        self.port_servo_dict = None # Dictionary containing data in the form of {# of servo:Porthandler object}
        self.port_used_dict = None # Dictionary containing data in the form of {# of servo:Port #}
        self.confirmed_action = [0,[]] # The desired action of moving one or several servos
        self.record_array = None # The desired fields for recording
        self.stride_numbers = None # The amount of strides and the positions for each
        self.PositionsMatrix = None # The positions each servo 1-16 should be moving to in 1 stride
        self.SpeedMatrix = None # The speeds each servo 1-16 should be moving at with respect to the positionsmatrix
        self.calc_end_time = tk.StringVar() # Calculated variable for the time it takes to complete the desired action
        self.act_end_time = tk.StringVar() # Measured variable for the time it takes to complete the desired action
        self.kin_file_display = tk.StringVar() # Displays the Kinematics file used
        self.set_file_display = tk.StringVar() # Display the Settings file used
        self.ServosDictionary = None # Establishes the dictionary to store the servo objects
        self.stay_move_selected = [0,0] # Establishes if one, both, or none of the stay/move buttons have been pressed

        self.after(250,self.stop_operation)

        self.servo_colors = {"gray":"#979A9A", # Colors used for servos in schematic AND indicator light
                        "yellow":"#F4D03F",
                        "orange":"#FFA500",
                        "red":"#E74C3C",
                        "green":"#27AE60",
                        "blue":"#3498DB",
                        "purple":"#6600CC"}

        self.Config_Options = {"baud_rate":None, # Valuse from the YAML file used as settings and in terminal mode
                            "positions_file":None,
                            "position_amount":None,
                            "stride_time":None,
                            "stride_amount":None,
                            "connected_servos":None,
                            "connected_limbs":None,
                            "connected_sensors":None,
                            "forelimb_stance_time":None,
                            "forelimb_swing_time":None,
                            "hindlimb_stance_time":None,
                            "hindlimb_swing_time":None,
                            "tot_ratio_time":None,
                            "move_one_servo_act":None,
                            "single_servo_to_move":None,
                            "move_multi_servo_act":None,
                            "servos_to_move":None,
                            "home_speed":None,
                            "out_file_name":None,
                            "out_file_dir":None,
                            "position_write":None,
                            "speed_write":None,
                            "time_write":None,
                            "posindex_write":None,
                            "stridecount_write":None,
                            "current_write":None,
                            "voltage_write":None,
                            "temp_write":None,
                            "neck_straight":None,
                            "spine_straight":None,
                            "tail_straight":None,
                            "silence_ext_output":None,
                            "run_digital_only":None}

        # Help Box
        self.hb_object_box = None # Help box object
        self.active_help_page = 1 # Set the active help page, used for changing page

        # Global Settings Box
        self.gs_object_box = None # Global Settings box object

        # Move Servos Box
        self.ms_object_box = None # Move servos box object
    
        # Record Data Box
        self.rd_object_box = None # Record Data box object
        self.rd_target_dir = tk.StringVar() # Establish the target directory for output files as a tkinter string variable
        self.rd_out_file_name = tk.StringVar() # Establish the target file name for output files as a tkinter string variable
    
        # Save Settings Box
        self.ss_object_box = None # Save Settings Box Object
        self.ss_settings_file_name = tk.StringVar() # Establish the target file name for an imported settings file as a tkinter string variable

        # Reboot / Reset Box
        self.rr_object_box = None # Reboot / Reset Box Object

        # Analyse Data Box
        self.analyse_data_box = None
        self.visualize_data_box = None
        
        #  Initialize the GUI Window
        self.title("Tilibot Visual Controller") # Title of the tkinter window
        self.geometry("1250x765+20+20") # Set size and origin position of tkinter window

        # create canvas
        self.myCanvas = tk.Canvas(master=self, bg="white", height = 750, width=650) # Create the canvas to draw on
        self.myCanvas.grid(column=0, row=0, rowspan=5 ,sticky=tk.W, padx=5, pady=5) # Put canvas on tkinter window

        # add to window and show
        helv36 = tkFont.Font(family='Helvetica',size=18, weight='bold', underline=1) # Establish a title font
        canvas_title = self.myCanvas.create_text(120,60,text='Tilibot Detection Schematic',font=helv36, width=300) # Create a title for the canvas/schematic

        # Create graphics and corresponding labels for each servo that would be connected in Tilibot
        self.id_srv_1 = self.myCanvas.create_rectangle(365, 195, 415, 245, fill=self.servo_colors["gray"],tags='servo_1') 
        id_srv_1_lbl = self.myCanvas.create_text(390,220,text='#1',tags='servo_1')
        self.id_srv_2 = self.myCanvas.create_rectangle(435, 195, 485, 245, fill=self.servo_colors["gray"],tags='servo_2')
        id_srv_2_lbl = self.myCanvas.create_text(460,220,text='#2',tags='servo_2')
        self.id_srv_3 = self.myCanvas.create_rectangle(505, 195, 555, 245, fill=self.servo_colors["gray"],tags='servo_3')
        id_srv_3_lbl = self.myCanvas.create_text(530,220,text='#3',tags='servo_3')
        self.id_srv_4 = self.myCanvas.create_rectangle(575, 195, 625, 245, fill=self.servo_colors["gray"],tags='servo_4')
        id_srv_4_lbl = self.myCanvas.create_text(600,220,text='#4',tags='servo_4')
        self.id_srv_5 = self.myCanvas.create_rectangle(225, 195, 275, 245, fill=self.servo_colors["gray"],tags='servo_5')
        id_srv_5_lbl = self.myCanvas.create_text(250,220,text='#5',tags='servo_5')
        self.id_srv_6 = self.myCanvas.create_rectangle(155, 195, 205, 245, fill=self.servo_colors["gray"],tags='servo_6')
        id_srv_6_lbl = self.myCanvas.create_text(180,220,text='#6',tags='servo_6')
        self.id_srv_7 = self.myCanvas.create_rectangle(85, 195, 135, 245, fill=self.servo_colors["gray"],tags='servo_7')
        id_srv_7_lbl = self.myCanvas.create_text(110,220,text='#7',tags='servo_7')
        self.id_srv_8 = self.myCanvas.create_rectangle(15, 195, 65, 245, fill=self.servo_colors["gray"],tags='servo_8')
        id_srv_8_lbl = self.myCanvas.create_text(40,220,text='#8',tags='servo_8')

        self.id_srv_9 = self.myCanvas.create_rectangle(365, 515, 415, 565, fill=self.servo_colors["gray"],tags='servo_9')
        id_srv_9_lbl = self.myCanvas.create_text(390,540,text='#9',tags='servo_9')
        self.id_srv_10 = self.myCanvas.create_rectangle(435, 515, 485, 565, fill=self.servo_colors["gray"],tags='servo_10')
        id_srv_10_lbl = self.myCanvas.create_text(460,540,text='#10',tags='servo_10')
        self.id_srv_11 = self.myCanvas.create_rectangle(505, 515, 555, 565, fill=self.servo_colors["gray"],tags='servo_11')
        id_srv_11_lbl = self.myCanvas.create_text(530,540,text='#11',tags='servo_11')
        self.id_srv_12 = self.myCanvas.create_rectangle(575, 515, 625, 565, fill=self.servo_colors["gray"],tags='servo_12')
        id_srv_12_lbl = self.myCanvas.create_text(600,540,text='#12',tags='servo_12')
        self.id_srv_13 = self.myCanvas.create_rectangle(225, 515, 275, 565, fill=self.servo_colors["gray"],tags='servo_13')
        id_srv_13_lbl = self.myCanvas.create_text(250,540,text='#13',tags='servo_13')
        self.id_srv_14 = self.myCanvas.create_rectangle(155, 515, 205, 565, fill=self.servo_colors["gray"],tags='servo_14')
        id_srv_14_lbl = self.myCanvas.create_text(180,540,text='#14',tags='servo_14')
        self.id_srv_15 = self.myCanvas.create_rectangle(85, 515, 135, 565, fill=self.servo_colors["gray"],tags='servo_15')
        id_srv_15_lbl = self.myCanvas.create_text(110,540,text='#15',tags='servo_15')
        self.id_srv_16 = self.myCanvas.create_rectangle(15, 515, 65, 565, fill=self.servo_colors["gray"],tags='servo_16')
        id_srv_16_lbl = self.myCanvas.create_text(40,540,text='#16',tags='servo_16')

        self.id_srv_17 = self.myCanvas.create_rectangle(295, 70, 345, 120, fill=self.servo_colors["gray"],tags='servo_17')
        id_srv_1_lbl = self.myCanvas.create_text(320,95,text='#17',tags='servo_17')
        self.id_srv_18 = self.myCanvas.create_rectangle(295, 140, 345, 190, fill=self.servo_colors["gray"],tags='servo_18')
        id_srv_1_lbl = self.myCanvas.create_text(320,165,text='#18',tags='servo_18')
        self.id_srv_19 = self.myCanvas.create_rectangle(295, 250, 345, 300, fill=self.servo_colors["gray"],tags='servo_19')
        id_srv_1_lbl = self.myCanvas.create_text(320,275,text='#19',tags='servo_19')
        self.id_srv_20 = self.myCanvas.create_rectangle(295, 320, 345, 370, fill=self.servo_colors["gray"],tags='servo_20')
        id_srv_1_lbl = self.myCanvas.create_text(320,345,text='#20',tags='servo_20')
        self.id_srv_21 = self.myCanvas.create_rectangle(295, 390, 345, 440, fill=self.servo_colors["gray"],tags='servo_21')
        id_srv_1_lbl = self.myCanvas.create_text(320,415,text='#21',tags='servo_21')
        self.id_srv_22 = self.myCanvas.create_rectangle(295, 460, 345, 510, fill=self.servo_colors["gray"],tags='servo_22')
        id_srv_1_lbl = self.myCanvas.create_text(320,485,text='#22',tags='servo_22')
        self.id_srv_23 = self.myCanvas.create_rectangle(295, 570, 345, 620, fill=self.servo_colors["gray"],tags='servo_23')
        id_srv_1_lbl = self.myCanvas.create_text(320,595,text='#23',tags='servo_23')
        self.id_srv_24 = self.myCanvas.create_rectangle(295, 640, 345, 690, fill=self.servo_colors["gray"],tags='servo_24')
        id_srv_1_lbl = self.myCanvas.create_text(320,665,text='#24',tags='servo_24')

        self.servo_graphics = {1:self.id_srv_1, # Create dictionary holding each servo graphics object for later changing of color
                            2:self.id_srv_2,
                            3:self.id_srv_3,
                            4:self.id_srv_4,
                            5:self.id_srv_5,
                            6:self.id_srv_6,
                            7:self.id_srv_7,
                            8:self.id_srv_8,
                            9:self.id_srv_9,
                            10:self.id_srv_10,
                            11:self.id_srv_11,
                            12:self.id_srv_12,
                            13:self.id_srv_13,
                            14:self.id_srv_14,
                            15:self.id_srv_15,
                            16:self.id_srv_16,
                            17:self.id_srv_17,
                            18:self.id_srv_18,
                            19:self.id_srv_19,
                            20:self.id_srv_20,
                            21:self.id_srv_21,
                            22:self.id_srv_22,
                            23:self.id_srv_23,
                            24:self.id_srv_24}

        # Create labels to distinguish between subsets of limbs
        neck_label = self.myCanvas.create_text(250,130,text='Neck')
        spine_label = self.myCanvas.create_text(415,380,text='Spine')
        tail_label = self.myCanvas.create_text(250,630, text='Tail')
        front_right_limb_label = self.myCanvas.create_text(500,285,text='Front Right Leg')
        front_left_limb_label = self.myCanvas.create_text(150,155,text='Front Left Leg')
        back_right_limb_label = self.myCanvas.create_text(500,480,text='Back Right Leg')
        back_left_limb_label = self.myCanvas.create_text(150,600,text='Back Left Leg')
        # Create curly brackets to enclose servos in select limbs
        neck_label_bracket_1 = self.myCanvas.create_line(290,70, 260,95, 290,125, smooth=1)
        neck_label_bracket_2 = self.myCanvas.create_line(290,125, 270,130, 290,135, smooth=0)
        neck_label_bracket_3 = self.myCanvas.create_line(290,135, 260,165, 290,190, smooth=1)
        spine_label_bracket_1 = self.myCanvas.create_line(350,250, 380,310, 350,375, smooth=1)
        spine_label_bracket_2 = self.myCanvas.create_line(350,375, 390,380, 350,385, smooth=0)
        spine_label_bracket_3 = self.myCanvas.create_line(350,385, 380,450, 350,510, smooth=1)
        tail_label_bracket_1 = self.myCanvas.create_line(290,570, 260,595, 290,625, smooth=1)
        tail_label_bracket_2 = self.myCanvas.create_line(290,625, 270,630, 290,635, smooth=0)
        tail_label_bracket_3 = self.myCanvas.create_line(290,635, 260,665, 290,690, smooth=1)
        front_right_label_bracket_1 = self.myCanvas.create_line(365,250, 428,280, 490,250,smooth=1)
        front_right_label_bracket_2 = self.myCanvas.create_line(490,250, 495,270, 500,250,smooth=0)
        front_right_label_bracket_3 = self.myCanvas.create_line(500,250, 563,280, 625,250,smooth=1)
        front_left_label_bracket_1 = self.myCanvas.create_line(15,190, 68,160, 140,190,smooth=1)
        front_left_label_bracket_2 = self.myCanvas.create_line(140,190, 145,170, 150,190, smooth=0)
        front_left_label_bracket_3 = self.myCanvas.create_line(150,190, 213,160, 275,190,smooth=1)
        back_right_label_bracket_1 = self.myCanvas.create_line(365,510, 428,480, 490,510,smooth=1)
        back_right_label_bracket_2 = self.myCanvas.create_line(490,510, 495,490, 500,510,smooth=0)
        back_right_label_bracket_3 = self.myCanvas.create_line(500,510, 563,480, 625,510,smooth=1)
        back_left_label_bracket_1 = self.myCanvas.create_line(15, 570, 68,600, 140,570,smooth=1)
        back_left_label_bracket_2 = self.myCanvas.create_line(140,570, 145,590, 150,570, smooth=0)
        back_left_label_bracket_3 = self.myCanvas.create_line(150,570, 213,600, 275,570,smooth=1)


        # Create Servo Color Legends and corresponding Objects
        color_leg_BoundingBox = self.myCanvas.create_rectangle(365,20,645,180)
        color_leg_Gray = self.myCanvas.create_rectangle(400, 30, 420, 50, fill=self.servo_colors["gray"])
        color_leg_Yellow = self.myCanvas.create_rectangle(400, 60, 420, 80, fill=self.servo_colors["yellow"])
        color_leg_Red = self.myCanvas.create_rectangle(400, 90, 420, 110, fill=self.servo_colors["red"])
        color_leg_Green = self.myCanvas.create_rectangle(400, 120, 420, 140, fill=self.servo_colors["green"])
        color_leg_Blue = self.myCanvas.create_rectangle(400, 150, 420, 170, fill=self.servo_colors["blue"])
        # Create legend labels
        color_leg_Gray_txt = self.myCanvas.create_text(480,40,text='Servo Undetected')
        color_leg_Yellow_txt = self.myCanvas.create_text(530,70,text='Servo Detected - No Option Selected')
        color_leg_Red_txt = self.myCanvas.create_text(515,100,text='Servo Detected - Do NOT Move')
        color_leg_Green_txt = self.myCanvas.create_text(493,130,text='Servo Detected - Move')
        color_leg_Blue_txt = self.myCanvas.create_text(505,160,text='Servo Detected - Issue/Error')

        # Create Indicator Light Legend and corresponding Objects
        indicator_BoundingBox = self.myCanvas.create_rectangle(365,580,645,740)
        color_indicator_Gray = self.myCanvas.create_oval(400, 585, 420, 605, fill=self.servo_colors["gray"])
        color_indicator_Red = self.myCanvas.create_oval(400, 610, 420, 630, fill=self.servo_colors["red"])
        color_indicator_Orange = self.myCanvas.create_oval(400, 635, 420, 655, fill=self.servo_colors["orange"])
        color_indicator_Yellow = self.myCanvas.create_oval(400, 660, 420, 680, fill=self.servo_colors["yellow"])
        color_indicator_Green = self.myCanvas.create_oval(400, 685, 420, 705, fill=self.servo_colors["green"])
        color_indicator_Purple = self.myCanvas.create_oval(400, 710, 420, 730, fill=self.servo_colors["purple"])
        # Create Legend Labels
        color_indicator_Gray_text = self.myCanvas.create_text(525, 595,text="Servos Not Detected and Marked")
        color_indicator_Red_text = self.myCanvas.create_text(497, 620,text="No Kinematics Loaded")
        color_indicator_Orange_text = self.myCanvas.create_text(534,645,text="Robot Ready - Not in Home Position")
        color_indicator_Yellow_text = self.myCanvas.create_text(523, 670, text="Robot Ready - In Home Position")
        color_indicator_Green_text = self.myCanvas.create_text(478, 695, text="Robot Running")
        color_indicator_Purple_text = self.myCanvas.create_text(500, 720, text="Robot Finished Running")

        # Create instructions legend and corresponding labels
        instructions_BoundingBox = self.myCanvas.create_rectangle(5,305,285,460)
        steps_title_label = self.myCanvas.create_text(35,295,text="Steps List",font=("Helvetica",'10',"bold")) # Make Bold and Slightly Bigger
        step_1_label = self.myCanvas.create_text(144,320,text='Step 1: Set the Global Settings or Load Settings File')
        step_2_label = self.myCanvas.create_text(66,334,text='Step 2: Detect Servos')
        step_3_label = self.myCanvas.create_text(132,348,text='Step 3: Mark Moving and Non-Moving Servos')
        step_4_label = self.myCanvas.create_text(118,362,text='Step 4: Set Options for Amount of Servos')
        step_5_label = self.myCanvas.create_text(132,376,text='Step 5: Set Options for Recording (OPTIONAL)')
        step_6_label = self.myCanvas.create_text(103,390,text='Step 6: Set Stride Time and Amount')
        step_7_label = self.myCanvas.create_text(93,404,text='Step 7: Load the Kinematics File')
        step_8_label = self.myCanvas.create_text(72,418,text='Step 8: Select Get Ready')
        step_9_label = self.myCanvas.create_text(56,432,text='Step 9: Select Run')
        step_10_label = self.myCanvas.create_text(134,446,text='Step 10: Select Reset to Run Again or Shutdown')

        # Create Port indicator lights and corresponding legend labels
        port_indicator_BoundingBox = self.myCanvas.create_rectangle(440,340, 530,440)
        port_indicator_title = self.myCanvas.create_text(485,330, text="Port Status",font=("Helvetica",'10',"bold"))
        self.port_1_indicator = self.myCanvas.create_polygon(445,360, 455,350, 465,360, 455,370, 445,360,fill=self.servo_colors["red"],outline="#000000")
        self.port_2_indicator = self.myCanvas.create_polygon(445,390, 455,380, 465,390, 455,400, 445,390,fill=self.servo_colors["red"],outline="#000000")
        self.port_3_indicator = self.myCanvas.create_polygon(445,420, 455,410, 465,420, 455,430, 445,420,fill=self.servo_colors["red"],outline="#000000")
        self.port_4_indicator = self.myCanvas.create_polygon(490,360, 500,350, 510,360, 500,370, 490,360,fill=self.servo_colors["red"],outline="#000000")
        self.port_5_indicator = self.myCanvas.create_polygon(490,390, 500,380, 510,390, 500,400, 490,390,fill=self.servo_colors["red"],outline="#000000")
        self.port_6_indicator = self.myCanvas.create_polygon(490,420, 500,410, 510,420, 500,430, 490,420,fill=self.servo_colors["red"],outline="#000000")
        port_1_label = self.myCanvas.create_text(475,360, text="P1")
        port_2_label = self.myCanvas.create_text(475,390, text="P2")
        port_3_label = self.myCanvas.create_text(475,420, text="P3")
        port_4_label = self.myCanvas.create_text(520,360, text="P4")
        port_5_label = self.myCanvas.create_text(520,390, text="P5")
        port_6_label = self.myCanvas.create_text(520,420, text="P6")
        port_notcon_indicator = self.myCanvas.create_polygon(580,335, 590,325, 600,335, 590,345, 580,335,fill=self.servo_colors["red"],outline="#000000")
        port_con_indicator = self.myCanvas.create_polygon(580,380, 590,370, 600,380, 590,390, 580,380,fill=self.servo_colors["green"],outline="#000000")
        port_prob_indicator = self.myCanvas.create_polygon(580,425, 590,415, 600,425, 590,435, 580,425,fill=self.servo_colors["blue"],outline="#000000")
        port_notcon_label = self.myCanvas.create_text(590,355, text="Port Not Connected")
        port_con_label = self.myCanvas.create_text(590,400, text="Port Connected")
        port_prob_label = self.myCanvas.create_text(590,445, text="Port Issue/Error")
        
        self.port_graphics = {1:self.port_1_indicator, # Create dictionary holding each port graphic for changing color later
                            2:self.port_2_indicator,
                            3:self.port_3_indicator,
                            4:self.port_4_indicator, # Create dictionary holding each port graphic for changing color later
                            5:self.port_5_indicator,
                            6:self.port_6_indicator}
        
        # Create Stop Button for stopping execution in case of problem
        stop_button = tk.Button(master=self,text="Stop!",bg="red",width=20,height=40,command=self.set_stop_to_true)
        # Place stop button at bottom left of canvas
        stop_button_window = self.myCanvas.create_window(20,695,width=200,height=60,window=stop_button,anchor=tk.W)
        
        frame_1 = tk.Frame(master=self, padx=5, pady=5) # Create frame for title and global buttons
        prog_title = tk.Label(master=frame_1, text="Tilibot Visual - GUI ", relief=tk.FLAT, font=helv36) # Create title
        frame_1.grid(column=2, row=0, columnspan=4, rowspan=1, padx=5, pady=15) # Place frame on tkinter window
        prog_title.grid(row=0,column=0,columnspan=3, sticky=tk.N+tk.W+tk.E) # Place title in frame 
        help_button = ttk.Button(master=frame_1, text="Help",command=self.open_help_box) # Create Help Button
        self.logo_canvas = tk.Canvas(master=frame_1,height=75, width=75) # Create the canvas to display the logo on
        self.photoimage = ImageTk.PhotoImage(file="Tilibot_mini_S.png")
        # img = ImageTk.PhotoImage(file=os.getcwd()+'\Tilibot_mini.png')
        self.logo_canvas.create_image(35,35,image=self.photoimage) 
        help_button.grid(column=0,row=1,pady=10,sticky=tk.W) # Place help button in frame
        global_settings_button = ttk.Button(master=frame_1, text="Global Settings",command=self.open_global_settings_box) # Create Global Settings Button
        global_settings_button.grid(column=2,row=1,pady=10,sticky=tk.E) # Place global settings button in frame
        self.logo_canvas.grid(row=0,column=5,rowspan=2,padx=10)
        
        

        frame_2 = tk.Frame(master=self) # Create Frame for servo detection tools
        detect_servos_button = ttk.Button(master=frame_2, text="Detect Connected Servos",command=self.detect_servos) # Create button for pinging servos to detect them and to populate the list
        list_of_detected_servos = () # Establish a list variable for the servo list to draw from and populate
        servo_list_var = tk.StringVar(value=list_of_detected_servos) # Establish a tkinter string variable to represent what goes in the servo list box
        self.servo_listbox = tk.Listbox( # Create the listbox to display each detected servo
            master=frame_2,
            listvariable=servo_list_var,
            height=24,
            selectmode='extended')
        mark_to_move_button = ttk.Button(master=frame_2, text='Mark Selected to Move',command=self.mark_servo_move) # Create button to mark the selected servos to move
        mark_to_stay_button = ttk.Button(master=frame_2, text='Mark Selected to Stay Straight',command=self.mark_servo_stay) # Create button to mark the selected servos to NOT move
        reboot_reset_button = ttk.Button(master=frame_2,text="Reboot / Reset",command=self.open_reboot_reset_box)
        frame_2.grid(column=1, row=0, rowspan=6, padx=5, pady=5) # Place frame on tkinter window
        detect_servos_button.grid(row=0,padx=5,pady=5) # Place detect servos button in frame
        self.servo_listbox.grid(row=1,rowspan=3,padx=10,pady=10) # Place listbox in frame
        mark_to_move_button.grid(row=4,padx=5,pady=5) # Place mark to move button in frame
        mark_to_stay_button.grid(row=5,padx=5,pady=5) # Place mark to stay button in frame
        reboot_reset_button.grid(column=0,row=6,padx=5,pady=5)
        
        frame_3 = tk.Frame(master=self) # Create frame to hold configuring options, buttons, and toggle indicators
        self.move_select = tk.IntVar() # Create tkinter variable to hold the choice of either moving one or multiple servos
        move_rb_one = ttk.Radiobutton(master=frame_3,text="Move One Servo",variable=self.move_select,value=0) # Create Radio Button for moving one servo
        move_rb_many = ttk.Radiobutton(master=frame_3,text="Move Multiple Servos",variable=self.move_select,value=1) # Create Radio Button for moving multiple servo
        self.move_select.set(1) # Set the Multiple Servo Move button to be selected by default
        move_configure_button = ttk.Button(master=frame_3,text="Configure Options",command=self.open_move_box) # Create the Configure Movement button to put in movement ratio numbers
        self.record_yesno = tk.IntVar() # Create a tkinter variable to record if the user wants to record data or not
        record_data_checkbox = ttk.Checkbutton(master=frame_3, text="Record Data?",onvalue = 1,offvalue = 0,variable=self.record_yesno) # Create the data record checkbox for indicating if the user wants to record data or not
        self.record_yesno.set(value=0) # Set the default value of the record checkbox to NOT be selected
        record_data_configure_button = ttk.Button(master=frame_3, text="Configure Options",command=self.open_record_data_box) # Create the data configure button
        frame_3.grid(column=2,row=1,sticky=tk.N) # Place the frame on the tkinter window
        move_rb_one.grid(row=0,column=0,sticky=tk.W) # Plcae the first radio button in frame
        move_rb_many.grid(row=1,column=0,stick=tk.W) # Place the second radio button in frame
        move_configure_button.grid(row=0,column=1,rowspan=2,sticky=tk.E,padx=5,pady=10) # Place the Move Configure button in frame
        record_data_checkbox.grid(row=2,column=0,sticky=tk.W) # Place the data checkbox in frame
        record_data_configure_button.grid(row=2,column=1,sticky=tk.E,padx=5,pady=10) # Place Data Configure button in frame
        self.movement_smoothing = tk.IntVar() # Create a tkinter variable to record if the user wants movement smoothing or not
        self.movement_smoothing.set(value=0) # Set the default value of the movement smoothing checkbox to NOT be selected
        movement_smoothing_checkbox = ttk.Checkbutton(master=frame_3, text="Smooth Movements?",onvalue = 1, offvalue = 0,variable=self.movement_smoothing) # Create checkbox to indicate whether to include movement smoothing
        movement_smoothing_checkbox.grid(row=3,column=0,sticky=tk.W) # Place the movement smoothing checkbox in the frame

        frame_4 = tk.Frame(master=self) # Create Frame for Stride Variable Inputs, Run Time Labels, and the Indicator Light
        frame_4.grid(column=2,row=2,sticky=tk.N) # Place frame on tkinter window
        self.stride_time_entry_string = tk.StringVar() # Create tkinter variable to hold the stride time entered into the entry box
        self.stride_amount_entry_string = tk.StringVar() # Create tkinter variable to hold the stride time entered into the entry box
        stride_time_label = ttk.Label(master=frame_4,text="Stride Time (sec): ") # Create label for stride time input
        stride_time_entry = ttk.Entry(master=frame_4,textvariable=self.stride_time_entry_string) # Create entry box for stride time input
        self.stride_time_entry_string.set("Float Only Here") # Set input box to display that only floats should be used here
        stride_amount_label = ttk.Label(master=frame_4,text="Stride Amount: ") # Create label for stride amount input
        stride_amount_entry = ttk.Entry(master=frame_4,textvariable=self.stride_amount_entry_string) # Create entry box for stride amount input
        self.stride_amount_entry_string.set("Integer Only Here") # Set input box to display that only integers should be used here
        stride_time_label.grid(column=0,row=0,sticky=tk.E,pady=5) # Put the input label in the frame
        stride_time_entry.grid(column=1,row=0,sticky=tk.W,pady=5) # Put the input entry box in the frame
        stride_amount_label.grid(column=0,row=1,sticky=tk.E,pady=5) # Put the input label in the frame
        stride_amount_entry.grid(column=1,row=1,sticky=tk.W,pady=5) # Put the input entry box in the frame
        calc_run_time_label = ttk.Label(master=frame_4,text="Calculated Run Time: ") # Create the label for the calculated run time 
        calc_run_time_number = ttk.Label(master=frame_4,textvariable=self.calc_end_time,background="#CCD1D1") # Create the changing label for the calculated run time
        act_run_time_label = ttk.Label(master=frame_4,text="Actual Run Time: ") # Create the label for the actual run time
        act_run_time_number = ttk.Label(master=frame_4,textvariable=self.act_end_time,background="#CCD1D1") # Create the changing label for the actual run time
        calc_run_time_label.grid(column=0,row=2,sticky=tk.E,pady=5) # Put the label in the frame
        calc_run_time_number.grid(column=1,row=2,sticky=tk.W,pady=5) # Put the label in the frame
        act_run_time_label.grid(column=0,row=3,sticky=tk.E,pady=20) # Put the label in the frame
        act_run_time_number.grid(column=1,row=3,sticky=tk.W,pady=20) # Put the label in the frame
        self.calc_end_time.set("0.000") # Set the starting time to 0 second float
        self.act_end_time.set("0.000") # Set the starting time to 0 second float
        self.stride_time_entry_string.trace('w',self.calculate_run_time) # Create a callback when the stride time entry string variable is changed
        self.stride_amount_entry_string.trace('w',self.calculate_run_time) # Create a callback when the stride amount entry string variable is changed
        load_kinematics_file_button = ttk.Button(master=frame_4,text="Load Kinematics File / Recalculate Speeds",command=self.load_kinem_file) # Create the Load Kinematics file button for importing Kinematics Data for movement
        load_kinematics_file_button.grid(row=4,column=0,columnspan=2,pady=10) # Place the load kinematics file button in frame
        indicator_label = ttk.Label(master=frame_4,text="Ready Indicator: ") # Create label for displaying the indicator light
        indicator_label.grid(column=0,row=5) # Put the label in the frame
        self.indicator_canvas = tk.Canvas(master=frame_4,width=50,height=50) # Create small canvas to place indicator light
        self.indicator_canvas.grid(column=1,row=5,sticky=tk.W+tk.E,pady=10) # Place the canvas in the tkinter window
        self.indic_oval = self.indicator_canvas.create_oval(20, 20, 40, 40)  # Create a circle on the Canvas
        self.indicator_canvas.itemconfig(self.indic_oval, fill="gray") # Fill the circle with the color gray

        frame_5 = tk.Frame(master=self) # Create a frame for the Settings Buttons, the Run Buttons, and the shutdown button
        save_settings_button = ttk.Button(master=frame_5,text="Save Current Settings",command=self.open_save_settings_box) # Create the button to save the current settings 
        load_settings_button = ttk.Button(master=frame_5,text="Load Settings File",command=self.load_settings_file) # Create the button for loading a settings file
        get_ready_button = ttk.Button(master=frame_5,text="Get Ready",command=self.tilibot_get_ready) # Create the Get Ready button to move the robot to home position
        run_button = ttk.Button(master=frame_5,text="Run",command = self.tilibot_run) # Create the Run button to run the robot through a trial
        reset_button = ttk.Button(master=frame_5,text="Reset",command = self.tilibot_reset) # Create the Reset button for reseting the robot between trials
        shutdown_button = ttk.Button(master=frame_5,text="Shutdown",command = self.tilibot_shutdown) # Create a button to Shut down the robot 
        data_analysis_button = ttk.Button(master=frame_5,text="Analyse Data",command=self.analyse_data)
        visualize_data_button = ttk.Button(master=frame_5,text="Visualize Data",command=self.visualize_data)
        frame_5.grid(column=2,row=3,columnspan=3,sticky=tk.N) # Place frame on tkinter window
        save_settings_button.grid(row=0,column=0,sticky=tk.W,padx=5,pady=5) # Place save settings button in frame
        load_settings_button.grid(row=1,column=0,sticky=tk.W+tk.E,padx=5,pady=5) # Place load settings button in frame
        get_ready_button.grid(row=0,column=1,sticky=tk.W+tk.E,padx=5,pady=5) # Place get ready button in frame
        run_button.grid(row=0,column=2,sticky=tk.W+tk.E,padx=5,pady=5) # Place run button in frame
        data_analysis_button.grid(column=1,row=1,sticky=tk.W+tk.E,padx=5,pady=5)
        visualize_data_button.grid(column=2,row=1,sticky=tk.W+tk.E,padx=5,pady=5)
        reset_button.grid(row=2,column=1,sticky=tk.E+tk.W,padx=5,pady=5) # Place reset button in frame
        shutdown_button.grid(row=2,column=2,sticky=tk.E,padx=5,pady=5) # Place shutdown button in frame
        
        frame_6 = tk.Frame(master=self) # Create a frame to display the kinematics and settings file names
        kinematics_file_label = ttk.Label(master=frame_6,text="Kinematics File: ") # Create label for the kinematics file name label
        settings_file_label = ttk.Label(master=frame_6,text="Settings File: ") # Create label for settings file name label
        kinematics_file_selected = ttk.Label(master=frame_6,textvariable=self.kin_file_display,background="#CCD1D1") # Create label for kinematics file name changing display
        settings_file_selected = ttk.Label(master=frame_6,textvariable=self.set_file_display,background="#CCD1D1") # Create label for settings file name changing display
        frame_6.grid(column=1,row=4,columnspan=4) # Place frame on tkinter window
        kinematics_file_label.grid(row=0,column=0,sticky=tk.E,pady=5) # Place label in frame
        settings_file_label.grid(row=1,column=0,sticky=tk.E,pady=5) # Place label in frame
        kinematics_file_selected.grid(row=0,column=1,sticky=tk.W,pady=5) # Place label in frame
        settings_file_selected.grid(row=1,column=1,sticky=tk.W,pady=5) # Place label in frame
        

    def stop_operation(self): # Function for stopping the operation of the robot when running
        global STOP_VALUE # Make the STOP_VALUE variable global so it may be accessed and changed
        if STOP_VALUE == True: # Check if STOP button has been pressed
            self.destroy() # If it has been pressed, destroy the tkinter main window
            sys.exit("Tilibot Operation Stopped") # Exit the execution of the entire program
        else:
            self.after(250,self.stop_operation) # If STOP button has not been pressed, check again after after 250 milliseconds

    def set_stop_to_true(self): # Function to set STOP_VALUE equal to true if the stop button is pressed
        global STOP_VALUE # Make the STOP_VALUE variable global so it may be accessed and changed
        STOP_VALUE = True # Set the STOP_VALUE variable to True after the Stop! button has been pressed

    def calculate_run_time(self,*args): # Function to calculate the run time that would occur in a perfect closed environment with no errors
        try:
            calc_num = float(self.stride_time_entry_string.get()) * float(int(self.stride_amount_entry_string.get())) # Calculate the perfect run time using the two input numbers
            self.calc_end_time.set('{:.3f}'.format(calc_num)) # Set the calculated label to display the result
            self.Config_Options["stride_time"] = float(self.stride_time_entry_string.get())
            self.Config_Options["stride_amount"] = int(self.stride_amount_entry_string.get())
        except:
            pass    

    def open_help_box(self): # Function to open the help box and populate it with the proper widgets
        self.hb_object_box = tk.Toplevel(self) # Create a new window for the help box object
        self.hb_object_box.geometry("650x450") # Set the geometry of the help box window
        self.hb_object_box.title("Help Box Window") # Set the title of the help box window
        frame_12 = tk.Frame(master=self.hb_object_box) # Create a frame to hold the page change buttons
        self.page_1_button = tk.Button(master=frame_12,text="Intro",command= lambda b=1:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying the intro
        self.page_2_button = tk.Button(master=frame_12,text="1-Global Settings",command= lambda b=2:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-1
        self.page_3_button = tk.Button(master=frame_12,text="2-Detect Servos",command= lambda b=3:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-2
        self.page_4_button = tk.Button(master=frame_12,text="3-Mark Servos",command=lambda b=4:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-3
        self.page_5_button = tk.Button(master=frame_12,text="4-Servo Options",command=lambda b=5:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-4
        self.page_6_button = tk.Button(master=frame_12,text="5-Recording Options",command=lambda b=6:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-5
        self.page_7_button = tk.Button(master=frame_12,text="6-Stride Numbers",command=lambda b=7:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-6
        self.page_8_button = tk.Button(master=frame_12,text="7-Kinematics File",command=lambda b=8:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-7
        self.page_9_button = tk.Button(master=frame_12,text="8-Get Ready",command=lambda b=9:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-8
        self.page_10_button = tk.Button(master=frame_12,text="9-Run",command=lambda b=10:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-9
        self.page_11_button = tk.Button(master=frame_12,text="10-Clean Up",command=lambda b=11:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying step-10
        self.page_12_button = tk.Button(master=frame_12,text="Other",command=lambda b=12:self.show_hide_page(b),bg='#e0e0e0') # Create a button for displaying other relevant information
        self.page_1_display = ttk.Label(master=self.hb_object_box,text="The Tilibot Visual Controller is used to guide the operation of the Tilibot Robot. Follow the steps presented for proper execution without issue. The order of exection is as follows:\n\n 1. Global Settings\n 2. Detect Servos\n 3. Mark Servos\n 4. Servo Options\n 5. Recording Options\n 6. Stride Numbers\n 7. Kinematics File\n 8. Get Ready\n 9. Run\n 10. Clean Up\n\n For further questions or inquiries, please contact danegibbons@gmail.com or text (631) 456-7733.")
        self.page_2_display = ttk.Label(master=self.hb_object_box,text="The first step is to set your Global Settings.\n\n 1. Select the Global Settings box under the main title next to the Help Button.\n 2. Enter the Baud Rate (the speed at which the servos communicate)\n 3. and the Home Speed (the sped at which the robot will move to each home position).\n 4. Select Digital or Physical only, to indicate if the execution will happen only digitally or in physical space.\n 5. Then check off if the Body Sensors are connected or not.\n\nAlternatively, you could press the Load Settings button to load a pre-filled out YAML file. This will fill all input boxes, checkboxes, and radio buttons to specified parameters. The Multiple Servos options will still need to be checked and the Apply button will need to be hit. Servos will still need to be detected and marked as well.")
        self.page_3_display = ttk.Label(master=self.hb_object_box,text="The second step is to detect your servos.\n\n 1. Simply hit the Detect Servos button and the list should populate itself.\n\n The colors of the servos on the schematic should turn yellow, indicating that the servo was detected, but no option was selected yet.")
        self.page_4_display = ttk.Label(master=self.hb_object_box,text="The third step is to mark your servos.\n\n 1. Highlight the specific servos on the list using your cursor which should be moving and select 'Mark Seleced to Move'.\n 2. You will repeat the process once again, marking the servos which should NOT move and hitting the 'Mark Selected to Stay Straight' button.\n\n Typically servos 1-16 should be marked as moving, due to them being the limb servos, and 17-24 should be marked as staying straight, as they are the spine.")
        self.page_5_display = ttk.Label(master=self.hb_object_box,text="The fourth step is to set your servo options.\n\n 1. Select if one servo or multiple servos are moving by selecting the corresponding radio button to the right of the Detect Connected Servos button.\n 2. Then hit Configure Options to open up the servos options box.\n\n 2a. Enter the Number of Positions a servo should hit for each stride.\n 2b. Enter the Forelimb Stance and Swing ratios (These are the relative time proportions the stance and swing sections of a stride are measured as being)\n *After entering these numbers, a total will be calculated to the right.\n 2c. Enter the Forelimb Stance and Swing ratios\n *If the top calculated number is not equal to the bottom calculated number, the run will not operate, and the numbers will need to be fixed so they match.\n 2d. Hit Apply")
        self.page_6_display = ttk.Label(master=self.hb_object_box,text="The fifth step is to set your recording options.\n\n 1. Check off if you will be recording data or not\n 2. Then hit the 'Configure Options' button.\n\n 2a. Hit the 'Select Target Directory' button. Select the directory location in which you want the data being exported to end up.\n 2b. Enter the name of the file to be exported.\n 2c. Select which options you'd like to record,as detailed below\n 2d. Hit Apply\n\n Position: The Servo Position in Dynamixel units\n Speed: The Servo Speed in Dynamixel Units\n Time: The time at which the servo stops moving per movement.\n Position Index: Which position out of the amount of positions indicated in Step 4\n Stride Count: Which stride each movement takes place in as indicated in Step 7\n Current: The Current at the end of each servo movement\n Voltage: The Voltage at the end of each servo movement\n Temperature: The Temperature at the end of each servo movement.")
        self.page_7_display = ttk.Label(master=self.hb_object_box,text="The sixth step is to set the stride time and amount\n\n 1. Enter the Stride Time (The amount of time in seconds it is desired one stride should take)\n 2. Enter the Stride Amount (The amount of strides the robot should attempt to make before being considered finished).")
        self.page_8_display = ttk.Label(master=self.hb_object_box,text="The seventh step is to load the Kinematics File.\n\n 1. Simply hit the 'Load Kinematics File' button. The selected file should be a .csv and should include servos 1-16 (or the servos that should move).\n\nNOTE: If you reset the robot to run again, then change the stride time and/or stride amount, hit the Kinematics File button to recalculate the speeds. It will not ask you to select another file to import.")
        self.page_9_display = ttk.Label(master=self.hb_object_box,text="The eighth step is to hit the 'Get Ready' Button.\n\n After hitting the button, the robot should rise its legs up in the air, then place them down, putting all servos at 90 degrees and suspending the robot in a basic standing position. It should then move its limbs to the official 'Home Position', in which its limbs are in the actual first position of a stride, as dictated by the kinematics file.")
        self.page_10_display = ttk.Label(master=self.hb_object_box,text="The ninth step is to hit the 'Run' Button.\n\n The robot should now run, using all the previous details to run according to the expected configurations. Once the desired amount of strides is complete, the robot will stop moving, remaining still but with the servos still activated.")
        self.page_11_display = ttk.Label(master=self.hb_object_box,text="The tenth step is to select either the 'Reset' Button to reset the robot for another run, or the 'Shutdown' Button to shutdown and finish using Tilibot.\n\n Reseting the robot will change the indicator light to orange, indicating that the robot is ready to run again, but is not in the designated Home Position. The torque for each servo should be turned off and the robot will fall to the floor.\n\n At this point you may repeat steps 8,9, and 10 to continue running Tilibot through trials. If recording data, please be sure to rename your file from Step 6 between runs so as to not cause an issue.\n\n When finished, please select 'Shutdown'.")
        self.page_12_display = ttk.Label(master=self.hb_object_box,text="When repeatedly using the Tilibot GUI, certain settings will be used over and over. Use the 'Save Current Settings' button to create a .yml file to save all the settings currently applied. When running in the future, you may use the 'Load Settings File' button to reapply all fields from the previous steps.\n\n *Note: The servos will still have to be detected and marked after loading a settings file.\n\n\n If at any point in time you have an issue with running and need to terminate the trial, press the Red 'Stop!' button at the bottom of the schematic.")
        frame_12.grid(row=0,column=0,pady=10,padx=5) # Place the frame with page buttons in the tkinter window
        self.page_1_button.grid(row=0,column=0,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_2_button.grid(row=0,column=1,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_3_button.grid(row=0,column=2,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_4_button.grid(row=0,column=3,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_5_button.grid(row=0,column=4,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_6_button.grid(row=0,column=5,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_7_button.grid(row=1,column=0,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_8_button.grid(row=1,column=1,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_9_button.grid(row=1,column=2,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_10_button.grid(row=1,column=3,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_11_button.grid(row=1,column=4,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.page_12_button.grid(row=1,column=5,pady=3,padx=3,sticky=tk.E+tk.W) # Place the button in the frame
        self.hb_dictionary_displays = {1:self.page_1_display,2:self.page_2_display,3:self.page_3_display,4:self.page_4_display, # Create dictionary with different displays stored for reference
                                  5:self.page_5_display,6:self.page_6_display,7:self.page_7_display,8:self.page_8_display,
                                  9:self.page_9_display,10:self.page_10_display,11:self.page_11_display,12:self.page_12_display} 
        self.hb_dictionary_buttons = {1:self.page_1_button,2:self.page_2_button,3:self.page_3_button,4:self.page_4_button, # Create dictionary with different buttons stored for reference
                                  5:self.page_5_button,6:self.page_6_button,7:self.page_7_button,8:self.page_8_button,
                                  9:self.page_9_button,10:self.page_10_button,11:self.page_11_button,12:self.page_12_button}                          
        self.hb_dictionary_buttons[self.active_help_page].config(bg="#9c9c9c") # Configure the active page button to be grayed darker than the rest
        self.hb_dictionary_displays[self.active_help_page].grid(row=1,column=0,sticky=tk.W+tk.E) # Place the proper corresponding display text when the box is opened
        self.hb_dictionary_displays[self.active_help_page].config(wraplength = 575) # Set the wraplength so the text fits within the box
        close_button = ttk.Button(master=self.hb_object_box,text="Close",command=self.close_help_box) # Create a close button to close the external window 
        close_button.grid(row=2,column=0,pady=10) # Place the button in the help box window

    def show_hide_page(self,button_clicked): # Function to change the current help box display after a page button is pressed
        if button_clicked == self.active_help_page: # Don't do anything if the button clicked is the same as the active help page
            pass
        else: # Otherwise, change the active help page
            self.hb_dictionary_buttons[self.active_help_page].config(bg='#e0e0e0') # Change the active help page button to be light gray like the other unselected buttons
            self.hb_dictionary_buttons[button_clicked].config(bg="#9c9c9c") # Change the new active help page button to a dark color to indicate it is the current selected page
            self.hb_dictionary_displays[self.active_help_page].grid_forget() # Get rid of the current displayed page text
            self.hb_dictionary_displays[button_clicked].grid(row=1,column=0,sticky=tk.W+tk.E) # Display the new selected page text
            self.hb_dictionary_displays[button_clicked].config(wraplength=575) # Set the wraplength so the text fits within the box
            self.active_help_page = button_clicked # Change the active_help_page variable to accurately represent the last button clicked

    def close_help_box(self): # Function to close the help box when the corresponding button is clicked
        self.hb_object_box.destroy() # Destroy the help box so it no longer exists

    def open_global_settings_box(self): # Function to open the global settings box and populate it with the proper widgets
        self.run_condition = tk.IntVar() # Create variable to house the run condition setting
        self.gs_object_box = tk.Toplevel(self) # Create a new window for the global settings box object
        self.gs_object_box.geometry("295x200") # Set the geometry for the new window
        self.gs_object_box.title("Global Settings") # Set the title for the new window
        self.baud_rate_entry_string = tk.StringVar() # Create string variable to store the baud rate value input
        self.home_speed_entry_string = tk.StringVar() # Create string variable to store home speed value input
        baud_rate_label = ttk.Label(master=self.gs_object_box,text="Baud Rate Here:") # Create label to display where to put baud rate input
        baud_rate_entry = ttk.Entry(master=self.gs_object_box,textvariable=self.baud_rate_entry_string) # Create entry to input baud rate
        home_speed_label = ttk.Label(master=self.gs_object_box,text="Home Speed Here:") # Create label to display where to put home speed input
        home_speed_entry = ttk.Entry(master=self.gs_object_box,textvariable=self.home_speed_entry_string) # Create entry to input home speed
        frame_7 = tk.Frame(master=self.gs_object_box) # Create Frame to house digital or physical radio buttons
        run_digital_rb = ttk.Radiobutton(master=frame_7,text="Digital Only",variable=self.run_condition,value=1) # Create radio button to indicate the trials will be digitally based only
        run_physical_rb = ttk.Radiobutton(master=frame_7,text="Physical Only",variable=self.run_condition,value=0) # Create radio button to indicate the trials will be physically based in 3d space
        self.run_condition.set(0) # Set the run condition to 0, assuming it is 3d space by default
        self.sensors_connect = tk.IntVar() # Create an integer variable to houes if external sensors are connected or not
        self.sensors_connect.set(0) # Set the sensors connected variable to 0, indicating by default that they are not connected
        sensors_connected_cb = ttk.Checkbutton(master=self.gs_object_box,text="Body Sensors Connected?",variable=self.sensors_connect) # Create check button to indicate if external body sensors are connected or not
        apply_button = ttk.Button(master=self.gs_object_box,text="Apply",command=self.apply_global_settings) # Create buton to apply settings changes
        close_button = ttk.Button(master=self.gs_object_box,text="Close",command=self.close_global_settings_box) # Create button to close global settings box
        baud_rate_label.grid(row=0,column=0,sticky=tk.W+tk.S,pady=5,padx=5) # Place label in tkinter window
        home_speed_label.grid(row=0,column=1,sticky=tk.W+tk.S,pady=5,padx=5) # Place label in tkinter window
        baud_rate_entry.grid(row=1, column=0,sticky=tk.W+tk.N,padx=5) # Place entry box in tkinter window
        home_speed_entry.grid(row=1, column=1,sticky=tk.E+tk.N,padx=5) # Place entry box in tkinter window
        frame_7.grid(row=2,column=0,columnspan=2) # Place the frame on the tkinter window
        run_digital_rb.grid(row=0,column=0,sticky=tk.W,pady=10,padx=5) # Place the radio button in the frame
        run_physical_rb.grid(row=0,column=1,sticky=tk.E,pady=10,padx=5) # Place the radio button in the frame
        sensors_connected_cb.grid(row=3,column=0, columnspan=2,pady=10) # Place the checkbox in the frame
        apply_button.grid(row=4,column=0,pady=10) # Put Apply button in global settings window
        close_button.grid(row=4,column=1,pady=10) # Put Close button in global settings window
        # Apply settings to widgets if pre-loaded
        if self.Config_Options["baud_rate"] != None: # If baud rate already exists
            self.baud_rate_entry_string.set(str(self.Config_Options["baud_rate"])) # Set the display baud rate to the pre-determined baud rate
        if self.Config_Options["home_speed"] != None: # If home speed already exists
            self.home_speed_entry_string.set(str(self.Config_Options["home_speed"])) # Set the display home speed to the rpe-determined home speed
        if self.Config_Options["run_digital_only"] == True: # If run digital only is pre-determined to be true
            self.run_condition.set(1) # Set the widget to be digital only
        elif self.Config_Options["run_digital_only"] == False: # Else if run digital only is pre-determined to be false
            self.run_condition.set(0) # Set the widget to be physical only
        if self.Config_Options["connected_sensors"] == True: # If sensors connected is pre-determined to be true
            self.sensors_connect.set(1) # Set the widget to be checked

    def apply_global_settings(self): # Function to apply global settings to config dictionary variable when button pressed
        global Step_Progressor
        self.Config_Options["baud_rate"] = int(self.baud_rate_entry_string.get()) # Set baud rate in Config_Options dictionary from entry input
        self.Config_Options["home_speed"] = int(self.home_speed_entry_string.get()) # Set home speed in Config_Options dictionary from entry input
        run_dig_result = self.run_condition.get() # Get the run condition from the radio buttons
        if run_dig_result == 1: # If run digital only is selected
            self.Config_Options["run_digital_only"] = True # Set the value to true
        else: # If run physically is selected
            self.Config_Options["run_digital_only"] = False # Set the value to false
        self.Config_Options["connected_sensors"] = bool(self.sensors_connect.get()) # Set the connected sensors variable equal to either true or false, dependent on the checkbox
        Step_Progressor = 1
        
    def close_global_settings_box(self): # Function to destroy 
        # Code to save and close
        self.gs_object_box.destroy() # Destroy the global settings window
    
    def open_move_box(self): # Function to open the move settings box and populate it with the proper widgets
        global Step_Progressor
        if Step_Progressor < 3:
            messagebox.showerror(title="Error",message="Error - Servos not marked yet. Cannot set move settings before servos are marked.")
        else:
            self.ms_object_box = tk.Toplevel(self) # Create a new window for Move Settings box object
            self.pos_per_stride = tk.StringVar() # Create a variable to hold the amount of positions per stride
            self.FL_st_ratio = tk.StringVar() # Create a variable to hold the forelimb stance ratio time
            self.FL_sw_ratio = tk.StringVar() # Create a variable to hold the forelimb swing ratio time
            self.HL_st_ratio = tk.StringVar() # Create a variable to hold the hindlimb stance ratio time
            self.HL_sw_ratio = tk.StringVar() # Create a variable to hold the hindlimb swing ratio time
            self.ms_object_box.geometry("450x250") # Set the geometry of the move settings box
            self.ms_object_box.title("Move Servo Options") # Set the title of the move settings box
            positions_per_stride_label = ttk.Label(master=self.ms_object_box,text="# of Positions per Stride Here") # Create label to indicate positions per stride input
            positions_per_stride_entry = ttk.Entry(master=self.ms_object_box,textvariable=self.pos_per_stride) # Create input for the amount of positions per stride
            Forelimb_Stance_label = ttk.Label(master=self.ms_object_box,text="Forelimb Stance Ratio:") # Create a label to indicate input for the forelimb stance ratio
            Forelimb_Stance_entry = ttk.Entry(master=self.ms_object_box,textvariable=self.FL_st_ratio) # Create an input for the Forelimb Stance Ratio time
            Forelimb_Swing_label = ttk.Label(master=self.ms_object_box,text="Forelimb Swing Ratio:") # Create a label to indicate input for the forelimb swing ratio
            Forelimb_Swing_entry = ttk.Entry(master=self.ms_object_box,textvariable=self.FL_sw_ratio) # Create an input for the Forelimb Swing Ratio time
            Hindlimb_Stance_label = ttk.Label(master=self.ms_object_box,text="Hindlimb Stance Ratio:") # Create a label to indicate input for the hindlimb stance ratio
            Hindlimb_Stance_entry = ttk.Entry(master=self.ms_object_box,textvariable=self.HL_st_ratio) # Create an input for the Hindlimb Stance Ratio time
            Hindlimb_Swing_label = ttk.Label(master=self.ms_object_box,text="Hindlimb Swing Ratio:") # Create a label to indicate input for the hindlimb swing ratio
            Hindlimb_Swing_entry = ttk.Entry(master=self.ms_object_box,textvariable=self.HL_sw_ratio) # Create an input for the Hindlimb Swing Ratio time
            self.Forelimb_Ratio_Time_label = ttk.Label(master=self.ms_object_box,text="= ",background='#979A9A') # Create label to display the sum of forelimb ratio times
            self.Hindlimb_Ratio_Time_label = ttk.Label(master=self.ms_object_box,text="= ",background='#979A9A') # Create a label to display the sum of hindlimb ratio times
            plus_a = ttk.Label(master=self.ms_object_box,text="+",background='#979A9A') # Create a label to display adding
            plus_b = ttk.Label(master=self.ms_object_box,text="+",background='#979A9A') # Create a label to display adding
            self.FL_st_ratio.trace('w',self.add_fl_nums) # Create a callback when forelimb stance ratio is changed
            self.FL_sw_ratio.trace('w',self.add_fl_nums) # Create a callback when forelimb swing ratio is changed
            self.HL_st_ratio.trace('w',self.add_hl_nums) # Create a callback when hindlimb stance ratio is changed
            self.HL_sw_ratio.trace('w',self.add_hl_nums) # Create a callback when hindlimb swing ratio is changed
            apply_button = ttk.Button(master=self.ms_object_box,text="Apply",command=self.apply_move_settings) # Create button to apply settings changes
            close_button = ttk.Button(master=self.ms_object_box,text="Close",command=self.close_move_box) # Create button to close/destroy the move settings box
            positions_per_stride_label.grid(row=0,column=0,pady=5,padx=10,sticky=tk.S) # Put label in tkinter window
            positions_per_stride_entry.grid(row=1,column=0,pady=5,sticky=tk.W,padx=10)# Put entry in tkinter window
            Forelimb_Stance_label.grid(row=2,column=0,sticky=tk.W,padx=10,pady=5) # Put label in tkinter window
            Forelimb_Stance_entry.grid(row=3,column=0,sticky=tk.W,padx=10,pady=5) # Put entry in tkinter window
            plus_a.grid(row=3,column=1,pady=5) # Put + in tkinter window
            Forelimb_Swing_label.grid(row=2,column=2,sticky=tk.E,padx=10,pady=5) # Put label in tkinter window
            Forelimb_Swing_entry.grid(row=3,column=2,sticky=tk.E,padx=10,pady=5) # Put entry in tkinter window
            self.Forelimb_Ratio_Time_label.grid(row=3,column=3,sticky=tk.W,padx=10,pady=5)
            Hindlimb_Stance_label.grid(row=4,column=0,sticky=tk.W,padx=10,pady=5) # Put label in tkinter window
            Hindlimb_Stance_entry.grid(row=5,column=0,sticky=tk.W,padx=10,pady=5) # Put entry in tkinter window
            plus_b.grid(row=5,column=1,pady=5) # Put + in tkinter window
            Hindlimb_Swing_label.grid(row=4,column=2,sticky=tk.E,padx=10,pady=5) # Put label in tkinter window
            Hindlimb_Swing_entry.grid(row=5,column=2,sticky=tk.E,padx=10,pady=5) # Put entry in tkinter window
            self.Hindlimb_Ratio_Time_label.grid(row=5,column=3,sticky=tk.W,padx=10,pady=5) # Put label in tkinter window
            apply_button.grid(row=6,column=0,pady=15) # Put Apply Button in tkinter window
            close_button.grid(row=6,column=3,pady=15) # Put Close Button in tkinter window
            # Apply settings to widgets if pre-loaded
            if self.Config_Options["position_amount"] != None: # If Position Amount is pre-determined
                self.pos_per_stride.set(str(self.Config_Options["position_amount"])) # Set the entry to display the pre-determined value
            if self.Config_Options["forelimb_stance_time"] != None: # If Forelimb Stance is pre-determined
                self.FL_st_ratio.set(str(self.Config_Options["forelimb_stance_time"])) # Set the entry to display the pre-determined value
            if self.Config_Options["forelimb_swing_time"] != None: # If Forelimb Swing is pre-determined
                self.FL_sw_ratio.set(str(self.Config_Options["forelimb_swing_time"])) # Set the entry to display the pre-determined value
            if self.Config_Options["hindlimb_stance_time"] != None: # If Hindlimb Stance is pre-determined
                self.HL_st_ratio.set(str(self.Config_Options["hindlimb_stance_time"])) # Set the entry to display the pre-determined value
            if self.Config_Options["hindlimb_swing_time"] != None: # If Hindlimb Swing is pre-determined
                self.HL_sw_ratio.set(str(self.Config_Options["hindlimb_swing_time"])) # Set the entry to display the pre-determined value
            Step_Progressor = 4
        
    def add_fl_nums(self,*args): # Function to add forelimb ratios to find the total time
        try:
            num_1 = float(self.FL_st_ratio.get()) # If possible, get the input float number and convert to number from string
        except:
            num_1 = 0.000000 # If not possible, set the ratio time to 0.000000
        try:
            num_2 = float(self.FL_sw_ratio.get()) # If possible, get the input float number and convert to number from string
        except:
            num_2 = 0.000000 # If not possible, set the ratio time to 0.000000
        num_3 = num_1 + num_2 # Sum the two ratio numbers together
        self.Forelimb_Ratio_Time_label['text'] = '{:.6f}'.format(num_3) # Format and display the sum time

    def add_hl_nums(self,*args): # Function to add hindlimb ratios to find the total time
        try:
            num_1 = float(self.HL_st_ratio.get()) # If possible, get the input float number and convert to number from string
        except:
            num_1 = 0.000000 # If not possible, set the ratio time to 0.000000
        try:
            num_2 = float(self.HL_sw_ratio.get()) # If possible, get the input float number and convert to number from string
        except:
            num_2 = 0.000000 # If not possible, set the ratio time to 0.000000
        num_3 = num_1 + num_2 # Sum the two ratio numbers together
        self.Hindlimb_Ratio_Time_label.config(text='{:.6f}'.format(num_3)) # Format and display the sum time

    def apply_move_settings(self): # Function to set Config_Options dictionary values to pre-determined values
        # Check that total ratio times match first
        if self.Forelimb_Ratio_Time_label['text'] == self.Hindlimb_Ratio_Time_label['text']: # If both ratio times match eachother
            self.Config_Options["position_amount"] = int(self.pos_per_stride.get()) # Set Position Amount to pre-determined value
            self.Config_Options["forelimb_stance_time"] = float(self.FL_st_ratio.get()) # Set Forelimb Stance Time to pre-determined value
            self.Config_Options["forelimb_swing_time"] = float(self.FL_sw_ratio.get()) # Set Forelimb Swing Time to pre-determined value
            self.Config_Options["hindlimb_stance_time"] = float(self.HL_st_ratio.get()) # Set Hindlimb Stance Time to pre-determined value
            self.Config_Options["hindlimb_swing_time"] = float(self.HL_sw_ratio.get()) # Set Hindlimb Swing Time to pre-determined value
            self.Config_Options["tot_ratio_time"] = float(self.Forelimb_Ratio_Time_label['text'])
            print("\nApplying move ratio settings - " + str(self.Config_Options["tot_ratio_time"]) + "s")
        else:
            messagebox.showwarning(title="Ratio Error", message="Ratio times for Front and Hind Limbs do not match. Please fix and try again.")
            
    def close_move_box(self): # Function to close/destroy settings box
        self.ms_object_box.destroy() # Destroy/close move settings box

    def ask_for_target_dir(self):
        self.rd_target_dir.set(str(fdlg.askdirectory()))

    def open_record_data_box(self): # Function to open the record data settings box and populate it with the proper widgets
        self.rd_object_box = tk.Toplevel(self) # Create a new window for the Record Data settings box object
        self.rd_object_box.geometry("340x260") # Create geometry for new window
        self.rd_object_box.title("Record Data Options Window") # Create title for new window
        frame_8=tk.Frame(master=self.rd_object_box) # Create frame to hold check boxes for recording options
        frame_9=tk.Frame(master=self.rd_object_box) # Create frame to hold apply and close buttons
        select_target_dir_button = ttk.Button(master=self.rd_object_box,text="Select Target Directory:",command=self.ask_for_target_dir) # Create button to select the target directory destination for out data file
        display_target_dir_label = ttk.Label(master=self.rd_object_box,textvariable=self.rd_target_dir,background="#979A9A") # Create label to display selected output directory
        output_name_label = ttk.Label(master=self.rd_object_box,text="Enter Output File Name Here:") # Create Label to indicate where to enter the output file name
        output_name_entry = ttk.Entry(master=self.rd_object_box,textvariable=self.rd_out_file_name) # Create Entry to type output file name
        self.pos_output = tk.IntVar() # Create variable to store if position is to be recorded
        self.pos_output.set(0) # Set the checkbox to be unchecked
        position_output_cb = ttk.Checkbutton(master=frame_8,text="Position",variable=self.pos_output) # Create Checkbutton to select option to be recorded
        self.speed_output = tk.IntVar() # Create variable to store if speed is to be recorded
        self.speed_output.set(0)# Set the checkbox to be unchecked
        speed_output_cb = ttk.Checkbutton(master=frame_8,text="Speed",variable=self.speed_output) # Create Checkbutton to select option to be recorded
        self.time_output = tk.IntVar() # Create variable to store if time is to be recorded
        self.time_output.set(0)# Set the checkbox to be unchecked
        time_output_cb = ttk.Checkbutton(master=frame_8,text="Time",variable=self.time_output) # Create Checkbutton to select option to be recorded
        self.pos_ind_output = tk.IntVar() # Create variable to store if position index is to be recorded
        self.pos_ind_output.set(0)# Set the checkbox to be unchecked
        position_index_cb = ttk.Checkbutton(master=frame_8,text="Position Index",variable=self.pos_ind_output) # Create Checkbutton to select option to be recorded
        self.stct_output = tk.IntVar() # Create variable to store if stride count is to be recorded
        self.stct_output.set(0)# Set the checkbox to be unchecked
        stride_count_cb = ttk.Checkbutton(master=frame_8,text="Stride Count",variable=self.stct_output) # Create Checkbutton to select option to be recorded
        self.current_output = tk.IntVar() # Create variable to store if current is to be recorded
        self.current_output.set(0)# Set the checkbox to be unchecked
        current_output_cb = ttk.Checkbutton(master=frame_8,text="Current",variable=self.current_output) # Create Checkbutton to select option to be recorded
        self.voltage_output = tk.IntVar() # Create variable to store if voltage is to be recorded
        self.voltage_output.set(0)# Set the checkbox to be unchecked
        voltage_output_cb = ttk.Checkbutton(master=frame_8,text="Voltage",variable=self.voltage_output) # Create Checkbutton to select option to be recorded
        self.temp_output = tk.IntVar() # Create variable to store if temperature is to be recorded
        self.temp_output.set(0)# Set the checkbox to be unchecked
        temperature_output_cb = ttk.Checkbutton(master=frame_8,text="Temperature",variable=self.temp_output) # Create Checkbutton to select option to be recorded
        apply_button = ttk.Button(master=frame_9,text="Apply",command=self.apply_record_settings) # Create apply button to set Config_Options dictionary to determined values
        close_button = ttk.Button(master=frame_9,text="Close",command=self.close_record_data_box) # Create Close button to destroy/close data settings window
        select_target_dir_button.grid(row=0,column=0,pady=10) # Place button in tkinter window
        display_target_dir_label.grid(row=1,column=0,sticky=tk.W+tk.E,padx=5,pady=5) # Place label in tkinter window
        output_name_label.grid(row=2,column=0,pady=5,sticky=tk.S) # Place label in tkinter window
        output_name_entry.grid(row=3,column=0,sticky=tk.W+tk.E+tk.N,padx=5,pady=5) # Place entry in tkinter window
        frame_8.grid(row=4,column=0,columnspan=3,pady=10) # Place frame in tkinter window
        position_output_cb.grid(row=0,column=0,sticky=tk.W,padx=10) # Place checkbox in frame
        speed_output_cb.grid(row=1,column=0,sticky=tk.W,padx=10) # Place checkbox in frame
        time_output_cb.grid(row=2,column=0,sticky=tk.W,padx=10) # Place checkbox in frame
        position_index_cb.grid(row=0,column=1,sticky=tk.W,padx=10) # Place checkbox in frame
        stride_count_cb.grid(row=1,column=1,sticky=tk.W,padx=10) # Place checkbox in frame
        current_output_cb.grid(row=0,column=2,sticky=tk.W,padx=10) # Place checkbox in frame
        voltage_output_cb.grid(row=1,column=2,sticky=tk.W,padx=10) # Place checkbox in frame
        temperature_output_cb.grid(row=2,column=2,sticky=tk.W,padx=10) # Place checkbox in frame
        frame_9.grid(row=5,column=0,columnspan=2,pady=10) # Place frame in tkinter window
        apply_button.grid(row=0,column=0,sticky=tk.W,padx=10) # Place button in frame
        close_button.grid(row=0,column=1,sticky=tk.W,padx=10) # Place button in frame
        # Apply settings to widgets if pre-loaded
        if self.Config_Options["out_file_dir"] != None: # If Output File Directory already exists
            self.rd_target_dir.set(self.Config_Options["out_file_dir"]) # Set option in display
        if self.Config_Options["out_file_name"] != None: # If Output File Name already exists
            self.rd_out_file_name.set(self.Config_Options["out_file_name"]) # Set option in Display
        if self.Config_Options["position_write"] != None: # If the Position record option is already selected
            self.pos_output.set(self.Config_Options["position_write"]) # Set option in display
        if self.Config_Options["speed_write"] != None: # If the Speed record option is already selected
            self.speed_output.set(self.Config_Options["speed_write"]) # Set option in display
        if self.Config_Options["time_write"] != None: # If the Time record option is already selected
            self.time_output.set(self.Config_Options["time_write"]) # Set option in display
        if self.Config_Options["posindex_write"] != None: # If the Position Index record option is already selected
            self.pos_ind_output.set(self.Config_Options["posindex_write"]) # Set option in display
        if self.Config_Options["stridecount_write"] != None: # If the Stride Count record option is already selected
            self.stct_output.set(self.Config_Options["stridecount_write"]) # Set option in display
        if self.Config_Options["current_write"] != None: # If the Current record option is already selected
            self.current_output.set(self.Config_Options["current_write"]) # Set option in display
        if self.Config_Options["voltage_write"] != None: # If the Voltage record option is already selected
            self.voltage_output.set(self.Config_Options["voltage_write"]) # Set option in display
        if self.Config_Options["temp_write"] != None: # If the Temperature record option is already selected
            self.temp_output.set(self.Config_Options["temp_write"]) # Set option in display

    def apply_record_settings(self): # Function to apply input settings to Config_Options dictionary
        self.Config_Options["out_file_dir"] = str(self.rd_target_dir.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["out_file_name"] = str(self.rd_out_file_name.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["position_write"] = bool(self.pos_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["speed_write"] = bool(self.speed_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["time_write"] = bool(self.time_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["posindex_write"] = bool(self.pos_ind_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["stridecount_write"] = bool(self.stct_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["current_write"] = bool(self.current_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["voltage_write"] = bool(self.voltage_output.get()) # Set variable in Config_Options dictionary to input value
        self.Config_Options["temp_write"] = bool(self.temp_output.get()) # Set variable in Config_Options dictionary to input value

    def select_targ_dir(self): # Function to open up a file explorer window to select a target directory when the button is hit
        selected_directory = fdlg.askdirectory() # Open up file explorer and ask for directory 
        self.rd_target_dir.set(selected_directory) # Set the label to reflect the selected directory

    def close_record_data_box(self): # Function to close/delete the record data box
        self.rd_object_box.destroy() # Destroy/close the record data settings box 

    def open_save_settings_box(self): # Function to open the save settings box and populate it with the proper widgets
        self.ss_object_box = tk.Toplevel(self) # Create a new window for the Save Settings box object
        self.ss_object_box.geometry("300x150") # Set geometry of the save settings box
        self.ss_object_box.title("Save Settings Options Window") #  Set title of the save settings boc
        frame_10=tk.Frame(master=self.ss_object_box) # Create frame to house the entry and label of the settings file to save
        frame_11=tk.Frame(master=self.ss_object_box) # Create frame to house save and close buttons of settings file box
        ss_settings_file_name_label = ttk.Label(master=frame_10,text="Enter the name of the Settings File you wish to save: ") # Create label to indicate settings file name input
        ss_settings_file_name_input = ttk.Entry(master=frame_10,textvariable=self.ss_settings_file_name) # Create entry to enter save file name
        ss_save_button = ttk.Button(master=frame_11,text="Save",command=self.save_settings_file) # Create save button to save input options
        ss_close_button = ttk.Button(master=frame_11,text="Close",command=self.close_save_settings_box) # Create close button to destroy/close save settings box
        ss_footnote_label = ttk.Label(master=self.ss_object_box,text="*Note: The .yml extension will be added after the name provided above. Please do not include it.") # Footnote reminder text
        frame_10.grid(rowspan=2,columnspan=2,column=0,row=0,padx=5) # Place frame in tkinter window
        ss_settings_file_name_label.grid(column=0,row=0,pady=5,padx=5) # Place label in frame
        ss_settings_file_name_input.grid(column=0,row=1,pady=5,sticky=tk.W+tk.E,padx=5) # Place input in frame
        frame_11.grid(columnspan=2,row=2,column=0,padx=5) # Place frame in tkinter window
        ss_save_button.grid(column=0,row=0,pady=5) # Place button in frame
        ss_close_button.grid(column=1,row=0,pady=5) # Place button in frame
        ss_footnote_label.grid(row=3,pady=5,padx=5) # Place footnote in tkinter window
        ss_footnote_label.config(wraplength = 275) # Place footnote in tkinter window

    def save_settings_file(self): # Function to save settings to external YAML file
        saved_settings_file = str(self.ss_settings_file_name.get()) + ".yml" # Extract name from entry and append .yml extension
        Write_Settings_Doc(self.Config_Options,saved_settings_file) # Write the settings to the YAML file with the designated name

    def close_save_settings_box(self): # Function to close/destroy save settings box
        self.ss_object_box.destroy() # Destroy/close save settings box

    def open_reboot_reset_box(self): # Function to open reboot / reset box and populate it with the proper widgets
        self.rr_object_box = tk.Toplevel(self) # Create a new window for the Reboot / Reset box object
        self.rr_object_box.geometry("430x300") # Set geometry of the reboot / reset box
        self.rr_object_box.title("Reboot / Reset Window") #  Set title of the reboot / reset box
        self.reset_mode = tk.IntVar() # Create variable to house the reset mode value
        frame_13=tk.Frame(master=self.rr_object_box) # Create frame to house the entry and label of the reboot widgets
        frame_14=tk.Frame(master=self.rr_object_box) # Create frame to house entry and label of reset widgets
        frame_15=tk.Frame(master=self.rr_object_box) # Create frame to house the close button
        reboot_section_label = ttk.Label(master=frame_13,text="Reboot")
        reset_section_label = ttk.Label(master=frame_14,text="Reset")
        reboot_description_label = ttk.Label(master=frame_13,text = "Turns the servo off and then on. Good for fixing stalled servos.")
        reboot_description_label.config(wraplength = 150) # Set the wraplength so the text fits within the box
        reset_description_label = ttk.Label(master=frame_14,text = "Factory Resets all servo trait values to default values. Options to keep one or two values are also available.")
        reset_description_label.config(wraplength = 250) # Set the wraplength so the text fits within the box
        reboot_button = ttk.Button(master=frame_13,text="Reboot",command=self.RebootServo)
        reset_radio_button_1 = ttk.Radiobutton(master=frame_14,text="1 - reset all values (ID to 1, baudrate to 57600)",variable=self.reset_mode,value=1)
        reset_radio_button_2 = ttk.Radiobutton(master=frame_14,text="2 - reset all values except ID (baudrate to 57600)",variable=self.reset_mode,value=2)
        reset_radio_button_3 = ttk.Radiobutton(master=frame_14,text="3 - reset all values except ID and baudrate.",variable=self.reset_mode,value=3)
        self.reset_mode.set(3)
        reset_button = ttk.Button(master=frame_14,text="Reset",command=lambda b=self.reset_mode:self.ResetServo(b))
        self.reboot_ind_canvas = tk.Canvas(master=frame_13,width=30,height=30) # Create small canvas to place indicator light
        self.reb_indic_oval = self.reboot_ind_canvas.create_oval(10, 10, 30, 30)  # Create a circle on the Canvas
        self.reset_ind_canvas = tk.Canvas(master=frame_14,width=30,height=30) # Create small canvas to place indicator light
        self.res_indic_oval = self.reset_ind_canvas.create_oval(10, 10, 30, 30)  # Create a circle on the Canvas
        self.reboot_ind_canvas.itemconfig(self.reb_indic_oval, fill=self.servo_colors["red"])
        self.reset_ind_canvas.itemconfig(self.res_indic_oval, fill=self.servo_colors["red"])
        separate_1 = ttk.Separator(master=self.rr_object_box,orient=tk.VERTICAL)
        rr_close_button = ttk.Button(master=frame_15,text="Close",command=self.close_reboot_reset_box) # Create close button to destroy/close save settings box
        frame_13.grid(row=0,column=0)
        separate_1.grid(row=0,column=1,sticky=tk.N+tk.S)
        frame_14.grid(row=0,column=2)   
        frame_15.grid(row=1,column=0,columnspan=3)
        reboot_section_label.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N,padx=5,pady=5)
        reboot_description_label.grid(row=1,column=0,sticky=tk.W+tk.E,padx=5,pady=5)
        reboot_button.grid(row=5,column=0,sticky=tk.S,padx=5,pady=5)
        self.reboot_ind_canvas.grid(row=6,column=0)
        reset_section_label.grid(row=0,column=0,sticky=tk.W+tk.E+tk.N,padx=5,pady=5)
        reset_description_label.grid(row=1,column=0,sticky=tk.W+tk.E+tk.N,padx=5,pady=5)
        reset_radio_button_1.grid(row=2,column=0,sticky=tk.W+tk.E,padx=5,pady=5)
        reset_radio_button_2.grid(row=3,column=0,sticky=tk.W+tk.E,padx=5,pady=5)
        reset_radio_button_3.grid(row=4,column=0,sticky=tk.W+tk.E,padx=5,pady=5)
        reset_button.grid(row=5,column=0,sticky=tk.S,padx=5,pady=5)
        self.reset_ind_canvas.grid(row=6,column=0)
        rr_close_button.grid(row=0,column=0,sticky=tk.W+tk.E,padx=5,pady=5)
        
    def close_reboot_reset_box(self): # Function to close/destroy reboot / reset box
        self.rr_object_box.destroy()

    def detect_servos(self): # Function to detect which servos are connected to the ports of the resident raspberry pi
        global Step_Progressor
        if Step_Progressor < 1:
            messagebox.showerror(title="Error",message="Error - Global Settings not set yet. Cannot detect servos without global settings.")
        else:
            if self.Config_Options["baud_rate"] != None: # If the baud rate has been set
                connected_servo_list = [] # Establish a list for all detected servos to be added to
                connected_limb_list = [] # Establish a list for all detected limbs to be added to
                portHandler_1, portHandler_2, portHandler_3, portHandler_4, portHandler_5, portHandler_6, self.packetHandler = Packet_Port_Setup(self.Config_Options["baud_rate"]) # Create port handler and packet handler objects
                self.port_hand_list = [portHandler_1, portHandler_2, portHandler_3, portHandler_4, portHandler_5, portHandler_6] # Append these objects to an easy to access list
                dxl_data_list = PingServos(self.port_hand_list,self.packetHandler) # Ping the ports to identify which servos are connected to the raspberry pi through the ports
                self.port_servo_dict, self.port_used_dict = Port_Servo_Assign(dxl_data_list,self.port_hand_list) # Create lists detailing which servos are assigned to which ports
                for each_servo in self.port_used_dict.keys(): # For each servo in the port used 
                    detected_servo = "Servo " + str(each_servo) # Create text object of the servo
                    self.servo_listbox.insert(tk.END,detected_servo) # Add servo to listbox next to schematic
                    self.change_servo_color(each_servo,"yellow") # Change the color of the corresponding servo graphic to yellow - detected but not designated 
                    connected_servo_list.append(each_servo) # Add each servo to the temporary variable connected_servo_list
                self.Config_Options["connected_servos"] = connected_servo_list # Replace the settings variable with the now populated connected servo list
                if(all(item in connected_servo_list for item in F_R_ARM)): # check if all front right leg servos are connected
                    connected_limb_list.append(1) # If yes, append front right limb to connected limbs list
                if(all(item in connected_servo_list for item in F_L_ARM)): # check if all front left leg servos are connected
                    connected_limb_list.append(2) # If yes, append front left limb to connected limbs list
                if(all(item in connected_servo_list for item in B_R_ARM)): # check if all back right leg servos are connected
                    connected_limb_list.append(3) # If yes, append back right limb to connected limbs list
                if(all(item in connected_servo_list for item in B_L_ARM)): # check if all back left leg servos are connected
                    connected_limb_list.append(4) # If yes, append back left limb to connected limbs list
                if(all(item in connected_servo_list for item in NECK)): # check if all neck servos are connected
                    connected_limb_list.append(5) # If yes, append neck to connected limbs list
                if(all(item in connected_servo_list for item in SPINE)): # check if all spine servos are connected
                    connected_limb_list.append(6) # If yes, append spine to connected limbs list
                if(all(item in connected_servo_list for item in TAIL)): # check if all tail servos are connected
                    connected_limb_list.append(7) # If yes, append tail to connected limbs list
                self.Config_Options["connected_limbs"] = connected_limb_list # Replace the settings variable with the now populated connected limb list
                for each_port in self.port_used_dict.values():
                    if each_port == 0: # If port 1 is identified as being used
                        self.myCanvas.itemconfig(self.port_1_indicator,fill=self.servo_colors["green"]) # Set the port 1 indicator to green
                    elif each_port == 1: # If port 2 is identified as being used
                        self.myCanvas.itemconfig(self.port_2_indicator,fill=self.servo_colors["green"]) # Set the port 2 indicator to green
                    elif each_port == 2: # If port 3 is identified as being used
                        self.myCanvas.itemconfig(self.port_3_indicator,fill=self.servo_colors["green"]) # Set the port 3 indicator to green
                    elif each_port == 3: # If port 4 is identified as being used
                        self.myCanvas.itemconfig(self.port_4_indicator,fill=self.servo_colors["green"]) # Set the port 2 indicator to green
                    elif each_port == 4: # If port 5 is identified as being used
                        self.myCanvas.itemconfig(self.port_5_indicator,fill=self.servo_colors["green"]) # Set the port 3 indicator to green
                    elif each_port == 5: # If port 6 is identified as being used
                        self.myCanvas.itemconfig(self.port_6_indicator,fill=self.servo_colors["green"]) # Set the port 3 indicator to green
                Step_Progressor = 2
            else:
                messagebox.showerror(title="Error",message="Error - Baud Rate not assigned in global settings. Please fix and try again.")
            
    def mark_servo_move(self): # Function to mark the servos which should move
        global Step_Progressor
        if Step_Progressor < 2:
            messagebox.showerror(title="Error",message="Error - Servos not yet detected. Cannot mark servos without detecting first.")
        else:
            selected_servos_tuple = self.servo_listbox.curselection() # Get which servos from the listbox have been highlighted/selected
            for selection_num in selected_servos_tuple:
                extracted_string = self.servo_listbox.get(selection_num) # Get the selected strings
                separated_string = extracted_string.split() # Split the string into the word "Servo" and the number
                for servo_numb in separated_string:
                    if servo_numb.isdigit(): # Extract the number
                        self.move_list.append(int(servo_numb)) # Append servo number to a list designated for servos that move, Starts with 0  
            self.confirmed_action[1] = []
            for selected_servo in self.move_list:
                self.change_servo_color(selected_servo,"green") # Change the corresponding servo graphic to green - detected and designated to move
                self.confirmed_action[1].append(selected_servo)
            if len(self.move_list) > 1:
                self.Config_Options["servos_to_move"] = self.move_list # If there's more than one servo selected, change Config_Options variable to represent this
                self.confirmed_action[0] = 2
            else:
                self.Config_Options["single_servo_to_move"] = self.move_list
                self.confirmed_action[0] = 1
            self.stay_move_selected[0] = 1
            if self.stay_move_selected[0] == 1 and self.stay_move_selected[1] == 1:
                self.indicator_canvas.itemconfig(self.indic_oval, fill="red") # Change indicator light to red, servos are designated but the robot is not in home position
                Step_Progressor = 3
        
    def mark_servo_stay(self): # Function to mark the servos which should stay straight
        global Step_Progressor
        if Step_Progressor < 2:
            messagebox.showerror(title="Error",message="Error - Servos not yet detected. Cannot mark servos without detecting first.")
        else:
            selected_servos_tuple = self.servo_listbox.curselection() # Get which servos from the listbox have been highlighted/selected
            for selection_num in selected_servos_tuple:
                extracted_string = self.servo_listbox.get(selection_num) # Get the selected strings
                separated_string = extracted_string.split() # Split the string into the word "Servo" and the number
                for servo_numb in separated_string:
                    if servo_numb.isdigit(): # Extract the number
                        self.dont_move_list.append(int(servo_numb)) # Append servo number to a list designated for servos that do not move,Starts with 0
            for selected_servo in self.dont_move_list:
                self.change_servo_color(selected_servo,"red") # Change the corresponding servo graphic to red - detected and designated to not move
            if (17 in self.dont_move_list) or (18 in self.dont_move_list): # If body length servos are selected, change Config_Options variable to represent this
                self.Config_Options["neck_straight"] = True
            else:
                self.Config_Options["neck_straight"] = False
            if (19 in self.dont_move_list) or (20 in self.dont_move_list) or (21 in self.dont_move_list) or (22 in self.dont_move_list):
                self.Config_Options["spine_straight"] = True
            else:
                self.Config_Options["spine_straight"] = False
            if (23 in self.dont_move_list) or (24 in self.dont_move_list):
                self.Config_Options["tail_straight"] = True
            else:
                self.Config_Options["tail_straight"] = False
            self.stay_move_selected[1] = 1
            if self.stay_move_selected[0] == 1 and self.stay_move_selected[1] == 1:
                self.indicator_canvas.itemconfig(self.indic_oval, fill="red") # Change indicator light to red, servos are designated but the robot is not in home position
                Step_Progressor = 3

    def change_servo_color(self,num_in,color_change): # Function to change the color of the corresponding servo in the schematic
        if (num_in >= 1 and num_in <= 24) and (color_change in self.servo_colors.keys()): # If the servo number entered into the function is one of the ones displayed on the schematic, and the color put into the function is one in the dictionary
            self.myCanvas.itemconfig(self.servo_graphics[num_in], fill=self.servo_colors[color_change]) # Change the corresponding servo in the schematic to the desired color
        else:
            print("Color or Servo Input not correct. Fix and try again.")

    def tilibot_get_ready(self): # Function to create servo and limb objects and move them to home position
        global Step_Progressor
        if Step_Progressor < 5:
            messagebox.showerror(title="Error",message="Error - Kinematics File not loaded. Cannot move servos without loaded Kinematics File.")
        else:
            Obj_list = [] # Create an empty list to house both the servo objects and the limb objects
            if 0 in self.stay_move_selected: # If both stay and move objects have been selected
                messagebox.showwarning(title="Move Selection Error", message="Servos have not been selected to either Move or Stay Still. Please fix and try again.")
                return
            config_array = list(self.Config_Options.values())
            servo_list_fix = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
            limb_list_fix = [False, False, False, False,False, False, False]
            limb_servo_count = [0,0,0,0,0,0,0]
            for i in DXL_ID:
                if i in config_array[5]:
                    servo_list_fix[i-1] = True
                    if i in F_R_ARM:
                        limb_servo_count[0] += 1
                    elif i in F_L_ARM:
                        limb_servo_count[1] += 1
                    elif i in B_R_ARM:
                        limb_servo_count[2] += 1
                    elif i in B_L_ARM:
                        limb_servo_count[3] += 1
                    elif i in NECK:
                        limb_servo_count[4] += 1
                    elif i in SPINE:
                        limb_servo_count[5] += 1
                    elif i in TAIL:
                        limb_servo_count[6] += 1
                else:
                    servo_list_fix[i-1] = False
            if limb_servo_count[0] == 4:
                limb_list_fix[0] = True
            else:
                limb_list_fix[0] = False
            if limb_servo_count[1] == 4:
                limb_list_fix[1] = True
            else:
                limb_list_fix[1] = False
            if limb_servo_count[2] == 4:
                limb_list_fix[2] = True
            else:
                limb_list_fix[2] = False
            if limb_servo_count[3] == 4:
                limb_list_fix[3] = True
            else:
                limb_list_fix[3] = False
            if limb_servo_count[4] == 2:
                limb_list_fix[4] = True
            else:
                limb_list_fix[4] = False
            if limb_servo_count[5] == 4:
                limb_list_fix[5] = True
            else:
                limb_list_fix[5] = False
            if limb_servo_count[6] == 2:
                limb_list_fix[6] = True
            else:
                limb_list_fix[6] = False
            config_array[5] = servo_list_fix
            config_array[6] = limb_list_fix
            self.stride_numbers = (config_array[4], config_array[2], config_array[3]) # Stride amount ,positions per stride, and stride time
            # if self.record_yesno.get() == 1:
            #     self.record_array[0] = True
            # else:
            #     self.record_array[0] = False
            self.record_array = RecordPreferences(config_array)
            self.ServosDictionary = Create_DigitalServos(config_array,self.port_used_dict,self.PositionsMatrix,
                self.SpeedMatrix) # Create a dictionary of digital servo objects to represent physical servos in digital space
            Obj_list.append(self.ServosDictionary) # Append the dictionary to the object list
            print("\n")
            if any(config_array[6]):
                LimbDictionary = Create_DigitalLimbs(config_array[6],self.ServosDictionary) # Create a dictionary of digital limb objects to represent physical servos in digital space
                Obj_list.append(LimbDictionary) # Append the dictionary to the object list
                print("\n")
            if self.confirmed_action[0] == 1: # Move Single Servo
                servo_to_move = self.ServosDictionary[self.confirmed_action[1]] # Identify single servo to move object
                servo_to_move.InitialSetup(self.port_servo_dict[servo_to_move.ID],config_array[31]) # Run digital servo through initial setup protocol to set system variables
                servo_to_move.ToggleTorque(1,self.port_servo_dict[servo_to_move.ID])  # Turn the torque on so the servo may move on command
                servo_to_move.MoveHome(config_array[17],self.port_servo_dict[servo_to_move.ID]) # Send servo to actual starting position (first position in stride)
            elif self.confirmed_action[0] == 2: # Move Numerous Servos
                if (config_array[28] == True):
                    for each_spine_servo in list(set(self.ServosDictionary.keys()).intersection(set(NECK))):
                        self.ServosDictionary[each_spine_servo].InitialSetup(self.port_servo_dict[each_spine_servo],False) # Run digital body length servos through initial setup protocol to set system variables
                        self.ServosDictionary[each_spine_servo].ToggleTorque(1,self.port_servo_dict[each_spine_servo]) # Turn the torque on so the servos may move on command
                if (config_array[29] == True):
                    for each_spine_servo in list(set(self.ServosDictionary.keys()).intersection(set(SPINE))):
                        self.ServosDictionary[each_spine_servo].InitialSetup(self.port_servo_dict[each_spine_servo],False) # Run digital body length servos through initial setup protocol to set system variables
                        self.ServosDictionary[each_spine_servo].ToggleTorque(1,self.port_servo_dict[each_spine_servo]) # Turn the torque on so the servos may move on command
                if (config_array[30] == True): # If neck, spine, and tail are all designated to stay straight
                    for each_spine_servo in list(set(self.ServosDictionary.keys()).intersection(set(TAIL))):
                        self.ServosDictionary[each_spine_servo].InitialSetup(self.port_servo_dict[each_spine_servo],False) # Run digital body length servos through initial setup protocol to set system variables
                        self.ServosDictionary[each_spine_servo].ToggleTorque(1,self.port_servo_dict[each_spine_servo]) # Turn the torque on so the servos may move on command
                StraightenSpine(self.ServosDictionary,self.port_hand_list,self.packetHandler,config_array[32]) # Straighten the spine to keep it stiff for movement
                for each_servo in self.confirmed_action[1]:
                    self.ServosDictionary[each_servo].InitialSetup(self.port_servo_dict[each_servo],False) # Run digital limb servos through initial setup protocol to set system variables
                    self.ServosDictionary[each_servo].ToggleTorque(1,self.port_servo_dict[each_servo]) # Turn the torque on so the servos may move on command
                Move_Spider_Up(self, self.move_list, self.ServosDictionary, self.port_hand_list, self.port_servo_dict, self.packetHandler,self.Config_Options["home_speed"],self.Config_Options["run_digital_only"]) # Move servos to spider position where the legs are raised up in the air
                time.sleep(2)
                Move_Spider_Down(self, self.move_list, self.ServosDictionary, self.port_hand_list, self.port_servo_dict, self.packetHandler,self.Config_Options["home_speed"], self.Config_Options["run_digital_only"]) # Move servos to spider position where it raises itself up off the ground
                time.sleep(2)
                for each_servo in self.confirmed_action[1]:
                    self.ServosDictionary[each_servo].MoveHome(config_array[17],self.port_servo_dict[each_servo]) # Send servos to actual starting position (first position in stride)
            self.indicator_canvas.itemconfig(self.indic_oval, fill=self.servo_colors["yellow"]) # Change indicator light to show status
            Step_Progressor = 6
            
    def tilibot_run(self): # Function to run the robot through one trial
        global Step_Progressor
        if Step_Progressor < 6:
            messagebox.showerror(title="Error",message="Error - Global Settings not set yet. Cannot detect servos without global settings.")
        else:
            self.indicator_canvas.itemconfig(self.indic_oval, fill=self.servo_colors["green"]) # Set the indicator light to green, indicating the robot is now running a trial
            print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print("Enter Tilibot Run - Start")
            config_array = list(self.Config_Options.values()) # Creat a config_array list using the dictionary values
            if self.confirmed_action[0] == 1: # Move One Servo
                print("Option Move One Servo - Detected")
                servo_to_move = self.ServosDictionary[self.confirmed_action[1]] # Fetch the servo object that is desired to move
                start_time = time.time() # Set a base time using the clock on the running computer
                out_data = servo_to_move.ContinuousMove(self.port_servo_dict[servo_to_move.ID], self.stride_numbers, self.record_array, start_time) # Go through using the Continuous Move Function for the corresponding servo
                if config_array[32] == False: # If run digital only is set to false
                    if self.record_array[0] == True: # If recording data is set to true
                        Write_Doc(self.record_array,out_data) # Write the data to the desired document
            elif self.confirmed_action[0] == 2: # Move Numerous Servos
                print("Option Move Multiple Servos Detected")
                start_time = time.time() # Set a base time using the clock on the running computer
                out_data = MoveNumerousServos(self,self.move_list,self.ServosDictionary,self.port_hand_list,self.port_servo_dict,
                    self.packetHandler,self.stride_numbers,self.record_array, start_time, self.movement_smoothing, config_array[32]) # Go through using the Continuous Move Function for the corresponding servos
                record_time = time.time() # Set a base End Time using the clock on the running computer
                end_time = record_time - start_time # Calculate the amount of time that passed over the trial
                self.act_end_time.set('{:.3f}'.format(end_time)) # Format the time difference as a string for display
                if config_array[32] == False: # If run digital only is set to false
                    if self.record_array[0] == True: # If recording data is set to true
                        Write_Doc(self.record_array,out_data) # Write the data to the desired document
            print("\nExit Tilibot Run - Finished With Time of: {:.3f}".format(end_time))
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n")

            self.indicator_canvas.itemconfig(self.indic_oval, fill="#6600CC") # Set the indicator to purple, indicating the robot is finished running the current trial
            Step_Progressor = 7

    def tilibot_reset(self): # Function to reset the robot for running more trials
        global Step_Progressor
        self.indicator_canvas.itemconfig(self.indic_oval, fill="#FFA500") # Set the indicator to orange, indicating the robot is not at home position but ready to run

        self.act_end_time.set("0.000") # Set the starting time to 0 second float
        Reset_For_Run(self.ServosDictionary,self.port_hand_list) # Kill the torque but keep all other values the same. 
        Step_Progressor = 5

    def tilibot_shutdown(self): # Function to shut down the robot and program after user is done running trials
        try:
            CleanUp(self.ServosDictionary,self.port_hand_list) # Perform the clean-up process by which the torque is turned off on all servos and the program is shut down
            ShutDown() # Execute the shutdown process
        finally:
            self.destroy() # Destroy the tkinter main window

    def load_settings_file(self): # Function to load the settings file into the universal configuration dictionary 
        global Step_Progressor
        desired_load_file = fdlg.askopenfilename() # Ask the user to open the settings file
        config_array = read_config_file(desired_load_file) # Read the configuration file into a configuration array 
        [invalidate_value, self.confirmed_action] = check_config_file(config_array,GUI_or_TERMINAL) # Check the assembled configuration array for any errors and return a desired action
        self.record_array = RecordPreferences(config_array) # Return what the recording preferences are 
        self.stride_numbers = (config_array[4], config_array[2],config_array[3]) # Stride amount, positions per stride, and stride time
        self.set_file_display.set(desired_load_file) # Change the display label to reflect the loaded file
        if invalidate_value == True: # If there is an error, shut the program down 
            print("Shutting Down Tilibot...")
            exit()
        else:
            self.Config_Options["baud_rate"] = config_array[0] # Set the internal config_options dictionary relevant to the GUI equal to what's in the settings file
            self.Config_Options["positions_file"] = config_array[1]
            self.Config_Options["position_amount"] = config_array[2]
            self.Config_Options["stride_time"] = config_array[3]
            self.Config_Options["stride_amount"] = config_array[4]
            self.Config_Options["connected_servos"] = config_array[5]
            self.Config_Options["connected_limbs"] = config_array[6]
            self.Config_Options["connected_sensors"] = config_array[7]
            self.Config_Options["forelimb_stance_time"] = config_array[8]
            self.Config_Options["forelimb_swing_time"] = config_array[9]
            self.Config_Options["hindlimb_stance_time"] = config_array[10]
            self.Config_Options["hindlimb_swing_time"] = config_array[11]
            self.Config_Options["tot_ratio_time"] = config_array[12]
            self.Config_Options["move_one_servo_act"] = config_array[13]
            self.Config_Options["single_servo_to_move"] = config_array[14]
            self.Config_Options["move_multi_servo_act"] = config_array[15]
            self.Config_Options["servos_to_move"] = config_array[16]
            self.Config_Options["home_speed"] = config_array[17]
            self.Config_Options["out_file_name"] = config_array[18]
            self.Config_Options["out_file_dir"] = config_array[19]
            self.Config_Options["position_write"] = config_array[20]
            self.Config_Options["speed_write"] = config_array[21]
            self.Config_Options["time_write"] = config_array[22]
            self.Config_Options["posindex_write"] = config_array[23]
            self.Config_Options["stridecount_write"] = config_array[24]
            self.Config_Options["current_write"] = config_array[25]
            self.Config_Options["voltage_write"] = config_array[26]
            self.Config_Options["temp_write"] = config_array[27]
            self.Config_Options["neck_straight"] = config_array[28]
            self.Config_Options["spine_straight"] = config_array[29]
            self.Config_Options["tail_straight"] = config_array[30]
            self.Config_Options["silence_ext_output"] = config_array[31]
            self.Config_Options["run_digital_only"] = config_array[32]

            # Set existing visual fields
            if (self.Config_Options["move_one_servo_act"] == True) and (self.Config_Options["move_multi_servo_act"] == False):
                self.move_select.set(0) # If only one servo is to move, set the desired movement to reflect this 
            elif (self.Config_Options["move_multi_servo_act"] == True) and (self.Config_Options["move_one_servo_act"] == False):
                self.move_select.set(1) # If multiple servos are to move, set the desired movement to reflect this
            self.stride_time_entry_string.set(self.Config_Options["stride_time"]) # Set the stride time entry to reflect the settings input
            self.stride_amount_entry_string.set(self.Config_Options["stride_amount"]) # Set the stride amount entry to reflect the settings input
            if self.record_array[0] == True: # If the record settings reflect that recording data is desired, set the checkbox to be checked
                self.record_yesno.set(1)
            else:
                self.record_yesno.set(0)
            Step_Progressor = 5
            
    def load_kinem_file(self): # Function to load the kinematics file when the button is pressed
        global Step_Progressor
        if Step_Progressor < 4:
            messagebox.showerror(title="Error",message="Error - Cannot load Kinematics File. Move Settings must be set before the Kinematics file may be loaded.")
        elif Step_Progressor >= 5:
            preprocessed_positions = ReadServoAngles(self.Config_Options["positions_file"]) # Read the angles within the file and determine the servo positions 
            self.PositionsMatrix = PostProcessPositions(preprocessed_positions) # Process the servo positions further to be easier to use and manipulate
            self.SpeedMatrix = DetermineSpeeds(self.Config_Options["stride_time"],self.PositionsMatrix, # Using the positions and the entered stride time, calculate the speeds by which the servos should move
                self.Config_Options["position_amount"],list(self.Config_Options.values()))
            self.indicator_canvas.itemconfig(self.indic_oval, fill=self.servo_colors["orange"])
        elif Step_Progressor == 4:
            self.Config_Options["positions_file"] = fdlg.askopenfilename() # Set the positions_file dictionary variable to the name of the file selected
            self.kin_file_display.set(self.Config_Options["positions_file"]) # Change the display widget at the bottom of the window to display the name of the file selected
            preprocessed_positions = ReadServoAngles(self.Config_Options["positions_file"]) # Read the angles within the file and determine the servo positions 
            self.PositionsMatrix = PostProcessPositions(preprocessed_positions) # Process the servo positions further to be easier to use and manipulate
            self.SpeedMatrix = DetermineSpeeds(self.Config_Options["stride_time"],self.PositionsMatrix, # Using the positions and the entered stride time, calculate the speeds by which the servos should move
                self.Config_Options["position_amount"],list(self.Config_Options.values()))
            self.indicator_canvas.itemconfig(self.indic_oval, fill=self.servo_colors["orange"])
            Step_Progressor = 5


    def analyse_data(self):
        # in_csv_data = fdlg.askopenfilename()
        # messagebox.showerror(title="Sorry!",message="Terribly sorry, this feature isn't functionally implemented yet!")
        self.analyse_data_box = tk.Toplevel(self) # Create a new window for the analyse data box window
        self.analyse_data_box.geometry("300x200") # Set the geometry for the new window
        self.analyse_data_box.title("Analyse Data") # Set the title for the new window


    def visualize_data(self):
        # in_analyzed_data = fdlg.askopenfilename()
        # messagebox.showerror(title="Sorry!",message="Terribly sorry, this feature isn't functionally implemented yet!")
        self.analyse_data_box = tk.Toplevel(self) # Create a new window for the analyse data box window
        self.visualize_data_box.geometry("300x200") # Set the geometry for the new window
        self.visualize_data_box.title("Visualize Data") # Set the title for the new window

    def RebootServo(self): # Function to Reboot the servos when required
        self.reboot_ind_canvas.itemconfig(self.reb_indic_oval, fill=self.servo_colors["yellow"])
        reboot_list = []
        selected_servos_tuple = self.servo_listbox.curselection() # Get which servos from the listbox have been highlighted/selected
        for selection_num in selected_servos_tuple:
            extracted_string = self.servo_listbox.get(selection_num) # Get the selected strings
            separated_string = extracted_string.split() # Split the string into the word "Servo" and the number
            for servo_numb in separated_string:
                if servo_numb.isdigit(): # Extract the number
                    reboot_list.append(int(servo_numb)) # Append servo number to a list designated for servos that move, Starts with 0
        for servo_num in reboot_list:
            if self.port_used_dict[servo_num] == 0:
                if self.port_hand_list[0].openPort():
                    if self.port_hand_list[0].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 1")
                    else:
                        print("Failed to change the baudrate - 1")
                else:
                    print("Failed to open the port - 1")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[0], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
            elif self.port_used_dict[servo_num] == 1:
                if self.port_hand_list[1].openPort():
                    if self.port_hand_list[1].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 2")
                    else:
                        print("Failed to change the baudrate - 2")
                else:
                    print("Failed to open the port - 2")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[1], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
            elif self.port_used_dict[servo_num] == 2:
                if self.port_hand_list[2].openPort():
                    if self.port_hand_list[2].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 3")
                    else:
                        print("Failed to change the baudrate - 3")
                else:
                    print("Failed to open the port - 3")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[2], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
            elif self.port_used_dict[servo_num] == 3:
                if self.port_hand_list[3].openPort():
                    if self.port_hand_list[3].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 4")
                    else:
                        print("Failed to change the baudrate - 4")
                else:
                    print("Failed to open the port - 4")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[3], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
            elif self.port_used_dict[servo_num] == 4:
                if self.port_hand_list[4].openPort():
                    if self.port_hand_list[4].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 5")
                    else:
                        print("Failed to change the baudrate - 5")
                else:
                    print("Failed to open the port - 5")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[4], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
            elif self.port_used_dict[servo_num] == 5:
                if self.port_hand_list[5].openPort():
                    if self.port_hand_list[5].setBaudRate(self.Config_Options["baud_rate"]):
                        print("Succeeded to change the baudrate for port 6")
                    else:
                        print("Failed to change the baudrate - 6")
                else:
                    print("Failed to open the port - 6")
                # Try reboot
                # Dynamixel LED will flicker while it reboots
                dxl_comm_result, dxl_error = self.packetHandler.reboot(self.port_hand_list[5], servo_num)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                print("[ID:%03d] reboot Succeeded\n" % servo_num)
                self.change_servo_color(servo_num,"green")
        self.reboot_ind_canvas.itemconfig(self.reb_indic_oval, fill=self.servo_colors["green"])
        

    def ResetServo(self,reset_value): # Function to Reset the servos when required
        self.reset_ind_canvas.itemconfig(self.res_indic_oval, fill=self.servo_colors["yellow"])
        #resets settings of Dynamixel to default values. The Factory reset function has three operation modes:
        #0xFF : reset all values (ID to 1, baudrate to 57600)
        #0x01 : reset all values except ID (baudrate to 57600)
        #0x02 : reset all values except ID and baudrate.
        print(reset_value)
        if reset_value.get() == 1:
            OPERATION_MODE = 0xFF
        elif reset_value.get() == 2:
            OPERATION_MODE = 0x01
        elif reset_value.get() == 3:
            OPERATION_MODE = 0x02
        else:
            print("Reset value not recognized. Please fix and try again.")
            quit()
        reset_list = []
        selected_servos_tuple = self.servo_listbox.curselection() # Get which servos from the listbox have been highlighted/selected
        for selection_num in selected_servos_tuple:
            extracted_string = self.servo_listbox.get(selection_num) # Get the selected strings
            separated_string = extracted_string.split() # Split the string into the word "Servo" and the number
            for servo_numb in separated_string:
                if servo_numb.isdigit(): # Extract the number
                    reset_list.append(int(servo_numb)) # Append servo number to a list designated for servos that move, Starts with 0
        for servo_num in reset_list:
            if self.port_used_dict[servo_num] == 0:
                # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[0], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            elif self.port_used_dict[servo_num] == 1:
               # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[1], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            elif self.port_used_dict[servo_num] == 2:
               # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[2], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            elif self.port_used_dict[servo_num] == 3:
               # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[3], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            elif self.port_used_dict[servo_num] == 4:
               # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[4], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            elif self.port_used_dict[servo_num] == 5:
               # Try factory reset
                print("[ID:%03d] Try factoryreset : " % (servo_num))
                dxl_comm_result, dxl_error = self.packetHandler.factoryReset(self.port_hand_list[5], servo_num, OPERATION_MODE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("Aborted")
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            # Wait for reset
            print("Wait for reset...")
            time.sleep(2.0)
            print("[ID:%03d] factoryReset Success!" % (servo_num))
            if self.port_used_dict[servo_num] == 0:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[0].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[0].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                time.sleep(0.2)
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[0], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            elif self.port_used_dict[servo_num] == 1:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[1].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[1].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                time.sleep(0.2)
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[1], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            elif self.port_used_dict[servo_num] == 2:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[2].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[2].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[2], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            elif self.port_used_dict[servo_num] == 3:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[3].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[3], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[3], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[3].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[3], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            elif self.port_used_dict[servo_num] == 4:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[4].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[4], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[4], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[4].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[4], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            elif self.port_used_dict[servo_num] == 5:
                # Set controller baudrate to Dynamixel default baudrate
                if self.port_hand_list[5].setBaudRate(FACTORYRST_DEFAULTBAUDRATE):
                    print("Succeeded to change the controller baudrate to : %d" % FACTORYRST_DEFAULTBAUDRATE)
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[5], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] DXL baudnum is now : %d" % (servo_num, dxl_baudnum_read))
                # Write new baudnum
                dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.port_hand_list[5], servo_num, ADDR_PRO_BAUDRATE, NEW_BAUDNUM)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Set Dynamixel baudnum to : %d" % (servo_num, NEW_BAUDNUM))
                # Set port baudrate to BAUDRATE
                if self.port_hand_list[5].setBaudRate(self.Config_Options["baud_rate"]):
                    print("Succeeded to change the controller baudrate to : %d" % self.Config_Options["baud_rate"])
                else:
                    print("Failed to change the controller baudrate")
                    print("Press any key to terminate...")
                time.sleep(0.2)
                # Read Dynamixel baudnum
                dxl_baudnum_read, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.port_hand_list[5], servo_num, ADDR_PRO_BAUDRATE)
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print("[ID:%03d] Dynamixel Baudnum is now : %d" % (servo_num, dxl_baudnum_read))
            self.change_servo_color(servo_num,"green")
root = MainWindow() # Create a MainWindow Object labeled root

root.mainloop() # Run root through the mainloop
