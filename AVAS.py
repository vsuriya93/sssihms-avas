'''
AVAS - Automated Voice Announcement System used in SSSIHMS for making urgent blood requests needed in the hospital.
This is the refactored code with comments. The main idea of the application is to use an stream end point of live bhajans from radiosai global harmony and play as a stream. When a request for the requirement of blood is received, the stream is paused and then the recorded announcement for the same is made. Then the stream is again played. In this selenium web browser is used.
'''
# Import the modules required for the application.
import pyaudio															   # package for playing audio.
import wave
import time
import datetime
import schedule
import os
import sys
import threading
import vlc
import urllib
# simple graphical user interface related package.
from easygui import *

# windows voice control related packages.
from ctypes import cast, POINTER
# windows voice control related packages.
from comtypes import CLSCTX_ALL
# windows voice control related packages.
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# Flask - Client server related packages.
from flask import Flask,render_template,request,session,redirect,url_for

from globals import (stream_or_game)
from Audio import (play_audio, play_all_blood_audio,
                   play_individual_blood_audio, bhajans_play,
                   pause, unpause)

# for stopping bhajans
value = 1

url = "http://stream.radiosai.org:8000/"

# initialize object of flask
app = Flask(__name__)

# check whether the stream is available or not if not then make the variable 1
# meaning we play through pygame.10
# variable stream_or_game: if 0 then through stream else through pygame we
# play the songs.

if (urllib.urlopen(url).getcode()) != 200:
    stream_or_game = 1

# initialize the pygame mixer.
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
songNo = 0
blood_group_list = ['O+', 'O-', 'A+', 'A-',
                    'B-', 'B+', 'AB-', 'AB+', 'ALL']


def run_thread(job_fun):
    try:
        job_thread = threading.Thread(target=job_fun)
        job_thread.start()
        return job_thread
    except (KeyboardInterrupt, SystemExit):
        print('\n! Received keyboard interrupt, quitting threads.\n')


def avas():
    print("The SSSIHMS-AVAS Server Started")
    try:
        if __name__ == "__main__":
            app.secret_key = '3sdadsdad4'
            app.run(host='0.0.0.0', threaded=True)
    except KeyboardInterrupt:
        print("You cancelled the program!")
        sys.exit(1)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def avas_stop():
    shutdown_server()


@app.route("/")
def main():
    return render_template('login.html')


@app.route("/bloodRequest", methods=['POST'])
def bloodRequest():
    result = request.form
    check= authenticate_user(result)
    if check is False:
        return render_template('error.html')
    if session['logged_in'] is False:
        return render_template('login.html')
    session['logged_in'] = True
    return render_template('home.html', blood_group_list=blood_group_list)


@app.route("/logout", methods=['POST'])
def Exit():
    return redirect(url_for('main'))


@app.route("/stop", methods=['GET','POST'])
def stop():
    global str_var
    str_var = 0
    unpause()
    return render_template('home.html', blood_group_list=blood_group_list)


@app.route("/adduser", methods=['POST'])
def adduser():
    return render_template('adduser.html')


@app.route("/Admin", methods=['GET', 'POST'])
def admin():
    return render_template('Admin.html')


@app.route("/Admin_home", methods=['POST'])
def admin_home():
    result = request.form
    check = authenticate_user(result)
    if check is False:
        return render_template('error.html')
    return render_template('Admin_home.html')


@app.route("/home", methods=['POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    return render_template('home.html', blood_group_list=blood_group_list)


@app.route("/addusers", methods=['POST'])
def addusers():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    result = request.form
    if result['passwd'] == result[passwd-rep]:
        s = "\n"+result['uname']+":"+result['passwd']
        fp = open('user/user_details.txt', 'ab')
        fp.write(s)
        fp.close()
        return 	render_template('user_added.html')
    else:
        return "Password missmatch"


@app.route("/request_blood", methods=["POST"])
def request_blood():
    if request.method == 'POST':
        result = request.form
        global flag
        flag = 0
        if result == {}:
            return render_template('home.html',
                                   blood_group_list=blood_group_list)
        pause()
        flag = 1
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.GetMute()
        volume.GetMasterVolumeLevel()
        volume.GetVolumeRange()
        volume.SetMasterVolumeLevel(-10.0, None)
        play_audio('audio/1.wav')
        time.sleep(1)
        for times in range(1, 3):
            if 'ALL' in result:
                play_all_blood_audio()
            else:
                play_individual_blood_audio(result)
            if times%2==1: # for 'I repeat'
                play_audio('audio/8.wav')
            time.sleep(0.5)
        play_audio('audio/9.wav')	
        volume.SetMasterVolumeLevel(-20.0, None)
        unpause()
        return render_template('after_announ.html')

run_thread(avas)
run_thread(bhajans_play)
