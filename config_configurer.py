# #, , \n, \t is used as comment in .config file

def config_loader():

    open_config_file = open("supportive_files/.config", "r")
    read_config_file = open_config_file.readlines()
    open_config_file.close()

    config_dict = {}

    for feature in read_config_file:

        if (feature.startswith("#") == True) or (feature.startswith(" ") == True) or (feature.startswith("\t") == True) or (feature.startswith("\n") == True):

            pass
        else:
            feature_dict = feature.replace("\n", "").replace("\t", "").replace(" = ", "=").replace("= ", "=").replace(" =", "=").split("=")
            #print(feature_dict)
            config_dict.update({feature_dict[0]:feature_dict[1]})

    return config_dict

def config_dumper(new_config_dict_details):

    # Saves the New Configuration details

    new_config_details = ''

    for config_name in (new_config_dict_details).keys():
        
        if config_name == (len(new_config_dict_details)-1):
            
            new_config_details+=f"{config_name} = {new_config_dict_details[config_name]}"
        
        else:
            new_config_details+=f"{config_name} = {new_config_dict_details[config_name]}\n"

    open_config_file = open("supportive_files/.config", "w")
    open_config_file.write(new_config_details)
    open_config_file.close()

    print()

def playlist_loader():

    # Loads the last accessed playlist

    open_play_list_config_file = open("supportive_files/playlist.config", "r")
    read_play_list_config_file = open_play_list_config_file.readlines()
    open_play_list_config_file.close()

    song_playlist_dict = {}

    for feature_index in range(len(read_play_list_config_file)):

        song_name =read_play_list_config_file[feature_index].replace("\n", "")
        #print(feature_dict)
        song_playlist_dict.update({feature_index:song_name})
    
    return song_playlist_dict # name of all the songs in the playlist | Format -> {index, song_name}

def playlist_dumper(new_playlist):
    
    # Saves the music in the playlist

    new_playlist_mod = ''

    for song_index in range(len(new_playlist)):
        
        if song_index == (len(new_playlist)-1):
            
            new_playlist_mod+=f"{new_playlist[song_index]}"
        
        else:
            new_playlist_mod+=f"{new_playlist[song_index]}\n"

    open_play_list_config_file = open("supportive_files/playlist.config", "w")
    open_play_list_config_file.write(new_playlist_mod)
    open_play_list_config_file.close()
