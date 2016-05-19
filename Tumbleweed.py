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
sendbox = 1
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
                newMessage(buddy_name + ' has disconnected.', "info")
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
                        newMessage(buddy_name + ' has connected.', "info")
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
            newMessage(buddy_name + ' has disconnected.', "info")
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
                newMessage(buddy + ' has connected.', "info")
        except:
            print("Unexpected error while connecting:", sys.exc_info()[0])
            pass

def discover(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    port = 50000
    while port <= 50005:
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
    if port == 50006:
        newMessage("No buddy is online.", "info")
    else:
        newMessage('You have connected to ' + addr + ':' + str(port) + '.', "info")
    

def scan():
    print("start scanning")


def buddys():
    print("listing buddys")
    print(buddy_list.keys())
    #print(buddy_list)


def chat(buddy, text):
    if len(text.strip().strip(';')) > 0:
        sendbox.delete(0, END)
        newMessage('You: ' + text.strip(';'))
        buddy_list[buddy].send(('C;' + text.strip(';')).encode('utf-8'))
        #print("message sent...\n\n")
    

def broadcast(text):
    if len(text.strip().strip(';')) > 0:
        sendbox.delete(0, END)
        newMessage('You' + ': ' + text.strip(';'))
        for buddy in buddy_list:
            buddy_list[buddy].send(('G;' + text.strip(';')).encode('utf-8'))
        #print("message sent...\n\n")


def disconnect():
    for buddy in buddy_list:
        buddy_list[buddy].send(('Q;').encode('utf-8'))
        #buddy_list[buddy].shutdown(socket.SHUT_RDWR)
        buddy_list[buddy].close()
    client_listener_stop.set()
    newMessage('You have disconnected.', "info")
    

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
    addrentry.bind("<Return>", (lambda event: startconnecting(filewin, addrentry.get(), nameentry.get())))
    nameentry.pack(side=RIGHT, expand=YES, fill=X)
    nameentry.bind("<Return>", (lambda event: startconnecting(filewin, addrentry.get(), nameentry.get())))
    Label(row2, text="Nickname:", width=15, anchor='w').pack(side=LEFT)
    okbutton = Button(row3, text="Ok", command=lambda: startconnecting(filewin, addrentry.get(), nameentry.get()))
    okbutton.pack(side=LEFT)
    cancelbutton = Button(row3, text="Cancel", command=filewin.destroy)
    cancelbutton.pack(side=RIGHT)

def startconnecting(root, addr, name):
    global nickname
    nickname = name
    root.destroy()
    newMessage("Searching for buddys . . .", "info")
    discover(addr)

    #input_thread = threading.Thread(target = input_processing, args = ())
    listener_thread = threading.Thread(target = port_listener, args = ())
    
    #input_thread.start()
    listener_thread.start()
    
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
    chat_box = Text(root, yscrollcommand = scrollbar.set, width=60, state=DISABLED)
    chat_box.tag_configure('color', foreground='#0080FF', font=('Tempus Sans ITC', 12, 'bold'))
    chat_box.tag_configure('info', foreground='#808080', font=('Tempus Sans ITC', 12, 'italic'))
    chat_box.tag_configure('error', foreground='#CC0000', font=('Tempus Sans ITC', 12, 'bold'))

    chat_box.pack( side = TOP, fill = BOTH )

    scrollbar.config( command = chat_box.yview )

def onlineframe(root):
    scrollbar = Scrollbar(root, troughcolor='#476042')
    scrollbar.pack( side = RIGHT, fill=Y)

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

def newMessage(msg, mode="color"):
    chat_box.config(state=NORMAL)
    chat_box.insert(END, msg + "\n", mode)
    chat_box.config(state=DISABLED)

def gui():
    root = Tk()
    root.title('Tumbleweed')
    root.minsize(507, 507)
    
    menubar(root)
    
    onlineframe(root)
    
    chatbox(root)
    
    global sendbox
    sendbox = Entry(root, width=80)
    sendbox.pack(side=LEFT, fill=X)
    sendbox.bind("<Return>", (lambda event: broadcast(sendbox.get())))
    button = Button(root, text="Send", command=lambda: broadcast(sendbox.get()))
    button.pack(side=LEFT)
    
    root.mainloop()



if __name__ == "__main__":
    main(sys.argv)