import tkinter as tk
from tkinter import filedialog
import os
import time

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def generate_copy():
    original_file_path = entry_file_path.get()
    new_extension = entry_new_extension.get()

    if not original_file_path or not new_extension:
        label_status.config(text="Please select a file and enter a new extension.")
        return

    original_dir, original_file = os.path.split(original_file_path)
    original_name, original_ext = os.path.splitext(original_file)

    new_dir = os.path.join(original_dir, new_extension)
    os.makedirs(new_dir, exist_ok=True)

    epoch_time = int(time.time())
    new_file_name = f"{original_name}_{epoch_time}.{new_extension}"
    new_file_path = os.path.join(new_dir, new_file_name)

    with open(original_file_path, 'rb') as original_file:
        data = original_file.read()

    with open(new_file_path, 'wb') as new_file:
        new_file.write(data)

    label_status.config(text=f"File copied to: {new_file_path}")

# GUI setup
root = tk.Tk()
root.title("File Copier")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

label_file_path = tk.Label(frame, text="Select File:")
label_file_path.grid(row=0, column=0, sticky="e")

entry_file_path = tk.Entry(frame, width=50)
entry_file_path.grid(row=0, column=1, padx=5)

button_browse = tk.Button(frame, text="Browse...", command=select_file)
button_browse.grid(row=0, column=2)

label_new_extension = tk.Label(frame, text="New Extension:")
label_new_extension.grid(row=1, column=0, sticky="e")

entry_new_extension = tk.Entry(frame, width=20)
entry_new_extension.grid(row=1, column=1, padx=5)

button_generate = tk.Button(frame, text="Generate Copy", command=generate_copy)
button_generate.grid(row=2, columnspan=3, pady=10)

label_status = tk.Label(frame, text="", fg="green")
label_status.grid(row=3, columnspan=3)

root.mainloop()
