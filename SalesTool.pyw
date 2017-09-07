from tkinter import *
from tkinter import ttk, messagebox

import os
import sys

from pprint import pprint
import json
from operator import itemgetter

from CustomWidgets import *

class SalesTool(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.controller = controller
        self.menus = {}
        
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=2)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=2)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True)

        self.detailsFrame = DetailsFrame(self.container, self)
        self.actionsFrame = ActionsFrame(self.container, self, bg="white")
        self.itemsFrame = ItemsFrame(self.container, self)

        self.detailsFrame.grid(row=0, column=0, rowspan=3, sticky=NSEW, padx=10, pady=10)
        self.actionsFrame.grid(row=0, column=1, sticky=NSEW)
        Label(self.container, text="Basket:", height=3).grid(row=1, column=1)
        self.itemsFrame.grid(row=2, column=1, sticky=NSEW)
        #self.fullscreen()
        self.title("Utopia - Sales Tool")
        self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        self.genMenu()
        self.bind("<Destroy>", self._destroy)

    def fullscreen(self):
        self.lift()
        self.state("zoomed")

    def genMenu(self):
        self.mainMenu = Menu(self)

        self.controller.makeMenusItem(self.mainMenu,
                                      {},
                                      {"Notes": lambda: self.controller.openWindow("NotesTool")},
                                      self.menus)
        
        self.controller.generateMenuBar(master=self, menuBar=self.mainMenu, menus=self.menus)

    def _destroy(self, event=None):
        self.controller.remove(self)

    def update(self):
        self.itemsFrame.update()
        
class DetailsFrame(Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        
        self.record = {}

        self.nameVar = StringVar()
        self.priceVar = StringVar()
        self.rarityVar = StringVar()
        self.quantityVar = StringVar()

        self.nameLabel = Label(self, text="Name:")
        self.nameVarEntry = Entry(self, textvariable=self.nameVar, state=DISABLED)
        self.priceLabel = Label(self, text="Price:")
        self.priceVarEntry = Entry(self, textvariable=self.priceVar, state=DISABLED)
        self.rarityLabel = Label(self, text="Rarity:")
        self.rarityVarEntry = Entry(self, textvariable=self.rarityVar, state=DISABLED)
        self.quantityLabel = Label(self, text="Quantity:")
        self.quantityVarEntry = Entry(self, textvariable=self.quantityVar, state=DISABLED)
        self.notesText = Text(self, height=10, width=50)

        self.nameLabel.grid(row=0, column=0, sticky=EW)
        self.nameVarEntry.grid(row=0, column=1, sticky=EW)
        self.priceLabel.grid(row=1, column=0, sticky=EW)
        self.priceVarEntry.grid(row=1, column=1, sticky=EW)
        self.rarityLabel.grid(row=2, column=0, sticky=EW)
        self.rarityVarEntry.grid(row=2, column=1, sticky=EW)
        self.quantityLabel.grid(row=3, column=0, sticky=EW)
        self.quantityVarEntry.grid(row=3, column=1, sticky=EW)
        self.notesText.grid(row=4, column=0, columnspan=2, sticky=NSEW)

    def update(self, record):
        self.record = record
        #pprint(record)

        self.nameVarEntry.config(state=NORMAL)
        self.priceVarEntry.config(state=NORMAL)
        self.rarityVarEntry.config(state=NORMAL)
        self.quantityVarEntry.config(state=NORMAL)
        
        self.nameVar.set((record.get("Name") or ""))
        self.nameVarEntry.delete(0, END)
        self.nameVarEntry.insert(0, (record.get("Name") or ""))

        self.priceVar.set((record.get("Price") or ""))
        self.priceVarEntry.delete(0, END)
        self.priceVarEntry.insert(0, (record.get("Price") or ""))

        self.rarityVar.set((record.get("Rarity") or ""))
        self.rarityVarEntry.delete(0, END)
        self.rarityVarEntry.insert(0, (record.get("Rarity") or ""))

        self.quantityVar.set((record.get("Quantity") or ""))
        self.quantityVarEntry.delete(0, END)
        self.quantityVarEntry.insert(0, (record.get("Quantity") or ""))

        self.notesText.delete(0.0, END)
        self.notesText.insert(END, (record.get("Notes") or ""))

        self.nameVarEntry.config(state=DISABLED)
        self.priceVarEntry.config(state=DISABLED)
        self.rarityVarEntry.config(state=DISABLED)
        self.quantityVarEntry.config(state=DISABLED)

class ActionsFrame(Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.confirmTransactionButton = Button(self, text="Complete Sale", command=self.confirmTransaction)
        self.clearBasketButton = Button(self, text="Clear Basket", command=self.clearBasket)

        self.confirmTransactionButton.grid(row=0, column=0, sticky=NSEW)
        self.clearBasketButton.grid(row=0, column=1, sticky=NSEW)

    def confirmTransaction(self, event=None):
        self.confirmer = SaleConfirmationDialog(controller=self.controller.controller)
        
    def clearBasket(self, event=None):
        self.controller.controller.clearBasket()
        self.controller.itemsFrame.update()
        self.controller.detailsFrame.update(record={})

class ItemsFrame(VerticalScrolledFrame):
    def __init__(self, parent, controller, *args, **kwargs):
        VerticalScrolledFrame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller

        self.update()

    def update(self):

        self.clearWidgets()
        
        for item in sorted(self.controller.controller.saleItems, key=itemgetter("Name")):
            itemButton = ItemButton(self.body, self.controller, record=item)
            itemButton.pack(side=TOP, fill=BOTH, expand=True)

class ItemButton(Frame):
    def __init__(self, parent, controller, record={}, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.controller = controller
        self.record = record

        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.nameButton = Button(self, text=self.record.get("Name"), height=2, command=self.updateDetailsFrame)

        self.nameButton.grid(row=0, column=0, sticky=NSEW)
        self.nameButton.bind("<Button-3>", self.popUp)

    def updateDetailsFrame(self, event=None):
        self.controller.detailsFrame.update(record=self.record)

    def popUp(self, event=None):
        self.popUp = PopUp(self, x=event.x_root, y=event.y_root)

        self.popUp.add_command(label="Remove Item", command=self.removeItem)
        self.popUp.add_command(label="Edit Item", command=self.editItem)

        self.popUp.show()

    def removeItem(self):
        print("Remove this item")
        self.destroy()

        for i in range(len(self.controller.controller.saleItems)):
            if self.record == self.controller.controller.saleItems[i]:
                self.controller.controller.saleItems.pop(i)
                break
        
        pprint(self.controller.controller.saleItems)

    def editItem(self):
        print("Edit this item")
        
        
class SaleConfirmationDialog(Tk):
    """Used to provide a confirmation dialog to confirm the items in the order,
       so as to make sure that the order is correct"""
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        self.mainFrame = Frame(self)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.title("Confirm Sale")
        self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        
        items = self.controller.saleItems
        price = 0.0
        self.sellerEntryVar = StringVar(self, "Ryan Crellin")
        self.clientEntryVar = StringVar(self, "Anonymous")
        
        for item in items: price += float(item.get("Price").replace("£", "").replace(" ", ""))

        self.finalDetailsFrame = Frame(self.mainFrame)
        self.finalDetailsFrame.grid_rowconfigure(0, weight=1)
        self.finalDetailsFrame.grid_rowconfigure(1, weight=1)
        self.finalDetailsFrame.grid_rowconfigure(2, weight=1)
        self.finalDetailsFrame.grid_rowconfigure(3, weight=1)
        self.finalDetailsFrame.grid_columnconfigure(0, weight=1)
        self.finalDetailsFrame.grid_columnconfigure(1, weight=2)
        self.finalDetailsFrame.grid(row=1, column=0)
        
        self.itemsFrame = ItemsFrame(self.mainFrame, self)
        self.detailsFrame = DetailsFrame(self.mainFrame, self)
        
        self.sellerLabel = Label(self.finalDetailsFrame, text="Vendor")
        self.sellerEntry = Entry(self.finalDetailsFrame, textvariable=self.sellerEntryVar)
        self.clientLabel = Label(self.finalDetailsFrame, text="Client")
        self.clientEntry = Entry(self.finalDetailsFrame, textvariable=self.clientEntryVar)
        self.priceLabel = Label(self.finalDetailsFrame, text="Price:")
        self.priceVarLabel = Label(self.finalDetailsFrame, text="£{0:.2f}".format(price))
        self.finalizeButton = Button(self.finalDetailsFrame, text="Finalize", command=self.finalize)

        self.itemsFrame.grid(row=0, column=0, sticky=NSEW)
        self.detailsFrame.grid(row=0, column=1, sticky=NSEW)

        self.sellerLabel.grid(row=0, column=0, sticky=NSEW)
        self.sellerEntry.grid(row=0, column=1, sticky=NSEW)
        self.clientLabel.grid(row=1, column=0, sticky=NSEW)
        self.clientEntry.grid(row=1, column=1, sticky=NSEW)
        self.priceLabel.grid(row=2, column=0, sticky=NSEW)
        self.priceVarLabel.grid(row=2, column=1, sticky=NSEW)
        self.finalizeButton.grid(row=3, column=0, columnspan=2, sticky=NSEW)


    def finalize(self):
        print("Completing the transaction")
        self.controller.seller = self.sellerEntryVar.get()
        self.controller.client = self.clientEntryVar.get()
        self.controller.makeSale()
        self.destroy()
        
if __name__ == "__main__":
    import main
    app = main.App()
    app.openWindow("SalesTool")








        



