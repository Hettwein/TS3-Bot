# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 17:39:09 2016

@author: Heiko
"""

from Message import Message

class NameMessage(Message):
    
    def __init__(self, name):
        self.name = name