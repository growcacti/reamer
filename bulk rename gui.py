import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

class FileRenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Renamer")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        # Directory Selection
        self.dir_label = tk.Label(self, text="Select Directory:")
        self.dir_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.dir_entry = tk.Entry(self, width=40)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        self.dir_button = tk.Button(self, text="Browse", command=self.select_directory)
        self.dir_button.grid(row=0, column=2, padx=5, pady=5)

        # Rename Options
        self.option_label = tk.Label(self, text="Choose Rename Format:")
        self.option_label.grid(row=1, column=0, columnspan=3, pady=5)

        self.rename_var = tk.IntVar()
        options = [
            ("1. Number-Text-Oldname", 1),
            ("2. Number-Only", 2),
            ("3. Date", 3),
            ("4. UPPERCASE", 4),
            ("5. lowercase", 5),
            ("6. Search/Replace", 6)
        ]

        for i, (text, value) in enumerate(options):
            tk.Radiobutton(self, text=text, variable=self.rename_var, value=value).grid(row=2+i, column=0, columnspan=3, sticky='w')

        # Search/Replace Inputs
        self.search_label = tk.Label(self, text="Search String:")
        self.search_label.grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=8, column=1, padx=5, pady=5)

        self.replace_label = tk.Label(self, text="Replace With:")
        self.replace_label.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        self.replace_entry = tk.Entry(self)
        self.replace_entry.grid(row=9, column=1, padx=5, pady=5)

        # Start Button
        self.start_button = tk.Button(self, text="Start Renaming", command=self.start_renaming)
        self.start_button.grid(row=10, column=0, columnspan=3, pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def start_renaming(self):
        path = self.dir_entry.get()
        if not os.path.isdir(path):
            messagebox.showerror("Error", "Invalid Directory")
            return

        rename_type = self.rename_var.get()
        file_list = os.listdir(path)

        for count, filename in enumerate(file_list, 1):
            source_file = os.path.join(path, filename)

            if rename_type == 1:
                new_name = f"{count}.{filename}"
            elif rename_type == 2:
                new_name = f"{count}"
            elif rename_type == 3:
                date_today = datetime.datetime.today().strftime('%d-%b-%Y')
                new_name = f"{date_today} {filename}"
            elif rename_type == 4:
                new_name = filename.upper()
            elif rename_type == 5:
                new_name = filename.lower()
            elif rename_type == 6:
                search_str = self.search_entry.get()
                replace_str = self.replace_entry.get()
                if search_str and replace_str:
                    new_name = filename.replace(search_str, replace_str)
                else:
                    messagebox.showerror("Error", "Enter search and replace strings for option 6")
                    return
            else:
                messagebox.showerror("Error", "Select a renaming option")
                return

            new_file_path = os.path.join(path, new_name)
            os.rename(source_file, new_file_path)

        messagebox.showinfo("Success", "Files renamed successfully!")

if __name__ == "__main__":
    app = FileRenamerApp()
    app.mainloop()
