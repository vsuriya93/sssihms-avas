#							 OM SRI SAIRAM
# SSSIHMS AVAS - Automated Voice Announcement System
AVAS is an open source contribution from DMACS (Dept. of Mathematics and Computer Science) Sri Sathya Sai Institue Of Higher learning Puttaparthi.
The main goal of the program is to make a recorded voice announcement for the approriate blood group.
There is a server running which serves the client through the webpages and when a request is made then the appropriate voice announcement is made.

The work flow of the module is given as below diagram :
![AVAS LOGO](./avas_outline.png) 

In our particular case of SSSIHMS a continous stream of music(Bhajans) are played. So when a request for the blood requirements are made
then the music is paused and the announcement is made and then is unpaused.

From the diagram we see that a python flask based webserver is running continiously, clients can be connected to the server through a web
interface and using their credentials they can log in and make the request for the blood.
Other details are as below:

The name of this Application is AVAS(Automated Voice Announcement System).
This Application Automates Voice announcements for blood groups in the Hospital.


For Setting up the Environment: (python v 2.7.*)

It is always a good approach to have separate virtual environments for our applications and install the required packages in that environment. 

Ubuntu Environment :

sudo apt-get install python-flask

sudo apt-get install python-pyaudio

we also use packages like schedule and pygame for pausing and playing while the announcement is being made.

Windows Environment :

Install Ananconda which is present in the folder or can be downloaded from Anaconda.org and can be installed system wide.

Install pyaudio which is also present in the folder or can be downloaded as wheel file and installed using the pip command.

Similarly  schedule and pygame packages wheel files can be downloaded and installed using pip command for each of them.



Directory Structure:
===
app.py -> 	code for the web server
templates -> 	contains html + css files for the rendering UI
users -> 	contains user credentials for log in
audio ->	contains .wav files for the audio (Thanks Ravi Sir, SSSIHMS)
static ->	contains the images which will be rendered to the user's browser.
playlists ->	contains the songs for every day to be played.
Packages to 
be installed -> contains a text file which has gives which packages are to be installed for running our program
This program will be runned in the directory where the playlists are present in the system

About the program:
==================  
    -> This AVAS program is a python based simple server client program where the server is locally hosted in the lan of the hospital and 	 any user can connect to the server with the server ip and a dedicated port no:5000.
    -> The user gets the web interface and can submit a request to the server.
    -> In the background the songs scheduled for the day will be played and when the request comes the music pauses makes the announcement  	   and plays the music back after the announcement.
    -> The user can stop the announcement in middle and then request a new one.
    -> Any new user can be added from the interface itself.
    -> This program automatically starts at a particular time in the morning and stops at the evening by itself. 
    -> To run the program in windows enviroment go to the press windows+r and enter cmd 
	.press cd Desktop
	.press the desired folder and enter python avas.py		



NOTE:
=====

This application allows addition and deletion of users by modifying user_details.txt in users folder.

Hard Syntax -> USERNAME:PASSWORD

Please follow the above syntax to add users. To delete users, just remove the corresponding entry.

In the UI aslo you can add user.

For removing the user you can follow the above step of removing the corresponding entry.

CONTACT:
========

For any clarification please drop in a mail at vsuriya93@gmail.com, gauthamdasu@gmail.com

Thanking Swami for giving us this opportunity to serve him,

Regards,
SSSIHL and SSSIHMSS
