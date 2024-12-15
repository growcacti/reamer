import os
import tkinter as tk
from tkinter import filedialog, messagebox

class BulkFileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Renamer")
        self.directory = ""
        
        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Label for directory selection
        self.dir_label = tk.Label(self.root, text="No directory selected")
        self.dir_label.pack(pady=10)
        
        # Button to select directory
        self.select_button = tk.Button(self.root, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=10)
        
        # Button to start renaming
        self.rename_button = tk.Button(self.root, text="Rename Files", command=self.rename_files, state=tk.DISABLED)
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

    def rename_files(self):
        counter = 0
        renamed_files_count = 0
        
        try:
            for root, _, files in os.walk(self.directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    name, extension = os.path.splitext(filename)
                    new_file = os.path.join(root, str(counter) + extension)
                    
                    # Ensure a unique filename
                    while os.path.exists(new_file):
                        counter += 1
                        new_file = os.path.join(root, str(counter) + extension)
                    
                    # Rename the file
                    os.rename(filepath, new_file)
                    counter += 1
                    renamed_files_count += 1

            messagebox.showinfo("Success", f"Renamed {renamed_files_count} files!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Set up the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = BulkFileRenamer(root)
    root.mainloop()
