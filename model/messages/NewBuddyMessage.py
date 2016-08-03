# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:38:13 2016

@author: Heiko
"""

from model.messages.Message import Message

class NewBuddyMessage(Message):
    
    def __init__(self, name, port, new, timestamp=0):
        super().__init__(timestamp)
        self.name = name
        self.port = port
        self.new = new
