
import os, platform

# If there is any problem during the installation of modules 
# then do use "pip3 install -r requirements.txt" command
# while in the current directory

try:
    import tkinter, tinytag, PIL, pygame, ttkthemes, mutagen, webbrowser

except ImportError:

    print("""Please run the setup.py file to setup the required modules for this project

Usage: python3 setup.py""")
    exit()


os.system("python3 splash_screen.py")
os.system("python3 music_player.py")
