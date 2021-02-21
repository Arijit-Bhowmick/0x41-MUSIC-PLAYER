from tkinter import *
#import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from PIL import *
from PIL import Image, ImageTk, ImageOps
import time

music_player_name = "0x41 Music Player"

##########################################
####  FUNCTIONS CONFIGURATION | START ####
##########################################

def exit_prog():
    exit()

def start():
    for i in range (100):
        
        progress_bar['value'] = i
        splash_root.update_idletasks() 
        time.sleep(0.02)

########################################
####  FUNCTIONS CONFIGURATION | END ####
########################################

#### Initiate a Window ####

splash_root = Tk()
splash_root.resizable(0, 0)

#######################################
#### Drag Frameless Window | START ####
#######################################

class Grip:
    ''' Makes a window dragable. '''
    def __init__ (self, parent, disable=None, releasecmd=None) :
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)

    def drag_wid (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x' :
            x = self.oriX
        elif d == 'y' :
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind (self, event) :
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None :
            self.releaseCMD()

#####################################
#### Drag Frameless Window | END ####
#####################################

grip = Grip(splash_root)

#####################################
###  STYLES CONFIGURATION | START ###
#####################################

# Styles for Splash Screen

style = ttk.Style()
style.theme_use('alt') # clam, alt, default, classic
style.configure("TProgressbar", troughrelief = 'flat', troughcolor="#1f2223", bordercolor="#1f2223", background="#9acc14", lightcolor="white", darkcolor="orange")

#####################################
###  STYLES CONFIGURATION | STOP ####
#####################################

############################################################
############## ICONS  CONFIGURATION | START ################
############################################################

# Create a photoimage object of the image in the path

music_player_img_open = Image.open("Images/music_player_icon.png").resize((100,100), Image.ANTIALIAS)
music_player_img = Image.new("RGBA", music_player_img_open.size, color="#1f2223")
music_player_img.paste(music_player_img_open, (0, 0), music_player_img_open)
music_player_icon = ImageTk.PhotoImage(music_player_img)

music_player_icon_view = Label(splash_root,image=music_player_icon, background="#1f2223").pack(pady=20)

############################################################
############## ICONS  CONFIGURATION | END ##################
############################################################

##################################################
####  ROOT MUSIC PLAYER CONFIGURATION | START ####
##################################################

# Gets the requested values of the height and width

window_width = splash_root.winfo_reqwidth()
window_height = splash_root.winfo_reqheight()

# Gets both 1/4 the screen width/height and window width/height
position_right = int(splash_root.winfo_screenwidth()/4 - window_width/4)
position_down = int(splash_root.winfo_screenheight()/4 - window_height/4)

splash_root.title("Splash Screen")
splash_root.geometry(f"630x380+{position_right}+{position_down}")

splash_root.configure(background="#1f2223")
# Hide the Title Bar
splash_root.overrideredirect(1)

#################################################
####  ROOT SPLASH SCREEN CONFIGURATION | END ####
#################################################

splash_label = Label(splash_root, text=music_player_name, font=("Papyrus", 22), background="#1f2223", foreground="#61ace6").pack(pady=20)

# Progress Bar
progress_bar = ttk.Progressbar(splash_root, style="TProgressbar", orient = HORIZONTAL, length = 500,  mode = 'determinate')
#progress_bar = ttk.Progressbar(splash_root, style="TProgressbar", orient = HORIZONTAL, length = 500,  mode = 'indeterminate')
progress_bar.configure()
progress_bar.pack(pady=20)

# Loading Text

splash_label = Label(splash_root, text="Loading...", font=("Segoe UI", 10), background="#1f2223", foreground="#61ace6").pack(pady=5)

# Developer Name

developer_name_label = Label(splash_root, text="Developed by : Arijit Bhowmick", font=("Segoe UI", 10), background="#1f2223", foreground="#61ace6", anchor="e").pack(fill="both", padx=10, pady=10)

splash_root.after(1000, start)
splash_root.after(3000, exit_prog)

splash_root.mainloop()