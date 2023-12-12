from tkinter import *
from tkinter import ttk, messagebox
from CustomWidgets import *
from time import sleep

import os
import sys

from pprint import pprint
import json
import csv
import glob

class NotesTool(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.controller = controller
        self.menus = {}
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        self.fullscreen()
        self.title("Notes")
        # self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        self.genMenu()
        self.resizable(width=True, height=True)

        self.bind_all("<Control-w>", self.close)
        self.bind_all("<Control-o>", self.openNote)
        self.bind_all("<Control-s>", self.saveNotes)
        self.bind_all("<Control-n>", self.openNewNote)
        self.bind("<Destroy>", self._destroy)

        self.tabs = []
            
        self.notebook = Notebook(self)

        try:
            self.tabs.append(Note(f="{0}\\Notes\\Tutorial.txt".format(os.getcwd())))
            self.notebook.addChild(NotePage(self, self, data=self.tabs[-1]), text=self.tabs[-1].title)
        except: pass
        
##        for file in glob.glob(os.getcwd()+"\\Notes\\*.txt"):
##            self.tabs.append(Note(f=file))
##
##        for tab in self.tabs:

        self.notebook.grid(row=0, column=0, sticky=NSEW)
        self.notebook.bind("<Button-3>", self.tabRightClick)
        self.notebook.bind("<Button-1>", self.changeNote)
        
    def genMenu(self):
        self.mainMenu = Menu(self, tearoff=0)
        self.fileMenu = Menu(self.mainMenu, tearoff=0)

        self.controller.makeMenusItem(self.mainMenu,
                                      {"File": self.fileMenu},
                                      {"Save": self.saveNotes},
                                      self.menus)
        self.controller.makeMenusItem(self.fileMenu,
                                      {},
                                      {"Open Note": self.openNote,
                                       "Open Receipt": self.openReceipt,
                                       "New Note": self.openNewNote},
                                      self.menus)

        self.controller.generateMenuBar(master=self, menuBar=self.mainMenu, menus=self.menus)

    def close(self, event=None):
        if messagebox.askyesno("Close", "Do you really want to close this application"):
            self.destroy()
        
    def _destroy(self, event=None):
        self.saveNotes()
        self.controller.remove(self)
        
    def fullscreen(self):
        self.lift()
        # self.state("zoomed")

    def openNote(self, event=None):
        NoteOpener(controller=self)

    def openReceipt(self, event=None):
        ReceiptOpener(controller=self)

    def openNewNote(self, event=None):
        NewNoteOpener(controller=self)

    def saveNotes(self, event=None):
        for i in range(self.tabs.__len__()):
            tab = self.notebook.slaves[i]
            self.tabs[i].save(text=tab.mainNotes.get(0.0, END))

    def tabRightClick(self, event=None):
        popup = PopUp(self, x=event.x_root, y=event.y_root)
        popup.add_command(label="Close", command=lambda: self.removeTab(event=event))
        popup.show()

    def removeTab(self, event=None):
##        pass
        tab = self.notebook.tk.call(self.notebook._w, "index", "@{0}, {1}".format(event.x, event.y))
        pprint(tab)
        self.notebook.slaves.pop(tab)
            
        self.notebook.forget(tab)

    def changeNote(self, event=None):
        tab = self.notebook.tk.call(self.notebook._w, "index", "@{0}, {1}".format(event.x, event.y))
        currTabTitle = self.tabs[tab].title
        self.title("Notes - {0}.txt".format(currTabTitle))

class Notebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        ttk.Notebook.__init__(self, *args, **kwargs)

        self.slaves = []

    def addChild(self, *args, **kwargs):
        self.add(*args, **kwargs)
        self.slaves.append(args[0])
        
class NotePage(Frame):
    def __init__(self, parent, controller, data={}):
        Frame.__init__(self, parent)

        self.mainNotes = Text(self)
        self.mainNotes.pack(side=TOP, fill=BOTH, expand=True)
        self.mainNotes.insert(0.0, data.text)

class NewNoteOpener(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        self.container = Frame(self)

        self.title("New Note")
        self.container.grid_rowconfigure(0, weight=4)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=25)

        self.newNoteTitle = StringVar(self, "New Note")

        Label(self.container, text="Enter a title for the note:").grid(row=0, column=0, sticky=NSEW)
        self.titleEntry = Entry(self.container, textvariable=self.newNoteTitle)
        self.submitButton = Button(self.container, text="Submit", command=self.submit)

        self.titleEntry.grid(row=1, column=0, sticky=NSEW)
        self.submitButton.grid(row=1, column=1, sticky=NSEW)

        self.titleEntry.bind("<Return>", self.submit)
        self.titleEntry.focus()

    def submit(self, event=None):
        with open("{0}\\Notes\\{1}.txt".format(os.getcwd(), self.newNoteTitle.get()), 'w') as f:
            f.write("")
            self.controller.tabs.append(Note(f=f.name))
            
        self.controller.notebook.addChild(NotePage(self.controller,
                                             self.controller,
                                             data=self.controller.tabs[-1]),
                                    text=self.newNoteTitle.get())
        self.destroy()

class NoteOpener(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("New Note")

        self.container = VerticalScrolledFrame(self)
        self.container.grid(row=0, column=0, padx=20, pady=25, sticky=NSEW)

        self.noteLocVar = StringVar()

        for note in glob.glob(os.getcwd()+"\\Notes\\*.txt"):
            button = NoteOpenerItem(self.container.body, controller=self, fileLoc=note, text=note.split("\\")[-1].strip(".txt"))
            button.pack(side=TOP, fill=BOTH, expand=True)

        self.openButton = Button(self, text="Open", command=self.submit)
        self.openButton.grid(row=1, column=0, sticky=NSEW)

    def updateNoteLoc(self, result):
        self.noteLocVar.set(result.fileLoc)

    def submit(self, event=None):
        with open(self.noteLocVar.get(), 'r') as f:
            noteF = Note(f=f.name)
            self.controller.tabs.append(noteF)

            self.controller.notebook.addChild(NotePage(self.controller,
                                             self.controller,
                                             data=self.controller.tabs[-1]),
                                    text=noteF.title)
        self.destroy()

class ReceiptOpener(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title("New Note")

        self.container = VerticalScrolledFrame(self)
        self.container.grid(row=0, column=0, padx=20, pady=25, sticky=NSEW)

        self.noteLocVar = StringVar()

        for note in glob.glob(os.getcwd()+"\\Receipts\\*.txt"):
            button = NoteOpenerItem(self.container.body, controller=self, fileLoc=note, text=note.split("\\")[-1].strip(".txt"))
            button.pack(side=TOP, fill=BOTH, expand=True)

        self.openButton = Button(self, text="Open", command=self.submit)
        self.openButton.grid(row=1, column=0, sticky=NSEW)

    def updateNoteLoc(self, result):
        self.noteLocVar.set(result.fileLoc)

    def submit(self, event=None):
        with open(self.noteLocVar.get(), 'r') as f:
            noteF = Note(f=f.name)
            self.controller.tabs.append(noteF)

            self.controller.notebook.addChild(NotePage(self.controller,
                                             self.controller,
                                             data=self.controller.tabs[-1]),
                                    text=noteF.title)
        self.destroy()

class NoteOpenerItem(Button):
    def __init__(self, parent, controller=None, fileLoc=None, *args, **kwargs):
        Button.__init__(self, parent, *args, **kwargs)
        self.fileLoc = fileLoc
        self.config(command=lambda: controller.updateNoteLoc(self))

class Note:
    def __init__(self, f=None):
        self.f = f
        print(f)
        self.title = f.split("\\")[-1].strip(".txt")
        self.text = open(f, 'r').read()

    def save(self, text=None):
        with open(self.f, "w") as f:
            f.write(text or self.text)
            self.text = text


if __name__ == "__main__":
    import main
    app = main.App()
    app.openWindow("NotesTool")
    



        







        
