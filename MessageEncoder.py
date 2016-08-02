# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 16:31:46 2016

@author: Heiko
"""

import json
from DiscoverMessage import DiscoverMessage
from NewBuddyMessage import NewBuddyMessage
from NameMessage import NameMessage
from ChatMessage import ChatMessage
from BroadcastMessage import BroadcastMessage
from QuitMessage import QuitMessage

class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DiscoverMessage):
            return {"discover": True, "addr": obj.addr, "port": obj.port}
        elif isinstance(obj, NewBuddyMessage):
            return {"newBuddy": True, "name": obj.name, "port": obj.port, "new": obj.new}
        elif isinstance(obj, NameMessage):
            return {"nameMsg": True, "name": obj.name}
        elif isinstance(obj, ChatMessage):
            return {"chat": True, "text": obj.text}
        elif isinstance(obj, BroadcastMessage):
            return {"broadcast": True, "text": obj.text}
        elif isinstance(obj, QuitMessage):
            return {"quit": True, "name": obj.name}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
        
def asMessage(dct):
    if("discover" in dct):
        return DiscoverMessage(dct["addr"], dct["port"])
    elif("newBuddy" in dct):
        print("bretzel " + dct["name"])# + str(dct["port"]) + str(dct["new"]))
        return NewBuddyMessage(dct["name"], dct["port"], dct["new"])
    elif("nameMsg" in dct):
        return NameMessage(dct["name"])
    elif("chat" in dct):
        return ChatMessage(dct["text"])
    elif("broadcast" in dct):
        return BroadcastMessage(dct["text"])
    elif("quit" in dct):
        return QuitMessage(dct["name"])
    return dct