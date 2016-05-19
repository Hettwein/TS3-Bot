# -*- coding: utf-8 -*-
"""
Created on Tue May 17 15:15:36 2016

@author: Heiko
"""

import socket
import threading
import sys
from tkinter import *


buddy_list = {}
gui_buddy_list = 1
chat_box = 1
nickname = ""
PORT_LISTENING = 50000
listener_stop= threading.Event()
client_listener_stop= threading.Event()
input_stop= threading.Event()


def main(argv):
    global nickname
    global PORT_LISTENING
    #nickname = input('Please enter nickname: ')
    #print('\nWelcome ', nickname, '!\n')
    if len(sys.argv) > 1:
        PORT_LISTENING = int(sys.argv[1])
    #print("listening on " + str(PORT_LISTENING))
    gui()


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
    print("start listening on " + str(PORT_LISTENING))    
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
                update()
                print(buddy_name + " has disconnected.\n")
                newMessage(buddy_name + ' has disconnected.')
                break
            elif data.split(';')[0] == 'C':
                print(buddy_name + ': ' + data.split(';')[1])
                newMessage(buddy_name + ': ' + data.split(';')[1])
            elif data.split(';')[0] == 'G':
                print('[All]' + buddy_name + ': ' + data.split(';')[1])
                newMessage(buddy_name + ': ' + data.split(';')[1])
            elif data.split(';')[0] == 'D':
                connect(data.split(';')[1], data.split(';')[2], 1)
            elif data.split(';')[0] =='N':
                connection.send(nickname.encode('utf-8'))
                buddy_name = data.split(';')[1]
                if int(data.split(';')[3]) > 0:
                    if int(data.split(';')[3]) == 2:
                        newMessage(buddy_name + ' has connected.')
                        for buddy in buddy_list:
                            buddy_list[buddy].send(('D;' + addr[0] + ';' + data.split(';')[2]).encode('utf-8'))
                    connect(addr[0], data.split(';')[2])

                
        except:
            print("Unexpected error:", sys.exc_info()[0])
            #disconnect()
            buddy_list[buddy_name].shutdown(socket.SHUT_RDWR)
            buddy_list[buddy_name].close()
            buddy_list.pop(buddy_name)
            update()
            newMessage(buddy_name + ' has disconnected.')
            break
    print("Connection to" + str(addr) + " closed.\n")

def connect(addr, port, new=0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    if sock.connect_ex((addr, int(port))) == 0:
        try:
            sock.send(('N;' + nickname + ';' + str(PORT_LISTENING) + ';' + str(new)).encode('utf-8'))
            buddy = sock.recv(1024).decode('utf-8')
            buddy_list[buddy] = sock
            update()
            if new == 1:
                newMessage(buddy + ' has connected.')
        except:
            print("Unexpected error while connecting:", sys.exc_info()[0])
            pass

def discover(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    port = 50000
    while port <= 50005:
        print(str(port))
        print(str(PORT_LISTENING))
        if port != PORT_LISTENING and sock.connect_ex((addr, port)) == 0:
            try:
                sock.send(('N;' + nickname + ';' + str(PORT_LISTENING) + ';2').encode('utf-8'))
                buddy = sock.recv(1024).decode('utf-8')
                buddy_list[buddy] = sock
                update()
                break
            except:
                print("Unexpected error while discovery:", sys.exc_info()[0])
                pass
        port += 1
    newMessage('You have connected to ' + addr + ':' + str(port) + '.')
    

def scan():
    print("start scanning")


def buddys():
    print("listing buddys")
    print(buddy_list.keys())
    #print(buddy_list)


def chat(buddy, text):
    newMessage('You: ' + text)
    buddy_list[buddy].send(('C;' + text).encode('utf-8'))
    print("message sent...\n\n")
    

def broadcast(text):
    newMessage('You' + ': ' + text)
    for buddy in buddy_list:
        buddy_list[buddy].send(('G;' + text).encode('utf-8'))
    print("message sent...\n\n")


def disconnect():
    for buddy in buddy_list:
        buddy_list[buddy].send(('Q;').encode('utf-8'))
        #buddy_list[buddy].shutdown(socket.SHUT_RDWR)
        buddy_list[buddy].close()
    client_listener_stop.set()
    newMessage('You have disconnected.')
    

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def connectdialog(root):
    filewin = Toplevel(root)
    row1 = Frame(filewin)
    row1.pack(side=TOP, fill=X, padx=5, pady=5)
    row2 = Frame(filewin)
    row2.pack(side=TOP, fill=X, padx=5, pady=5)
    row3 = Frame(filewin)
    row3.pack(side=TOP, fill=X, padx=5, pady=5)
    Label(row1, text="Peer address:", width=15, anchor='w').pack(side=LEFT)
    addrentry = Entry(row1)
    nameentry = Entry(row2)
    #addrentry.bind("<Return>", (lambda e1=filewin, e2=addrentry.get(), e3=nameentry.get(): startconnecting(e1, e2, e3)))
    #nameentry.bind("<Return>", (lambda e1=filewin, e2=addrentry.get(), e3=nameentry.get(): startconnecting(e1, e2, e3)))
    addrentry.pack(side=RIGHT, expand=YES, fill=X)
    nameentry.pack(side=RIGHT, expand=YES, fill=X)
    Label(row2, text="Nickname:", width=15, anchor='w').pack(side=LEFT)
    okbutton = Button(row3, text="Ok", command=lambda: startconnecting(filewin, addrentry.get(), nameentry.get()))
    okbutton.pack(side=LEFT)
    cancelbutton = Button(row3, text="Cancel", command=filewin.destroy)
    cancelbutton.pack(side=RIGHT)

def startconnecting(root, addr, name):
    global nickname
    nickname = name
    discover(addr)

    #input_thread = threading.Thread(target = input_processing, args = ())
    listener_thread = threading.Thread(target = port_listener, args = ())
    
    #input_thread.start()
    listener_thread.start()
    root.destroy()
    
    #listener_thread.join()
    #input_thread.join()
    
    #print("bye")


def menubar(root):
    menubar = Menu(root)
    
    connectionsmenu = Menu(menubar, tearoff=0)
    connectionsmenu.add_command(label="Connect", command=lambda: connectdialog(root))
    connectionsmenu.add_command(label="Disconnect", command=disconnect)
    connectionsmenu.add_separator()
    connectionsmenu.add_command(label="Exit", command=root.quit)
    
    menubar.add_cascade(label="Connections", menu=connectionsmenu)
    
    contactsmenu = Menu(menubar, tearoff=0)
    contactsmenu.add_command(label="Manage contacts", command=donothing)
    contactsmenu.add_command(label="Manage favorites", command=donothing)
    
    menubar.add_cascade(label="Contacts", menu=contactsmenu)
    
    settingsmenu = Menu(menubar, tearoff=0)
    settingsmenu.add_command(label="Sound", command=donothing)
    settingsmenu.add_command(label="Identity", command=donothing)
    settingsmenu.add_command(label="Hotkeys", command=donothing)
    settingsmenu.add_separator()
    settingsmenu.add_command(label="Preferences", command=donothing)
    
    menubar.add_cascade(label="Settings", menu=settingsmenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help", command=donothing)
    helpmenu.add_command(label="About...", command=donothing)
    
    menubar.add_cascade(label="Help", menu=helpmenu)
    
    root.config(menu=menubar)

def chatbox(root):
    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill=Y )
    
    global chat_box
    chat_box = Listbox(root, yscrollcommand = scrollbar.set, width=60)
    #chat_box.insert(END, "You have connected.")
    chat_box.pack( side = TOP, fill = BOTH )
    #mylist.place(x=10, y=200)
    scrollbar.config( command = chat_box.yview )

def onlineframe(root):
    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill=Y )
    #scrollbar.place
    global gui_buddy_list
    gui_buddy_list = Listbox(root, yscrollcommand = scrollbar.set, height=20, width=40)

    gui_buddy_list.pack( side = TOP, fill = BOTH )
    #mylist.place(x=10, y=10)
    scrollbar.config( command = gui_buddy_list.yview )

def update():
    print(str(gui_buddy_list))
    gui_buddy_list.delete(0, END)
    for buddy in buddy_list:
        gui_buddy_list.insert(END, buddy)

def newMessage(msg):
    chat_box.insert(END, msg)

def gui():
    root = Tk()
    root.title('Tumbleweed')
    root.minsize(507, 507)
    
    menubar(root)
    
    onlineframe(root)
    
    chatbox(root)
    
    text1 = Entry(root, bd=5)
    text1.pack(side=BOTTOM)
    text1.bind("<Return>", (lambda event, e=text1.get(): broadcast(e)))
    button = Button(root, text="Send", command=lambda: broadcast(text1.get()))
    button.pack(side=BOTTOM)
    
    root.mainloop()



if __name__ == "__main__":
    main(sys.argv)