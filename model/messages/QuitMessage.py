# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:03:59 2016

@author: Heiko
"""

from model.messages.Message import Message

class QuitMessage(Message):
    
    def __init__(self, name, timestamp=0):
        super().__init__(timestamp)
        self.name = name