import time
import datetime
import pygame
import webbrowser


# Module for playing that days playlist.
def get_day():
	now = datetime.datetime.now()
	if now.strftime("%A")== "Monday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Tuesday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Wednesday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Thursday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Friday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Saturday":
		day=now.strftime("%A")
	if now.strftime("%A")== "Sunday":
		day=now.strftime("%A")
	print "Todays day is",day
	print "Playing the playlist of",day
	print "Server will start soon"




def user_box(msg):
	title = "Login Information"
	fieldNames = [ "User Name", "Password"]
	fieldValues = []  
	fieldValues = multpasswordbox(msg,title, fieldNames)		
									#To make sure that none of the fields was left blank
	while 1:  						# Loop till the accepatable values are found.
		if fieldValues == None: 
        		break
		errmsg = ""   		 
		for i in range(len(fieldNames)):
			if fieldValues[i].strip() == "":
				errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
		if errmsg == "": 
        		break
    		else:
        		fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)	
	return fieldValues	




def validate(fieldValues):
	fp = open('user/user_details.txt','r')
	details = fp.readlines()
	for row in details:
		values=row.strip().split(':')
		if fieldValues[0]==values[0] and fieldValues[1]==values[1]:
			return 1	
	user_box("Enter Valid credentials")	



def Admin_box():	
	msgbox("Hello admin please login to use.", title = "SAIRAM")
	msg = "Enter the details:"
	fieldValues=user_box(msg)
	val=valid(fieldValues)
	
	while 1:
		msg="Hello Admin";
		choices= ["pause","play","stop","help"]
		reply=buttonbox(msg,choices=choices,title="SAIRAM")
		if reply is "pause": 
			p.pause()   						#pygame.mixer.music.pause()
		elif reply is "play":
			p.play() 							#pygame.mixer.music.unpause()
		elif reply is "stop":
			p.stop()							#pygame.mixer.music.pause()
		elif reply is "help":
			webbrowser.open("./help.html") 



