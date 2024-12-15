import tkinter as tk
from tkinter import messagebox, ttk
import re
import string
import random
MAX_NAME_LEN = 255

class TabbedControlFilters:
    def __init__(self, parent, file_navigator):
        self.parent = parent
        self.fn = file_navigator
        
        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, sticky='nsew')
        self.frm1 = ttk.Frame(self.notebook)
        self.frm2 = ttk.Frame(self.notebook)
        self.frm3 = ttk.Frame(self.notebook)
        self.frm4 = ttk.Frame(self.notebook)
        self.frm5 = ttk.Frame(self.notebook)
        self.frm6 = ttk.Frame(self.notebook)
        self.frm7 = ttk.Frame(self.notebook)
        self.frm8 = ttk.Frame(self.notebook)
        self.frm9 = ttk.Frame(self.notebook)
        self.frm10 = ttk.Frame(self.notebook)
        self.frm11 = ttk.Frame(self.notebook)
        self.frm12 = ttk.Frame(self.notebook)
      
         
        self.frm1.grid(row=1, column=1)
        self.frm2.grid(row=1, column=2)
        self.frm3.grid(row=1, column=3)
        self.frm4.grid(row=1, column=4)
        self.frm5.grid(row=1, column=5)
        self.frm6.grid(row=1, column=6)
        self.frm7.grid(row=0, column=7)
        self.frm8.grid(row=1, column=8)
        self.frm9.grid(row=1, column=9)
        self.frm10.grid(row=1, column=10)
        self.frm11.grid(row=1, column=11)
        self.frm12.grid(row=1, column=12)

        self.notebook.add(self.frm1, text='Regexp')
        
       
        self.can1 = tk.Canvas(self.frm1, bg="SlateGray4",bd=20,width=100, height=40)
        self.can1.grid(row=1, column=1)
        self.frm1.columnconfigure(0, weight=1)
        self.frm1.rowconfigure(0, weight=1)

 
        tk.Label(self.can1, text="Match & Replace Regular Expression").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self.can1, text="                                     ").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(self.can1, text="Match:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.match_entry = tk.Entry(self.can1)
        self.match_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(self.can1, text="Replace:").grid(row=4, column=0, sticky="w")
        self.replace_entry = tk.Entry(self.can1)
        self.replace_entry.grid(row=4, column=1, sticky="ew")

        self.apply_button = tk.Button(self.can1, text="Apply", command=self.apply_regexp)
        self.apply_button.grid(row=6, column=2, sticky="e", padx=5, pady=5)

                
     
        self.notebook.add(self.frm2, text='Case')
        
        self.can2= tk.Canvas(self.frm2, background="azure4",bd=10)
        self.can2.grid(row=1,column=0)

        # Dropdown for case selection
        tk.Label(self.can2, text="").grid(row=1, column=0)
        tk.Label(self.can2, text="").grid(row=1, column=1)
        tk.Label(self.can2, text="Select Case").grid(row=2, column=2)
        self.case_type_combobox = ttk.Combobox(self.can2, values=["Upper", "Lower", "Title","Capitalize","SwapCase","Strip"])
        self.case_type_combobox.grid(row=3,column=2)

        # Apply button
        self.apply_button = tk.Button(self.can2, text="Apply", command=lambda : self.apply_case_change())
        self.apply_button.grid(row=3,column=3)

        self.notebook.add(self.frm3, text='Replace ')
       
        self.can3= tk.Canvas(self.frm3, background="dark sea green",bd=150)
        self.can3.grid(row=1,column=0)
        # Entry for match pattern
        tk.Label(self.can3, text="Replace:").grid(row=2,column=2)
        self.match_entry = tk.Entry(self.can3)
        self.match_entry.grid(row=3, column=3)

        # Entry for replace pattern
        tk.Label(self.can3, text="With:").grid(row=4,column=3)
        self.replace_entry = tk.Entry(self.can3)
        self.replace_entry.grid(row=5, column=3)

        # Apply button
        self.apply_button = tk.Button(self.can3, text="Apply", command=None)
        self.apply_button.grid(row=7,column=3)
       
     
        self.notebook.add(self.frm4, text='Numbering')
        self.can4= tk.Canvas(self.frm4, background="seashell3",bd=15)
        self.can4.grid(row=1,column=0)
        self.apply_button = tk.Button(self.can4, text="Apply", command=None)
        self.apply_button.grid(row=2, column=2)
        # Starting Number
        tk.Label(self.can4, text="Starting Number:").grid(row=0, column=0)
        self.start_num_entry = tk.Entry(self.can4)
        self.start_num_entry.grid(row=0, column=1)
        self.start_num_entry.insert(0, "1")  # Default starting number

        # Prefix or Suffix
        tk.Label(self.can4, text="Position:").grid(row=1, column=0)
        self.position_combobox = ttk.Combobox(self.can4, values=["Prefix", "Suffix"])
        self.position_combobox.grid(row=1, column=1)
        self.position_combobox.current(0)  # Default to Prefix

        # Delimiter
        tk.Label(self.can4, text="Delimiter:").grid(row=2, column=0)
        self.delimiter_entry = tk.Entry(self.can4)
        self.delimiter_entry.grid(row=2, column=1)
        self.delimiter_entry.insert(0, "_")  # Default delimiter

        # Apply Button
        self.apply_numbering_button = tk.Button(self.can4, text="Apply Numbering", command=self.apply_numbering)
        self.apply_numbering_button.grid(row=3, column=0, columnspan=2)

        self.notebook.add(self.frm5, text='Add to String')
        self.can5= tk.Canvas(self.frm5, background="LavenderBlush3",bd=150)
        self.can5.grid(row=1,column=0)

        self.varr2 = tk.BooleanVar()
        self.entry = tk.Entry(self.can5)
        self.entry.grid(row=6, column=1, sticky="ew", padx=5)
        self.spinbox = ttk.Spinbox(self.can5, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
        self.spinbox.grid(row=7, column=1, sticky="ew", padx=5)
        self.checkbutton = ttk.Checkbutton(self.can5, text="label_text", variable=self.varr2)
        self.checkbutton.grid(row=9, column=0, columnspan=2, sticky="w", padx=5)
        
        self.frm5.columnconfigure(0, weight=1)
        self.frm5.rowconfigure(0, weight=1)
        self.notebook.add(self.frm6, text='Shift Chars')
        self.can6 = tk.Canvas(self.frm6, background="plum3",bd=15)
        self.can6.grid(row=1,column=0)
        tk.Label(self.can6, text="").grid(row=1,column=1)
        tk.Label(self.can6, text="").grid(row=2,column=2)
        tk.Label(self.can6, text="Shift Value:").grid(row=3,column=3)
        self.sp =tk.Spinbox(self.can6, from_=-26,to=26, width=10)
        self.sp.grid(row=4,column=3)
        self.b1 = tk.Button(self.can6, text="Send", command=lambda : self.fn.shiftrename_files(self.sp.get()))
        self.b1.grid(row=6, column=3)
        self.notebook.add(self.frm7, text='Remove')
        self.can7= tk.Canvas(self.frm7, background="MistyRose4",bd=15)
        self.can7.grid(row=1,column=0)
      
        tk.Label(self.can7, text="Remove first n characters:",).grid(row=0, column=3)
        self.first_n = tk.IntVar()
        self.sp1 = tk.Spinbox(self.can7, from_=0, to=MAX_NAME_LEN)
        self.sp1.grid(row=5, column=3)

        tk.Label(self.can7, text="Remove last n characters:",).grid(row=1, column=0)
        self.last_n = tk.IntVar()
        self.sp2 = tk.Spinbox(self.can7, from_=0, to=MAX_NAME_LEN)
        self.sp2.grid(row=7, column=3)
        self.btn1 =tk.Button(self.can7, text="Apply", command=self.apply_removal)
        self.btn1.grid(row=8, column=0, columnspan=2)
        self.frm7.columnconfigure(2, weight=1)
        self.frm7.rowconfigure(2, weight=1)
        self.notebook.add(self.frm8, text='Extension Replace ')
        
        self.can8 = tk.Canvas(self.frm8,background="azure4",borderwidth=8,width=100, height=40) 
        self.can8.grid(row=1, column=1)
        
       
        self.new_ext_entry = tk.Entry(self.can8, width=20)
        self.new_ext_entry.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

        self.sendchange_button = tk.Button(self.can8, text="Change ext", command=self.ext_change)
        self.sendchange_button.grid(column=1, row=4, padx=5, pady=5)

        self.reset_button = tk.Button(self.can8, text="Reset", command=self.reset_widget)
        self.reset_button.grid(column=2, row=0, padx=5, pady=5)

       
        self.notebook.add(self.frm9, text='Name Basic')
        self.can9= tk.Canvas(self.frm9, background="thistle3",bd=15)
        self.can9.grid(row=1,column=0)
        tk.Label(self.can9, text="Name").grid(column=0, row=0, sticky="w")
      
      
        self.fixed_name_entry = tk.Entry(self.can9, bd=80,width=10)
        self.fixed_name_entry.grid(column=1, row=1, sticky="ew")

        self.reset_button = tk.Button(self.can9, text="Reset", command=self.reset_widget)
        self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)
        
       
       

##        # Entry for specifying the number of characters to move/copy
##        self.chars_count = tk.IntVar(value=0)
##        tk.Label(self.can6, text="Number of Characters:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
##        self.chars_entry = tk.Spinbox(self.can6, from_=0, to=100)
##        self.chars_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
##
##        # Dropdown for selecting the new position
##        self.new_position = tk.StringVar(value="Start")
##        position_options = ["Start", "End", "Specific Position"]
##        tk.Label(self.frm7, text="To Position:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
##        self.position_menu = tk.OptionMenu(self.frm78, self.new_position, self.new_position.get(), *position_options)
##        self.position_menu.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
##
##        # Entry for specifying the specific position (if applicable)
##        self.specific_pos = tk.IntVar(value=0)
##        self.specific_pos_entry = tk.Spinbox(self.frm8, from_=0, to=100)
##        self.specific_pos_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Apply button
        self.apply_button = tk.Button(self.can7, text="Apply", command=self.apply_move)
        self.apply_button.grid(row=4, column=1, sticky="e", padx=5, pady=5)
        self.notebook.add(self.frm10, text='Fix Suffix Prefix')
        self.fix = PrefixSuffixApplication(self.frm10,self.fn)
        self.notebook.add(self.frm11, text='Custom')
        self.notebook.add(self.frm12, text='Custom2')
        self.setup_add_to_string_tab()
        
    def setup_add_to_string_tab(self):
        self.varr2 = tk.BooleanVar()
        self.entry = tk.Entry(self.can5)
        self.entry.grid(row=6, column=1, sticky="ew", padx=5)
        self.spinbox = ttk.Spinbox(self.can5, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
        self.spinbox.grid(row=7, column=1, sticky="ew", padx=5)
        # Checkbox for using current file name
        self.checkbutton1 = ttk.Checkbutton(self.frm1, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton1.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton2 = ttk.Checkbutton(self.frm2, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton2.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton3 = ttk.Checkbutton(self.frm3, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton3.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton4 = ttk.Checkbutton(self.frm4, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton4.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)

        self.checkbutton5 = ttk.Checkbutton(self.can5, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton5.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
      
       
        self.notebook.add(self.frm6, text='Shift Chars')
        self.checkbutton6 = ttk.Checkbutton(self.frm6, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton6.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton7 = ttk.Checkbutton(self.can7, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton7.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton8 = ttk.Checkbutton(self.frm8, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton8.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.checkbutton9 = ttk.Checkbutton(self.frm9, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton9.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)

        self.checkbutton10 = ttk.Checkbutton(self.frm10, text="Use current file name", variable=self.varr2,
                                           command=self.update_use_current_filename)
        self.checkbutton10.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        
    def update_use_current_filename(self):
        if self.varr2.get():  # If the checkbox is checked
             if self.fn.rename_history:
                current_file_name = self.fn.rename_history[-1]  # Get the last item in the history
                self.current_file_name.set(current_file_name)
        else:
            self.current_file_name.set("")  # Reset current file name if checkbox is unchecked
            self.use_current_filename.set(self.varr2.get())
         
    def apply_changes(self):
        if self.use_current_filename.get():
            current_file_name = self.get_current_file_name()  
            modified_file_name = self.apply_modifications(current_file_name)  
            # Apply modified_file_name to the selected files or perform other actions as needed
        else:
            # Directly apply modifications to the selected files
            selected_items = self.fn.tree_files.selection()
            if not selected_items:
                selected_items = self.fn.tree_files.get_children()
            
            if not selected_items:
                messagebox.showinfo("Info", "No files selected.")
                return
            
            for item_id in selected_items:
                old_name = self.fn.tree_files.item(item_id, 'text')
                new_name = self.apply_modifications(old_name)  # Apply modifications directly to each file name
                # Here you can update the file name in your application's interface or perform any other necessary action




    def regexptab(self,fn):
       
        self.fn =fn
        self.fn.selected_files = self.fn.tree_files.selection()
     
    def apply_regexp(self):
        pattern = self.match_entry.get()
        replace_pattern = self.replace_entry.get()

        if not self.fn.selected_files:
            messagebox.showinfo("Info", "No files selected.")
            return
        selected_items = self.fn.tree_files.selection()
        if not selected_items:
            selected_items = self.fn.tree_files.get_children()
        self.fn.regex(pattern,replace_pattern)    
    def casetab(self,fn):
        self.fn = fn
        
    def apply_case_change(self):
        namecase = self.case_type_combobox.get()
        self.fn.case(namecase)
    
    def apply_replacement(self):
        replace_text = self.match_entry.get()
        with_text = self.replace_entry.get()
        self.fn.replacement(replace_text,with_text)
      





    def add(self,fn):
    
        self.fn =fn
        self.fn.selected_files = self.fn.tree_files.selection()
       
        
    def apply_numbering(self):
        try:
            start = int(self.start_num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Starting number must be an integer.")
            return

        position = self.position_combobox.get()
        delimiter = self.delimiter_entry.get()

       
        self.fn.numbering_files(start, prefix=position == "Prefix", delimiter=delimiter)

    def reset_widget(self):
        self.prefix.set("")
        self.insert_this.set("")
        self.at_pos.set(0)
        self.suffix.set("")



    def shiftchar(self,fn):
        
        self.fn = fn
        self.fn.selected_files = self.fn.tree_files.selection()
       
    def apply_move(self):
        sample_name = "ExampleFile.txt"
        result = "Moved/Copied_Part_" + sample_name

        # Displaying the result in a temporary label for demonstration
        result_label = tk.Label(self.can8, text=f"Result: {result}")
        result_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)


     
        
    def apply_removal(self):
        first_n = self.first_n.get()
        last_n = self.last_n.get()
      
        print(f"Removing first {first_n} and last {last_n} characters from filenames")


    def create_spinbox(self, label, variable, row):
        var = tk.StringVar()
        ttk.Spinbox(self.can8, from_=0, to=MAX_NAME_LEN,).grid(row=row, column=1)

    def bind_entries(self):
        self.first_n.trace_add("write", self.update)
      
    def reset_widget(self):
        self.first_n.set(0)
        self.last_n.set(0)
        # Continues for all resettable variables...

    def update(self, *args):
        print("First n:", self.first_n.get())
        print("Last n:", self.last_n.get())
        

   
    def remove_n_chars(self, name):
        first_n = self.first_n.get()
        last_n = -self.last_n.get() if self.last_n.get() > 0 else None

        # If last_n is None, slicing will go to the end of the string.
        return name[first_n:last_n]

   
       
    def ext_change(self):
        
        self.new_ext = self.new_ext_entry.get()
        self.fn.ext_replace(self.new_ext)
        


           
    def reset_widget(self):
        self.new_ext_entry.delete(0, tk.END)
    

        

    def name(self,fn):
        pass

   


       
        

  
class PrefixSuffixApplication:
    def __init__(self, parent,fn):
        self.frm10 = parent
        self.fn = fn
        
        # Entry for prefix
        tk.Label(self.frm10, text="Prefix:").grid(row=0, column=0)
        self.prefix_entry = tk.Entry(self.frm10)
        self.prefix_entry.grid(row=0, column=1)
        
        # Entry for suffix
        tk.Label(self.frm10, text="Suffix:").grid(row=1, column=0)
        self.suffix_entry = tk.Entry(self.frm10)
        self.suffix_entry.grid(row=1, column=1)
        
        # Apply button
        self.apply_btn = tk.Button(self.frm10, text="Apply", command=self.apply_prefix_suffix)
        self.apply_btn.grid(row=2, column=0, columnspan=2)

    def apply_prefix_suffix(self):
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        
        # Determine if any items are selected; if not, apply to all items
        selected_items = self.fn.tree_files.selection()
        if not selected_items:
            selected_items = self.fn.tree_files.get_children()
        
        if not selected_items:
            messagebox.showinfo("Info", "No files selected.")
            return
        
        for item_id in selected_items:
            old_name = self.fn.tree_files.item(item_id, 'text')
            new_name = f"{prefix}{old_name}{suffix}"
            self.fn.tree_files.item(item_id, values=(new_name,))
            self.fn.prefix_suffix(item_id, old_name, new_name)
