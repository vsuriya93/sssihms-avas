'''
This file has the global variables related to the application, which will be imported and used in different locations or methods.
'''
import sys

flag = 0
stream_or_game = 0
str_var = 1
stream1 = ""
previousFile = None
ENDEVENT = 42
songNo = 0

# for stopping bhajans
value = 1

url = "http://stream.radiosai.org:8000/"

# VLC is optional — may not be available on all platforms
try:
    import vlc
    vlc_player = vlc.MediaPlayer(url)
    vlc_available = True
except (ImportError, OSError):
    vlc_player = None
    vlc_available = False
