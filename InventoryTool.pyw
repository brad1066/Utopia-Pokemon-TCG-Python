from tkinter import *
from tkinter import ttk, messagebox

import os
import sys

from pprint import pprint
import json
from operator import itemgetter

from CustomWidgets import *

class InventoryTool(Tk):
    def __init__(self, controller=None, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.controller = controller
        self.menus = {}
        
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        
        self.searchFrame = SearchFrame(self.container, self)
        self.detailsFrame = DetailsFrame(self.container, self)
        
        self.searchFrame.grid(row=0, column=0, sticky=NSEW)
        self.detailsFrame.grid(row=0, column=1, sticky=NSEW)
        
        #self.fullscreen()
        self.title("Utopia - Inventory")
        self.iconbitmap("{0}\\Images\\utopia_ico.ico".format(os.getcwd()))
        self.genMenu()
        self.resizable(width=True, height=True)
         
        self.bind("<Destroy>", self._destroy)

        self.searchFilters = {"Sets": set(),
                              "Types": set()}
        
    def fullscreen(self):
        self.lift()
        self.state("zoomed")
            
    def genMenu(self):
        self.mainMenu = Menu(self)
        self.fileMenu = Menu(self.mainMenu, tearoff=0)
        self.searchFiltersMenu = Menu(self.mainMenu, tearoff=0)
        self.setFilterMenu = Menu(self.searchFiltersMenu, tearoff=0)
        self.typeFilterMenu = Menu(self.searchFiltersMenu, tearoff=0)

        for gen, sets in self.controller.data["Sets"].items():
            setMenu = Menu(self.searchFiltersMenu, tearoff=0)
            for _set in sets:
                setMenu.add_command(label=_set, command=lambda _set=_set: self.addSetSearchFilter(_set))

            self.setFilterMenu.add_cascade(label=gen, menu=setMenu)

        for _type in self.controller.data["Item Types"]:
            self.typeFilterMenu.add_command(label=_type, command=lambda _type=_type: self.addTypeSearchFilter(_type))
        
        self.controller.makeMenusItem(self.mainMenu,
                                      {"File": self.fileMenu,
                                       "Filter": self.searchFiltersMenu},
                                      {"Checkout": lambda: self.controller.openWindow("SalesTool"),
                                       "Notes": lambda: self.controller.openWindow("NotesTool")},
                                      self.menus)
        
        self.controller.makeMenusItem(self.fileMenu,
                                      {},
                                      {"Open Item": lambda: self.controller.openWindow("EditItemTool"),
                                       "Add Item(s)": lambda: self.controller.openWindow("AddItemTool")},
                                      self.menus)
        
        self.controller.makeMenusItem(self.searchFiltersMenu,
                                      {"Set": self.setFilterMenu,
                                       "Type": self.typeFilterMenu},
                                      {"Clear Filter": self.clearSearchFilters},
                                      self.menus)
        
        self.controller.generateMenuBar(master=self, menuBar=self.mainMenu, menus=self.menus)

        self.searchFiltersMenu.add_separator()
            
    def _destroy(self, event=None):
        self.controller.remove(self)

    def addSetSearchFilter(self, _filter=None, event=None):
        if _filter not in self.searchFilters["Sets"]:
            self.searchFilters["Sets"].add(_filter)
            index = self.searchFilters["Sets"].__len__()-1
            self.searchFiltersMenu.add_command(label = "Set: "+_filter,
                                               command = lambda _filter=_filter,
                                                                index=index: self.removeFilter("Sets",
                                                                                               _filter,
                                                                                               index))

    def addTypeSearchFilter(self, _filter=None, event=None):
        if _filter not in self.searchFilters["Types"]:
            self.searchFilters["Types"].add(_filter)
            index = self.searchFilters["Types"].__len__()-1
            self.searchFiltersMenu.add_command(label = "Type: "+_filter,
                                               command = lambda _filter=_filter,
                                                                index=index: self.removeFilter("Types",
                                                                                               _filter,
                                                                                               index))
    def clearSearchFilters(self, event=None):
        self.searchFiltersMenu.delete(4, END)
        self.searchFilters["Sets"].clear()
        self.searchFilters["Types"].clear()

    def removeFilter(self, _type, _filter, index):
        self.searchFilters[_type].remove(_filter)
        self.searchFiltersMenu.delete(self.searchFiltersMenu.index("{0}: {1}".format(_type.replace("s", ""), _filter)))
        
class SearchFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        
        self.searchValue = StringVar()
        self.searchEntry = Entry(self, textvariable=self.searchValue)
        self.searchButton = Button(self, text="Search", command=self.search)
        self.searchResultsFrame = VerticalScrolledFrame(self)
        
        self.searchResults = {}
        
        self.searchEntry.grid(row=0, column=0, sticky=EW)
        self.searchButton.grid(row=0, column=1, sticky=EW)
        self.searchResultsFrame.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        
        self.body = self.searchResultsFrame.body
        
        self.searchEntry.bind("<Return>", self.search)
        
    def search(self, event=None):
        self.searchResults = []
        
        search = self.searchValue.get()
        
        for pokemon in self.controller.controller.data.get("Stock"):
                #pprint("Adding result to list")
            if len(self.controller.searchFilters["Sets"]) != 0:
                if pokemon.get("Set") not in self.controller.searchFilters["Sets"]:
                    continue
                
            if len(self.controller.searchFilters["Types"]) != 0:
                if pokemon.get("Type") not in self.controller.searchFilters["Types"]:
                    continue
            
            if search in pokemon.get("Name"):
                self.searchResults.append(pokemon)

        self.showResults()
        
    def showResults(self):
        self.searchResultsFrame.clearWidgets()
        for result in sorted(self.searchResults, key=itemgetter("Name")):
            tmpButton = SearchResult(self.body, self.controller, result=result)
            tmpButton.pack(side=TOP, fill=BOTH, expand=True)
            #pprint(result)
            
    def updateSelectedRecord(self, record):
        self.controller.controller.currentRecord = record
        
class SearchResult(Frame):
    def __init__(self, parent, controller, result=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        self.controller = controller
        self.result = result
        
        self.button = Button(self, text=self.result["Name"], height=3, command=self.update)
        
        self.button.pack(side=TOP, expand=True, fill=BOTH)
        
    def update(self, event=None):
        self.controller.controller.currentRecord = self.result
        self.controller.detailsFrame.update()
        
class DetailsFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        
        self.priceVar = StringVar()
        try: self.quantityRange = range(1, int(self.controller.controller.currentRecord.get("Quantity"))+1)
        except: self.quantityRange = []
        
        
        self.nameLabel = Label(self, text="Name:")
        self.nameVarLabel = Label(self, bg="white")
        self.priceLabel = Label(self, text="Price:")
        self.priceVarEntry = Entry(self, relief=FLAT, textvariable=self.priceVar)
        self.rarityLabel = Label(self, text="Rarity")
        self.rarityVarLabel = Label(self, bg="white")
        self.setLabel = Label(self, text="Set")
        self.setVarLabel = Label(self, bg="white")
        self.quantityLabel = Label(self, text="Quantity")
        self.quantitySpinbox = Spinbox(self, values=[i for i in self.quantityRange], command=self.updatePrice)
        
        self.nameLabel.grid(row=0, column=0, sticky=EW, padx=2.5, pady=5)
        self.nameVarLabel.grid(row=0, column=1, sticky=EW, padx=2.5, pady=5)
        self.priceLabel.grid(row=1, column=0, sticky=EW, padx=2.5, pady=5)
        self.priceVarEntry.grid(row=1, column=1, sticky=EW, padx=2.5, pady=5)
        self.rarityLabel.grid(row=2, column=0, sticky=EW, padx=2.5, pady=5)
        self.rarityVarLabel.grid(row=2, column=1, sticky=EW, padx=2.5, pady=5)
        self.setLabel.grid(row=3, column=0, sticky=EW, padx=2.5, pady=5)
        self.setVarLabel.grid(row=3, column=1, sticky=EW, padx=2.5, pady=5)
        self.quantityLabel.grid(row=4, column=0, sticky=EW, padx=2.5, pady=5)
        self.quantitySpinbox.grid(row=4, column=1, sticky=EW, padx=2.5, pady=5)

        Label(self, text="Notes:").grid(row=7, column=0, sticky=W, padx=2.5)
        self.notesText = Text(self, height=10, width=25)
        self.notesText.grid(row=8, column=0, columnspan=2, sticky=NSEW, padx=2.5, pady=5)
        
        self.addToBasketButton = Button(self, text="Add To Basket", command=self.addToBasket, height=2)
        self.addToBasketButton.grid(row=9, column=0, columnspan=2, sticky=NSEW, padx=2.5, pady=5)

    def updatePrice(self, event=None):
        data = self.controller.controller.currentRecord
        self.priceVar.set("£{0:.2f}".format(float(float(data["Price"].replace("£", ""))*int(self.quantitySpinbox.get()))))
        print(self.priceVar.get())

    def update(self, event=None):
        data = self.controller.controller.currentRecord
        #pprint(data)
        self.nameVarLabel.config(text=data["Name"])
        self.priceVar.set(data["Price"])
        self.rarityVarLabel.config(text=data["Rarity"])
        self.setVarLabel.config(text=data["Set"])
        try: self.quantityRange = range(1, int(self.controller.controller.currentRecord.get("Quantity"))+1)
        except: self.quantityRange = []
        self.quantitySpinbox = Spinbox(self, values=[i for i in self.quantityRange], command=self.updatePrice)
        self.quantitySpinbox.grid(row=4, column=1, sticky=EW, padx=2.5, pady=5)

        self.notesText.delete(0.0, END)
        
        
    def addToBasket(self, event=None):
        if self.controller.controller.currentRecord != {}:
            for item in self.controller.controller.saleItems:
                if item["Name"] == self.controller.controller.currentRecord.get("Name"):
                    self.controller.controller.saleItems.remove(item)
                    record = self.controller.controller.currentRecord.copy()
                    record["Quantity"] = int(self.quantitySpinbox.get())
                    record["Notes"] = self.notesText.get(0.0, END)
                    price = float(record["Price"].replace("£", ""))*record["Quantity"]
                    record["Price"] = "£{0:.2f}".format(price)
                    self.controller.controller.saleItems.append(record)
                    messagebox.showinfo("Basket Update", "Added {0} x {1} to the basket".format(record["Name"], record["Quantity"]))  
                    return
                
            record = self.controller.controller.currentRecord.copy()
            record["Quantity"] = int(self.quantitySpinbox.get())
            record["Notes"] = self.notesText.get(0.0, END)
            price = float(record["Price"].replace("£", ""))*record["Quantity"]
            record["Price"] = "£{0:.2f}".format(price)
            self.controller.controller.saleItems.append(record)
            messagebox.showinfo("Basket Update", "Added {0} x {1} to the basket".format(record["Name"], record["Quantity"])) 
                
        try:
            saleToolCode = self.controller.controller.lookup.get("SalesTool")
            self.controller.controller.currentWindows[saleToolCode].update()
            
        except: None


if __name__ == "__main__":
    import main
    app = main.App()
    app.openWindow("InventoryTool")




















        

        
