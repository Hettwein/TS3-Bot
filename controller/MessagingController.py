# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 17:20:22 2016

@author: Heiko
"""

from controller.MessagingCommunicator import MessagingReceiver, MessagingSender
from controller.VoiceCommunicator import VoiceReceiver, VoiceSender
from model.User import User
from view.Gui import Gui
from model.messages.DiscoverMessage import DiscoverMessage
from model.messages.ChatMessage import ChatMessage
from model.messages.BroadcastMessage import BroadcastMessage
from model.messages.NameMessage import NameMessage
from model.messages.QuitMessage import QuitMessage

class MessagingController:
       
    def __init__(self):
        self.gui = Gui(self)
        self.gui.gui()
    
    def connect(self, nickname, addr, port="50001"):
        self.user = User(nickname, addr, port)
        self.receiver = MessagingReceiver(port, self, nickname)
        self.sender = MessagingSender()
        self.receiver.discover(addr)
        self.voiceReceiver = VoiceReceiver()
        self.voiceSender = VoiceSender()
    
    def newBuddy(self, socket, data, addr):
        msg = NameMessage(self.user.name)
        self.sender.send(socket, msg)
        if data.new > 0:
            if data.new == 2:
                msg = DiscoverMessage(addr, data.port)
                self.sender.sendAll(self.user.buddys, msg)
            self.receiver.connect(addr, data.port)
    
    def addBuddy(self, data, socket):
        self.user.buddys[data.name] = socket
        self.gui.update(self.user.buddys)
        self.newMessage("[" + data.timestamp + "]" + data.name + ' has connected.', "info")
        
    def chat(self, name, message):
        data = ChatMessage(message, self.user.name)
        self.sender.send(self.user.buddys[name], data)
        self.newMessage("[" + data.timestamp + "]" + "You: " + message)
        
    def broadcast(self, message):
        data = BroadcastMessage(message, self.user.name)
        self.sender.sendAll(self.user.buddys, data)
        self.newMessage("[" + data.timestamp + "]" + "You: " + message)

    def removeBuddy(self, data):
        self.user.buddys[data.name].close()
        self.user.buddys.pop(data.name)
        self.gui.update(self.user.buddys)
        self.newMessage("[" + data.timestamp + "]" + data.name + ' has disconnected.', "info")

    def newMessage(self, data, mode="color"):
        if(isinstance(data, str)):
            self.gui.newMessage(data, mode)
        else:
            self.gui.newMessage("[" + data.timestamp + "]" + data.text, mode)

    def disconnect(self):
        data = QuitMessage(self.user.name)
        self.sender.sendAll(self.user.buddys, data)
        for buddy in self.user.buddys:
            #buddy_list[buddy].shutdown(socket.SHUT_RDWR)
            self.user.buddys[buddy].close()
        self.receiver.clientListenerStop.set()
        self.newMessage("[" + data.timestamp + "]" + 'You have disconnected.', "info")
        self.gui.update(self.user.buddys)

    def startTalking(self):
        print("mic on")
        self.voiceSender.startStream()

    def stopTalking(self):
        print("mic off")
        self.voiceSender.stopStream()

    def startListening(self):
        print("sound on")
        self.voiceReceiver.startListening()

    def stopListening(self):
        print("sound off")
        self.voiceReceiver.stopListening()
