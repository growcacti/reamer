# Create a Notebook widget
self.notebook = ttk.Notebook(self.parent)
self.notebook.grid(row=6, column=0, sticky='nsew')

# Creating multiple frames and configuring them using a loop
self.frames = {}
for i in range(2, 13):  # Frame indexes from 2 to 12
    frame = ttk.Frame(self.notebook)
    self.frames[i] = frame  # Store the frame in a dictionary
    column = i if i <= 6 else i - 1  # Adjust column for grid placement
    frame.grid(row=1 if i <= 6 else 0, column=column)  # Position frames
    if i == 2:
        self.notebook.add(frame, text='Case')  # Add the first frame to the notebook with a tab label
