'''
This module has the methods related to the audio part of the application.
This includes:
				 1. Playing audio of all the blood groups.
				 2. Play only group names.
				 3. Play individual blood group names and etc.		
'''

import pyaudio
import wave
import time
import datetime
import schedule
import os
import pygame
import sys
from globals import *                # import all the variable required from the global.py

def play_audio(path):
	chunk = 1048#1024 
	f = wave.open(path,"rb")  
	p = pyaudio.PyAudio()  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),channels = f.getnchannels(),rate = f.getframerate(),output = True)  	
	global str_var
	global flag
	data = f.readframes(chunk)  
	while data:  
	  if (str_var==0 and flag==1):
		  str_var=1	
		  stream.stop_stream()
		  stream.close()  
		  p.terminate() 
	  if (str_var==1):
		  stream.start_stream()
	  stream.write(data)  
	  data = f.readframes(chunk) 
	stream.stop_stream()  
	stream.close()  
	p.terminate()



def play_all_blood_audio():                                       # Method to play all the blood groups.
 	path = 'audio/bloodgroup/'+'ALL'+str('.wav')
	play_audio(path)
	play_audio('audio/2.wav')
	play_audio('audio/7.wav')
	play_audio('audio/6.wav')

def play_blood_names(result):									 # Play only specific blood group names given as results.
	count=1
	for element in result:
		path = 'audio/bloodgroup/'+str(element)+str('.wav')
		play_audio(path)
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		count=count+1

def play_blood_groups(result):									 # play only group names.
	count=1 											     		# variable for number of groups to be read. lije o+ve, 0-ve count =2 
	for element in result:
		path = 'audio/bloodgroup/'+str(element)+str('.wav')	
		play_audio(path)
		play_audio('audio/only_groups/bloodgroup.wav')		
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		count=count+1


def play_group(result):
	count=1                                                   		# variable for number of groups to be read. lije o+ve, 0-ve count =2 
	for element in result:
		path = 'audio/only_groups/'+str(element)+str('.wav')
		play_audio(path)
		if ((len(result))!=i):		
			play_audio('audio/and.wav')
		count=count+1



def play_individual_blood_audio(result):							# Method to play individual blood group names.
	play_blood_names(result) 										#plays names of checked blood groups
	time.sleep(0.7)
		
	play_audio('audio/2.wav')
	time.sleep(0.5)
	
	play_audio('audio/3.wav')
	time.sleep(0.5)	
	
	play_group(result)
	time.sleep(0.5)

	if len(result)>1:
		play_audio('audio/only_groups/bloodgroups.wav')
	
	if len(result)==1:		
		play_audio('audio/only_groups/bloodgroup.wav')		
	
	time.sleep(0.5)	
	
	play_audio('audio/5.wav')
	time.sleep(0.5)	
	
	play_audio('audio/6.wav')
	
	
def play(filename,day):								# Module for playing the bhajans for the particular day.	
	global songNo
	songNo += 1
	pygame.mixer.music.stop()
	previousFile = filename
	pygame.mixer.music.load('./playlist/'+day+'/'+ filename)
	print "Now playing " + filename + " songNo " + str(songNo)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy():
		pygame.time.Clock().tick(1000)
		

def bhajans_play(vlc_val):							# Using radio sai stream we are playing the bhajans
    while(value!=0 ):        
        if(stream_or_game):
            vlc_player.play()
        if(vlc_val):
            vlc_player.stop()
        elif(stream_or_game==1):
            global value
            pygame.mixer.music.set_volume(0.1)
            vol=pygame.mixer.music.get_volume()
            playlist,cur_day=day()
            for filename in playlist:
	        	if value==0 and stream_or_game==1:    
		     		return schedule.CancelJob
	       		play(filename,cur_day)
    	
    
def bhajans_stop():
    if(stream_or_game==0):    
        vlc_player.stop()
    else:
        global value
        print('{} Now the system will exit '.format(datetime.datetime.now())) #this works ok
        pygame.mixer.music.stop()
        value=0
        schedule.clear('daily-tasks')	
        sys.exit()
        return scheduke.CancelJob	
       
def pause():
    vlc_player.stop()
    if(stream_or_game==0):    
        vlc_player.stop()
    else:       
     	   pygame.mixer.music.pause()

def unpause():
    vlc_player.play()
    if(stream_or_game==0):    
        vlc_player.play()
    else:
        pygame.mixer.music.unpause()

def exit():
    print('{} Now the system will exit '.format(datetime.datetime.now())) #this works ok
    if(stream_or_game==0):    
            vlc_player.stop()
    else:
            pygame.mixer.music.stop() 		    
    sys.exit()
