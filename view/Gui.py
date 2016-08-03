# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 15:17:32 2016

@author: Heiko
"""

from tkinter import *

class Gui:
    
    def __init__(self, controller):
        self.controller = controller
        #self.gui()
    
    def donothing(self):
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def connectdialog(self, root):
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
        addrentry.bind("<Return>", (lambda event: self.startconnecting(filewin, addrentry.get(), nameentry.get())))
        nameentry.pack(side=RIGHT, expand=YES, fill=X)
        nameentry.bind("<Return>", (lambda event: self.startconnecting(filewin, addrentry.get(), nameentry.get())))
        Label(row2, text="Nickname:", width=15, anchor='w').pack(side=LEFT)
        okbutton = Button(row3, text="Ok", command=lambda: self.startconnecting(filewin, addrentry.get(), nameentry.get()))
        okbutton.pack(side=LEFT)
        cancelbutton = Button(row3, text="Cancel", command=filewin.destroy)
        cancelbutton.pack(side=RIGHT)
    
    def startconnecting(self, root, addr, name):
        self.nickname = name
        root.destroy()
        self.controller.connect(name, addr)
    
        #input_thread = threading.Thread(target = input_processing, args = ())
        #listener_thread = threading.Thread(target = port_listener, args = ())
        
        #input_thread.start()
        #listener_thread.start()
        
        #listener_thread.join()
        #input_thread.join()
        
        #print("bye")
    
    
    def menubar(self, root):
        menubar = Menu(root)
        
        connectionsmenu = Menu(menubar, tearoff=0)
        connectionsmenu.add_command(label="Connect", command=lambda: self.connectdialog(root))
        connectionsmenu.add_command(label="Disconnect", command=self.controller.disconnect)
        connectionsmenu.add_separator()
        connectionsmenu.add_command(label="Exit", command=root.quit)
        
        menubar.add_cascade(label="Connections", menu=connectionsmenu)
        
        contactsmenu = Menu(menubar, tearoff=0)
        contactsmenu.add_command(label="Manage contacts", command=self.donothing)
        contactsmenu.add_command(label="Manage favorites", command=self.donothing)
        
        menubar.add_cascade(label="Contacts", menu=contactsmenu)
        
        settingsmenu = Menu(menubar, tearoff=0)
        settingsmenu.add_command(label="Sound", command=self.donothing)
        settingsmenu.add_command(label="Identity", command=self.donothing)
        settingsmenu.add_command(label="Hotkeys", command=self.donothing)
        settingsmenu.add_separator()
        settingsmenu.add_command(label="Preferences", command=self.donothing)
        
        menubar.add_cascade(label="Settings", menu=settingsmenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        root.config(menu=menubar)
    
    def chatbox(self, root):
        scrollbar = Scrollbar(root)
        scrollbar.pack( side = RIGHT, fill=Y )
        
        global chat_box
        chat_box = Text(root, yscrollcommand = scrollbar.set, width=60, state=DISABLED)
        chat_box.tag_configure('color', foreground='#0080FF', font=('Tempus Sans ITC', 12, 'bold'))
        chat_box.tag_configure('info', foreground='#808080', font=('Tempus Sans ITC', 12, 'italic'))
        chat_box.tag_configure('error', foreground='#CC0000', font=('Tempus Sans ITC', 12, 'bold'))
    
        chat_box.pack( side = TOP, fill = BOTH )
    
        scrollbar.config( command = chat_box.yview )
    
    def onlineframe(self, root):
        scrollbar = Scrollbar(root, troughcolor='#476042')
        scrollbar.pack( side = RIGHT, fill=Y)
    
        self.guiBuddyList = Listbox(root, yscrollcommand = scrollbar.set, height=20, width=40)
    
        self.guiBuddyList.pack( side = TOP, fill = BOTH )
        #mylist.place(x=10, y=10)
        scrollbar.config( command = self.guiBuddyList.yview )
    
    def update(self, buddys):
        print(str(self.guiBuddyList))
        self.guiBuddyList.delete(0, END)
        for buddy in buddys:
            self.guiBuddyList.insert(END, buddy)
    
    def newMessage(self, msg, mode="color"):
        chat_box.config(state=NORMAL)
        chat_box.insert(END, msg + "\n", mode)
        chat_box.config(state=DISABLED)
    
    def gui(self):
        root = Tk()
        root.title('Tumbleweed')
        #root.minsize(507, 507)
        
        self.menubar(root)
        
        topframe = Frame(root)
        topframe.pack(side=TOP)
        self.onlineframe(topframe)
        
        midframe = Frame(root)
        midframe.pack(side=TOP)
        self.chatbox(midframe)
        
        global sendbox
        sendbox = Entry(root, width=80)
        sendbox.pack(side=LEFT, fill=X)
        sendbox.bind("<Return>", (lambda event: self.controller.broadcast(sendbox.get())))
        button = Button(root, text="Send", command=lambda: self.controller.broadcast(sendbox.get()))
        button.pack(side=LEFT)
        
        root.mainloop()