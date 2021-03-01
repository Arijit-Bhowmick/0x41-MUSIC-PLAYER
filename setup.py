import os, platform

try:
    import tkinter, tinytag, PIL, pygame, ttkthemes, mutagen, webbrowser
# For Linux sudo apt install python3-pil
#sudo apt install python3-tk
except ImportError:

    if int(platform.python_version()[0]) >= 3:

        if platform.system().upper() == "WINDOWS":
            os.system("pip3 install -r requirements.txt")
        
        if platform.system().upper() == "LINUX":

            ### PIL and Tkinter module requires root access to work in linux based systems ###

            print("Linux based System Required root privilages to \ninstall PIL and Tkinter module")
            os.system("sudo apt install python3-pil")
            os.system("sudo apt install python3-tk")
            os.system("pip3 install -r requirements.txt")
    else:
        print(f"""This Software only support in python versions >= 3.0.0
Your Python Version is {platform.python_version()}""")
        exit()