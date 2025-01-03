import os
import re
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from time import localtime, strftime


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Renamer with Treeview")
        self.root.geometry("1000x700")

        # Directory selection
        tk.Label(root, text="Select Directory:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dir_entry = tk.Entry(root, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)

        # Treeview for folder and file structure
        self.tree = ttk.Treeview(root, columns=("Type"), show="tree headings", height=20)
        self.tree.heading("#0", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.column("Type", width=150, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Scrollbar for Treeview
        tree_scroll = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=tree_scroll.set)
        tree_scroll.grid(row=1, column=3, sticky="ns")

        # Options
        self.add_string = tk.StringVar()
        self.replace_string = tk.StringVar()
        self.delete_string = tk.StringVar()
        self.pattern = tk.StringVar()
        self.new_extension = tk.StringVar()
        self.recursive = tk.BooleanVar()
        self.verbose = tk.BooleanVar()
        self.skip_char_pos = tk.IntVar(value=0)
        self.ztrip_char_pos = tk.IntVar(value=0)

        tk.Label(root, text="Add String:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.add_string).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Replace String:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.replace_string).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(root, text="Delete String:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.delete_string).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(root, text="Regex Pattern:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.pattern).grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="New Extension:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.new_extension).grid(row=6, column=1, padx=5, pady=5)

        tk.Label(root, text="Skip Chars:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        tk.Spinbox(root, from_=0, to=100, textvariable=self.skip_char_pos).grid(row=7, column=1, padx=5, pady=5)

        tk.Label(root, text="Trim Chars:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        tk.Spinbox(root, from_=0, to=100, textvariable=self.ztrip_char_pos).grid(row=8, column=1, padx=5, pady=5)

        tk.Checkbutton(root, text="Recursive", variable=self.recursive).grid(row=9, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(root, text="Verbose", variable=self.verbose).grid(row=9, column=1, columnspan=2, sticky="w")

        # Action Buttons
        tk.Button(root, text="Load Files", command=self.load_files).grid(row=10, column=0, padx=5, pady=5)
        tk.Button(root, text="Rename Files", command=self.rename_files).grid(row=10, column=1, padx=5, pady=5)
        tk.Button(root, text="Exit", command=root.quit).grid(row=10, column=2, padx=5, pady=5)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.load_files()

    def load_files(self):
        self.tree.delete(*self.tree.get_children())
        directory = self.dir_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return
        for root, dirs, files in os.walk(directory) if self.recursive.get() else [(directory, [], os.listdir(directory))]:
            for name in dirs:
                self.tree.insert("", "end", text=name, values=["Folder"])
            for name in files:
                self.tree.insert("", "end", text=name, values=["File"])

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            filename = self.tree.item(selected_item[0])["text"]
            self.status_message(f"Selected: {filename}")

    def status_message(self, message):
        print(message)

    def rename_files(self):
        directory = self.dir_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return
        for item_id in self.tree.get_children():
            old_name = self.tree.item(item_id, "text")
            new_name = self.apply_renaming_rules(old_name)
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            if os.path.exists(old_path):
                try:
                    os.rename(old_path, new_path)
                    self.tree.item(item_id, text=new_name)
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

    def apply_renaming_rules(self, filename):
        # Methods for renaming operations
        new_name = filename
        new_name = self.skip_name(new_name, self.skip_char_pos.get())
        new_name = self.ztrip_name(new_name, self.ztrip_char_pos.get())
        if self.add_string.get():
            new_name = f"{self.add_string.get()}{new_name}"
        if self.replace_string.get():
            new_name = new_name.replace(self.replace_string.get(), "")
        if self.delete_string.get():
            new_name = new_name.replace(self.delete_string.get(), "")
        if self.pattern.get():
            new_name = re.sub(self.pattern.get(), "", new_name)
        if self.new_extension.get():
            _, ext = os.path.splitext(new_name)
            new_name = new_name.replace(ext, self.new_extension.get())
        return new_name

    # Methods extracted from functions
    def skip_name(self, filename, skip):
        return filename[skip:].strip()

    def ztrip_name(self, filename, skip):
        return filename[:-skip] if skip < len(filename) else filename


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
