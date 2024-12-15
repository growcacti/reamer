import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

class BulkFileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Copier with Renaming")
        self.directory = ""
        self.new_directory = ""
        
        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Label for directory selection
        self.dir_label = tk.Label(self.root, text="No directory selected")
        self.dir_label.pack(pady=10)
        
        # Button to select directory
        self.select_button = tk.Button(self.root, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)
        
        # Entry to input custom name
        self.name_label = tk.Label(self.root, text="Enter new file name:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.pack(pady=5)
        
        # Button to start renaming
        self.rename_button = tk.Button(self.root, text="Copy and Rename Files", command=self.copy_and_rename_files, state=tk.DISABLED)
        self.rename_button.pack(pady=10)
        
        # Listbox to display files
        self.file_listbox = tk.Listbox(self.root, width=60, height=15)
        self.file_listbox.pack(pady=10)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.dir_label.config(text=f"Selected directory: {self.directory}")
            self.rename_button.config(state=tk.NORMAL)
            self.load_files()
        else:
            self.dir_label.config(text="No directory selected")
            self.rename_button.config(state=tk.DISABLED)

    def load_files(self):
        # Clear the listbox
        self.file_listbox.delete(0, tk.END)
        
        for root, _, files in os.walk(self.directory):
            for filename in files:
                self.file_listbox.insert(tk.END, filename)

    def create_new_directory(self):
        # Create a new directory to store renamed copies
        base_directory = os.path.join(self.directory, "Renamed_Files")
        counter = 1
        new_directory = base_directory
        
        # Ensure directory name is unique
        while os.path.exists(new_directory):
            new_directory = base_directory + f"_{counter}"
            counter += 1
        
        os.makedirs(new_directory)
        self.new_directory = new_directory

    def copy_and_rename_files(self):
        custom_name = self.name_entry.get()
        if not custom_name:
            messagebox.showwarning("Warning", "Please enter a name for the files!")
            return
        
        self.create_new_directory()  # Create new directory for the renamed files
        counter = 1
        renamed_files_count = 0
        
        try:
            for root, _, files in os.walk(self.directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    name, extension = os.path.splitext(filename)
                    new_file = os.path.join(self.new_directory, f"{custom_name}{counter}{extension}")
                    
                    # Ensure a unique filename
                    while os.path.exists(new_file):
                        counter += 1
                        new_file = os.path.join(self.new_directory, f"{custom_name}{counter}{extension}")
                    
                    # Copy the original file to the new directory with a new name
                    shutil.copy(filepath, new_file)
                    counter += 1
                    renamed_files_count += 1

            messagebox.showinfo("Success", f"Copied and renamed {renamed_files_count} files to '{self.new_directory}'!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Set up the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = BulkFileRenamer(root)
    root.mainloop()
