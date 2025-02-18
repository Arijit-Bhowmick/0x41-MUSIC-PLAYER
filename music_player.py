from tkinter import *
import pygame
from tinytag import TinyTag
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import ttk
import webbrowser
import config_configurer
from PIL import *
from PIL import Image, ImageTk, ImageOps
import time
import os
from pygame import mixer
#from ttkthemes import themed_tk as ttkt
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import time


mixer.init()

music_player_name = "0x41 Music Player"
config_dict = config_configurer.config_loader()
playing = 0
paused = 0
current_time = 0
auto_play_color_dict = {"0":"#bc3c3c", "1":"#9acc14"} # Auto Play option for playing music automatically
auto_play = config_dict["auto_play"] # Provides 1 or 0 for ON/OFF auto_play mode
auto_play_text = config_dict["auto_play_text"] # provides String for identifying auto_play ON/OFF
last_song_index = config_dict["last_song_index"] # index of last song in the playlist
last_song_name = config_dict["last_song_name"] # Name of the last song
song_playlist = config_configurer.playlist_loader() # dictionary of all the songs | Format = {index, song_name}
get_updated_playlist = [] # Compare the current playlist
song_index = 0
playlist_location = config_dict["playlist_location"] # Location from where the songs are fetched
total_audio_duration = 0
last_volume = config_dict["last_volume"] # Last volume to be used
total_volume = 100
percent_of_progress = "0"
mute = "1"
previous_volume_percent = 0
album_art_new_icon = ''
total_audio_duration = 1
current_song_duration = 0
slider_time_global = 0
music_back_btn_progress = 0
music_back_btn_progress_referer = 0
double_click_event = 'None'
pre_index = "0"
repeat = 1
double_click = 0
song_index = 0
song_ended = "None"
song_change_tracker = 0
top_most = config_dict["top_most"]

# 0 means that music player is running
# 1 means that mini window is running
minimize_maximize_tracker = 0




##########################################
####  FUNCTIONS CONFIGURATION | START ####
##########################################


##############################################################
#### if the playlist location doesn't end with /  |  START ###
#### then it will add / or else pass the argument |       ###
##############################################################

if playlist_location[-1] != "/":

    playlist_location = playlist_location+"/"

elif playlist_location[-1] == "/":
    pass
    
##############################################################
#### if the playlist location doesn't end with /  |       ####
#### then it will add / or else pass the argument |  STOP ####
##############################################################


def mini_exit_prog(double_click):
    exit_prog()

def exit_prog():
    
    global playing
    global config_dict

    mixer.music.stop()
    playing = 0
    config_dict["last_volume"] = sound_slider.get() # Modify the last volume used
    config_dict["auto_play_text"] = auto_play_text # Modify the autoplay name info in config file
    config_dict["auto_play"] = auto_play # Modify the ON/OFF value for autoplay info in config file

    config_configurer.playlist_dumper(song_playlist)
    config_configurer.config_dumper(config_dict)
    music_player_root.destroy()
    root.destroy()

def mini_minimize_prog(double_click):

    global minimize_maximize_tracker

    if minimize_maximize_tracker==0:
    
        music_player_root.attributes("-alpha", 0.0)
        minimize_maximize_tracker = 1

def minimize_prog():

    global minimize_maximize_tracker

    if minimize_maximize_tracker==0:

        music_player_root.attributes("-alpha", 0.0)
        minimize_maximize_tracker = 1

    elif minimize_maximize_tracker==1:

        music_player_root.attributes("-alpha", 1.0)
        minimize_maximize_tracker = 0


def maximize_prog(double_click):

    global minimize_maximize_tracker

    if minimize_maximize_tracker==1:
    
        music_player_root.attributes("-alpha", 1.0)
        minimize_maximize_tracker = 0

    music_player_root.attributes("-topmost", 1)
    music_player_root.attributes("-topmost", 0)
    


def always_on_top():

    global top_most

    if top_most == "1":

        music_player_root.attributes("-topmost", 1)
        music_player_root.attributes("-topmost", 1)
        top_most = "0"
    
    elif top_most == "0":
        music_player_root.attributes("-topmost", 1)
        music_player_root.attributes("-topmost", 0)


        top_most = "1"


#######################################################


def support():

    webbrowser.open('https://arijit-bhowmick.github.io/supportive_webpages/support.html',new=1)

def about_player():

    mb.showinfo("About",f"""This is an exclusive distribution of {music_player_name}.
Creator of this application is Arijit Bhowmick.

The project is available at 
https://github.com/Arijit-Bhowmick/0x41-MEDIA-PLAYER

Please support me if you want at 
https://arijit-bhowmick.github.io/supportive_webpages/support.html

Thanks For Using The Application.""")

## Autoplay option
def autoplay_music():

    global auto_play
    global autoplay_button
    global auto_play_text

    if auto_play == "0":


        auto_play = "1"
        autoplay_button["text"] = "AUTOPLAY ON "
        auto_play_text = "AUTOPLAY ON "
        autoplay_button["background"] = auto_play_color_dict[auto_play]

    elif auto_play == "1":
    

        auto_play = "0"
        autoplay_button["text"] = "AUTOPLAY OFF"
        auto_play_text = "AUTOPLAY OFF"
        autoplay_button["background"] = auto_play_color_dict[auto_play]

##############################
### Get current file names ###
##############################

def get_updated_playlist():

    global updated_playlist

    music_ex = ['mp3','wav','mpeg','m4a','wma','ogg']

    updated_playlist = {}

    dir = os.listdir(playlist_location)
    
    for item_index in range(len(dir)):

        for extension in music_ex:

            if dir[item_index].endswith(extension):

                updated_playlist.update({item_index:dir[item_index]})

    return updated_playlist

## Add songs to the playlist.
def set_playlist():

    global music_listbox
    global playlist_location
    global song_playlist
    global config_dict


    music_ex = ['mp3','wav','mpeg','m4a','wma','ogg']
    #dir_ =  filedialog.askdirectory(initialdir=f'{os.getcwd()}',title='Select Directory')
    dir_ =  filedialog.askdirectory(initialdir=f'{playlist_location}',title='Select Directory')

    try:

        dir_files = os.listdir(dir_)

    except FileNotFoundError:

        # If the user close the dialog box then it will
        # gather the previous playlist
        dir_ = playlist_location
        dir_files = song_playlist.values()

    if playlist_location[-1] == "/":
        playlist_location = dir_
    if playlist_location[-1] != "/":
        playlist_location = dir_+"/"
    print(playlist_location)

    config_dict["playlist_location"] = playlist_location # Update the location of the playlist in config_dictionary
    
    music_name['text'] = 'Playlist Updated.'
    

    # Delete the items from the listbox

    for song_name_index in range(len(song_playlist)):
        music_listbox.delete(0)


    song_playlist = {} # Create new dictionary and remove old playlist 
    for file in dir_files:
        exten = file.split('.')[-1]
        for ex in music_ex:
            if exten == ex:
                music_listbox.insert(END,file) # Add each file name in the playlist
                song_playlist.update({(len(song_playlist)):file}) # Add each file in the playlist

    


def next_song():
    global percent_of_progress
    global repeat
    global song_change_tracker

    if song_index != len(song_playlist)-1:
        repeat = 0
        song_change_tracker = 1
        repeat_once_button["image"] = no_repeat_once_icon
        percent_of_progress = str(99)



def previous_song():


    global percent_of_progress
    global song_index
    global repeat
    global song_change_tracker

    if song_index != 0:

        song_change_tracker = 1
        repeat = 0
        song_index-=2
        repeat_once_button["image"] = no_repeat_once_icon
        percent_of_progress = str(99)
        
        
        

def repeat_once():

    global repeat

    if repeat == 0:

        repeat_once_button["image"] = repeat_once_icon # change the icon of the repeat button to repeat once image

        repeat = 1

    elif repeat == 1:

        repeat_once_button["image"] = no_repeat_once_icon # change the icon of the repeat button to no repeat once image

        repeat = 0



def change_album_art():
    global song_index
    global song_playlist
    global album_art_new_icon
    #global music_album_art

    tags = ID3(playlist_location+song_playlist[song_index])

    pict = tags.getall('APIC')[0].data
    im = Image.open(BytesIO(pict))
    im.save(fp="ALBUM_ART/temp.jpg") # Saves the picture of the album art

    


    #### Generate the image from the file ####

    album_art_new_img_open = Image.open("ALBUM_ART/temp.jpg").resize((400,400), Image.ANTIALIAS)
    album_art_new_icon = ImageTk.PhotoImage(album_art_new_img_open)
    
    ## Change the album art ###


    music_album_art.itemconfig(canvas_img,image=album_art_new_icon)

    # change to function 3

    update_3()


def music_stop():

    global playing
    global music_back_btn_progress_referer

    playing = 0
    mixer.music.stop() # stop the song
    music_slider.set("0")
    # Set music playing status to False
    music_back_btn_progress_referer = 0
    play_pause_button["image"] = pause_icon
    progress_bar['value'] = 0
    music_total_time["text"] = "--:--"
    music_progress_time["text"] = "--:--"

    ## Change the album art to Music player image ###

    music_album_art.itemconfig(canvas_img,image=album_art_icon)
    

def play_pause():

    global playing
    global paused

    if playing == 0:
        play_pause_button["image"] = pause_icon
        playing = 1
        paused = 0

        mixer.music.unpause()

    elif playing == 1:
        play_pause_button["image"] = play_icon
        playing = 0
        paused = 1
        mixer.music.pause()

    progress_value_update()


def song_detail_update():
    global song_playlist
    global song_index
    global total_audio_duration

    audio = TinyTag.get(playlist_location+song_playlist[song_index])
    total_audio_duration = audio.duration

    music_name["text"] = song_playlist[song_index] # Update the name of the current song

    music_total_time["text"] = str(int(total_audio_duration)) # Update the total audio duration

    update_2()

def progress_value_update():


    global percent_of_progress
    global current_song_duration
    global song_index
    global song_playlist
    global playing
    global song_change_tracker
    
    while (playing == 1) and (int(float(percent_of_progress))!=99):


        


        current_song_duration = music_back_btn_progress_referer+mixer.music.get_pos()*0.001 # get the curret time of duration of the song in second

        percent_of_progress = str((current_song_duration*100/total_audio_duration)) # percentage of progress

        music_progress_time['text'] = str(int(current_song_duration))

        progress_bar['value'] = percent_of_progress # Update the progressbar Value
        progress_bar.update()
        if playing == 1:

            music_slider.set(percent_of_progress) # Update the music slider Value
        time.sleep(0.02)

    

    if ((auto_play == "0") and (song_change_tracker == 0)) and (repeat == 0) and int(float(percent_of_progress))>=99:

        mixer.music.stop()
        music_stop()
        

    elif ((auto_play == "1") or (song_change_tracker == 1)) and int(float(percent_of_progress))>=99:
        
        song_change_tracker = 0

        if song_index<len(song_playlist):


            song_index +=1 # If Autoplay is on then if the music ends it will play the next song
            
            if repeat == 1:
    
                song_index -= 1
          
            update_0()
            
        elif song_index==len(song_playlist):
            mixer.music.stop()
            music_stop()





def music_progress_backward_updater():
    global current_song_duration
    global percent_of_progress
    global music_back_btn_progress
    global music_back_btn_progress_referer
    
    

    if current_song_duration>5:
        
        music_back_btn_progress = -5
        music_back_btn_progress_referer += (mixer.music.get_pos()*0.001)+music_back_btn_progress

        mixer.music.rewind()
        mixer.music.play(start=float(current_song_duration))
    else:
        pass

    
    
    update_4()

def music_progress_forward_updater():
    global current_song_duration
    global percent_of_progress
    global music_back_btn_progress
    global music_back_btn_progress_referer

    if current_song_duration<total_audio_duration:
        music_back_btn_progress = 5
        music_back_btn_progress_referer += (mixer.music.get_pos()*0.001)+music_back_btn_progress

        mixer.music.rewind()
        mixer.music.play(start=float(music_back_btn_progress_referer))
    else:
        pass

    
    
    update_4()


    

def volume_update(volume_value):
    global mute
    global previous_volume_percent

    # Function for updating volume functions
    mixer.music.set_volume(float(volume_value)/total_volume) # Increase or decrease the volume according to slider value
    previous_volume_percent = volume_value

    if volume_value=="0":

        sound_on_off_button["image"] = sound_off_icon # Set mute icon
        


    if float(volume_value)>int("0"):

        sound_on_off_button["image"] = sound_on_icon # Set Sound on icon


def volume_button_update():
    
    global previous_volume_percent
    global mute
    # Function for volume button

    if mute=="0":
    
        sound_on_off_button["image"] = sound_on_icon # Set mute icon
        sound_slider.set(50) # Set to previous volume
        mixer.music.set_volume(float(50))
        mute = "1"



    elif mute=="1":

        sound_on_off_button["image"] = sound_off_icon # Set Sound on icon
        sound_slider.set(0) # Set the volume to
        mixer.music.set_volume(float(0))
        mute = "0"


def music_play(event):
    global auto_play
    global playing
    global music_listbox
    global repeat
    global song_playlist
    global pre_index
    global percent_of_progress
    global double_click
    global song_index
    global music_back_btn_progress_referer

    #### Load and play the Song ####


    if double_click == 1:

        song_index = music_listbox.curselection()[0]


    elif double_click == 0:

        if song_index != pre_index:
    
            pass

        elif song_index == pre_index:

            if repeat == 0:
                music_stop()
            elif repeat == 1:
                song_index = pre_index

        

    updated_playlist = get_updated_playlist() # Retrive the updated playlist
    double_click = 0
    percent_of_progress = "0"
    repeat = 0
    repeat_once_button["image"] = no_repeat_once_icon
    pre_index = song_index # track the previous index

    music_back_btn_progress_referer = 0
    play_pause_button["image"] = pause_icon
    progress_bar['value'] = 0
    music_total_time["text"] = "--:--"
    music_progress_time["text"] = "--:--"

    mixer.music.stop()

    old_playlist = song_playlist

    if song_index > len(song_playlist)-1:
        music_stop()


    try:

        mixer.music.load(playlist_location+song_playlist[song_index]) # Load the song from the list of songs
        mixer.music.play() # Play the song

    except pygame.error or KeyError:

        song_index = 0

        for song_name_index in range(len(old_playlist)):
            music_listbox.delete(0)

        #song_playlist = {} # Create new dictionary and remove old playlist
        
        song_playlist = updated_playlist # Update the playlist


        for song_name in song_playlist.values():
            music_listbox.insert(END,song_name) # Add each file name in the playlist

        music_stop()
        
    
    play_pause_button["image"] = pause_icon
    playing = 1

    #### Change the Canvas Picture ####
    update_1()



def double_click_music_play(event):
    global double_click_event
    global double_click
    global song_index

 
    song_index = music_listbox.curselection()[0]

    
    double_click = 1

    double_click_event = event


    update_0()
    
    

def update_0():

    music_play(double_click_event)

def update_1():
    song_detail_update()

def update_2():
    change_album_art()

def update_3():
    progress_value_update()

def update_4():


    progress_value_update()



############################################
#### FUNCTIONS FOR WINDOW CONFIGURATION ####
############################################

#toplevel follows root taskbar events (minimize, restore)
def onRootIconify(event):
    music_player_root.withdraw()
    root.bind("<Unmap>", onRootIconify)
def onRootDeiconify(event):
    music_player_root.deiconify()
    root.bind("<Map>", onRootDeiconify)
########################################
####  FUNCTIONS CONFIGURATION | END ####
########################################

root = Tk()
root.attributes("-alpha",0.0)

music_player_root = Toplevel(root)
music_player_root.overrideredirect(1) #removes border but undesirably from taskbar too (usually for non toplevel windows)
#music_player_root.attributes("-topmost", 1)
music_player_root.attributes("-alpha", 1.0)

mini_app_float_window = Toplevel(music_player_root) # If Media player is minimized then it will show up
mini_app_float_window.overrideredirect(1)
mini_app_float_window.attributes("-topmost", 1)
#mini_app_float_window.attributes("-alpha", minimize_maximize_tracker)


#### Initiate a Window ####


music_player_root_frame = tk.Frame(master=root)



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

#############################################
########## FRAMES CONFIGURATION | START #####
#############################################



########################
### titlebar Frame ###
#########################

titlebar_bg_color_before = "#3b4045"
titlebar_bg_color_after = "#1f2223"

titlebar = tk.Frame(music_player_root, background=titlebar_bg_color_before)
titlebar.pack(side=TOP, fill=X)

### Make the window move while using Titlebar ###

grip = Grip(titlebar)
grip2 = Grip(mini_app_float_window)
###############################

########################
### toolbar Frame ###
#########################

toolbar_bg_color_before = "#1f2223"
toolbar_bg_color_after = "#3b4045"

toolbar = tk.Frame(music_player_root, background=toolbar_bg_color_before)
toolbar.pack(side=TOP, fill=X)

########################
### Music content Area Frame ###
#########################

music_content_bg_color_before = "#1f2223"
music_content_bg_color_after = "#3b4045"

music_content = tk.Frame(music_player_root, background=music_content_bg_color_before)
music_content.pack(side=TOP, fill=BOTH)


########################
### Music Name Frame ###
#########################

music_name_bg_color_before = "#1f2223"
music_name_bg_color_after = "#1f2250"

music_name_content = tk.Frame(music_player_root, background=music_name_bg_color_before)
music_name_content.pack(side=TOP, fill=X)

########################
### Progress Bar Area Frame ###
#########################

progress_bar_controls_color_before = "#1f2223"
progress_bar_controls_color_after = "#1f2250"

progress_bar_content = tk.Frame(music_player_root, background=progress_bar_controls_color_before)
progress_bar_content.pack(side=TOP, fill=X)

###########################
### Music Control Frame ###
###########################


music_slider_set_content = tk.Frame(music_player_root, background="#1f2223")
music_slider_set_content.pack(side=TOP, fill=X)

###########################
### Music Control Frame ###
###########################

music_controls_color_before_click = "#1f2223"
music_controls_color_after_click = "#1f2250"

music_control_content = tk.Frame(music_player_root, background=music_controls_color_before_click)
music_control_content.pack(side=TOP, fill=X)



###########################
### Sound Control Frame ###
###########################

sound_control_bg_color = "#1f2223"

sound_control_content = tk.Frame(music_player_root, background=sound_control_bg_color)
sound_control_content.pack(side=TOP, fill=X)

#############################################
########## FRAMES CONFIGURATION | END #######
#############################################

############################################################
############## ICONS  CONFIGURATION | START ################
############################################################

#### Application Icon ####

app_icon = PhotoImage(file = "Images/music_player_icon.png")

#### Music Titlebar icon ####
 
music_player_img_open = Image.open("Images/music_player_icon.png").resize((15,15), Image.ANTIALIAS)
music_player_img = Image.new("RGBA", music_player_img_open.size, color=titlebar_bg_color_before)
music_player_img.paste(music_player_img_open, (0, 0), music_player_img_open)
music_player_icon = ImageTk.PhotoImage(music_player_img)



#### Close Icon ####
 
close_button_img_open = Image.open("Icons/close.png").resize((15,15), Image.ANTIALIAS)
close_button_img = Image.new("RGBA", close_button_img_open.size, color=titlebar_bg_color_before)
close_button_img.paste(close_button_img_open, (0, 0), close_button_img_open)
close_icon = ImageTk.PhotoImage(close_button_img)

#### maximize Photo ####

maximize_img_open = Image.open("Icons/maximize.png").resize((15,15), Image.ANTIALIAS)
maximize_button_img = Image.new("RGBA", maximize_img_open.size, color="#1f2223")
maximize_button_img.paste(maximize_img_open, (0, 0), maximize_img_open)
maximize_icon = ImageTk.PhotoImage(maximize_button_img)

#### Minimize Icon ####

minimize_button_img_open = Image.open("Icons/minimize.png").resize((15,15), Image.ANTIALIAS)
minimize_button_img = Image.new("RGBA", minimize_button_img_open.size, color=titlebar_bg_color_before)
minimize_button_img.paste(minimize_button_img_open, (0, 0), minimize_button_img_open)
minimize_icon = ImageTk.PhotoImage(minimize_button_img)

#### Mini Window Icon ####

mini_app_button_img_open = Image.open("Images/music_player_icon.png").resize((40,40), Image.ANTIALIAS)
mini_app_button_img = Image.new("RGBA", mini_app_button_img_open.size, color=titlebar_bg_color_before)
mini_app_button_img.paste(mini_app_button_img_open, (0, 0), mini_app_button_img_open)
mini_app_icon = ImageTk.PhotoImage(mini_app_button_img)


# Creating a photoimage object icon for #### Album Art Canvas ####

album_art_img_open = Image.open("Images/music_player_icon.png").resize((400,400), Image.ANTIALIAS)
album_art_img = Image.new("RGBA", album_art_img_open.size, color="#1f2223")
album_art_img.paste(album_art_img_open, (0, 0), album_art_img_open)
album_art_icon = ImageTk.PhotoImage(album_art_img)

# Creating a photoimage object icon for #### play button ####

play_img_open = Image.open("Icons/play.png").resize((30,30), Image.ANTIALIAS)
play_img = Image.new("RGBA", play_img_open.size, color="#1f2223")
play_img.paste(play_img_open, (0, 0), play_img_open)
play_icon = ImageTk.PhotoImage(play_img)

# Creating a photoimage object icon for #### Pause button ####

pause_img_open = Image.open("Icons/pause.png").resize((30,30), Image.ANTIALIAS)
pause_img = Image.new("RGBA", pause_img_open.size, color="#1f2223")
pause_img.paste(pause_img_open, (0, 0), pause_img_open)
pause_icon = ImageTk.PhotoImage(pause_img)

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

no_repeat_once_img_open = Image.open("Icons/no_repeat.png").resize((30,30), Image.ANTIALIAS)
no_repeat_once_img = Image.new("RGBA", no_repeat_once_img_open.size, color="#1f2223")
no_repeat_once_img.paste(no_repeat_once_img_open, (0, 0), no_repeat_once_img_open)
no_repeat_once_icon = ImageTk.PhotoImage(no_repeat_once_img)


# Creating a photoimage object icon for #### Repeat Once button ####

repeat_once_img_open = Image.open("Icons/repeat_once.png").resize((30,30), Image.ANTIALIAS)
repeat_once_img = Image.new("RGBA", repeat_once_img_open.size, color="#1f2223")
repeat_once_img.paste(repeat_once_img_open, (0, 0), repeat_once_img_open)
repeat_once_icon = ImageTk.PhotoImage(repeat_once_img)


# Creating a photoimage object icon for #### Faast Forward button ####

fast_forward_img_open = Image.open("Icons/fast_forward.png").resize((30,30), Image.ANTIALIAS)
fast_forward_img = Image.new("RGBA", fast_forward_img_open.size, color="#1f2223")
fast_forward_img.paste(fast_forward_img_open, (0, 0), fast_forward_img_open)
fast_forward_icon = ImageTk.PhotoImage(fast_forward_img)


# Creating a photoimage object icon for #### Fast Backward button ####

fast_backward_img_open = Image.open("Icons/fast_backward.png").resize((30,30), Image.ANTIALIAS)
fast_backward_img = Image.new("RGBA", fast_backward_img_open.size, color="#1f2223")
fast_backward_img.paste(fast_backward_img_open, (0, 0), fast_backward_img_open)
fast_backward_icon = ImageTk.PhotoImage(fast_backward_img)

# Creating a photoimage object icon for #### Sound ON button ####

sound_on_img_open = Image.open("Icons/speaker_on.png").resize((40,40), Image.ANTIALIAS)
sound_on_img = Image.new("RGBA", sound_on_img_open.size, color="#1f2223")
sound_on_img.paste(sound_on_img_open, (0, 0), sound_on_img_open)
sound_on_icon = ImageTk.PhotoImage(sound_on_img)

# Creating a photoimage object icon for #### Sound OFF button ####

sound_off_img_open = Image.open("Icons/speaker_off.png").resize((40,40), Image.ANTIALIAS)
sound_off_img = Image.new("RGBA", sound_off_img_open.size, color="#1f2223")
sound_off_img.paste(sound_off_img_open, (0, 0), sound_off_img_open)
sound_off_icon = ImageTk.PhotoImage(sound_off_img)

############################################################
############## ICONS  CONFIGURATION | END ##################
############################################################

#####################################
###  STYLES CONFIGURATION | START ###
#####################################

##### Style for Progress Bar ######

style = ttk.Style()
style.theme_use('alt') # clam, alt, default, classic
style.configure("TProgressbar", troughrelief = 'flat', background="#0064bd", troughcolor="#1f2223", bordercolor="#1f2223", relief=FLAT, lightcolor="white", darkcolor="orange")

#####################################
###  STYLES CONFIGURATION | STOP ####
#####################################

#########################################
##### MINI APP CONFIGURATION | START ####
#########################################

mini_app_icon = Label(mini_app_float_window, image=music_player_icon, text=music_player_name, font=("Segoe UI", 11), background=titlebar_bg_color_before, foreground="#149414").pack(side=LEFT, padx=10, pady=0)

#### SET ICON on Mini floating window | Maximize button ####
mini_app_maximize_button = tk.Button(mini_app_float_window, image = maximize_icon, relief=FLAT, highlightthickness=0, background=titlebar_bg_color_before, activebackground=titlebar_bg_color_after)
mini_app_maximize_button.pack(side = LEFT, padx = 5, pady=0)
mini_app_maximize_button.bind('<Double-Button>', maximize_prog)

#### SET ICON on Mini floating window | Minimize button ####
mini_app_minimize_button = tk.Button(mini_app_float_window, image = minimize_icon, relief=FLAT, highlightthickness=0, background=titlebar_bg_color_before, activebackground=titlebar_bg_color_after)
mini_app_minimize_button.pack(side = LEFT, padx = 5, pady=0)
mini_app_minimize_button.bind('<Double-Button>', mini_minimize_prog)

#### SET ICON on Mini floating window | Close button ####
mini_app_close_button = tk.Button(mini_app_float_window, image = close_icon, relief=FLAT, highlightthickness=0, background=titlebar_bg_color_before, activebackground=titlebar_bg_color_after)
mini_app_close_button.pack(side = LEFT, padx = 5, pady=0)
mini_app_close_button.bind('<Double-Button>', mini_exit_prog)

#########################################
##### MINI APP CONFIGURATION | STOP #####
#########################################

#########################################
##### TITLEBAR CONFIGURATION | START ####
#########################################

#### Music Player ICON ###

music_player_icon_name = Label(titlebar, image=music_player_icon, text=music_player_name, font=("Segoe UI", 11), background=titlebar_bg_color_before, foreground="#149414").pack(side=LEFT, padx=6, pady=0)



#### SET ICON on close button ####
close_button = tk.Button(titlebar, image = close_icon, relief=FLAT, highlightthickness=0, background=titlebar_bg_color_before, activebackground=titlebar_bg_color_after, command=exit_prog)
close_button.pack(side = RIGHT, padx = 0, pady=0)

#### SET ICON on Minimize button ####
minimize_button = tk.Button(titlebar, image = minimize_icon, relief=FLAT, highlightthickness=0, background=titlebar_bg_color_before, activebackground=titlebar_bg_color_after, command=minimize_prog)
minimize_button.pack(side = RIGHT, padx = 0, pady=0)

#### Music Player Titlebar Name ###

music_player_titlebar_name = Label(titlebar, text=music_player_name, font=("Segoe UI", 11), background=titlebar_bg_color_before, foreground="#9acc14").pack(padx=0, pady=0)

#######################################
##### TITLEBAR CONFIGURATION | END ####
#######################################


########################################
##### TOOLBAR CONFIGURATION | START ####
########################################

#### Drop down MENU ITEMS ####

file_menu= tk.Menubutton(toolbar, text="MENU", font=("Segoe UI", 8), foreground="#9acc14", activeforeground="#fff", highlightthickness=0, background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, relief=FLAT)
file_menu.menu =  Menu ( file_menu, tearoff = 0 )
file_menu["menu"] =  file_menu.menu


file_menu.menu.add_command( label="Open Folder", font=("Segoe UI", 8), foreground="#fff", background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, command=set_playlist)
file_menu.menu.add_command( label="Always On Top", font=("Segoe UI", 8), foreground="#fff", background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, command=always_on_top)
file_menu.menu.add_separator(background="#1f2223") # Seperator between two menu Items
file_menu.menu.add_command( label="Exit", font=("Segoe UI", 8), foreground="#fff", background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, command=exit_prog)

file_menu.pack(side=LEFT)

#### set About DROP DOWN ####
 
about_button= tk.Menubutton(toolbar, text="ABOUT", font=("Segoe UI", 8), foreground="#9acc14", activeforeground="#fff", highlightthickness=0, background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, relief=FLAT)
about_button.menu =  Menu(about_button, tearoff = 0)
about_button["menu"] =  about_button.menu

about_button.menu.add_command(label="About", font=("Segoe UI", 8), foreground="#fff", background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, command=about_player)
about_button.menu.add_command(label="Support Us", font=("Segoe UI", 8), foreground="#fff", background=toolbar_bg_color_before, activebackground=toolbar_bg_color_after, command=support)
about_button.pack(side=LEFT)


#### SET Autoplay music button ####
autoplay_button = tk.Button(toolbar, text=auto_play_text, font=("Segoe UI", 8), relief=FLAT, highlightthickness=0, foreground="#fff", activeforeground="#fff", background=auto_play_color_dict[auto_play], activebackground=toolbar_bg_color_after, command=autoplay_music)
autoplay_button.pack(side = RIGHT, padx = 5, pady=0)

######################################
##### TOOLBAR CONFIGURATION | END ####
######################################


##############################################
##### MUSIC CONTENT CONFIGURATION | START ####
##############################################

#### Music Album Art Canvas ####

music_album_art = Canvas(music_content, width = 400, height = 410, highlightthickness=0, relief=FLAT, borderwidth=0, background=music_content_bg_color_before)
music_album_art.pack(side = LEFT, padx = 3, pady=0)
canvas_img = music_album_art.create_image(0, 4, image=album_art_icon, anchor=NW)

#### Add Music Folder button #### 
add_music_folder_button = tk.Button(music_content, text = "Add Music Folder", font=("Segoe UI", 8), foreground = "#9acc14", relief=FLAT, highlightthickness=0, background=music_content_bg_color_after, activebackground="#292e33", command=set_playlist)
add_music_folder_button.pack(side = TOP, fill=X)

#### Music Name List ####

music_listbox = tk.Listbox(music_content, font=("Segoe UI", 8), height=27, highlightthickness=0, foreground = "#fff", relief=FLAT, background=music_content_bg_color_before)
for item_num in range(len(song_playlist)):
    
    music_listbox.insert(item_num, song_playlist[item_num])
music_listbox.bind('<Double-Button>', double_click_music_play)

music_listbox.pack(side = TOP, fill=BOTH, padx=2, pady=5)

############################################
##### MUSIC CONTENT CONFIGURATION | END ####
############################################

###########################################
##### MUSIC NAME CONFIGURATION | START ####
###########################################

#### Music Name ####

music_name = Label(music_name_content, text=f"WELCOME TO {music_player_name}", font=("Segoe UI", 11), background=music_name_bg_color_before, foreground="#fff")
music_name.pack(padx=3, pady=3)

#########################################
##### MUSIC NAME CONFIGURATION | END ####
#########################################

###############################################
##### MUSIC PROGRESS CONFIGURATION | START ####
###############################################

### music progress time ###

music_progress_time = Label(progress_bar_content, text="--:--", font=("Segoe UI", 10), background=progress_bar_controls_color_before, foreground="#fff")
music_progress_time.pack(side = LEFT, padx=3, pady=0)

### music total time ###

music_total_time = Label(progress_bar_content, text="--:--", font=("Segoe UI", 10), background=progress_bar_controls_color_before, foreground="#fff")
music_total_time.pack(side = RIGHT, padx=3, pady=0)

#### Progress Bar ####

progress_bar = ttk.Progressbar(progress_bar_content, style="TProgressbar", orient = HORIZONTAL, length = 500,  mode = 'determinate')
progress_bar.configure()
progress_bar.pack(fill=BOTH, padx=3, pady=3)


#############################################
##### MUSIC PROGRESS CONFIGURATION | END ####
#############################################

######################################################
##### MUSIC SLIDER CONTROLS CONFIGURATION | START ####
######################################################

#### Update the position of the music, slider and progress bar

music_progress_button_bakward_updater = tk.Button(music_slider_set_content, image=fast_backward_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=music_progress_backward_updater)
music_progress_button_bakward_updater.pack(side = LEFT, padx=5, pady=8)

music_progress_button_forward_updater = tk.Button(music_slider_set_content, image=fast_forward_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=music_progress_forward_updater)
music_progress_button_forward_updater.pack(side = RIGHT, padx=5, pady=8)

#### Slider for Music timeline ####

music_slider = tk.Scale(music_slider_set_content, from_= 0, to=100, width=4, length=2000, orient=HORIZONTAL, highlightthickness=0, border=0, relief=FLAT, sliderrelief=RIDGE, foreground = "#fff", background="#1f2223", activebackground="#1d3d47", troughcolor="#f19250")
music_slider.pack(side=LEFT, fill=X, padx=5, pady=0)



####################################################
##### MUSIC SLIDER CONTROLS CONFIGURATION | END ####
####################################################

###############################################
##### MUSIC CONTROLS CONFIGURATION | START ####
###############################################

#### set Play/Pause button ####
play_pause_button = tk.Button(music_control_content, image=play_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=play_pause)
play_pause_button.pack(side = LEFT, padx=8, pady=3)


#### set Backward button ####
previous_song_button = tk.Button(music_control_content, image=backward_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=previous_song)
previous_song_button.pack(side = LEFT, padx=5, pady=3)

#### set Stop button ####
stop_button = tk.Button(music_control_content, image=stop_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=music_stop)
stop_button.pack(side = LEFT, padx=5, pady=3)

#### set Forward button ####
next_song_button = tk.Button(music_control_content, image=forward_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=next_song)
next_song_button.pack(side = LEFT, padx=5, pady=3)

#### set Repeat All button ####
repeat_once_button = tk.Button(music_control_content, image=no_repeat_once_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=music_controls_color_before_click, activebackground=music_controls_color_after_click, command=repeat_once)
repeat_once_button.pack(side = LEFT, padx=5, pady=3)

#### set Sound ON/OFF button ####
sound_on_off_button = tk.Button(music_control_content, image=sound_off_icon, font=("Segoe UI", 8), foreground = "#fff", relief=FLAT, highlightthickness=0, background=sound_control_bg_color, activebackground=sound_control_bg_color, command=volume_button_update)
sound_on_off_button.pack(side = LEFT, padx=5, pady=3)

#### Slider for Sound ####

sound_slider = tk.Scale(music_control_content, from_= 0, to=total_volume, width=3, length=2000, orient=HORIZONTAL, highlightthickness=0, border=0, relief=FLAT, sliderrelief=RIDGE, foreground = "#fff", background="#1f2223", activebackground="#1d3d47", troughcolor="#487e59", command=volume_update)
sound_slider.pack(side=LEFT, fill=X, padx=5, pady=0)
sound_slider.set(last_volume) # Set the last volume before the music player was closed




#############################################
##### MUSIC CONTROLS CONFIGURATION | END ####
#############################################


##################################################
####  ROOT MUSIC PLAYER CONFIGURATION | START ####
##################################################

#### Gets the requested values of the height and width ####

window_width = music_player_root_frame.winfo_reqwidth()
window_height = music_player_root_frame.winfo_reqheight()

#### Gets both 1/4 the screen width/height and window width/height ####
position_right = int(music_player_root_frame.winfo_screenwidth()/4 - window_width/4)
position_down = int(music_player_root_frame.winfo_screenheight()/4 - window_height/4)

#### Music Player Position Configuration ####

music_player_root.iconphoto(False, app_icon)
music_player_root.title(music_player_name)
music_player_root.geometry(f"900x620+{position_right}+{position_down}")
music_player_root.configure(background="#1f2223")

mini_app_float_window.iconphoto(False, app_icon)
mini_app_float_window.title(music_player_name)
mini_app_float_window.geometry(f"130x30+{0}+{0}")
mini_app_float_window.configure(background=titlebar_bg_color_before)



root.iconphoto(False, app_icon)
root.title(music_player_name)
root.resizable(0, 0)
root.geometry(f"0x0+{position_right}+{position_down}")


music_player_root_frame.configure(background="#1f2223")


################################################
####  ROOT MUSIC PLAYER CONFIGURATION | END ####
################################################

music_player_root_frame.mainloop()