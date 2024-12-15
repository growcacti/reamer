import os
import re
import tkinter as tk
from tkinter import Toplevel,filedialog, messagebox
from tkinter import ttk, Menu
import string
import time
import random


from gui_ctrl import *

class DirectoryTreeNavigator:
    def __init__(self, master, path=os.getcwd(), on_directory_selected=None):
        self.path = path
        self.nodes = {}  # Tracks the nodes that have been expanded.
  
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, sticky="nsew")

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Path display and editing
        self.path_entry = ttk.Entry(self.frame)
        self.path_entry.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        self.path_entry.insert(0, path)
        self.path_entry.bind('<Return>', self.on_path_entry_return)

        # Treeview for navigating directories
        self.tree_nav = ttk.Treeview(self.frame, selectmode="browse")
        self.tree_nav.heading("#0", text="Directory Browser", anchor="w")
        self.tree_nav.column("#0", width=280, stretch=True)

        # Scrollbars for the Treeview
        ysb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree_nav.yview)
        xsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree_nav.xview)
        self.tree_nav.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.tree_nav.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        ysb.grid(row=1, column=1, sticky="ns")
        xsb.grid(row=2, column=0, sticky="ew")

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.tree_nav.bind("<<TreeviewOpen>>", self.on_treeview_open)

        # Initialize the treeview with the root path
        self.initialize_treeview(path)
        self.on_directory_selected = on_directory_selected
    def on_path_entry_return(self, event=None):
        path = self.path_entry.get()
        self.initialize_treeview(path)

    def initialize_treeview(self, path):
        self.tree_nav.delete(*self.tree_nav.get_children())  # Clear existing tree
        if os.path.isdir(path):
            self.insert_node("", path, path)
            self.tree_nav.item(path, open=True)  # Optionally open the root node
 

    def insert_node(self, parent, path, text, open=False):
        node = self.tree_nav.insert(parent, 'end', iid=path, text=text, open=open)
        if os.path.isdir(path):
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

class FileNavigator:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.grid(row=1, column=1, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        
        self.active_path = ""
        self.rename_history = []

        self.tree_files = ttk.Treeview(self.frame, selectmode="extended", columns=("old_name", "new_name"))
        ysb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree_files.yview)
        xsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree_files.xview)
        self.tree_files.configure(yscroll=ysb.set, xscroll=xsb.set)

        self.tree_files.heading("#0", text="File Name", anchor="w")
        self.tree_files.column("#0", anchor="w", width=150)
        self.tree_files.heading("old_name", text="Old Name", anchor="w")
        self.tree_files.column("old_name", anchor="w", width=150)
        self.tree_files.heading("new_name", text="New Name", anchor="w")
        self.tree_files.column("new_name", anchor="w", width=150)

        self.tree_files.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")

        self.info_bar = InfoBar(self.master, self)
        self.bind_entries()

    def populate_tree(self, parent, path):
        for entry in os.scandir(path):
            if entry.is_file():
                self.insert_node(parent, entry)

    def insert_node(self, parent, entry):
        # Insert a new node with both old and new names initially set to the entry's name
        node_id = self.tree_files.insert(parent, 'end', iid=entry.path, text=entry.name, values=(entry.name, entry.name))

    def update_node(self, item_id, old_name=None, new_name=None):
        # Update the node specified by item_id with new old and new names
        values = (old_name if old_name is not None else "", new_name if new_name is not None else "")
        self.tree_files.item(item_id, values=values)

    def bind_entries(self):
        self.tree_files.bind("<<TreeviewSelect>>", self.on_selection_change)
        self.tree_files.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_selection_change(self, event=None):
        self.info_bar.num_items_refresh()

    def on_tree_select(self, event):
        selected_items = self.tree_files.selection()
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            print("Selected item:", item_text)
            self.info_bar.num_items_refresh()

    def delete_children(self):
        for item in self.tree_files.get_children():
            self.tree_files.delete(item)

    def refresh_view(self, path):
        self.active_path = path
        self.delete_children()  # Clear existing file view
        self.populate_tree("", path)

    def regex(self,pattern, replace_pattern):
        
        selected_items = self.tree_files.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for preview.")
            return
        new_name = pattern.replace("{name}", replace_paterrn)
    def case(self, case):
        selected_items = self.tree_files.selection()
        
        for item_id in selected_items:
            old_name = self.tree_files.item(item_id, 'text')  # Get the current name from the tree
            currrent_name = old_name
            # Decide the new name based on the case condition
            if case == "Upper":
                new_name = old_name.upper()
            elif case == "Lower":
                new_name = old_name.lower()
            elif case == "Title":
                new_name = old_name.title()
            elif case == "Capitalize":
                new_name = old_name.capitalize()
            elif case == "SwapCase":
                new_name = old_name.swapcase()
            elif case == "Strip":
                new_name = old_name.strip()
            else:
                continue  

           
            new_name = f"{new_name}"
            current_name = new_name
            
            self.tree_files.item(item_id, values=(new_name))
            new_name = self.tree_files.item(item_id, 'text')  # Get the current name from the tree
          
            print(item_id)
       
            # Construct old and new paths for the rename operation
            old_path = os.path.join(self.active_path, old_name)
            new_path = os.path.join(self.active_path, new_name)
            
            self.rename_history.append(new_name)
                # Try to rename the file on the file system

    def numbering_files(self, start, prefix=True, delimiter="_", retain_name=True):
        selected_items = self.tree_files.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected for numbering.")
            return

        count = start
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            base, ext = os.path.splitext(item_text)
            if retain_name:
                new_name = f"{base}{delimiter}{count}{ext}" if prefix else f"{count}{delimiter}{base}{ext}"
            else:
                new_name = f"{count}{delimiter}{ext}" if prefix else f"{ext}{delimiter}{count}"

            self.rename_file(item_id, new_name)
            count += 1
    def replacement(self,replace_text,with_text):
        selected_items = self.tree_files.selection()
        old_name = self.tree_files.item(item_id, 'text')  # Get the current name from the tree
        currrent_name = old_name
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            if not new_ext.startswith('.'):
                newname = '.' + new_ext
                new_name = item_text.replace(replace_text, with_text)

            self.tree_files.item(item_id, values=(new_name))
            self.rename_history.append(new_name)


        
    def ext_replace(self, new_ext):
        selected_items = self.tree_files.selection()
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            current_ext = os.path.splitext(item_text)
            if not new_ext.startswith('.'):
                new_name = item_text.replace(current_ext[1], f".{new_ext}")
                self.tree_files.item(item_id, text=new_name)
                old_path = os.path.join(self.active_path, item_text)
                new_path = os.path.join(self.active_path, new_name)
                self.rename_history.append((old_path, new_path))

             


    def shift_character(self, c, shift):
        """Shifts a character by a given number of positions, wrapping around the alphabet."""
        if c.isalpha():
            start = ord('a') if c.islower() else ord('A')
            return chr((ord(c) - start + shift) % 26 + start)
        return c

    def shift_filename_chars(self, filename, shift):
        """Converts filename to a list of characters, applies shift, and reassembles the filename."""
        char_list = list(filename)  # Convert filename to list of characters
        shifted_list = [shift_character(c, shift) for c in char_list]  # Apply shift to each character
        new_name = ''.join(shifted_list)  # Reassemble the filename
        return new_name

    def shiftrename_files(self,shift_value):
        selected_items = self.tree_files.selection()
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            current_name = self.rename_history[-1]
            shift = int(shift_value)
            name, ext = os.path.splitext(filename)
            new_name = shift_filename_chars(name, shift) + ext
            messagebox.showinfo("Success", "Files have been renamed.")



    def undo_last_rename(self):
        if not self.rename_history:
            tk.messagebox.showinfo("Undo", "No more actions to undo.")
            return
        
        # Get the last rename operation
        old_path, new_path = self.rename_history.pop()
        try:
            # Rename the file back to its original name
            os.rename(new_path, old_path)
            # Find the item in the tree view and update its name
            item_id = self.tree_files.selection()[0]  # Adjust this line if necessary to target the correct item
            self.tree_files.item(item_id, text=os.path.basename(old_path))
            tk.messagebox.showinfo("Undo", "Last action undone successfully.")
        except Exception as e:
            tk.messagebox.showerror("Undo Error", f"Failed to undo last action: {e}")

    def prefix_suffix(self, item_id, old_name, new_name):
        old_path = os.path.join(self.active_path, old_name)
        new_path = os.path.join(self.active_path, new_name)
        self.rename_history.append((old_path, new_path))
        self.set_name(item_id,old_path,new_path)
        return self.tree_files.item(item_id, values=(new_name))
    def set_name(self,item_id,old_path,new_path):
        print(old_path)
        print(new_path)
        
    def rename_file(self, item_id, new_name):
        old_path = os.path.join(self.active_path, self.tree_files.item(item_id, 'text'))
        new_path = os.path.join(self.active_path, new_name)

        try:
            #os.rename(old_path, new_path)
            self.tree_files.item(item_id, text=new_name, values=(new_name,))
            self.rename_history.append((old_path, new_path))
            messagebox.showinfo("Rename Success", f"Successfully renamed {old_path} to {new_name}")
        except Exception as e:
            messagebox.showerror("Rename Error", f"Failed to rename {old_path} to {new_name}: {e}")







class InfoBar:
    def __init__(self, master, fn):
        self.fn = fn  # Reference to the FileNavigator instance
        self.frame = ttk.Frame(master)
        self.frame.grid(column=0, row=2, columnspan=2, sticky="we")  # Ensure it spans across the window
        self.frame.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()
        self.num_items_refresh()

        # Items labelon_path_entry_return
        self.items_label = ttk.Label(self.frame, textvariable=self.items_text_var, relief="sunken")
        self.items_label.grid(column=0, row=0, ipadx=50, ipady=2, padx=4)

        # Last completed action label
        self.action_label = ttk.Label(self.frame, textvariable=self.action_text_var, relief="sunken")
        self.action_label.grid(column=1, row=0, sticky="we", ipady=2, padx=4)
    def num_items_refresh(self):
        # Update the total item and selected item counts
        num_items = len(self.fn.tree_files.get_children())
        num_sel_items = len(self.fn.tree_files.selection())
        self.items_text_var.set(f"{num_items} items ({num_sel_items} selected)")

  

    def last_action_refresh(self, action):
        self.action_text_var.set(action)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Explorer')
        self.geometry('1200x600')
##        self.initial_path = os.path.expanduser("~")
        self.initial_path = os.getcwd()
        self.pathlist = []
        # Initialize main and lower frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=5)
        self.fn = FileNavigator(self.main_frame)
        self.lower_frame = ttk.Frame(self)
        self.lower_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=5)
        self.tab = Ctrl_Tabs(self.lower_frame,self.fn)
        # Configure window to expand frames with size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4)  # Main frame gets more weight
        self.rowconfigure(1, weight=1)  # Lower frame gets less weight
        
        self.fn.frame.grid(row=0, column=1, sticky="nsew")
        self.rename_btn= ttk.Button(self.main_frame, text="Rename File(s)", command=None)
        self.rename_btn.grid(row=3, column=1)
        self.undo_button = ttk.Button(self.main_frame, text="Undo Last Rename", command=self.fn.undo_last_rename)
        self.undo_button.grid(row=3, column=0, padx=5, pady=5)  # Adjust grid positioning as needed
        # Initialize components
        self.dirnav = DirectoryTreeNavigator(self.main_frame, self.initial_path, self.fn.refresh_view)

      
      
        
        # Adjust main_frame layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
       
       # Menubar setup
        self.menubar = tk.Menu(self, tearoff=False)
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="Refresh View", underline=1, command=lambda: self.fn.refresh_view(self.initial_path)
        )
       
        self.file_menu.add_command(
            label="Load Directory", underline=1, command=lambda: self.targetdir())
        self.dirnav.on_path_entry_return()
        self.config(menu=self.menubar)
    def open_prefix_suffix_dialog(self):
        self.fn.init_prefix_suffix_feature()

    def open_suffix_dialog(self):
        Suffix(self.fn)
       


        # Initialize other components like InfoBar and TabbedControlFilters
        self.infobar = InfoBar(self.main_frame, self.fn)
        self.fn.update_view(self.initial_path)  # Example initial path setup
        self.fn.info_bar = self.infobar 

        self.suffix_btn = ttk.Button(self.main_frame, text="Add Suffix", command=self.open_suffix_dialog)
        self.suffix_btn.grid(row=2, column=0, padx=5, pady=5)
      
             
        # Configure the menubar
        self.config(menu=self.menubar)        
    def targetdir(self):
            directory_path = filedialog.askdirectory()
            self.pathlist.append(directory_path)
            self.dirnav.path_entry.delete(0, tk.END)
            self.dirnav.path_entry.insert(0, directory_path)
            self.dirnav.on_path_entry_return()
            return directory_path



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()


