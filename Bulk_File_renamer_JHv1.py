import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
from tkinter import ttk
import os

# CONSTANTS
MAX_NAME_LEN = 255

class FileExplorer:
    def __init__(self, master, path):
        self.master = master
        self.path = path
        self.nodes = {}  # Tracks the nodes that have been expanded.
        self.entry_frame = tk.Frame(self.master, width=165)
        self.entry_frame.grid(row=0, column=0, columnspan=4)
        self.frm1 = ttk.Frame(self.master)
        self.frm1.grid(row=1, column=0, rowspan=4, columnspan=10, sticky="ns")
        self.canvas = tk.Canvas(self.frm1, width=50, bg="seashell2")
        self.canvas.grid(row=2, column=0)
        self.frm2 = ttk.Frame(self.master)
        self.frm2.grid(row=1, column=4, sticky="ns")
        self.master.grid_columnconfigure(4, weight=1)
        self.rename_history = []
        self.rename_selection = []
        self._path_list = []
        self.count = 0
        # Path display and editing
        self.path_entry = tk.Entry(self.entry_frame, bd=8, bg="azure", width=155)
        self.path_entry.grid(row=0, column=0, columnspan=2, sticky="ew")
       
        self.path_entry.bind('<Return>', self.on_path_entry_return)

        # Treeview for navigating directories
        self.dir_nav = ttk.Treeview(self.frm1, selectmode="browse")
        self.dir_nav.heading("#0", text="Directory Browser", anchor="w")
        self.dir_nav.column("#0", width=300, stretch=True)

        # Scrollbars for the Treeview
        ysb = ttk.Scrollbar(self.frm1, orient="vertical", command=self.dir_nav.yview)
        xsb = ttk.Scrollbar(self.frm1, orient="horizontal", command=self.dir_nav.xview)

        self.dir_nav.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.dir_nav.grid(row=1, column=0, rowspan=4, columnspan=2, sticky="nsew")
        ysb.grid(row=1, column=3, sticky="ns")
        xsb.grid(row=20, column=0, sticky="ew")

        self.dir_nav.bind("<<TreeviewOpen>>", self.on_treeview_open)
        self.can = tk.Canvas(self.frm1, bg="alice blue", width=180, height=70)
        self.can.grid(row=2, column=4, columnspan=8)
        tk.Label(self.can, text="Original Filenames").grid(row=3, column=1)
        tk.Label(self.can, text="Preview New Filenames").grid(row=3, column=6)
        self.lb1 = tk.Listbox(self.can, bd=10, width=50, height=25, selectmode=tk.MULTIPLE)
        self.lb1.grid(row=4, column=1, rowspan=2, columnspan=2)
        self.lb2 = tk.Listbox(self.can, bd=10, width=50, height=25, selectmode=tk.MULTIPLE)
        self.lb2.grid(row=4, column=6, rowspan=2, columnspan=3)
        self.switch = 1
        self.yscrollbar = tk.Scrollbar(self.can)
        self.yscrollbar.grid(row=4, column=10)
        self.xscrollbar = tk.Scrollbar(self.can, orient="horizontal")
        self.xscrollbar.grid(row=2, column=1)
        self.yscrollbar.config(command=self.lb1.yview)
        self.xscrollbar.config(command=self.lb1.xview)
        self.lb1.config(bg="light yellow", yscrollcommand=self.yscrollbar.set)
        self.lb1.config(bg="wheat", xscrollcommand=self.xscrollbar.set)
        self.lb1.bind("<MouseWheel>", lambda event: self.yscrolllistbox(event, self.lb2))
        self.lb2.bind("<MouseWheel>", lambda event: self.yscrolllistbox(event, self.lb1))
        self.xscrollbar2 = ttk.Scrollbar(self.can, orient="horizontal", command=self.lb2.xview)
        self.xscrollbar2.grid(row=2, column=6)

        self.esync = tk.Entry(self.can, bd=7, bg="lavender", width=40)
        self.esync.grid(row=19, column=2)
        self.syncbt = tk.Button(self.can, text="Sync/Independent Scroll", bd=4, bg="light blue", command=self.do_switch)
        self.syncbt.grid(row=19, column=1)
        self.list_files()
        self.bind_entries()

    def bind_entries(self):
        self.dir_nav.bind("<<TreeviewOpen>>", self.on_directory_expand)
        
    def sync(self):
        self.lb2.config(bg="seashell", yscrollcommand=self.yscrollbar.set)
        self.lb1.config(bg="seashell", yscrollcommand=self.yscrollbar.set)

    def nosync(self):
        self.yscrollbar2 = ttk.Scrollbar(self.can, orient="vertical", command=self.lb2.yview)
        self.yscrollbar2.grid(row=4, column=10)
        self.lb1.config(bg="snow")

    def on_path_entry_return(self, event=None):
        self.path = self.path_entry.get()
        self.initialize_treeview(self.path)

    def initialize_treeview(self, path):
        self.path = path
        self.dir_nav.delete(*self.dir_nav.get_children())  # Clear existing tree
        if os.path.isdir(self.path):
            self.insert_node("", self.path, self.path)
            self.dir_nav.item(self.path, open=True)
            self.path_entry.insert(0, self.path)
            self.lb1.delete(0, tk.END)
            self.lb2.delete(0, tk.END)
            for file in os.listdir(self.path):
                self.lb1.insert(tk.END, file)
                self.lb2.insert(tk.END, file)

    def insert_node(self, parent, path, text, open=False):
        node = self.dir_nav.insert(parent, 'end', iid=path, text=text, open=open)
        if os.path.isdir(path):
            self.dir_nav.insert(node, 'end', iid=path + "_placeholder", text="")
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def on_treeview_open(self, event):
        node_id = self.dir_nav.focus()
        if node_id not in self.nodes and os.path.isdir(node_id):
            self.nodes[node_id] = True
            try:
                for entry in os.scandir(node_id):
                    if entry.is_dir():
                        self.insert_node(node_id, entry.path, entry.name)
            except PermissionError as e:
                print(e)
        if hasattr(self, 'on_directory_selected'):
            self.on_directory_selected(node_id)

    def list_files(self):
        self.path = os.getcwd()
        node_id = self.path
        if node_id not in self.nodes and os.path.isdir(self.path):
            self.nodes[node_id] = True
        try:
            for entry in os.scandir(node_id):
                if entry.is_dir():
                    self.path_entry.delete(0, tk.END)
                    self.path_entry.insert(0, self.path)
                    os.chdir(self.path)
                    self.flist = os.listdir(self.path)
                    self.lb1.delete(0, tk.END)
                    self.lb2.delete(0, tk.END)
                    for files in self.flist:
                        self.lb1.insert(0, files)
                        self.lb2.insert(0, files)
        except PermissionError as e:
            print(e)

    def newdirlist(self):
        self.path = filedialog.askdirectory()
        node_id = self.path
        if node_id not in self.nodes and os.path.isdir(self.path):
            self.nodes[node_id] = True
            try:
                for entry in os.scandir(node_id):
                    if entry.is_dir():
                        self.path_entry.delete(0, tk.END)
                        self.path_entry.insert(0, self.path)
                        os.chdir(self.path)
                        self.flist = os.listdir(self.path)
                        self.lb1.delete(0, tk.END)
                        self.lb2.delete(0, tk.END)
                        for files in self.flist:
                            self.lb1.insert(0, files)
                            self.lb2.insert(0, files)
            except PermissionError as e:
                print(e)
  
        
    def do_switch(self):
        if self.switch:
            self.switch = 0
            text = "Independent Scrolling"
            self.esync.delete(0, tk.END)
            self.esync.insert(0, text)
            self.nosync()
        else:
            self.switch = 1
            text = "In Sync Scrolling Up/Down"
            self.sync()
            self.esync.delete(0, tk.END)
            self.esync.insert(0, text)

    def yscrolllistbox(self, event, lb):
        self.lb = lb
        if self.switch == 1:
            self.lb.yview_scroll(int(-4 * (event.delta / 120)), "units")
            self.sync()

    def xscrolllistbox(self, event, lb):
        self.lb = lb
        if self.switch == 1:
            self.lb.xview_scroll(int(-4 * (event.delta / 120)), "units")
            self.sync()

    def on_double_click(self, event):
        sel = self.lb1.curselection()
        if sel:
            item_path = self.lb1.get(sel[0])
            if os.path.isdir(item_path):
                self.lb1.delete(0, tk.END)
                self.lb2.delete(0, tk.END)
                for file in os.listdir(item_path):
                    self.lb1.insert(0, file)
                    self.lb2.insert(0, file)
            else:
                self.update_view(item_path)

    def store_selections(self):
        file = self.lb1.curselection()
        if file:
            self.rename_selection.append(file)
        else:
            self.rename_selection.pop(file)
        return file

    def on_directory_expand(self, event):
        item_id = self.dir_nav.focus()
        return item_id
       

    def on_directory_select(self):
        current_dir = self.dir_nav.item(item_id, 'text')
        
    def show_rename_preview(self, pattern):
        selected_items = self.lb1.curselection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for preview.")
            return

        preview_win = tk.Toplevel(self.master)
        preview_win.title("Rename Preview")
        preview_tree = ttk.Treeview(preview_win, columns=("Original", "New"), show="headings")
        preview_tree.heading("Original", text="Original Filename")
        preview_tree.heading("New", text="New Filename")
        preview_tree.pack(fill=tk.BOTH, expand=True)

        for index, item in enumerate(selected_items):
            current_name = self.lb1.get(item)
            new_name = self.generate_new_name(current_name, pattern)
            preview_tree.insert("", tk.END, iid=str(index), text=str(index), values=(current_name, new_name))

    def generate_new_name(self, old_name, pattern):
        # Implement the renaming logic based on the provided pattern
        return pattern.replace("*", old_name)

    def refresh_view(self, path):
        self.path = path
        self.delete_children()
        for entry in os.scandir(self.path):
            if entry.is_file():
                self.lb1.insert(tk.END, entry.name)
                self.lb2.insert(tk.END, entry.name)

    def delete_children(self):
        for item in self.dir_nav.get_children():
            self.dir_nav.delete(item)

    def update_view(self, path):
        self.path = path
        self.delete_children()
        self.path_entry.delete(0, tk.END)
        self.lb2.delete(0, tk.END)
        try:
            if os.path.isdir(self.path):
                for entry in os.scandir(self.path):
                    self.path_entry.insert(0, self.path)
                    self.dir_nav.item(self.path, open=True)
                    self.insert_node("", entry.path, entry.name)
        except PermissionError:
            messagebox.showerror("Error", "You do not have permissions to access this directory")

class InfoBar:
    def __init__(self, appframe, fn):
        self.frame = appframe
        self.fn = fn  
      
        self.frame.grid(column=22, row=2, columnspan=2, sticky="we")  # Ensure it spans across the window
        self.frame.columnconfigure(1, weight=1)

        self.items_text_var = tk.StringVar()
        self.action_text_var = tk.StringVar()
        self.num_items_refresh()

        self.items_label = ttk.Label(self.frame, textvariable=self.items_text_var, relief="sunken")
        self.items_label.grid(row=15, column=0, ipadx=50, ipady=2, padx=4)

        self.action_label = ttk.Label(self.frame, textvariable=self.action_text_var, relief="sunken")
        self.action_label.grid(row=16, column=0, sticky="we", ipady=2, padx=4)

    def num_items_refresh(self):
        num_items = self.fn.lb1.size()
        num_sel_items = len(self.fn.lb1.curselection())
        self.items_text_var.set(f"{num_items} items ({num_sel_items} selected)")

    def last_action_refresh(self, action):
        self.action_text_var.set(action)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Explorer')
        self.geometry('1200x600')
        self.path = self.initial_path()
        self.pathlist = []
        self.app_frm = tk.Frame(self)
        self.app_frm.grid(row=24, column=2)
        self.fn = FileExplorer(self, self.path)
        self.lower_frame = ttk.Frame(self)
        self.lower_frame.grid(row=28, column=2, sticky="nsew", padx=(5, 5), pady=5)
        self.tab = Ctrl_Tabs(self.lower_frame, self.fn)
        self.columnconfigure(6, weight=1)
        self.rowconfigure(28, weight=4)
        self.rowconfigure(1, weight=1)

        self.menubar = tk.Menu(self, tearoff=False)
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load Directory", underline=1, command=self.targetdir)
        self.fn.on_path_entry_return()
        self.config(menu=self.menubar)

        self.suffix_btn = ttk.Button(self.app_frm, text="Add Suffix", command=self.open_suffix_dialog)
        self.suffix_btn.grid(row=2, column=0, padx=5, pady=5)
        self.infobar = InfoBar(self.app_frm, self.fn)
       
        self.fn.info_bar = self.infobar
        self.dirset()
    def initial_path(self):
        self.path = os.getcwd()
       
              
    def dirset(self):
        self.path = os.getcwd()
        self.fn.initialize_treeview(self.path)
                 
        
    def open_suffix_dialog(self):
        # Remove or define Suffix class/function if needed
        pass

    def targetdir(self):
        directory_path = filedialog.askdirectory()
        self.pathlist.append(directory_path)
        self.fn.path_entry.delete(0, tk.END)
        self.fn.path_entry.insert(0, directory_path)
        self.fn.on_path_entry_return()
        return directory_path

class Ctrl_Tabs:
    def __init__(self, parent, fn):
        self.parent = parent
        self.fn = fn

        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, columnspan=6, sticky='nsew')

        self.frames = {}
        self.canvases = {}

        colors = ['ivory2', 'DarkSeaGreen1', 'alice blue', 'khaki1', 'light pink', 'light cyan',
                  'seashell', 'honeydew', 'azure4', 'cornsilk3', 'grey67', 'powder blue', 'navajo white']

        labels = ['RegEx', 'Case', 'Replace', 'Numbering', 'Add to String', 'Shift Char',
                  'Remove', 'Ext Replace', 'Naming', 'Prefix Suffix', 'Random', 'Custom', 'Overflow']

        for i in range(1, 14):
            frame = ttk.Frame(self.notebook)
            canvas = tk.Canvas(frame, bg=colors[i-1] if i <= len(colors) else 'white')
            canvas.grid(row=0, column=0, sticky='nsew')
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

            self.frames[i] = frame
            self.canvases[i] = canvas

            self.add_widgets_to_tab(i, canvas)

            if i <= len(labels):
                self.notebook.add(frame, text=labels[i-1])

    def add_widgets_to_tab(self, index, canvas):
        if index == 1:
            ttk.Label(canvas, text='Enter RegEx:').grid(row=0, column=0, padx=10, pady=10)
            ttk.Entry(canvas).grid(row=0, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Apply').grid(row=0, column=2, padx=10, pady=10)
        elif index == 2:
            tk.Label(canvas, text='Choose Case:').grid(row=0, column=0, padx=10, pady=10)
            cb = ttk.Combobox(canvas, values=["Upper", "Lower", "Title", "Capitalize", "SwapCase", "Strip"])
            cb.grid(row=3, column=2)
            self.bt = tk.Button(canvas, text='Select Apply Case Change', command=lambda: self.case(cb.get()))
            self.bt.grid(row=1, column=0, padx=10, pady=10)

    def case(self, case):
        self.fn.renamer_selection.append(self.fn.lb1.curselection())
        for i in self.fnrenmae_selection:
        
            selected_items = self.fn.rename_selection[i]
            for file in selected_items:
                old_name = self.fn.lb1.get(file)
                if case == "Upper":
                    new_name = old_name.upper()
                elif case == "Lower":
                    new_name = old_name.lower()
                elif case == "Title":
                    new_name = old_name.title()
                elif case == "Capitalize":
                    new_name = old_name.capitalize()
                elif case == "SwapCase":
                    new_name = old_name.swapcase()
                elif case == "Strip":
                    new_name = old_name.strip()
                else:
                    continue

                self.fn.lb2.delete(0, tk.END)
                self.fn.lb2.insert(0, new_name)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
