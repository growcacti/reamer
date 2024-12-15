import os
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk File Renamer with Treeview")
        self.root.geometry("900x600")

        # Directory selection
        tk.Label(root, text="Select Directory:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dir_entry = tk.Entry(root, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(root, text="Load Tree", command=self.load_tree).grid(row=0, column=3, padx=5, pady=5)

        # Options
        self.add_string = tk.StringVar()
        self.replace_string = tk.StringVar()
        self.delete_string = tk.StringVar()
        self.pattern = tk.StringVar()
        self.new_extension = tk.StringVar()
        self.recursive = tk.BooleanVar()
        self.verbose = tk.BooleanVar()

        tk.Label(root, text="Add String:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.add_string).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Replace String:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.replace_string).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Delete String:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.delete_string).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(root, text="Regex Pattern:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.pattern).grid(row=4, column=1, padx=5, pady=5)

        tk.Label(root, text="New Extension:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(root, textvariable=self.new_extension).grid(row=5, column=1, padx=5, pady=5)

        tk.Checkbutton(root, text="Recursive", variable=self.recursive).grid(row=6, column=0, columnspan=2, sticky="w")
        tk.Checkbutton(root, text="Verbose", variable=self.verbose).grid(row=6, column=1, columnspan=2, sticky="w")

        # Treeview for Directory and Files
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.tree = ttk.Treeview(self.tree_frame, columns=("Type", "Size"), show="tree headings")
        self.tree.heading("#0", text="Name", anchor="w")
        self.tree.heading("Type", text="Type", anchor="w")
        self.tree.heading("Size", text="Size", anchor="e")
        self.tree.column("#0", stretch=True)
        self.tree.column("Type", width=100, anchor="w")
        self.tree.column("Size", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True)

        # Action Buttons
        tk.Button(root, text="Rename Files", command=self.rename_files).grid(row=8, column=1, padx=5, pady=5)
        tk.Button(root, text="Exit", command=root.quit).grid(row=8, column=2, padx=5, pady=5)

        # Status
        self.status_label = tk.Label(root, text="", anchor="w")
        self.status_label.grid(row=9, column=0, columnspan=4, padx=5, pady=5, sticky="w")

        # Configure grid weights
        root.grid_rowconfigure(7, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def load_tree(self):
        directory = self.dir_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return
        self.tree.delete(*self.tree.get_children())
        self.insert_tree_items("", directory)

    def insert_tree_items(self, parent, path):
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    folder_id = self.tree.insert(parent, "end", text=item, values=("Folder", ""), open=False)
                    self.insert_tree_items(folder_id, full_path)  # Recursive for subdirectories
                else:
                    size = os.path.getsize(full_path)
                    self.tree.insert(parent, "end", text=item, values=("File", f"{size} bytes"))
        except PermissionError:
            pass  # Skip folders without permission

    def rename_files(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected for renaming.")
            return

        directory = self.dir_entry.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return

        for item in selected_items:
            item_text = self.tree.item(item, "text")
            parent = self.tree.parent(item)
            parent_path = self.get_parent_path(parent)
            old_path = os.path.join(parent_path, item_text)
            new_name = self.apply_renaming_rules(item_text)
            new_path = os.path.join(parent_path, new_name)

            if os.path.exists(old_path) and old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    if self.verbose.get():
                        print(f"Renamed: {old_path} -> {new_path}")
                    self.tree.item(item, text=new_name)  # Update the Treeview
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename {old_path}: {str(e)}")

        self.status_label.config(text="Renaming completed.")

    def get_parent_path(self, parent):
        if not parent:
            return self.dir_entry.get()
        parent_text = self.tree.item(parent, "text")
        grandparent = self.tree.parent(parent)
        return os.path.join(self.get_parent_path(grandparent), parent_text)

    def apply_renaming_rules(self, filename):
        new_name, ext = os.path.splitext(filename)
        if self.add_string.get():
            new_name = f"{self.add_string.get()}{new_name}"
        if self.replace_string.get():
            new_name = new_name.replace(self.replace_string.get(), "")
        if self.delete_string.get():
            new_name = new_name.replace(self.delete_string.get(), "")
        if self.pattern.get():
            new_name = re.sub(self.pattern.get(), "", new_name)
        if self.new_extension.get():
            ext = self.new_extension.get()
        return f"{new_name}{ext}"


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
