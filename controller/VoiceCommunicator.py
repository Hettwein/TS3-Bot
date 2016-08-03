# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 15:15:28 2016

@author: Heiko
"""

import socket
import threading
import pyaudio

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10240
    
class VoiceReceiver:
    
    def __init__(self):
        self.listeningStop = threading.Event()        
        
        # Pyaudio Initialization        
        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        output = True)

    def listeningThread(self):
        # Socket Initialization
        host = '127.0.0.1'
        port = 50002
        backlog = 5
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host,port))
        s.listen(backlog)
        print("listening ...")
        
        client, address = s.accept()
        
        # Main Functionality
        while not self.listeningStop.is_set():
            data = client.recv(size)
            if data:
                # Write data to pyaudio stream
                self.stream.write(data)  # Stream the recieved audio data
                client.send('ACK'.encode('utf-8'))  # Send an ACK
        
        client.close()
        self.stream.close()
        self.p.terminate()

    def startListening(self):
        self.listeningStop.clear()
        threading.Thread(target = self.listeningThread, args = ()).start()
    
    def stopListening(self):
        self.listeningStop.set()


class VoiceSender:

    def __init__(self):
        self.streamStop = threading.Event()        
        
        # Pyaudio Initialization
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 10240
        
        self.p = pyaudio.PyAudio()
        
        self.stream = self.p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)

    def streamThread(self):
        # Socket Initialization
        host = '127.0.0.1'
        port = 50002
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        
        # Main Functionality
        while not self.streamStop.is_set():
            data = self.stream.read(chunk)
            s.send(data)
            s.recv(size)
        
        s.close()
        self.stream.close()
        self.p.terminate()

    def startStream(self):
        self.streamStop.clear()
        threading.Thread(target = self.streamThread, args = ()).start()
    
    def stopStream(self):
        self.streamStop.set()