from tkinter import *
from tkinter import ttk, messagebox
from CustomWidgets import *

import os
import sys

from pprint import pprint
import json

class AddItemTool(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.controller = controller
        self.menus = {}
        
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        self.detailsEntryFrame = DetailsEntryFrame(self.container, self)

        self.detailsEntryFrame.pack(side=TOP, fill=BOTH, expand=True)
        
        self.bind_all("<Control-w>", self.close)
        self.title("Utopia - Add Item")
        # self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        self.genMenu()
        self.resizable(width=False, height=False)
        
        self.bind("<Destroy>", self._destroy)

    def fullscreen(self):
        self.lift()
        self.state("zoomed")

    def close(self, event=None):
        if messagebox.askyesno("Close", "Do you really want to close this application"):
            self.destroy()

    def genMenu(self):
        self.mainMenu = Menu(self)
        
        self.controller.makeMenusItem(self.mainMenu, {}, {}, self.menus)
        
        self.controller.generateMenuBar(self, self.mainMenu, self.menus)

    def _destroy(self, event=None):
        self.controller.remove(self)

class DetailsEntryFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=3)

        self.nameEntryVar = StringVar(self, "")
        self.itemTypeOptionVar = StringVar(self, "-- Please Select One --")
        self.itemTypeOptions = [Type for Type in self.controller.controller.data.get("Item Types")]
        self.setOptionVar = StringVar(self, "-- Please Select One --")
        self.setOptions = [Set for Set in self.controller.controller.data.get("Sets")]
        self.setNumberVar = IntVar(self, 0)
        self.rarityRatingOptionVar = StringVar(self, "-- Please Select One --")
        self.rarityRatingOptions = [rarity for rarity in self.controller.controller.data.get("Rarities")]
        self.priceRankingOptionVar = StringVar(self, "-- Please Select One --")
        self.priceRankings = [rarity for rarity in self.controller.controller.data.get("Price Rankings")]
        self.priceEntryVar = StringVar(self, "0.00")
        self.quantityEntryVar = StringVar(self, "1")

        self.nameLabel = Label(self, text="Name: ")
        self.nameEntry = Entry(self, textvariable=self.nameEntryVar)
        self.itemTypeLabel = Label(self, text="Item Type:")
        self.itemTypeOptionMenu = OptionMenu(self, self.itemTypeOptionVar, *self.itemTypeOptions, command=self.updateType)
        self.setLabel = Label(self, text="Set:")
        self.setOptionMenu = OptionMenu(self, self.setOptionVar, *self.setOptions, command=self.updateSeries)
        self.setNumberLabel = Label(self, text="Number:")
        self.setNumberEntry = Entry(self, textvariable=self.setNumberVar)
        self.rarityLabel = Label(self, text="Rarity")
        self.rarityOptionMenu = OptionMenu(self, self.rarityRatingOptionVar, *self.rarityRatingOptions, command=self.updatePriceRankings)
        self.priceRankingLabel = Label(self, text="Price Ranking")
        self.priceRankingOptionMenu = OptionMenu(self, self.priceRankingOptionVar, *self.priceRankings, command=self.updatePrice)
        self.priceLabel = Label(self, text="Price:")
        self.priceEntry = Entry(self, textvariable=self.priceEntryVar)
        self.quantityLabel = Label(self, text="Quantity")
        self.quantityEntry = Entry(self, textvariable=self.quantityEntryVar)
        self.addButton = Button(self, text="Add", command=self.addRecord)

        self.nameLabel.grid(row=0, column=0, sticky=NSEW)
        self.nameEntry.grid(row=0, column=1, sticky=NSEW)
        self.itemTypeLabel.grid(row=1, column=0, sticky=NSEW)
        self.itemTypeOptionMenu.grid(row=1, column=1, sticky=NSEW)
        self.setLabel.grid(row=2, column=0, sticky=NSEW)
        self.setOptionMenu.grid(row=2, column=1, sticky=NSEW)
        self.setNumberLabel.grid(row=3, column=0, sticky=NSEW)
        self.setNumberEntry.grid(row=3, column=1, sticky=NSEW)
        self.rarityLabel.grid(row=4, column=0, sticky=NSEW)
        self.rarityOptionMenu.grid(row=4, column=1, sticky=NSEW)
        self.priceRankingLabel.grid(row=5, column=0, sticky=NSEW)
        self.priceRankingOptionMenu.grid(row=5, column=1, sticky=NSEW)
        self.priceLabel.grid(row=6, column=0, sticky=NSEW)
        self.priceEntry.grid(row=6, column=1, sticky=NSEW)
        self.quantityLabel.grid(row=7, column=0, sticky=NSEW)
        self.quantityEntry.grid(row=7, column=1, sticky=NSEW)
        self.addButton.grid(row=8, column=0, columnspan=2, sticky=NSEW)

        self.addButton.bind("<Button-1>", self.addRecord)

    def updatePriceRankings(self, event=None):
        if self.rarityRatingOptionVar.get() not in self.priceRankings:
            self.priceRankingOptionVar.set("Other")
            self.priceRankingOptionMenu.config(state=DISABLED)
            self.updatePrice()
        else:
            self.priceRankingOptionVar.set(self.rarityRatingOptionVar.get())
            self.priceRankingOptionMenu.config(state=NORMAL)
            self.updatePrice()

    def updatePrice(self, event=None):
        if self.priceRankingOptionVar.get() != "Other":
            self.priceEntry.delete(0, END)
            self.priceEntry.insert(0, self.controller.controller.data.get\
                                   ("Price Rankings").get(self.priceRankingOptionVar.get()))
            self.priceEntryVar.set(self.controller.controller.data.get\
                                   ("Price Rankings").get(self.priceRankingOptionVar.get()))
            self.priceEntry.config(state=DISABLED)
        else:
            self.priceEntry.config(state=NORMAL)

    def addRecord(self, event=None):
        print("Saving...")
        data = {}
        data["Name"] = self.nameEntryVar.get()
        data["Rarity"] = self.rarityRatingOptionVar.get()
        data["Price Ranking"] = self.priceRankingOptionVar.get()
        data["Price"] = "\u00a3"+self.priceEntryVar.get().replace("\u00a3", "")
        data["Quantity"] = self.quantityEntryVar.get()
        data["Type"] = self.itemTypeOptionVar.get()
        data["Set"] = self.setOptionVar.get()
        data["Number"] = int(self.setNumberVar.get())

        self.controller.controller.data["Stock"].append(data)

        pprint(self.controller.controller.data["Stock"])

        self.controller.controller.saveData()

        messagebox.showinfo("Saved", "The data has been added to the stock list")

    def updateSeries(self, event):
        print("Updating Series")
        print(event)
        series = self.setOptionVar.get()
        popUp = PopUp(self, x=self.setOptionMenu.winfo_rootx(), y=self.setOptionMenu.winfo_rooty()+self.setOptionMenu.winfo_height())

        for _set in self.controller.controller.data["Sets"][series]:
            popUp.add_command(label=_set, command=lambda _set=_set: self.setOptionVar.set(_set))
##            print("\t\t"+_set)
        popUp.show()

    def updateType(self, event=None):
        print(self.itemTypeOptionVar.get())
        return

if __name__ == "__main__":
    import main
    app = main.App()
    app.openWindow("AddItemTool")






















