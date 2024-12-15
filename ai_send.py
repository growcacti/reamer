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
    """
    Manages the display and interaction with a tree view of files and filess, allowing for renaming and other file operations.
    """

    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.grid(row=1, column=1, sticky="we")
        self.frame.columnconfigure(2, weight=1)
        self.active_path = ""
        self.rename_history = []
        self.count = 0
        self.tree_files = ttk.Treeview(self.frame, selectmode="extended")
        ysb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree_files.yview)
        xsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree_files.xview)
        self.tree_files.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree_files.heading("#0", text="Old Name", anchor="w")
        self.tree_files["columns"] = ("new_name",)
        self.tree_files.heading("new_name", text="New Name", anchor="w")
        self.tree_files.grid(row=0, column=2, sticky="we")
        ysb.grid(row=0, column=3, sticky="ns")
        xsb.grid(row=1, column=2, sticky="ew")
        self.info_bar = InfoBar(self.master,self)
        self.bind_entries()
       
    
    def bind_entries(self):
        # Existing bindings
            self.tree_files.bind("<<TreeviewOpen>>", self.on_directory_expand)
            self.tree_files.bind("<<TreeviewSelect>>", self.on_double_click)
            self.tree_files.bind("<<TreeviewSelect>>", self.on_selection_change)
            self.tree_files.bind("<<TreeviewSelect>>", self.on_tree_select)
            
    def on_directory_expand(self, event):
        item_id = self.tree_files.focus()  # Get the ID of the node being expanded
    
    def populate_tree(self, parent, path):
        for entry in os.scandir(path):
            if entry.is_file():  # This line is modified to only check for files
                self.insert_node(parent, entry)
                

    def insert_node(self, parent, entry, tag=""):
        # Assuming entry has 'path' and 'name' attributes correctly assigned
        node_id = self.tree_files.insert(parent, "end", iid=entry.path, text=entry.name, values=(entry.name,), tags=(tag,))
      
  

    def on_double_click(self, event):
        item_id = self.tree_files.identify_row(event.y)
        if item_id:
            item = self.tree_files.item(item_id)
            item_path = item['text']  # Assuming the item text contains the path or name
            # Determine if the item is a directory
            if os.path.isdir(item_path):
                # Logic to either expand/collapse or navigate into the directory
                if self.tree_files.item(item_id, 'open'):  # If the node is open
                        self.tree_files.item(item_id, open=False)  # Close it
                else:
                    self.tree_files.item(item_id, open=True)  # Open it
                    self.update_view(item_path)  # Optional: navigate into the directory
            print(f"Double-clicked on directory: {item_path}")
    def show_rename_preview(self, pattern):
        selected_items = self.tree_files.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for preview.")
            return

        # Create a new window for the preview
        preview_window = tk.Toplevel(self.master)
        preview_window.title("Rename Preview")

        # Set up the preview tree view
        preview_tree = ttk.Treeview(preview_window, columns=("current_name", "new_name"))
        preview_tree.heading("#0", text="Index", anchor="w")
        preview_tree.heading("current_name", text="Current Name", anchor="w")
        preview_tree.heading("new_name", text="New Name", anchor="w")
        preview_tree.column("#0", width=40)
        preview_tree.column("current_name", width=150)
        preview_tree.column("new_name", width=150)
        preview_tree.pack(fill=tk.BOTH, expand=True)

        # Generate the preview data
        for index, item_id in enumerate(selected_items, start=1):
            current_name = self.tree_files.item(item_id, 'text')
            new_name = self.generate_new_name(current_name, pattern)  # Implement this method based on your renaming logic
            preview_tree.insert("", tk.END, iid=str(index), text=str(index), values=(current_name, new_name))


   
    def on_selection_change(self, event=None):
        # When the selection changes, refresh the info bar to show the new selection count.
        self.info_bar.num_items_refresh()

    def right_click_path_to_clip(self, event):
        path = self.tree_files.identify_row(event.y)
        if not path:
            messagebox.showinfo("Info", "No item selected.")
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(path)
        name = os.path.basename(path)
        messagebox.showinfo("Info", f'Copied "{name}" Path to Clipboard')

    def refresh_view(self, path):
        self.active_path = path
        self.delete_children()  # Clear existing file view
        for entry in os.scandir(path):
            if entry.is_file():  # Ensure only files are displayed
                self.insert_node("", entry)
                

    def on_tree_select(self, event):
        selected_items = self.tree_files.selection()
        # You can process the selected items here
        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            print("Selected item:", item_text)
            self.info_bar.num_items_refresh()
    def delete_children(self):
        for item in self.tree_files.get_children():
            self.tree_files.delete(item)
            
           


    def update_view(self, path):
        self.active_path = path
        self.tree_files.delete(*self.tree_files.get_children())  # Clear existing entries
        try:
            for entry in os.scandir(path):
                if entry.is_dir() or entry.is_file():  # Check if it's a directory or file
                    self.insert_node("", entry)  # Corrected to include both arguments
        except PermissionError:
            messagebox.showerror("Error", "You do not have permissions to access this directory")

   
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

            # Apply the new name to the tree view item
            new_name = f"{new_name}"
            current_name = new_name
            self.tree_files.item(item_id, values=(new_name))
            print(item_id)
       
            # Construct old and new paths for the rename operation
            old_path = os.path.join(self.active_path, old_name)
            new_path = os.path.join(self.active_path, new_name)
            
            self.rename_history.append(new_name)
            # Try to rename the file on the file system

    def numbering_files(self, start, prefix=True, delimiter="_"):
        """
        Renames the selected files by adding a sequential number to their name.

        Parameters:
        start (int): The starting number for the sequence.
        prefix (bool): True if the number should be a prefix; False for suffix.
        delimiter (str): The delimiter between the number and the file name.
        """
        selected_items = self.tree_files.selection()
        self.count = start

        for item_id in selected_items:
            item_text = self.tree_files.item(item_id, 'text')
            base, ext = os.path.splitext(item_text)
            if prefix:
                new_name = f"{self.count}{delimiter}{base}{ext}"
            else:
                new_name = f"{base}{delimiter}{self.count}{ext}"
            self.rename_file(item_id, new_name) 
            
            self.count += 1
            self.rename_history.append(new_name)



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
        pass
##        old_path = self.tree_files.item(item_id, 'text')  # This should be adjusted to get the full path, not just the text
##        new_path = os.path.join(os.path.dirname(old_path), new_name)
##
##        try:
##            os.rename(old_path, new_path)
##            # Update the tree view to reflect the new name
##            self.tree_files.item(item_id, text=new_name, values=(new_name,))
##            # Add the rename operation to the history
##            self.rename_history.append((old_path, new_path))
##        except Exception as e:
##            messagebox.showerror("Error", f"Failed to rename file {old_path} to {new_name}: {e}")
##
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



import tkinter as tk
from tkinter import ttk
import random
import os


MAX_NAME_LEN = 255


class Ctrl_Tabs:
    def __init__(self, parent, file_navigator=None):
        self.parent = parent
        self.fn = file_navigator

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, columnspan=6, sticky='nsew')

        self.frames = {}
        self.canvases = {}

        # Define colors for each canvas
        colors = ['ivory2', 'DarkSeaGreen1', 'alice blue', 'khaki1', 'light pink', 'light cyan',
                  'seashell', 'honeydew', 'azure4', 'cornsilk3', 'grey67', 'powder blue', 'navajo white']
        
        # Tab labels
        labels = ['RegEx', 'Case', 'Replace', 'Numbering', 'Add to String', 'Shift Char',
                  'Remove', 'Ext Replace', 'Naming', 'Prefix Suffix', 'Random', 'Combination', 'Overflow']
        
        # Create frames and canvases, assign colors and add widgets
        for i in range(1, 14):  # Frame indexes from 1 to 13
            frame = ttk.Frame(self.notebook)
            canvas = tk.Canvas(frame, bg=colors[i-1] if i <= len(colors) else 'white')
            canvas.grid(row=0, column=0, sticky='nsew')
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

            self.frames[i] = frame
            self.canvases[i] = canvas

            # Adding widgets to the canvas
            self.add_widgets_to_tab(i, canvas)

            # Add tabs to notebook with labels
            if i <= len(labels):
                self.notebook.add(frame, text=labels[i-1])
     
    def add_widgets_to_tab(self, index, canvas):
        if index == 1:
            # Example for RegEx tab using ComboBox
            ttk.Label(canvas, text='Select RegEx pattern:').grid(row=0, column=0, padx=10, pady=10)
            pattern_combo = ttk.Combobox(canvas, values=["^[a-zA-Z]+", "^\\d+", "[a-zA-Z0-9]"])
            pattern_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Label(canvas, text="Pattern Match and Replace").grid(row=3,column=1)
            patternmatch=ttk.Entry(canvas)
            patternmatch.grid(row=4, column=1, padx=10, pady=10)
            regex_btn = ttk.Button(canvas, text='Apply',command=self.apply_regexp)
            regex_btn.grid(row=0, column=2, padx=10, pady=10)
            checkbutton1 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            checkbutton1.grid(row=9, column=0, columnspan=2, sticky="w", padx=5)

        elif index == 2:
            # Example for Case tab using ComboBox
            ttk.Label(canvas, text='Select case operation:').grid(row=0, column=0, padx=10, pady=10)
            operation_combo = ttk.Combobox(canvas, values=["Upper", "Lower", "Title","Capitalize","SwapCase","Strip"])
            operation_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Apply').grid(row=0, column=2, padx=10, pady=10)
            checkbutton2 = ttk.Checkbutton(canvas, text="current file", variable=None)
            checkbutton2.grid(row=9, column=0, columnspan=2, sticky="w", padx=5)

        elif index == 3:
            # Example for Replace tab using ComboBox
            ttk.Label(canvas, text='Find what:').grid(row=0, column=0, padx=10, pady=10)
            find_combo = ttk.Combobox(canvas, values=["Error", "Warning", "Notice"])
            find_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Label(canvas, text='Replace with:').grid(row=1, column=0, padx=10, pady=10)
            replace_entry = ttk.Entry(canvas)
            replace_entry.grid(row=1, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Replace').grid(row=1, column=2, padx=10, pady=10)
        elif index == 4:
           pass
           self.position_combobox = ttk.Combobox(canvas, values=["Prefix", "Suffix"])
           self.position_combobox.grid(row=1, column=1)
           tk.Label(canvas, text="Delimiter:").grid(row=2, column=0)
           self.delimiter_entry = tk.Entry(canvas)
           self.delimiter_entry.grid(row=2, column=1)
           self.delimiter_entry.insert(0, "_") 

        elif index == 5:
##           
            self.entry = tk.Entry(canvas)
            self.entry.grid(row=6, column=1, sticky="ew", padx=5)
            self.spinbox = ttk.Spinbox(canvas, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
            self.spinbox.grid(row=7, column=1, sticky="ew", padx=5)
            self.checkbutton = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton.grid(row=9, column=2, sticky="ew", padx=5)


      
        elif index == 6:
            self.shift = ttk.Spinbox(canvas, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
            self.shift.grid(row=7, column=1, sticky="ew", padx=5)

            self.checkbutton6 = ttk.Checkbutton(canvas, text="current_name")
            self.checkbutton6.grid(row=9, column=2, sticky="ew", padx=5)

            pass
        elif index == 7:
            tk.Label(canvas, text="Remove first n characters:",).grid(row=4, column=3)
            self.first_n = tk.IntVar()
            self.sp1 = tk.Spinbox(canvas, from_=0, to=MAX_NAME_LEN)
            self.sp1.grid(row=5, column=3)

            tk.Label(canvas, text="Remove last n characters:",).grid(row=6, column=3)
            self.last_n = tk.IntVar()
            self.sp2 = tk.Spinbox(canvas, from_=0, to=MAX_NAME_LEN)
            self.sp2.grid(row=7, column=3)
            self.btn1 =tk.Button(canvas, text="Apply", command=self.apply_removal)
            self.btn1.grid(row=10, column=0)
            self.checkbutton7 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton7.grid(row=9, column=2, sticky="ew", padx=5)
        elif index == 8:
            self.new_ext_entry = tk.Entry(canvas, width=20)
            self.new_ext_entry.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

            self.sendchange_button = tk.Button(canvas, text="Change ext", command=self.ext_change)
            self.sendchange_button.grid(column=1, row=4, padx=5, pady=5)

            self.reset_button = tk.Button(canvas, text="Reset", command=self.reset_widget)
            self.reset_button.grid(column=2, row=0, padx=5, pady=5)
            self.checkbutton8 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton8.grid(row=9, column=2, sticky="ew", padx=5)
 
       

            
            pass
        elif index == 9:
            tk.Label(canvas, text="Name").grid(column=0, row=0, sticky="w")
            self.name_option_combo = ttk.Combobox(
            canvas,
            width=10,
            state="readonly",            values=("Keep", "Remove", "Reverse", "Fixed","Random",))
            self.name_option_combo.grid(column=1, row=0, sticky="ew")
            self.name_option_combo.current(0)

            self.fixed_name_entry = tk.Entry(canvas, bd=80,width=10)
            self.fixed_name_entry.grid(column=1, row=1, sticky="ew")

            self.reset_button = tk.Button(canvas, text="Reset", command=self.reset_widget)
            self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)

            self.name_button = tk.Button(canvas, text="Name", command=self.apply_name)
            self.name_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)
        
        elif index == 10:
            tk.Label(canvas, text="Prefix:").grid(row=0, column=0)
            self.prefix_entry = tk.Entry(canvas)
            self.prefix_entry.grid(row=0, column=1)

            # Entry for suffix
            tk.Label(canvas, text="Suffix:").grid(row=1, column=0)
            self.suffix_entry = tk.Entry(canvas)
            self.suffix_entry.grid(row=1, column=1)

            # Apply button
            self.apply_btn = tk.Button(canvas, text="Apply", command=None)
            self.apply_btn.grid(row=2, column=0, columnspan=2)

            
            
        elif index == 11:
            random_entry = ttk.Entry(canvas)
            random_entry.grid(row=1, column=1, padx=10, pady=10)
            
            self.apply_btn = tk.Button(canvas, text="Apply Random", command=None)
            self.apply_btn.grid(row=2, column=0, columnspan=2)
            
            
        elif index == 12:
            pass
        elif index == 13:
            pass
        elif index == 14:
            pass

    def update_use_current_filename(self):
        if self.varr2.get():  # If the checkbox is checked
             if self.fn.rename_history:
                current_file_name = self.fn.rename_history[-1]  # Get the last item in the history
                self.current_file_name.set(current_file_name)
        else:
            self.current_file_name.set("")  # Reset current file name if checkbox is unchecked
            self.use_current_filename.set(self.varr2.get())
         
    def apply_changes(self):
        if self.use_current_filename.get():
            current_file_name = self.get_current_file_name()  
            modified_file_name = self.apply_modifications(current_file_name)  
            # Apply modified_file_name to the selected files or perform other actions as needed
        else:
            # Directly apply modifications to the selected files
            selected_items = self.fn.tree_files.selection()
            if not selected_items:
                selected_items = self.fn.tree_files.get_children()
            
            if not selected_items:
                messagebox.showinfo("Info", "No files selected.")
                return
            
            for item_id in selected_items:
                old_name = self.fn.tree_files.item(item_id, 'text')
                new_name = self.apply_modifications(old_name)  # Apply modifications directly to each file name
                # Here you can update the file name in your application's interface or perform any other necessary action




    def regexptab(self,fn):
       
        self.fn =fn
        self.fn.selected_files = self.fn.tree_files.selection()
     
    def apply_regexp(self):
        pattern = self.match_entry.get()
        replace_pattern = self.replace_entry.get()

        if not self.fn.selected_files:
            messagebox.showinfo("Info", "No files selected.")
            return
        selected_items = self.fn.tree_files.selection()
        if not selected_items:
            selected_items = self.fn.tree_files.get_children()
        self.fn.regex(pattern,replace_pattern)    
    def casetab(self,fn):
        self.fn = fn
        
    def apply_case_change(self):
        namecase = self.case_type_combobox.get()
        self.fn.case(namecase)
    
    def apply_replacement(self):
        replace_text = self.match_entry.get()
        with_text = self.replace_entry.get()
        self.fn.replacement(replace_text,with_text)
      





    def add(self,fn):
    
        self.fn =fn
        self.fn.selected_files = self.fn.tree_files.selection()
       
        
    def apply_numbering(self):
        try:
            start = int(self.start_num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Starting number must be an integer.")
            return

        position = self.position_combobox.get()
        delimiter = self.delimiter_entry.get()

       
        self.fn.numbering_files(start, prefix=position == "Prefix", delimiter=delimiter)

    def reset_widget(self):
        self.prefix.set("")
        self.insert_this.set("")
        self.at_pos.set(0)
        self.suffix.set("")



    def shiftchar(self,fn):
        
        self.fn = fn
        self.fn.selected_files = self.fn.tree_files.selection()
       
    def apply_move(self):
        sample_name = "ExampleFile.txt"
        result = "Moved/Copied_Part_" + sample_name

        # Displaying the result in a temporary label for demonstration
        result_label = tk.Label(self.can8, text=f"Result: {result}")
        result_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)


     
        
    def apply_removal(self):
        first_n = self.first_n.get()
        last_n = self.last_n.get()
      
        print(f"Removing first {first_n} and last {last_n} characters from filenames")


    def create_spinbox(self, label, variable, row):
        var = tk.StringVar()
        ttk.Spinbox(self.can8, from_=0, to=MAX_NAME_LEN,).grid(row=row, column=1)

    def bind_entries(self):
        self.first_n.trace_add("write", self.update)
      
    def reset_widget(self):
        self.first_n.set(0)
        self.last_n.set(0)
        # Continues for all resettable variables...

    def update(self, *args):
        print("First n:", self.first_n.get())
        print("Last n:", self.last_n.get())





    def ext_change(self):
          self.new_ext = self.new_ext_entry.get()
          self.fn.ext_replace(self.new_ext)   

   
    def remove_n_chars(self, name):
        first_n = self.first_n.get()
        last_n = -self.last_n.get() if self.last_n.get() > 0 else None

        # If last_n is None, slicing will go to the end of the string.
        return name[first_n:last_n]

   
       
    def ext_change(self):
        
        self.new_ext = self.new_ext_entry.get()
        self.fn.ext_replace(self.new_ext)
        


           
    def reset_widget(self):
        self.new_ext_entry.delete(0, tk.END)
    

        

    def name(self,fn):
        
        pass

   


       
        

  


class PrefixSuffixApplication:
    def __init__(self, parent,fn):
        self.frm10 = parent
        self.fn = fn
        
        # Entry for prefix
        tk.Label(self.frm10, text="Prefix:").grid(row=0, column=0)
        self.prefix_entry = tk.Entry(self.frm10)
        self.prefix_entry.grid(row=0, column=1)
        
        # Entry for suffix
        tk.Label(self.frm10, text="Suffix:").grid(row=1, column=0)
        self.suffix_entry = tk.Entry(self.frm10)
        self.suffix_entry.grid(row=1, column=1)
        
        # Apply button
        self.apply_btn = tk.Button(self.frm10, text="Apply", command=self.apply_prefix_suffix)
        self.apply_btn.grid(row=2, column=0, columnspan=2)

    def apply_prefix_suffix(self):
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        
        # Determine if any items are selected; if not, apply to all items
        selected_items = self.fn.tree_files.selection()
        if not selected_items:
            selected_items = self.fn.tree_files.get_children()
        
        if not selected_items:
            messagebox.showinfo("Info", "No files selected.")
            return
        
        for item_id in selected_items:
            old_name = self.fn.tree_files.item(item_id, 'text')
            new_name = f"{prefix}{old_name}{suffix}"
            self.fn.tree_files.item(item_id, values=(new_name,))
            self.fn.prefix_suffix(item_id, old_name, new_name)

            
        
##if __name__ == '__main__':
##    root = tk.Tk()
##    root.title('Complex Control with Tabs')
##    root.geometry('800x600')  # Set initial size of the window
##    ct = Ctrl_Tabs(root)
  



