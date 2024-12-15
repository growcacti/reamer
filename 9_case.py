import os
import tkinter as tk
from tkinter import messagebox, ttk

class FileNavigator:
    # Other parts of your class here...
    
    def case(self, case):
        selected_items = self.tree_files.selection()
        
        for item_id in selected_items:
            old_name = self.tree_files.item(item_id, 'text')  # Get the current name from the tree
            
            # Decide the new name based on the case condition
            if case == "upper":
                new_name = old_name.upper()
            elif case == "lower":
                new_name = old_name.lower()
            else:
                continue  # If the case is neither 'upper' nor 'lower', skip to the next item

            # Apply the new name to the tree view item
            self.tree_files.item(item_id, text=new_name)
            print(item_id)
       
            # Construct old and new paths for the rename operation
            old_path = os.path.join(self.active_path, old_name)
            new_path = os.path.join(self.active_path, new_name)
            
            # Try to rename the file on the file system
            try:
                os.rename(old_path, new_path)
                # Optionally, track this action for undo functionality
                self.rename_history.append((new_path, old_path))  # Track the rename for undoing
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {old_name} to {new_name}: {e}")
                break  # Exit the loop on error to avoid partial rename operations
