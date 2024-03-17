import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import os

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer Tool")
        self.root.geometry("800x600")  # Adjust size as needed

        self.path = os.getcwd()
        self.output_folder = ''

       
        self.create_menu()

 
        self.list_frame = ttk.Frame(self.root)
        self.list_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.root.grid_columnconfigure(1, weight=1)

        # Original File List
        self.original_file_list_label = ttk.Label(self.list_frame, text="Original Filenames")
        self.original_file_list_label.grid(row=0, column=0, padx=5, pady=5)

        self.original_file_list = tk.Listbox(self.list_frame, width=50, height=20)
        self.original_file_list.grid(row=1, column=0,columnspan=3, padx=5, pady=5, sticky="nsew")

        # Changed File List
        self.changed_file_list_label = ttk.Label(self.list_frame, text="New Filenames")
        self.changed_file_list_label.grid(row=0, column=4, padx=5, pady=5)

        self.changed_file_list = tk.Listbox(self.list_frame, width=50, height=20)
        self.changed_file_list.grid(row=1, column=4,columnspan=3, padx=5, pady=5, sticky="nsew")

        self.list_frame.grid_rowconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=1)

        # Rename Options Frame
        self.rename_frame = ttk.Frame(self.root)
        self.rename_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.rename_frame, text="Prefix:").grid(row=0, column=0, padx=5, pady=5)
        self.prefix_entry = ttk.Entry(self.rename_frame)
        self.prefix_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.rename_frame, text="Suffix:").grid(row=1, column=0, padx=5, pady=5)
        self.suffix_entry = ttk.Entry(self.rename_frame)
        self.suffix_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(self.rename_frame, text="Preview Rename", command=self.preview_rename).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.rename_frame.grid_columnconfigure(1, weight=1)
        self.prefix_entry.bind('<KeyRelease>', lambda event: self.update_preview())
        self.suffix_entry.bind('<KeyRelease>', lambda event: self.update_preview())
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Select Directory", command=self.select_directory)
        self.file_menu.add_command(label="update preview", command=self.update_preview)
        self.file_menu.add_command(label="preview rename", command=self.preview_rename)
        self.file_menu.add_command(label="preview rename", command=self.apply_rename)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

    def select_directory(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.preview_rename()
    def update_preview(self):
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        self.changed_file_list.delete(0, tk.END)  # Clear the list before updating

        for index in range(self.original_file_list.size()):
            original_filename = self.original_file_list.get(index)
            base_name, ext = os.path.splitext(original_filename)
            new_filename = f"{prefix}{base_name}{suffix}{ext}"
            self.changed_file_list.insert(tk.END, new_filename)


    def preview_rename(self):
        self.original_file_list.delete(0, tk.END)
        self.changed_file_list.delete(0, tk.END)

        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()

        try:
            for file in os.listdir(self.path):
                self.original_file_list.insert(tk.END, file)
                base_name, ext = os.path.splitext(file)
                new_filename = f"{prefix}{base_name}{suffix}{ext}"
                self.changed_file_list.insert(tk.END, new_filename)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read directory contents: {e}")
    def apply_rename(self):
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()

        for index in range(self.original_file_list.size()):
            original_filename = self.original_file_list.get(index)
            base_name, ext = os.path.splitext(original_filename)
            new_filename = f"{prefix}{base_name}{suffix}{ext}"

            original_path = os.path.join(self.path, original_filename)
            new_path = os.path.join(self.path, new_filename)

            try:
                os.rename(original_path, new_path)
            except OSError as e:
                messagebox.showerror("Error", f"Failed to rename '{original_filename}' to '{new_filename}': {e}")
                return

        messagebox.showinfo("Success", "Files renamed successfully!")
        self.populate_file_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
