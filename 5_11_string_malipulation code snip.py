import tkinter as tk
from tkinter import ttk
import itertools
import functools
import string

# String manipulation functions
def concatenate(strings):

    return ', '.join(strings)

def permute(strings):
    perms = list(itertools.permutations(strings))
    output = '; '.join(['strings '.join(p) for p in perms])
    result_text.insert("1.0", output)

# Function triggered by the button
def manipulate():
    user_input = entry.get()
    strings = [s.strip() for s in user_input.split(',')]
    selected_method = method_var.get()
    if selected_method == "Concatenate":
        result = concatenate(strings)
    elif selected_method == "Permute":
        result = permute(strings)
    else:
        result = "Unknown method"
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.insert(tk.END, result)  # Insert new result

# Setup GUI
root = tk.Tk()
root.title("String Manipulator")

# Layout using grid
entry = tk.Entry(root, width=50)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

method_var = tk.StringVar()
method_var.set("Concatenate")  # default value
method_dropdown = ttk.Combobox(root, textvariable=method_var)
method_dropdown['values'] = ("Concatenate", "Permute")
method_dropdown.grid(row=1, column=0, padx=10, pady=10)

manipulate_button = tk.Button(root, text="Manipulate", command=manipulate)
manipulate_button.grid(row=1, column=1, padx=10, pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
