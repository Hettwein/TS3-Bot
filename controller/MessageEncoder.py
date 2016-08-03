# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 16:31:46 2016

@author: Heiko
"""

import json
from model.messages.DiscoverMessage import DiscoverMessage
from model.messages.NewBuddyMessage import NewBuddyMessage
from model.messages.NameMessage import NameMessage
from model.messages.ChatMessage import ChatMessage
from model.messages.BroadcastMessage import BroadcastMessage
from model.messages.QuitMessage import QuitMessage

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DiscoverMessage):
            return {"discover": True, "addr": obj.addr, "port": obj.port, "timestamp": obj.timestamp}
        elif isinstance(obj, NewBuddyMessage):
            print(obj.timestamp)
            return {"newBuddy": True, "name": obj.name, "port": obj.port, "new": obj.new, "timestamp": obj.timestamp}
        elif isinstance(obj, NameMessage):
            return {"nameMsg": True, "name": obj.name, "timestamp": obj.timestamp}
        elif isinstance(obj, ChatMessage):
            return {"chat": True, "text": obj.text, "name": obj.name, "timestamp": obj.timestamp}
        elif isinstance(obj, BroadcastMessage):
            return {"broadcast": True, "text": obj.text, "name": obj.name, "timestamp": obj.timestamp}
        elif isinstance(obj, QuitMessage):
            return {"quit": True, "name": obj.name, "timestamp": obj.timestamp}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
        
def asMessage(dct):
    if("discover" in dct):
        return DiscoverMessage(dct["addr"], dct["port"], dct["timestamp"])
    elif("newBuddy" in dct):
        print("bretzel " + dct["name"])# + str(dct["port"]) + str(dct["new"]))
        return NewBuddyMessage(dct["name"], dct["port"], dct["new"], dct["timestamp"])
    elif("nameMsg" in dct):
        return NameMessage(dct["name"], dct["timestamp"])
    elif("chat" in dct):
        return ChatMessage(dct["text"], dct["name"], dct["timestamp"])
    elif("broadcast" in dct):
        return BroadcastMessage(dct["text"], dct["name"], dct["timestamp"])
    elif("quit" in dct):
        return QuitMessage(dct["name"], dct["timestamp"])
    return dct