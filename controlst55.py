import tkinter as tk
from tkinter import ttk
import random
import os


MAX_NAME_LEN = 255


class Ctrl_Tabs:
    def __init__(self, parent, file_navigator=None):
        self.parent = parent
        self.fn = file_navigator

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, columnspan=6, sticky='nsew')

        self.frames = {}
        self.canvases = {}

        # Define colors for each canvas
        colors = ['ivory2', 'DarkSeaGreen1', 'alice blue', 'khaki1', 'light pink', 'light cyan',
                  'seashell', 'honeydew', 'azure4', 'cornsilk3', 'grey67', 'powder blue', 'navajo white']
        
        # Tab labels
        labels = ['RegEx', 'Case', 'Replace', 'Numbering', 'Add to String', 'Shift Char',
                  'Remove', 'Ext Replace', 'Naming', 'Prefix Suffix', 'Random', 'Combination', 'Overflow']
        
        # Create frames and canvases, assign colors and add widgets
        for i in range(1, 14):  # Frame indexes from 1 to 13
            frame = ttk.Frame(self.notebook)
            canvas = tk.Canvas(frame, bg=colors[i-1] if i <= len(colors) else 'white')
            canvas.grid(row=0, column=0, sticky='nsew')
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

            self.frames[i] = frame
            self.canvases[i] = canvas

            # Adding widgets to the canvas
            self.add_widgets_to_tab(i, canvas)

            # Add tabs to notebook with labels
            if i <= len(labels):
                self.notebook.add(frame, text=labels[i-1])
     
    def add_widgets_to_tab(self, index, canvas):
        if index == 1:
            # Example for RegEx tab using ComboBox
            ttk.Label(canvas, text='Select RegEx pattern:').grid(row=0, column=0, padx=10, pady=10)
            pattern_combo = ttk.Combobox(canvas, values=["^[a-zA-Z]+", "^\\d+", "[a-zA-Z0-9]"])
            pattern_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Label(canvas, text="Pattern Match and Replace").grid(row=3,column=1)
            patternmatch=ttk.Entry(canvas)
            patternmatch.grid(row=4, column=1, padx=10, pady=10)
            regex_btn = ttk.Button(canvas, text='Apply',command=self.apply_regexp)
            regex_btn.grid(row=0, column=2, padx=10, pady=10)
            checkbutton1 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            checkbutton1.grid(row=9, column=0, columnspan=2, sticky="w", padx=5)

        elif index == 2:
            # Example for Case tab using ComboBox
            ttk.Label(canvas, text='Select case operation:').grid(row=0, column=0, padx=10, pady=10)
            operation_combo = ttk.Combobox(canvas, values=["Upper", "Lower", "Title","Capitalize","SwapCase","Strip"])
            operation_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Apply').grid(row=0, column=2, padx=10, pady=10)
            checkbutton2 = ttk.Checkbutton(canvas, text="current file", variable=None)
            checkbutton2.grid(row=9, column=0, columnspan=2, sticky="w", padx=5)

        elif index == 3:
            # Example for Replace tab using ComboBox
            ttk.Label(canvas, text='Find what:').grid(row=0, column=0, padx=10, pady=10)
            find_combo = ttk.Combobox(canvas, values=["Error", "Warning", "Notice"])
            find_combo.grid(row=0, column=1, padx=10, pady=10)
            ttk.Label(canvas, text='Replace with:').grid(row=1, column=0, padx=10, pady=10)
            replace_entry = ttk.Entry(canvas)
            replace_entry.grid(row=1, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Replace').grid(row=1, column=2, padx=10, pady=10)
        elif index == 4:
           pass
           self.position_combobox = ttk.Combobox(canvas, values=["Prefix", "Suffix"])
           self.position_combobox.grid(row=1, column=1)
           tk.Label(canvas, text="Delimiter:").grid(row=2, column=0)
           self.delimiter_entry = tk.Entry(canvas)
           self.delimiter_entry.grid(row=2, column=1)
           self.delimiter_entry.insert(0, "_") 

        elif index == 5:
##           
            self.entry = tk.Entry(canvas)
            self.entry.grid(row=6, column=1, sticky="ew", padx=5)
            self.spinbox = ttk.Spinbox(canvas, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
            self.spinbox.grid(row=7, column=1, sticky="ew", padx=5)
            self.checkbutton = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton.grid(row=9, column=2, sticky="ew", padx=5)


      
        elif index == 6:
            self.shift = ttk.Spinbox(canvas, from_=-MAX_NAME_LEN, to=MAX_NAME_LEN)
            self.shift.grid(row=7, column=1, sticky="ew", padx=5)

            self.checkbutton6 = ttk.Checkbutton(canvas, text="current_name")
            self.checkbutton6.grid(row=9, column=2, sticky="ew", padx=5)

            pass
        elif index == 7:
            tk.Label(canvas, text="Remove first n characters:",).grid(row=4, column=3)
            self.first_n = tk.IntVar()
            self.sp1 = tk.Spinbox(canvas, from_=0, to=MAX_NAME_LEN)
            self.sp1.grid(row=5, column=3)

            tk.Label(canvas, text="Remove last n characters:",).grid(row=6, column=3)
            self.last_n = tk.IntVar()
            self.sp2 = tk.Spinbox(canvas, from_=0, to=MAX_NAME_LEN)
            self.sp2.grid(row=7, column=3)
            self.btn1 =tk.Button(canvas, text="Apply", command=self.apply_removal)
            self.btn1.grid(row=10, column=0)
            self.checkbutton7 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton7.grid(row=9, column=2, sticky="ew", padx=5)
        elif index == 8:
            self.new_ext_entry = tk.Entry(canvas, width=20)
            self.new_ext_entry.grid(column=1, row=0, padx=5, pady=5, sticky="ew")

            self.sendchange_button = tk.Button(canvas, text="Change ext", command=self.ext_change)
            self.sendchange_button.grid(column=1, row=4, padx=5, pady=5)

            self.reset_button = tk.Button(canvas, text="Reset", command=self.reset_widget)
            self.reset_button.grid(column=2, row=0, padx=5, pady=5)
            self.checkbutton8 = ttk.Checkbutton(canvas, text="current_name", variable=None)
            self.checkbutton8.grid(row=9, column=2, sticky="ew", padx=5)
 
       

            
            pass
        elif index == 9:
            tk.Label(canvas, text="Name").grid(column=0, row=0, sticky="w")
            self.name_option_combo = ttk.Combobox(
            canvas,
            width=10,
            state="readonly",            values=("Keep", "Remove", "Reverse", "Fixed","Random",))
            self.name_option_combo.grid(column=1, row=0, sticky="ew")
            self.name_option_combo.current(0)

            self.fixed_name_entry = tk.Entry(canvas, bd=80,width=10)
            self.fixed_name_entry.grid(column=1, row=1, sticky="ew")

            self.reset_button = tk.Button(canvas, text="Reset", command=self.reset_widget)
            self.reset_button.grid(column=2, row=2, sticky="e", padx=2, pady=2)


        
        elif index == 10:
            tk.Label(canvas, text="Prefix:").grid(row=0, column=0)
            self.prefix_entry = tk.Entry(canvas)
            self.prefix_entry.grid(row=0, column=1)

            # Entry for suffix
            tk.Label(canvas, text="Suffix:").grid(row=1, column=0)
            self.suffix_entry = tk.Entry(canvas)
            self.suffix_entry.grid(row=1, column=1)

            # Apply button
            self.apply_btn = tk.Button(canvas, text="Apply", command=None)
            self.apply_btn.grid(row=2, column=0, columnspan=2)

            
            
        elif index == 11:
            random_entry = ttk.Entry(canvas)
            random_entry.grid(row=1, column=1, padx=10, pady=10)
            
            self.apply_btn = tk.Button(canvas, text="Apply Random", command=None)
            self.apply_btn.grid(row=2, column=0, columnspan=2)
            
            
        elif index == 12:
            pass
        elif index == 13:
            pass
        elif index == 14:
            pass

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





    def ext_change(self):
          self.new_ext = self.new_ext_entry.get()
          self.fn.ext_replace(self.new_ext)   

   
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

            pass
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Complex Control with Tabs')
    root.geometry('800x600')  # Set initial size of the window
    ct = Ctrl_Tabs(root)
    root.mainloop()
