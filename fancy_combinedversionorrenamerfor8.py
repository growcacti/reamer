import tkinter as tk
from tkinter import Toplevel,filedialog, messagebox
from tkinter import ttk, Menu
import os
import sys
import re
import string
import time
import random

#CONSTANTS
MAX_NAME_LEN = 255
from ct9 import *

class FileExplorer:
    def __init__(self, master, path, on_directory_selected=None):
        self.master = master
        self.path = path
        self.nodes = {}  # Tracks the nodes that have been expanded.
        self.entry_frame = tk.Frame(self.master, width=100)
        self.entry_frame.grid(row=0, column=0,columnspan=4)
        self.frm1 = ttk.Frame(self.master)
        self.frm1.grid(row=1, column=0, rowspan=4,columnspan=10,sticky="ns")
        self.canvas = tk.Canvas(self.frm1,width=50,bg="seashell2")
        self.canvas.grid(row=2, column=0)
        self.frm2 = ttk.Frame(self.master)
        self.frm2.grid(row=1, column=4, sticky="ns")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(4, weight=1)
        self.rename_history = []
        self.rename_selection = []
        self.path_history=[]
        self.count = 0
        # Path display and editing
        self.path_entry = tk.Entry(self.entry_frame, bd=8, bg="azure", width=155)
        self.path_entry.grid(row=0, column=0,columnspan=2, sticky="ew")
        self.path_entry.insert(0, self.path)
        self.path_entry.bind('<Return>', self.on_path_entry_return)
        
        # Treeview for navigating directories
        self.dir_nav = ttk.Treeview(self.frm1, selectmode="browse")
        self.dir_nav.heading("#0", text="Directory Browser", anchor="w")
        self.dir_nav.column("#0", width=300, stretch=True)

        # Scrollbars for the Treeview
        ysb = ttk.Scrollbar(self.frm1, orient="vertical", command=self.dir_nav.yview)
        xsb = ttk.Scrollbar(self.frm1, orient="horizontal", command=self.dir_nav.xview)
       
        self.dir_nav.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.dir_nav.grid(row=1, column=0,rowspan=4,columnspan=2, sticky="nsew")
        ysb.grid(row=1, column=3, sticky="ns")
        xsb.grid(row=20, column=0, sticky="ew")

        self.dir_nav.bind("<<TreeviewOpen>>", self.on_treeview_open)       
        self.can=tk.Canvas(self.frm1, bg="alice blue", width=180, height=70)
        self.can.grid(row=2, column=4,columnspan=8)
        tk.Label(self.can, text="Original Filenames").grid(row=3,column=1)
        tk.Label(self.can, text="Preview New Filenames").grid(row=3,column=6)
        self.lb1 = tk.Listbox(self.can,bd=10,width=50, height=25,selectmode=tk.MULTIPLE)
        self.lb1.grid(row=4, column=1,rowspan=2,columnspan=2)
        self.lb2 = tk.Listbox(self.can,bd=10,width=50, height=25,selectmode=tk.MULTIPLE)
        self.lb2.grid(row=4, column=6,rowspan=2,columnspan=3)
        self.switch=1
        self.yscrollbar = tk.Scrollbar(self.can)
        self.yscrollbar.grid(row=4,column=10)
        self.xscrollbar = tk.Scrollbar(self.can,orient="horizontal")
        self.xscrollbar.grid(row=2,column=1)
        self.yscrollbar.config(command=self.lb1.yview)
        self.xscrollbar.config(command=self.lb1.xview)
        self.lb1.config(bg="light yellow", yscrollcommand=self.yscrollbar.set)
        self.lb1.config(bg="wheat", xscrollcommand=self.xscrollbar.set)       
        self.lb1.bind("<MouseWheel>", lambda event: self.yscrolllistbox(event, self.lb2))
        self.lb2.bind("<MouseWheel>", lambda event: self.yscrolllistbox(event, self.lb1))
        self.xscrollbar2= ttk.Scrollbar(self.can, orient="horizontal", command=self.lb2.xview)
        self.xscrollbar2.grid(row=2,column=6)
      
        self.esync=tk.Entry(self.can,bd=7,bg="lavender",width=40)
        self.esync.grid(row=19,column=2)
        self.syncbt =  tk.Button(self.can, text= "Sync/Independent Scroll",bd=4, bg="light blue", command=self.do_switch)
        self.syncbt.grid(row=19,column=1)
        self.info_bar = InfoBar(self.master,self)
        self.initialize_treeview(self.path)
        self.bind_entries()
      


    def bind_entries(self):
        # Existing bindings
        self.dir_nav.bind("<<TreeviewOpen>>", self.on_directory_expand)
        self.dir_nav.bind("<<TreeviewSelect>>", self.on_selection_change)
        self.lb1.bind('<Double-1>', self.store_selections) 




    def sync(self):
              
        self.lb2.config(bg="seashell", yscrollcommand=self.yscrollbar.set)
        self.lb1.config(bg="seashell", yscrollcommand=self.yscrollbar.set)

    def nosync(self):
       
        self.yscrollbar2= ttk.Scrollbar(self.can, orient="vertical", command=self.lb2.yview)
        self.yscrollbar2.grid(row=4,column=10)
        self.lb1.config(bg="snow")  
          
    def on_path_entry_return(self, event=None):
        self.path = self.path_entry.get()
        print(self.path)
        self.initialize_treeview(self.path)

    def initialize_treeview(self, path):
        self.path = path
        self.dir_nav.delete(*self.dir_nav.get_children())  # Clear existing tree
        if os.path.isdir(self.path):
            self.insert_node("", self.path, self.path)
            self.dir_nav.item(self.path, open=True)  # Optionally open the root node
            self.path_entry.insert(0, self.path)
            self.path_history.append(self.path)
            self.lb1.delete(0, tk.END)
            self.lb2.delete(0, tk.END)
            for file in os.listdir(self.path):
                self.lb1.insert(tk.END, file)
                self.lb2.insert(tk.END, file)

    def insert_node(self, parent, path, text, open=False):
        node = self.dir_nav.insert(parent, 'end', iid=self.path, text=text, open=open)
        if os.path.isdir(self.path):
            # Insert a placeholder to make the node expandable
            self.dir_nav.insert(node, 'end', iid=self.path + "_placeholder", text="")
            
    def on_treeview_open(self, event):
        node_id = self.dir_nav.focus()
        if node_id not in self.nodes and os.path.isdir(node_id):
            self.nodes[node_id] = True            
            try:
                for entry in os.scandir(node_id):
                    if entry.is_dir():
                        self.path_entry.delete(0, tk.END)
                        self.path_entry.insert(0, entry)
                        self.path_history.appeend(entry)
                        self.insert_node(node_id, entry.path, entry.name)
            except PermissionError as e:
                print(e)
        if self.on_directory_selected:  
            self.on_directory_selected(node_id)
            entry = self.path_entry.get()
            self.path = entry
            return self.path



    def list_files(self):
        self.path = os.getcwd()     
        self.path_entry.insert(0, self.path)
        self.path_history.append(self.path)
        self.lb1.delete(0, tk.END)
        self.lb2.delete(0, tk.END)
        for file in os.listdir(self.path):
            if os.path.isfile(self.path):
                self.lb1.insert(tk.END, file)
                self.lb2.insert(tk.END, file)
            
    def newdirlist(self):
        self.path = askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.path)
        self.path_history.append(self.path)
        os.chdir(self.path)
        self.flist = os.listdir(self.path)
        self.lb1.delete(0, tk.END)
        self.lb2.delete(0, tk.END)
        for file in os.listdir(self.flist):
            if os.path.isfile(self.flist):
                self.lb1.insert(0, file)
                self.lb2.insert(0, file)
            
       
    def do_switch(self):
        if self.switch:
            self.switch = 0
            text = "Independent Scrolling"
            self.esync.delete(0,tk.END)
            self.esync.insert(0, text)
            self.nosync()
        else:
            self.switch = 1
            text ="In Sync Scrolling Up/Down"
            self.sync()
            self.esync.delete(0,tk.END)
            self.esync.insert(0, text)
           
    def yscrolllistbox(self,event, lb):
        self.lb = lb
        if self.switch==1:
            self.lb.yview_scroll(int(-4*(event.delta/120)), "units")           
            self.sync()    
    def xscrolllistbox(self,event, lb):
        self.lb = lb
        if self.switch==1:
            self.lb.xview_scroll(int(-4*(event.delta/120)), "units")         
            self.sync()
            

    def on_double_click_dir(self, event):
            dir = self.dir_nav.focus()
            current_dir = self.dir_nav.item(item_id, 'text')
            if os.path.isdir(self.path):
                self.path = self.path_entry.get()
                current_dir = self.path
            else:
                current_dir = dir
    def on_double_click_file(self, event):
        sel = self.lb1.curselection()
        if sel:
            self.store_selectionsself.lb1.curselection()
            if os.path.isfile(file):
                 self.lb1.delete(0, tk.END)
                 self.lb2.delete(0, tk.END)
                 for file in os.listdir(item_path):
                    self.lb1.insert(0, file)
                    self.lb2.insert(0, file)                   
            else:
                item_path = self.lb1.curselection()                        
                self.update_view(item_path)  
    def store_selections(self):
        filenames = self.lb1.curselection()
        for filename in filenames:
            print(filename)
            if filenames:
                self.rename_selection.append(filename)
            else:
                 self.rename_selection.pop(filename)

            return filenames             
        
    def on_directory_expand(self, event):
            item_id = self.dir_nav.focus()
            self.on_directory_select()
        
    def on_directory_select(self):
        current_dir = self.dir_nav.item(item_id, 'text')
        if os.path.isdir(current_dir):
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, current_dir)
    def on_selection_change(self, event=None):
        # When the selection changes, refresh the info bar to show the new selection count.
        self.info_bar.num_items_refresh()        
    def show_rename_preview(self, pattern):
        selected_items = self.lb1.curselection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for preview.")
            return

            # Create a new window for the preview
            preview_win = tk.Toplevel(self.master)
            preview_win.title("Rename Preview")

            # Set up the preview tree view
            self.lb3 = tk.Listbox(preview_win,bd=10,width=50, height=25,selectmode=tk.MULTIPLE)
            self.lb3.grid(row=1, column=1)
         
            for filename in self.rename_selection in enumerate(selected_items, start=1):
                current_name = self.rename.selection(filename)
                new_name = self.generate_new_name(current_name, pattern)  # Implement this method based on your renaming logic
                preview_tree.insert("", tk.END, iid=str(index), text=str(index), values=(current_name, new_name))

    def refresh_view(self, path):
            self.active_path = path
            self.delete_children()  # Clear existing file view
            for entry in os.scandir(path):
                if entry.is_file():  # Ensure only files are displayed
                    self.lb1.delete(0, tk.END)
                    self.lb1.insert(0, entry)
    def delete_children(self):
        for item in self.dir_nav.get_children():
            self.self.dir_nav.delete(item)
    def update_view(self, path):
        self.active_path = path
        self.dir_nav.delete(*self.dir_nav.get_children())  # Clear existing entries
        self.lb2.delete(0,  tk,END) # Clear existing entries
        try:
            if entry.is_dir():
                for entry in os.scandir(self.active_path):
                    if os.path.isdir(self.active_path):
                        self.insert_node("", entry)
                        self.dir_nav.item(self.active_path, open=True)
                       
        except PermissionError:
            messagebox.showerror("Error", "You do not have permissions to access this directory")

        

         


class InfoBar:
    def __init__(self, master, fn):
        self.fn = fn  # Reference to the FileNavigator instance
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.grid(column=22, row=2, columnspan=2, sticky="we")  # Ensure it spans across the window
        self.frame.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()
        self.num_items_refresh()

        # Items labelon_path_entry_return
        self.items_label = ttk.Label(self.frame, textvariable=self.items_text_var, relief="sunken")
        self.items_label.grid(row=15,column=0, ipadx=50, ipady=2, padx=4)

        # Last completed action label
        self.action_label = ttk.Label(self.frame, textvariable=self.action_text_var, relief="sunken")
        self.action_label.grid(row=16, column=0, sticky="we", ipady=2, padx=4)
    def num_items_refresh(self):
        # Update the total item and selected item counts
        num_items = self.fn.lb1.size()
        num_sel_items = self.fn.lb1.curselection()
        self.items_text_var.set(f"{num_items} items ")
        self.action_text_var.set(f"({num_sel_items} selected)")
  

    def last_action_refresh(self, action):
        self.action_text_var.set(action)


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Explorer')
        self.geometry('1200x1200')
        self.path = os.getcwd()
        self.pathlist = []
        self.app_frm = tk.Frame(self)
        self.app_frm.grid(row=24, column=2)
      
        self.fn = FileExplorer(self, self.path)
    
        self.lower_frame = ttk.Frame(self)
        self.lower_frame.grid(row=28, column=0, sticky="nsew", padx=(5, 5), pady=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4)  # Main frame gets more weight
        self.rowconfigure(1, weight=1)  # Lower frame gets less weight      

        self.app_frm.columnconfigure(0, weight=1)
        self.app_frm.columnconfigure(1, weight=2)
        self.app_frm.rowconfigure(0, weight=1)
     
           
       # Menubar setup
        self.menubar = tk.Menu(self, tearoff=False)
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
              
        self.file_menu.add_command(
            label="Load Directory", underline=1, command=self.targetdir())
##        self.fn.on_path_entry_return()
        self.config(menu=self.menubar)
    def open_prefix_suffix_dialog(self):
        self.fn.init_prefix_suffix_feature()

    def open_suffix_dialog(self):
        Suffix(self.fn)
       


        # Initialize other components like InfoBar and TabbedControlFilters
        self.infobar = InfoBar(self.app_frm, self.fn)
        self.fn.update_view(self.path)  # Example initial path setup
        self.fn.info_bar = self.infobar 

        self.suffix_btn = ttk.Button(self.app_frm, text="Add Suffix", command=self.open_suffix_dialog)
        self.suffix_btn.grid(row=2, column=0, padx=5, pady=5)
      
             
        # Configure the menubar
        self.config(menu=self.menubar)        
    def targetdir(self):
           self.fn.newdirlist()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()











