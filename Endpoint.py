# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:46:09 2016

@author: Heiko
"""

import socket
import threading
import sys
import json

class Endpoint:
    
    def __init__(self):
        pass
    
    def send(self, addr, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((addr, int(port))) == 0:
            try:
                sock.send(('N;' + nickname + ';' + str(PORT_LISTENING) + ';' + str(new)).encode('utf-8'))
                buddy = sock.recv(1024).decode('utf-8')
                buddy_list[buddy] = sock
                update()
                if new == 1:
                    newMessage(buddy + ' has connected.', "info")
            except:
                print("Unexpected error while connecting:", sys.exc_info()[0])
                pass
        addr.send(json.dumps(message).encode('utf-8'))
    
    def blockingReceive(self):
        pass
    
    def nonblockingReceive(self):
        pass