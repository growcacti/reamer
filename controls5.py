import tkinter as tk
from tkinter import ttk

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
                  'Remove', 'Ext Replace', 'Naming', 'Prefix Suffix', 'Random', 'Custom', 'Overflow']
        
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
            # Example for RegEx tab
            ttk.Label(canvas, text='Enter RegEx:').grid(row=0, column=0, padx=10, pady=10)
            ttk.Entry(canvas).grid(row=0, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Apply').grid(row=0, column=2, padx=10, pady=10)
        elif index == 2:
            # Example for Case tab
            ttk.Label(canvas, text='Enter text:').grid(row=0, column=0, padx=10, pady=10)
            cb = ttk.Combobox(canvas, values=["Upper", "Lower", "Title","Capitalize","SwapCase","Strip"])
            cb.grid(row=3,column=2)
            ttk.Button(canvas, text='Send').grid(row=1, column=0, padx=10, pady=10)
            ttk.Button(canvas, text='Reset').grid(row=1, column=1, padx=10, pady=10)
        elif index == 3:
            # Example for Replace tab
            ttk.Label(canvas, text='Find what:').grid(row=0, column=0, padx=10, pady=10)
            ttk.Entry(canvas).grid(row=0, column=1, padx=10, pady=10)
            ttk.Label(canvas, text='Replace with:').grid(row=1, column=0, padx=10, pady=10)
            ttk.Entry(canvas).grid(row=1, column=1, padx=10, pady=10)
            ttk.Button(canvas, text='Replace').grid(row=1, column=2, padx=10, pady=10)
        # Add more conditions for other tabs similarly

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Complex Control with Tabs')
    root.geometry('800x600')  # Set initial size of the window
    ct = Ctrl_Tabs(root)
    root.mainloop()
