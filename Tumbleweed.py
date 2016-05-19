# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:15:36 2016

@author: Heiko
"""

import socket
import threading
import sys

#PORT_LISTENING = sys.argv[1]

buddy_list = {}

nickname = input('Please enter nickname: ')
print('\nWelcome ', nickname, '!\n')
if len(sys.argv) > 1:
    PORT_LISTENING = int(sys.argv[1])
    print("listening on " + sys.argv[1])
else:
    PORT_LISTENING = 50001


def input_processing():
    while True:
        
        text = input('What\'s next?\nScan: S     List: L     Chat: C     Group-Chat: G     Quit: Q\n\n')
        command = str(text.split()[:1]).strip('[\'\']')
        
        if command == 's' or command == 'S':
            scan()
        elif command == 'l' or command == 'L':
            buddys()
        elif command == 'c' or command == 'C':
            buddy = input("Chat with?\n")
            msg = input("Your text:\n")
            chat(buddy, msg)
        elif command == 'g' or command == 'G':
            msg = input("Your text:\n")
            broadcast(msg)
        elif command == 'q' or command == 'Q':
            disconnect()
            print("quit")
            listener_stop.set()
            break

def port_listener():
    print("start listening")    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', PORT_LISTENING))
    sock.listen(10)
    
    threading.Thread(target = end_listener, args = (sock,)).start()

    #own Thread for every connection
    while not listener_stop.is_set():
        try:
            connection, addr = sock.accept()
            threading.Thread(target = client_listener, args = (addr, connection)).start()
        except:
            print("Connection has been shutdown.")
            break
    print("listening stopped")

           
def end_listener(sock):
    listener_stop.wait()
    sock.close()


def client_listener(addr, connection):
    buddy_name = ""    
    while not client_listener_stop.is_set():
        try:
            data = connection.recv(1024).decode('utf-8')
            #print("message received: " + data)
            if data.split(';')[0] == 'Q':
                buddy_list[buddy_name].close()
                buddy_list.pop(buddy_name)
                print(buddy_name + " has disconnected.\n")
                break
            elif data.split(';')[0] == 'C':
                print(buddy_name + ': ' + data.split(';')[1])
            elif data.split(';')[0] == 'G':
                print('[All]' + buddy_name + ': ' + data.split(';')[1])
            elif data.split(';')[0] == 'D':
                connect(data.split(';')[1], data.split(';')[2], 1)
            elif data.split(';')[0] =='N':
                connection.send(nickname.encode('utf-8'))
                buddy_name = data.split(';')[1]
                if int(data.split(';')[3]) > 0:
                    if int(data.split(';')[3]) == 2:
                        for buddy in buddy_list:
                            buddy_list[buddy].send(('D;' + addr[0] + ';' + data.split(';')[2]).encode('utf-8'))
                    connect(addr[0], data.split(';')[2])       

                
        except:
            print("Unexpected error:", sys.exc_info()[0])
            disconnect()
            buddy_list[buddy_name].shutdown(socket.SHUT_RDWR)
            buddy_list[buddy_name].close()
            print("\nDisconnected.\n")
            break
    print("Connection to" + str(addr) + " closed.\n")

def connect(addr, port, new=0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    print(port)
    print(addr)
    if sock.connect_ex((addr, int(port))) == 0:
        try:
            sock.send(('N;' + nickname + ';' + str(PORT_LISTENING) + ';' + str(new)).encode('utf-8'))
            buddy = sock.recv(1024).decode('utf-8')
            buddy_list[buddy] = sock
        except:
            pass

def discover(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    port = 50000
    while port <= 50005:
        if port != PORT_LISTENING and sock.connect_ex((addr, port)) == 0:
            try:
                sock.send(('N;' + nickname + ';' + str(PORT_LISTENING) + ';2').encode('utf-8'))
                buddy = sock.recv(1024).decode('utf-8')
                buddy_list[buddy] = sock
                break
            except:
                pass
        port += 1
    

def scan():
    print("start scanning")


def buddys():
    print("listing buddys")
    print(buddy_list.keys())
    #print(buddy_list)


def chat(buddy, text):
    buddy_list[buddy].send(('C;' + text).encode('utf-8'))
    print("message sent...\n\n")
    

def broadcast(text):
    for buddy in buddy_list:
        buddy_list[buddy].send(('G;' + text).encode('utf-8'))
    print("message sent...\n\n")


def disconnect():
    for buddy in buddy_list:
        buddy_list[buddy].send(('Q;').encode('utf-8'))
        #buddy_list[buddy].shutdown(socket.SHUT_RDWR)
        buddy_list[buddy].close()
    client_listener_stop.set()
    

discover('127.0.0.1')

input_thread = threading.Thread(target = input_processing, args = ())
listener_thread = threading.Thread(target = port_listener, args = ())

listener_stop= threading.Event()
client_listener_stop= threading.Event()
input_stop= threading.Event()

input_thread.start()
listener_thread.start()

listener_thread.join()
input_thread.join()

print("bye")