import os
import re
import tkinter as tk
from tkinter import ttk, Menu, Toplevel, filedialog

import time
from fix import *


class DirectoryTreeNavigator:
    def __init__(self, root, path, on_directory_selected=None):
        self.path = path
        self.nodes = {}  # Tracks the nodes that have been expanded.

        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, sticky="nsew")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

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

    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root)
        self.frame.grid(row=1, column=1, sticky="we")
        self.frame.columnconfigure(2, weight=1)
        self.active_path = ""
        self.rename_history = []
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
        self.info_bar = InfoBar(self.root,self)
        self.bind_entries()

    def init_prefix_suffix_feature(self):
        PrefixSuffixApplication(self)



    def bind_entries(self):
        # Existing bindings
            self.tree_files.bind("<<TreeviewOpen>>", self.on_directory_expand)
            self.tree_files.bind("<<TreeviewSelect>>", self.on_double_click)
            self.tree_files.bind("<<TreeviewSelect>>", self.on_selection_change)

    def on_directory_expand(self, event):
        item_id = self.tree_files.focus()  # Get the ID of the node being expanded
    
    def populate_tree(self, parent, path):
        for entry in os.scandir(path):
            if entry.is_file():  # This line is modified to only check for files
                self.insert_node(parent, entry)


    def insert_node(self, parent, entry, tag=""):
        # Assuming entry has 'path' and 'name' attributes correctly assigned
        node_id = self.tree_files.insert(parent, "end", iid=entry.path, text=entry.name, values=(entry.name,), tags=(tag,))
      
    def apply_conditional_rename(self, pattern, start_num=1):
        selected_items = self.tree_files.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected for renaming.")
            return

        condition_pattern = re.compile(r'\{if:ext=(\.\w+)\}(.+?)\{else\}(.+?)\{endif\}')
        num = start_num
        for item_id in selected_items:
            old_name = self.tree_files.item(item_id, 'text')
            extension = os.path.splitext(old_name)[1]
            base_name = os.path.splitext(old_name)[0]

            # Check if the pattern includes a conditional statement
            match = condition_pattern.search(pattern)
            if match:
                condition_ext, if_true, if_false = match.groups()
                # Apply the conditional renaming
                if extension == condition_ext:
                    new_name = if_true.replace('{num}', str(num)).replace('{name}', base_name)
                else:
                    new_name = if_false.replace('{num}', str(num)).replace('{name}', base_name)
            else:
                # Fallback to a simple pattern replacement if no condition is found
                new_name = pattern.replace('{num}', str(num)).replace('{name}', base_name)

            new_path = os.path.join(self.active_path, new_name + extension)
            old_path = os.path.join(self.active_path, old_name)

            try:
                os.rename(old_path, new_path)
                self.tree_files.item(item_id, text=new_name + extension)
                num += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file {old_name} to {new_name}: {e}")
                break  # Stop the renaming process on error

        messagebox.showinfo("Success", "Conditional rename completed successfully.")


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
        preview_window = tk.Toplevel(self.root)
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


    def generate_new_name(self, current_name, pattern, num):
        base, ext = os.path.splitext(current_name)
        # Basic conditional pattern matching (simplified for example purposes)
        condition_match = re.search(r'\{ifext:(\w+)\}(.+?)\{else\}(.+?)\{endif\}', pattern)
        if condition_match:
            condition_ext, if_pattern, else_pattern = condition_match.groups()
            # Check if the extension matches the condition
            if ext[1:].lower() == condition_ext.lower():  # Removing the dot from the extension and case-insensitive comparison
                pattern = if_pattern
            else:
                pattern = else_pattern

        # Replace placeholders in the chosen pattern
        new_name = pattern.replace("{name}", base).replace("{num}", f"{num:02d}").replace("{ext}", ext)
        return new_name
    def rename_files(self, pattern):
        selected_items = self.tree_files.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for renaming.")
            return
             
         
        if messagebox.askyesno("Confirm Rename", "Do you want to proceed with renaming the selected files?"):
            num = 1  # Starting number for sequential numbering
            for item_id in selected_items:
                current_name = self.tree_files.item(item_id, 'text')
                new_name = self.generate_new_name(current_name, pattern, num)
                old_path = os.path.join(self.active_path, current_name)
                new_path = os.path.join(self.active_path, new_name)
                

                try:
                    os.rename(old_path, new_path)
                    # Update the item in the tree view to reflect the new name
                    self.tree_files.item(item_id, text=new_name)
                    self.rename_history.append((old_path, new_path))
                    num += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename '{current_name}' to '{new_name}': {e}")
                    break  # Stop the renaming process on error
            messagebox.showinfo("Success", "Files have been renamed successfully.")
    def on_selection_change(self, event=None):
        # When the selection changes, refresh the info bar to show the new selection count.
        self.info_bar.num_items_refresh()

    def right_click_path_to_clip(self, event):
        path = self.tree_files.identify_row(event.y)
        if not path:
            messagebox.showinfo("Info", "No item selected.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(path)
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

    def update_new_name_preview(self, suffix):
        for item_id in self.tree_files.get_children():
            original_name = self.tree_files.item(item_id, 'text')
            new_name = f"{original_name}{suffix}"
            self.tree_files.item(item_id, values=(new_name,))

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


    def rename_selected_file(self): 
        selected_items = self.tree_files.selection()
        
        if not selected_items:
            messagebox.showinfo("Info", "No file selected for renaming.")
            return

        # Assuming single selection for simplicity
        item_id = selected_items[0]
       
        old_name = self.tree_files.item(item_id, 'text')
        old_path = os.path.join(self.active_path, old_name)

        new_name = simpledialog.askstring("Rename", "Enter new name for the file:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            # No change made or cancelled
            return

        new_path = os.path.join(self.active_path, new_name)
        try:
            os.rename(old_path, new_path)
            # Update the tree view to reflect the change
            self.tree_files.item(item_id, text=new_name)
            messagebox.showinfo("Success", "File renamed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename file: {e}")

class InfoBar:
    def __init__(self, root, fn):
        self.fn = fn  # Reference to the FileNavigator instance
        self.frame = ttk.Frame(root)
        self.frame.grid(column=0, row=2, columnspan=2, sticky="we")  # Ensure it spans across the window
        self.frame.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()
        self.num_items_refresh()

        # Items label
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
        self.initial_path = os.path.expanduser("~")  # Set initial path to the user's home directory
        self.pathlist = []
        # Initialize main and lower frames
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=5)
        self.lower_frame = ttk.Frame(self)
        self.lower_frame.grid(row=1, column=0, sticky="nsew", padx=(5, 5), pady=5)
        
        # Configure window to expand frames with size
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=4)  # Main frame gets more weight
        self.rowconfigure(1, weight=1)  # Lower frame gets less weight
        self.fn = FileNavigator(self.main_frame)
        self.undo_button = ttk.Button(self.main_frame, text="Undo Last Rename", command=self.fn.undo_last_rename)
        self.undo_button.grid(row=3, column=0, padx=5, pady=5)  # Adjust grid positioning as needed
        # Initialize components
        self.dtn = DirectoryTreeNavigator(self.main_frame, self.initial_path, self.fn.refresh_view)

      
        self.fn.frame.grid(row=0, column=1, sticky="nsew")
        
        # Adjust main_frame layout
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
       # Menubar setup

        self.menubar = Menu(self, tearoff=False)
        self.file_menu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
      
        self.file_menu.add_command(label="Go To Target Directory", command=self.targetdir)
        self.config(menu=self.menubar)

        self.config(menu=self.menubar)
     

        # Initialize other components like InfoBar and TabbedControlFilters
        self.infobar = InfoBar(self.main_frame, self.fn)
        self.fn.update_view(self.initial_path)  # Example initial path setup
        self.fn.info_bar = self.infobar 

     
      
             
        # Configure the menubar
        self.config(menu=self.menubar)        
    def targetdir(self):
            directory_path = filedialog.askdirectory()
            self.pathlist.append(directory_path)
            self.dtn.path_entry.delete(0, tk.END)
            self.dtn.path_entry.insert(0, directory_path)
            return directory_path



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()






