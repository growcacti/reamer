import tkinter as tk
from tkinter import ttk

class StringManipulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("String Manipulator")

        # Counter for numbering
        self.counter = 0

        # Setup GUI components
        self.entry = tk.Entry(master, width=50)
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.method_var = tk.StringVar()
        self.method_var.set("Concatenate")  # default value
        self.method_dropdown = ttk.Combobox(master, textvariable=self.method_var, width=47)
        self.method_dropdown['values'] = ("Concatenate", "Number (Prefix)", "Number (Suffix)")
        self.method_dropdown.grid(row=1, column=0, padx=10, pady=10)

        self.manipulate_button = tk.Button(master, text="Manipulate", command=self.manipulate)
        self.manipulate_button.grid(row=1, column=2, padx=10, pady=10)

        self.result_text = tk.Text(master, height=10, width=50)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def manipulate(self):
        user_input = self.entry.get()
        strings = [s.strip() for s in user_input.split(',')]
        selected_method = self.method_var.get()

        if selected_method == "Concatenate":
            result = self.concatenate(strings)
        elif selected_method == "Number (Prefix)":
            result = self.number_strings(strings, prefix=True)
        elif selected_method == "Number (Suffix)":
            result = self.number_strings(strings, prefix=False)
        else:
            result = ["Unknown method"]

        self.result_text.delete(1.0, tk.END)  # Clear existing text
        self.result_text.insert(tk.END, '\n'.join(result))  # Insert new result

    def concatenate(self, strings):
        self.counter += 1
        return [f"{self.counter}. " + ', '.join(strings)]

    def number_strings(self, strings, prefix=True):
        result = []
        for s in strings:
            self.counter += 1
            if prefix:
                result.append(f"{self.counter}_{s}")
            else:
                result.append(f"{s}_{self.counter}")
        return result

# Main application
def main():
    root = tk.Tk()
    app = StringManipulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
