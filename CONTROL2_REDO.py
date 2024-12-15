import tkinter as tk
from tkinter import messagebox, ttk

MAX_NAME_LEN = 255

class TabbedControlFilters:
    def __init__(self, parent, file_navigator):
        self.parent = parent
        self.fn = file_navigator
        
        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, sticky='nsew', columnspan=3)  # Adjusted for a better layout
                self.varr2 = tk.BooleanVar()
        self.entry = tk.Entry(self.frm5)
        self.entry.grid(row=6, column=1, sticky="ew", padx=5)
        self.spinbox = ttk.Spinbox(self.frm5, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
        self.spinbox.grid(row=7, column=1, sticky="ew", padx=5)
               # Simplify frame creation and tab addition
        self.tabs = ['Regexp', 'Case', 'Replace', 'Numbering', 'Add to String', 'Shift Chars', 'Remove', 'Extension Replace', 'Name Basic', 'Fix Suffix Prefix', 'Custom', 'Custom2']
        self.frames = {}
        for tab in self.tabs:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab)
            self.frames[tab] = frame
            if tab == 'Regexp':
                self.setup_regexp_tab(frame)
            if tab == 'Case':
                self.setup_case_tab(frame)
            if tab == 'Replace':
                self.setup_replace_tab(frame)
            if tab =='Numbering':
                self.setup_numbering(frame)
            if tab == 'Add to String':
                self.setup_add_string(frame)
            if tab == 'Shift Chars':
                self.setup_add_string(frame)
            if tab == 'Remove':
                self.setup_add_string(frame)
            if tab == 'Extension Replace':
                self.setup_ext(frame)
            if tab == 'Name Basic':
                self.setup_add_string(frame)
            if tab == 'Fix Suffix Prefix':
                self.setup_add_string(frame)
            if tab == 'Custom':
                self.setup_custom(frame)
            if tab == 'Custom2':
                self.setup_custome2(frame)
            if tab == '3':
                self.setup_three(frame)
            if tab == '4':
                self.setup_four(frame)

        self.notebook.pack(expand=True, fill='both')  # Ensure the notebook expands to fill the space
    
    def setup_regexp_tab(self, frame):
        # Example setup for the Regexp tab
        tk.Label(frame, text="Match:").grid(row=0, column=0, padx=5, pady=5)
        self.match_entry = tk.Entry(frame)
        self.match_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        tk.Label(frame, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        self.replace_entry = tk.Entry(frame)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        apply_button = tk.Button(frame, text="Apply", command=self.apply_regexp)
        apply_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        
        frame.columnconfigure(1, weight=1)  # Make the second column within the frame expandable

    def apply_regexp(self):
        # Implementation for applying the regex operation
        pattern = self.match_entry.get()
        replace_pattern = self.replace_entry.get()
        # Simulated operation:
        print(f"Applying regex: Match '{pattern}' Replace with '{replace_pattern}'")
        # Actual implementation would involve invoking a method on `self.fn` with these parameters

