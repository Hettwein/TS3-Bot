# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 16:03:59 2016

@author: Heiko
"""

from Message import *

class QuitMessage(Message):
    
    def __init__(self, name):
        self.name = name