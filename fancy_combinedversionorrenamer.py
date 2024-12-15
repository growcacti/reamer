import os
import re
import tkinter as tk
from tkinter import ttk
import time
import time
import re


class FileExplorer:
    def __init__(self, master, path, on_directory_selected=None):
        self.path = path
        self.nodes = {}  # Tracks the nodes that have been expanded.
        self.entry_frame = tk.Frame(master, width=100)
        self.entry_frame.grid(row=0, column=0,columnspan=4)
        self.frm1 = ttk.Frame(master)
        self.frm1.grid(row=1, column=0, rowspan=4,columnspan=10,sticky="ns")
        self.canvas = tk.Canvas(self.frm1,width=50,bg="seashell2")
        self.canvas.grid(row=2, column=0)
        self.frm2 = ttk.Frame(master)
        self.frm2.grid(row=1, column=4, sticky="ns")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(4, weight=1)

        # Path display and editing
        self.path_entry = tk.Entry(self.entry_frame, bd=8, bg="azure", width=155)
        self.path_entry.grid(row=0, column=0,columnspan=2, sticky="ew")
        self.path_entry.insert(0, self.path)
        self.path_entry.bind('<Return>', self.on_path_entry_return)
        
        # Treeview for navigating directories
        self.tree_nav = ttk.Treeview(self.frm1, selectmode="browse")
        self.tree_nav.heading("#0", text="Directory Browser", anchor="w")
        self.tree_nav.column("#0", width=280, stretch=True)

        # Scrollbars for the Treeview
        ysb = ttk.Scrollbar(self.frm1, orient="vertical", command=self.tree_nav.yview)
        xsb = ttk.Scrollbar(self.frm1, orient="horizontal", command=self.tree_nav.xview)
       
        self.tree_nav.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.tree_nav.grid(row=1, column=0,rowspan=4,columnspan=2, sticky="nsew")
        ysb.grid(row=1, column=3, sticky="ns")
        xsb.grid(row=20, column=0, sticky="ew")

        self.tree_nav.bind("<<TreeviewOpen>>", self.on_treeview_open)

        # Initialize the treeview with the root path
        self.initialize_treeview(path)
        self.on_directory_selected = on_directory_selected
        self.can=tk.Canvas(self.frm1, bg="alice blue", width=180, height=70)
        self.can.grid(row=2, column=4,columnspan=8)
        tk.Label(self.can, text="Original Filenames").grid(row=3,column=1)
        tk.Label(self.can, text="Preview New Filenames").grid(row=3,column=4)
        self.lb1 = tk.Listbox(self.can,bd=8,width=50, height=45)
        self.lb1.grid(row=4, column=1,rowspan=2,columnspan=2)
        self.lb2 = tk.Listbox(self.can,bd=8,width=50, height=45)
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
      
        self.esync=tk.Entry(self.can,bd=5,bg="lavender")
        self.esync.grid(row=19,column=1)
        self.syncbtn=tk.Button(self.can, text= "Sync/unsync", command=self.do_switch)
        self.syncbtn.grid(row=20,column=2)

    def sync(self):
        self.yscrollbar2 = tk.Scrollbar(self.can)
        self.yscrollbar2.grid(row=4,column=11)
        self.lb2.config(bg="light pink", yscrollcommand=self.yscrollbar2.set)
        self.lb1.config(bg="light green", yscrollcommand=self.yscrollbar.set)

    def nosync(self):
       
        self.yscrollbar2= ttk.Scrollbar(self.can, orient="vertical", command=self.lb2.yview)
        self.yscrollbar2.grid(row=4,column=10)    
          
    def on_path_entry_return(self, event=None):
        self.path = self.path_entry.get()
        self.initialize_treeview(self.path)

    def initialize_treeview(self, path):
        self.tree_nav.delete(*self.tree_nav.get_children())  # Clear existing tree
        if os.path.isdir(self.path):
            self.insert_node("", self.path, self.path)
            self.tree_nav.item(self.path, open=True)  # Optionally open the root node
 

    def insert_node(self, parent, path, text, open=False):
        node = self.tree_nav.insert(parent, 'end', iid=path, text=text, open=open)
        if os.path.isdir(self.path):
            # Insert a placeholder to make the node expandable
            self.tree_nav.insert(node, 'end', iid=path + "_placeholder", text="")
    def on_treeview_open(self, event):
        node_id = self.tree_nav.focus()
        if node_id not in self.nodes and os.path.isdir(node_id):
            self.nodes[node_id] = True
            
            try:
                for entry in os.scandir(node_id):
                    if entry.is_dir():
                        self.insert_node(node_id, entry.path, entry.name)
            except PermissionError as e:
                print(e)
            


        if self.on_directory_selected:  
            self.on_directory_selected(node_id)  # Call the callback with the selected directory path





    def list_files(self):
        path = os.getcwd()
      
        self.path_entry.insert(0, path)
        self.lb1.delete(0, tk.END)
        self.lb2.delete(0, tk.END)
        for file in os.listdir(path):
            self.lb1.insert(tk.END, file)
            self.lb2.insert(tk.END, file)
            
    def newdirlist(self):
        self.path = askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.path)
        os.chdir(self.path)
        self.flist = os.listdir(self.path)
        
           
        self.lb1.delete(0, tk.END)
        self.lb2.delete(0, tk.END)
        

        for files in self.flist:
            self.lb1.insert(0, files)
            self.lb2.insert(0, files)


    def refresh_view(self, path):
        self.active_path = path
        self.lb1.delete(0, tk.END)
        self.lb2.delete(0, tk.END)# Clear existing file view
        for files in os.scandir(self.active_path):
            self.lb1.insert(files, tk.END)
            self.lb2.insert(0, files)                   
    

    def do_switch(self):
        if self.switch:
            self.switch = 0
            text = "No Sync"
            self.esync.delete(0,tk.END)
            self.esync.insert(0, text)
            self.nosync()
        else:
            self.switch = 1
            text =" In Sync up/down"
            self.sync()
            self.esync.delete(0,tk.END)
            self.esync.insert(0, text)
           


    def yscrolllistbox(self,event, lb):
        self.lb = lb
        if self.switch==1:
            self.lb.yview_scroll(int(-4*(event.delta/120)), "units")
           
            self.sync()
            print(event)


    def xscrolllistbox(self,event, lb):
        self.lb = lb
        if self.switch==1:
            self.lb.xview_scroll(int(-4*(event.delta/120)), "units")
         
            self.sync()
            print(event)



class InfoBar:
    def __init__(self, master, fn):
        pass
##       # Reference to the FileNavigator instance
##        self.frm = ttk.Frame(master)
##        self.frm.grid(column=0, row=2, columnspan=2, sticky="we")  # Ensure it spans across the window
##        self.frm.columnconfigure(1, weight=1)
##
##        self.items_text_var = tk.StringVar()
##        self.action_text_var = tk.StringVar()
##        self.num_items_refresh()
##       
##      
##        # Items label
##        self.items_label = ttk.Label(self.frm, textvariable=self.items_text_var, relief="sunken")
##        self.items_label.grid(column=0, row=0, ipadx=50, ipady=2, padx=4)
##
##        # Last completed action label
##        self.action_label = ttk.Label(self.frm, textvariable=self.action_text_var, relief="sunken")
##        self.action_label.grid(column=1, row=0, sticky="we", ipady=2, padx=4)
##    def num_items_refresh(self):
##        # Update the total item and selected item counts
##        num_items = len(self.lb1.get())
##        #num_sel_items = len(self.file_nav())
##        #self.items_text_var.set(f"{num_items} items ({num_sel_items} selected)")
##
##  

    def last_action_refresh(self, action):
        self.action_text_var.set(action)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Explorer')
        self.geometry('1600x800')
        self.path = os.getcwd()   
        # Initialize main and lower frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
##        self.lower_frame = ttk.Frame(self)
##        self.lower_frame.grid(row=1, column=0, sticky="nsew")       
##        # Configure window to expand frames with size
##        self.columnconfigure(0, weight=1)
##        self.rowconfigure(0, weight=4)  # Main frame gets more weight
##        self.rowconfigure(1, weight=1)  # Lower frame gets less weight
        self.fn = FileExplorer(self.main_frame,self.path)
        
        # Initialize components
       
              
        # Adjust main_frame layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        self.fn.list_files()
##       


        # Initialize other components like InfoBar and TabbedControlFilters
        self.infobar = InfoBar(self.main_frame, self.fn)
      
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()






