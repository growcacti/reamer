import tkinter as tk
from tkinter import ttk
import itertools
import string

# String manipulation functions
def concatenate(strings):
    return ', '.join(strings)

def permute(strings):
    perms = list(itertools.permutations(strings))
    return '; '.join([' '.join(p) for p in perms])

def number_strings(strings, prefix=True):
    if prefix:
        return [f"{i+1}_{s}" for i, s in enumerate(strings)]
    else:
        return [f"{s}_{i+1}" for i, s in enumerate(strings)]

def shift_characters(strings, n=1):
    def shift(s):
        return s[-n:] + s[:-n]
    return [shift(s) for s in strings]

# Function triggered by the button
def manipulate():
    user_input = entry.get()
    strings = [s.strip() for s in user_input.split(',')]
    selected_method = method_var.get()
    if selected_method == "Concatenate":
        result = concatenate(strings)
    elif selected_method == "Permute":
        result = permute(strings)
    elif selected_method == "Number (Prefix)":
        result = number_strings(strings, prefix=True)
    elif selected_method == "Number (Suffix)":
        result = number_strings(strings, prefix=False)
    elif selected_method == "Shift Characters":
        result = shift_characters(strings, shift_var.get())
    else:
        result = "Unknown method"
    result_text.delete(1.0, tk.END)  # Clear existing text
    result_text.insert(tk.END, result)  # Insert new result

# Setup GUI
root = tk.Tk()
root.title("String Manipulator")

# Layout using grid
entry = tk.Entry(root, width=50)
entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

method_var = tk.StringVar()
method_var.set("Concatenate")  # default value
method_dropdown = ttk.Combobox(root, textvariable=method_var)
method_dropdown['values'] = ("Concatenate", "Permute", "Number (Prefix)", "Number (Suffix)", "Shift Characters")
method_dropdown.grid(row=1, column=0, padx=10, pady=10)

shift_var = tk.IntVar(value=1)  # default shift value
shift_spinbox = tk.Spinbox(root, from_=-10, to=10, width=5, textvariable=shift_var)
shift_spinbox.grid(row=1, column=1, padx=10, pady=10)

manipulate_button = tk.Button(root, text="Manipulate", command=manipulate)
manipulate_button.grid(row=1, column=2, padx=10, pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
