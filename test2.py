def about_details():
        mb.showinfo('About','Creator of this apllication is Arijit Bhowmick.\nThis was completed on DATE.\n Thanks For Using The Application.')

## Add songs to the playlist.
def set_playlist():
    music_ex = ['mp3','wav','mpeg','m4a','wma','ogg']
    dir_ =  filedialog.askdirectory(initialdir=f'{os.getcwd()}',title='Select Directory')
    os.chdir(dir_)
    music_name['text'] = 'Playlist Updated.'
    dir_files = os.listdir(dir_)
    songs = []
    for file in dir_files:
        exten = file.split('.')[-1]
        for ex in music_ex:
            if exten == ex:
                music_listbox.insert(END,file)
                songs.append(file)

def stop(self):
    mixer.music.stop()
    global playing
    global paused
    global music_progress_time
    global progress_bar
    global cur_playing
    global current_time
    global to_break
    to_break = True
    current_time=0
    cur_playing = ''
    playing = False
    paused = False
    music_progress_time['text'] = '--:--'
    music_total_time['text'] = '--:--'
    progress_bar['value'] = 0.0
    progress_bar.update()

    music_album_art.itemconfig(0, 4, image=album_art_icon, anchor=NW)

    #self.album_art_label.configure(image=None)
    #self.album_art_label.image = None

        
    play_pause_button['image'] = play_icon
    music_name['text'] = 'Music Stopped'
    to_break = False

    return None

def play_music(self):
    global playing
    global cur_playing
    try:
        if playing == False:
            global file
            file = music_listbox.get(ACTIVE)
            cur_playing = file
            mixer.music.load(file)
            mixer.music.play()
            music_name['text'] = 'Playing - '+file
            play_pause_button['image'] = pause_icon
            playing = True
            #self.show_details(file)
        else:
            global paused
            if paused == True:
                mixer.music.unpause()
                paused = False
                music_name['text'] = 'Playing - '
                play_pause_button['image'] = pause_icon
            else:
                mixer.music.pause()
                paused = True
                play_pause_button['image'] = pause_icon
                music_name['text'] = 'Music Paused'
    except:
            mb.showerror('error','No file found to play.')


def play_song_initial(*args):
        stop()
        play_music()