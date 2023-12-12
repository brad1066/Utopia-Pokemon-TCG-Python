from tkinter import *
from tkinter import ttk, messagebox

import os
import sys

from pprint import pprint
import json
from operator import itemgetter

from CustomWidgets import *

class EditItemTool(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.controller = controller
        self.menus = {}
        
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        
        #self.fullscreen()
        self.title("Utopia - Sales Tool")
        # self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        self.genMenu()
        self.bind("<Destroy>", self._destroy)

    def fullscreen(self):
        self.lift()
        # self.state("zoomed")

    def genMenu(self):
        self.mainMenu = Menu(self)
        
        self.controller.generateMenuBar(master=self, menuBar=self.mainMenu, menus=self.menus)

    def _destroy(self, event=None):
        self.controller.remove(self)

if __name__ == "__main__":
    import main
    app = main.App()
    app.openWindow("EditItemTool")
