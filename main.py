from tkinter import *
from tkinter import ttk, messagebox
from CustomWidgets import *

from SalesTool import SalesTool
from AddItemTool import AddItemTool
from InventoryTool import InventoryTool
from NotesTool import NotesTool
from EditItemTool import EditItemTool

import os
import sys
from pprint import pprint
import json
import atexit
import time

class App():
    def __init__(self):
        with open("data.json", "r", encoding="utf-8") as jsonf:
            self.data = json.load(jsonf)

        self.currentRecord = {}
        self.saleItems = []
        self.currentWindows = {}
        
        self.lookup = {"InventoryTool": InventoryTool,
                       "AddItemTool": AddItemTool,
                       "EditItemTool": EditItemTool,
                       "SalesTool": SalesTool,
                       "NotesTool": NotesTool}

        self.seller = "Ryan Crellin"
        self.client = "Anonymous"

    def makeMenusItem(self, parent, cascades, commands, menus):
        menus[parent] = {"cascades": cascades,
                         "commands": commands}

    def generateMenuBar(self, master, menuBar, menus):
        for menu, currMenu in menus.items():
            for addType, values in currMenu.items():
                if addType == "cascades":
                    for label, extendMenu in values.items():
                        menu.add_cascade(label=label, menu=extendMenu)
                    
                elif addType == "commands":
                    try:
                        for label, command in values.items():
                            menu.add_command(label=label, command=command)
                            
                    except: pass
                    
        master.config(menu=menuBar)

    def remove(self, obj):
        for window in self.currentWindows:
            if self.currentWindows[window] == obj:
                self.currentWindows.pop(window)
                print("Closed window")
                break
        if len(self.currentWindows) == 0: sys.exit()
            
    def openWindow(self, name):
        if self.lookup.get(name) not in self.currentWindows:
            self.currentWindows[self.lookup.get(name)] = self.lookup.get(name)(controller=self)
            self.currentWindows[self.lookup.get(name)].lift()
            self.currentWindows[self.lookup.get(name)].focus()
            self.currentWindows[self.lookup.get(name)].mainloop()

        else:
            self.currentWindows[self.lookup.get(name)].lift()
            self.currentWindows[self.lookup.get(name)].focus()

    def saveData(self):
        with open("data.json", "w", encoding="utf-8") as jsonf:
            json.dump(self.data, jsonf)

    def clearBasket(self):
        self.saleItems.clear()

    def makeSale(self):
        items = self.saleItems
        price = float()

        seller = self.seller
        client = self.client

        try: self.currentWindows.get("InventoryTool").detailsFrame.update()
        except: pass

        saleString = time.strftime("%H:%M:%S; %d/%m/%Y; ")
        saleString += client+"; "
        saleString += seller+"; "
        
        for item in items:
            price += float(item.get("Price").replace("£", "").replace(" ", ""))

        saleString += "{0:.2f}; ".format(price)
        
        receiptString = time.strftime("Time: %H:%M:%S\n")
        receiptString += time.strftime("Date: %d/%m/%Y\n")
        receiptString += "Client: {0}\n".format(client)
        receiptString += "Seller: {0}\n".format(seller)
        receiptString += "Price: {0:.2f}\n".format(price)
        receiptString += "Sale Items:\n\t"
        
        for item in items:
            receiptString += "{0} {1} x{2} @{3:.2f}\n\t".format(item.get("Name").replace(" ", ""),
                                                                item.get("Type").replace(" ", ""),
                                                                item.get("Quantity"),
                                                                float(item.get("Price").replace("£", "").replace(" ", ""))/int(item.get("Quantity")))
            
            saleString += "{0} {1} x{2} @{3:.2f}; ".format(item.get("Name").replace(" ", ""),
                                                           item.get("Type").replace(" ", ""),
                                                           item.get("Quantity"),
                                                           float(item.get("Price").replace("£", "").replace(" ", ""))/int(item.get("Quantity")))

        
        
        print(saleString)
        print(receiptString)

        with open("Sales.txt", "a") as f:
            f.write(saleString+"\n")

        with open(time.strftime("{0}\\Receipts\\%d-%m-%Y_%H-%M-%S.txt".format(os.getcwd())), 'w') as f:
            f.write(receiptString)

        self.updateStock()

    def updateStock(self):

        items = self.saleItems

        for item in self.data["Stock"]:
            for saleItem in items:
                if saleItem.get("Name") == item.get("Name"):
                    if saleItem.get("Rarity") == item.get("Rarity"):
                        if saleItem.get("Number") == item.get("Number"):
                            print("{0:<20} ==> {1:>20}".format(item["Quantity"], saleItem["Quantity"]))
                            item["Quantity"] = int(item["Quantity"])-int(saleItem["Quantity"])
                            if item["Quantity"] <= 0:
                                self.data["Stock"].remove(item)
                            else: continue
                        
##        pprint(self.data["Stock"])

        self.saleItems.clear()
        self.saveData()
        
        
app = App()
atexit.register(app.saveData)

if __name__ == "__main__":
    
    app = App()
##    atexit.register(app.saveData)
    app.openWindow("InventoryTool")
    
    

#https://code.activestate.com/pypm/decovent/

#Receipt Format: %d-%m-%Y_%H-%M-%S
