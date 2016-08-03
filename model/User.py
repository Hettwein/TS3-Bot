# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:10:00 2016

@author: Heiko
"""

class User:
    
    def __init__(self, name, addr, port):
        self.name = name
        self.addr = addr
        self.port = port
        self.buddys = {}
