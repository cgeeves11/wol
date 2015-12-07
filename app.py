from __future__ import with_statement
from flask import Flask, request, url_for, redirect, render_template, session, send_from_directory
import socket
import struct
import os
import sys
import ConfigParser


app = Flask(__name__)
app.config.from_pyfile('../app.cfg')

generalbroadcast='192.168.0.255'
livroom ='D4-BE-D9-A4-52-6F'


@app.route('/', methods=['GET', 'POST'])
def home_page():
    try:

        return render_template('home.html')

    except Exception,e:
        return render_template('error.html',resultsSET=e)



@app.route('/sendPacket', methods=['GET', 'POST'])
def sendWolPacket():
    try:

        # Get variables
        computername=request.form['computername']

        # error checking
        if not computername:
            return render_template('error.html',resultsSET='Please enter a computer name')

        computername=str(computername).lower()

        #Get correct MAC for specifid machine
        if computername=='livroom':
            macaddress = livroom
        else:
            return render_template('error.html',resultsSET='Not a valid machine name')


        # Check macaddress format and try to compensate.
        if len(macaddress) == 12:
            pass
        elif len(macaddress) == 12 + 5:
            sep = macaddress[2]
            macaddress = macaddress.replace(sep, '')
        else:
            raise ValueError('Incorrect MAC address format')

        # Pad the synchronization stream.
        data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
        send_data = ''

        # Split up the hex values and pack.
        for i in range(0, len(data), 2):
            send_data = ''.join([send_data,struct.pack('B', int(data[i: i + 2], 16))])

        # Broadcast it to the LAN.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (generalbroadcast, 7))

        return render_template('wolresult.html',result='success')

    except Exception,e:
        return render_template('error.html',resultsSET=e)



app.secret_key = app.config['SECRET_KEY']

#main
if __name__ == '__main__':
    app.debug=app.config['DEBUG'] #reload on code changes. show traceback
    app.run()
