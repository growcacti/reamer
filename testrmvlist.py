import tkinter as tk
from tkinter import simpledialog, messagebox
import re

class FilenameRemover:
    def __init__(self, parent):
        self.parent = parent
        self.filenames = ["example1.txt", "sample_test2.doc", "test3.pdf"]  # Example filenames
        
        # Display filenames
        self.listbox = tk.Listbox(parent)
        self.listbox.pack(padx=10, pady=10)
        self.update_listbox()

        # Button to remove patterns
        self.remove_button = tk.Button(parent, text="Remove Pattern", command=self.remove_pattern)
        self.remove_button.pack(pady=10)

    def update_listbox(self):
        """Update the displayed list of filenames."""
        self.listbox.delete(0, tk.END)  # Clear current items
        for filename in self.filenames:
            self.listbox.insert(tk.END, filename)

    def remove_pattern(self):
        """Prompt for a pattern and remove it from selected filenames."""
        pattern = simpledialog.askstring("Input", "Enter pattern to remove:", parent=self.parent)
        if pattern is not None:
            try:
                updated_filenames = []
                for filename in self.filenames:
                    updated_filename = re.sub(pattern, '', filename)  # Remove pattern
                    updated_filenames.append(updated_filename)
                self.filenames = updated_filenames
                self.update_listbox()
            except re.error as e:
                messagebox.showerror("Error", f"Invalid regular expression: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Filename Remover")
    app = FilenameRemover(root)
    root.mainloop()
