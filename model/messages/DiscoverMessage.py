# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:02:20 2016

@author: Heiko
"""

from model.messages.Message import Message

class DiscoverMessage(Message):
    
    def __init__(self, addr, port, timestamp=0):
        super().__init__(timestamp)
        self.addr = addr
        self.port = port
