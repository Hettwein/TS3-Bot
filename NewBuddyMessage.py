# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:38:13 2016

@author: Heiko
"""

from Message import *

class NewBuddyMessage(Message):
    
    def __init__(self, name, port, new):
        self.name = name
        self.port = port
        self.new = new
