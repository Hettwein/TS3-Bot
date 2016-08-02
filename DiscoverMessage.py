# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:02:20 2016

@author: Heiko
"""

from Message import Message

class DiscoverMessage(Message):
    
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
