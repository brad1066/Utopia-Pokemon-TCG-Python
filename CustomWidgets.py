from tkinter import *
from tkinter import ttk
import sys
import os

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.vscrollbar = Scrollbar(self, orient=VERTICAL, elementborderwidth=0)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=False)
        
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self.vscrollbar.set, height=0, width=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.vscrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.body = body = Frame(self.canvas)
        body_id = self.canvas.create_window(0, 0, window=body, anchor=NW)
        
        def _configBody(event):
            size = (body.winfo_reqwidth(), body.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if body.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width=body.winfo_reqwidth())

        def _configcanvas(event):
            if body.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.itemconfigure(body_id, width=self.canvas.winfo_width())

        def On_MouseWheel(event):
            if self.focus:
                self.canvas.yview_scroll(int(-1*(event.delta/100)), "units") 
                
        self.body.bind('<Configure>', _configBody)
        self.canvas.bind('<Configure>', _configcanvas)
        self.canvas.bind_all("<MouseWheel>", On_MouseWheel)

    def clearWidgets(self):
        for widget in self.body.winfo_children():
            if widget != self.body or widget != self.canvas or widget != self.vscrollbar:
                widget.destroy()

class ttkButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None, text=None, command=None, style="ttkButton.TFrame"):
        ttk.Frame.__init__(self, parent, height=height, width=width, style=style)

        self.pack_propagate(0)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=BOTH, expand=1)

class PopUp(Menu):
    def __init__(self, parent, x, y, *args, **kwargs):
        Menu.__init__(self, parent, tearoff=0)

        self.parent = parent
        self.tk = parent.tk
        self.xPos = x
        self.yPos = y

    def show(self):
        self.post(self.xPos, self.yPos)














        
        
