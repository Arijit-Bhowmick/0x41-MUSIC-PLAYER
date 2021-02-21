from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from PIL import *
from PIL import Image, ImageTk, ImageOps
import time

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen import File
from scipy.io.netcdf import FILL_DOUBLE

#########################################################
# Icons
#########################################################

# Application Icon

app_icon = PhotoImage(file = "Images/music_player_icon.png")

# Creating a photoimage object icon for #### Music Titlebar icon ####
 
music_player_img_open = Image.open("Images/music_player_icon.png").resize((15,15), Image.ANTIALIAS)
music_player_img = Image.new("RGBA", music_player_img_open.size, color=titlebar_bg_color_before)
music_player_img.paste(music_player_img_open, (0, 0), music_player_img_open)
music_player_icon = ImageTk.PhotoImage(music_player_img)



# Creating a photoimage object icon for #### Close button ####
 
close_button_img_open = Image.open("Icons/close.png").resize((15,15), Image.ANTIALIAS)
close_button_img = Image.new("RGBA", close_button_img_open.size, color=titlebar_bg_color_before)
close_button_img.paste(close_button_img_open, (0, 0), close_button_img_open)
close_icon = ImageTk.PhotoImage(close_button_img)

# Creating a photoimage object icon for #### minimize button ####

minimize_button_img_open = Image.open("Icons/minimize.png").resize((15,15), Image.ANTIALIAS)
minimize_button_img = Image.new("RGBA", minimize_button_img_open.size, color=titlebar_bg_color_before)
minimize_button_img.paste(minimize_button_img_open, (0, 0), minimize_button_img_open)
minimize_icon = ImageTk.PhotoImage(minimize_button_img)

# Creating a photoimage object icon for #### minimize to tray button ####

minimize_to_tray_button_img_open = Image.open("Icons/minimize_to_tray.png").resize((15,15), Image.ANTIALIAS)
minimize_to_tray_button_img = Image.new("RGBA", minimize_to_tray_button_img_open.size, color="#1f2223")
minimize_to_tray_button_img.paste(minimize_to_tray_button_img_open, (0, 0), minimize_to_tray_button_img_open)
minimize_to_tray_icon = ImageTk.PhotoImage(minimize_to_tray_button_img)

# Creating a photoimage object icon for #### Album Art Canvas ####

album_art_img_open = Image.open("Images/music_player_icon.png").resize((400,400), Image.ANTIALIAS)
album_art_img = Image.new("RGBA", album_art_img_open.size, color="#1f2223")
album_art_img.paste(album_art_img_open, (0, 0), album_art_img_open)
album_art_icon = ImageTk.PhotoImage(album_art_img)

# Creating a photoimage object icon for #### play/pause button ####

play_pause_img_open = Image.open("Icons/play.png").resize((30,30), Image.ANTIALIAS)
play_pause_img = Image.new("RGBA", play_pause_img_open.size, color="#1f2223")
play_pause_img.paste(play_pause_img_open, (0, 0), play_pause_img_open)
play_pause_icon = ImageTk.PhotoImage(play_pause_img)

# Creating a photoimage object icon for #### Backward button ####

backward_img_open = Image.open("Icons/backward.png").resize((30,30), Image.ANTIALIAS)
backward_img = Image.new("RGBA", backward_img_open.size, color="#1f2223")
backward_img.paste(backward_img_open, (0, 0), backward_img_open)
backward_icon = ImageTk.PhotoImage(backward_img)


# Creating a photoimage object icon for #### Forward button ####

forward_img_open = Image.open("Icons/forward.png").resize((30,30), Image.ANTIALIAS)
forward_img = Image.new("RGBA", forward_img_open.size, color="#1f2223")
forward_img.paste(forward_img_open, (0, 0), forward_img_open)
forward_icon = ImageTk.PhotoImage(forward_img)

# Creating a photoimage object icon for #### Stop button ####

stop_img_open = Image.open("Icons/stop.png").resize((30,30), Image.ANTIALIAS)
stop_img = Image.new("RGBA", stop_img_open.size, color="#1f2223")
stop_img.paste(stop_img_open, (0, 0), stop_img_open)
stop_icon = ImageTk.PhotoImage(stop_img)

# Creating a photoimage object icon for #### Shuffle All button ####

shuffle_all_img_open = Image.open("Icons/shuffle_all.png").resize((30,30), Image.ANTIALIAS)
shuffle_all_img = Image.new("RGBA", shuffle_all_img_open.size, color="#1f2223")
shuffle_all_img.paste(shuffle_all_img_open, (0, 0), shuffle_all_img_open)
shuffle_all_icon = ImageTk.PhotoImage(shuffle_all_img)


# Creating a photoimage object icon for #### Repeat All button ####

repeat_all_img_open = Image.open("Icons/repeat_all.png").resize((30,30), Image.ANTIALIAS)
repeat_all_img = Image.new("RGBA", repeat_all_img_open.size, color="#1f2223")
repeat_all_img.paste(repeat_all_img_open, (0, 0), repeat_all_img_open)
repeat_all_icon = ImageTk.PhotoImage(repeat_all_img)

# Creating a photoimage object icon for #### Repeat Once button ####

repeat_once_img_open = Image.open("Icons/repeat_once.png").resize((30,30), Image.ANTIALIAS)
repeat_once_img = Image.new("RGBA", repeat_once_img_open.size, color="#1f2223")
repeat_once_img.paste(repeat_once_img_open, (0, 0), repeat_once_img_open)
repeat_once_icon = ImageTk.PhotoImage(repeat_once_img)

# Creating a photoimage object icon for #### Sound ON/OFF button ####

sound_on_off_img_open = Image.open("Icons/speaker_on.png").resize((40,40), Image.ANTIALIAS)
sound_on_off_img = Image.new("RGBA", sound_on_off_img_open.size, color="#1f2223")
sound_on_off_img.paste(sound_on_off_img_open, (0, 0), sound_on_off_img_open)
sound_on_off_icon = ImageTk.PhotoImage(sound_on_off_img)

# Creating a photoimage object icon for #### Add Folder button ####

#add_folder_img_open = Image.open("Icons/add-folder.png").resize((15,15), Image.ANTIALIAS)
#add_folder_img = Image.new("RGBA", add_folder_img_open.size, color="#1f2223")
#add_folder_img.paste(add_folder_img_open, (0, 0), add_folder_img_open)
#add_folder_icon = ImageTk.PhotoImage(add_folder_img)

# here, image option is used to 