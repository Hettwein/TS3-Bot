# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:38:12 2016

@author: Heiko
"""

from model.messages.Message import Message

class BroadcastMessage(Message):
    
    def __init__(self, text, name, timestamp=0):
        super().__init__(timestamp)
        self.text = text
        self.name = name
