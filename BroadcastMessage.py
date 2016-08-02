# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:38:12 2016

@author: Heiko
"""

from Message import *

class BroadcastMessage(Message):
    
    def __init__(self, text):
        self.text = text