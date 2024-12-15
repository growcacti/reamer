import tkinter as tk
from tkinter import ttk

class Ctrl_Tabs:
    def __init__(self, parent, file_navigator=None):
        self.parent = parent
        self.fn = file_navigator

        # Create a Notebook widget
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.grid(row=6, column=0, sticky='nsew')

        self.frame = {}
        self.canvas = {}

        # Define colors for each canvas
        colors = ['ivory2', 'DarkSeaGreen1', 'alice blue', 'khaki1', 'light pink', 'light cyan',
                  'seashell', 'honeydew', 'azure4', 'cornsilk3', 'grey67', 'powder blue', 'navajo white']


        # Create frames and canvases, assign colors
        for i in range(1, 14):  # Frame indexes from 1 to 13
            self.frame[i] = ttk.Frame(self.notebook)
            self.canvas[i] = tk.Canvas(self.frame[i], bg=colors[i-1] if i <= len(colors) else 'white')

            # Position frames and canvases
            column = i if i <= 6 else i - 6
            self.frame[i].grid(row=0, column=column)
            self.canvas[i].grid(row=1, column=0, sticky='nsew')

            # Add tabs to notebook with labels
            labels = ['RegEx', 'Case', 'Replace', 'Numbering', 'Add to String', 'Shift Char',
                      'Remove', 'RegEx', 'Ext Replace', 'Naming', 'Prefix Suffix', 'Random', 'Custom']
            if i <= len(labels):
                self.notebook.add(self.frame[i], text=labels[i-1])

            print(self.frame)
            print(self.canvas)

if __name__ == '__main__':
    root = tk.Tk()
    ct = Ctrl_Tabs(root)
    root.mainloop()
