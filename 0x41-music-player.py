#import splash_screen
import os, platform

# If there is any problem during the installation of modules 
# then do use "pip3 install -r requirements.txt" command
# while in the current directory

try:
    import tkinter, tinytag, PIL, pygame, ttkthemes, mutagen, webbrowser
# For Linux sudo apt install python3-pil
#sudo apt install python3-tk
except ImportError:

    if int(platform.python_version()[0]) >= 3:
        os.system("pip3 install -r requirements.txt")
    else:
        print(f"""This Software only support in python versions >= 3.0.0
Your Python Version is {platform.python_version()}""")
        exit()


os.system("python3 splash_screen.py")
os.system("python3 music_player_linux.py")
