# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 17:20:22 2016

@author: Heiko
"""

from MessagingCommunicator import MessagingReceiver, MessagingSender
from ChatMessage import ChatMessage
from User import User
from Gui import Gui

class MessagingController:
    
    def __init__(self):
        self.gui = Gui(self)
    
    def connect(self, nickname, addr, port="50000"):
        self.user = User(nickname, addr, port)
        self.receiver = MessagingReceiver(port, self, nickname)
        self.sender = MessagingSender()
        self.receiver.discover(addr)
    
    def newBuddy(self, socket, name, addr, port, new):
        self.sender.sendName(socket, self.user.name)
        if new > 0:
            if new == 2:
                for buddy in self.user.buddys:
                    self.sender.sendDiscover(buddy, addr, port)
            self.receiver.connect(addr, port)
    
    def addBuddy(self, name, socket):
        self.user.buddys[name] = socket
        
    def chat(self, name, message):
        self.sender.send(self.user.buddys[name], message)
        
    def broadcast(self, message):
        self.sender.sendAll(self.user.buddys, message)
        
    #def quit(self, name, message):
    #    self.sender.sendQuit(self.user.buddys, self.user.name)

    def removeBuddy(self, name):
        self.user.buddys[name].close()
        self.user.buddys.pop(name)
        #update()
        self.newMessage(ChatMessage(name + ' has disconnected.'), "info")

    def newMessage(self, message, mode="color"):
        print(self.user.name)
        #self.gui.newMessage(message.text, mode)

    def disconnect(self):
        self.sender.sendQuit(self.user.buddys, self.user.name)
        for buddy in self.user.buddys:
            #buddy_list[buddy].shutdown(socket.SHUT_RDWR)
            self.user.buddys[buddy].close()
        self.receiver.clientListenerStop.set()
        self.newMessage(ChatMessage('You have disconnected.'), "info")        