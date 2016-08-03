# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:41:06 2016

@author: Heiko
"""

from datetime import datetime

class Message:
    
    def __init__(self, time):
        if(time == 0):
            self.timestamp = datetime.now().time().strftime("%H:%M")
        else:
            self.timestamp = time