  def rename_files(self, pattern):
        selected_items = self.tree_files.selection()
        if not selected_items:
            tk.messagebox.showinfo("Info", "No files selected for renaming.")
            return
             
         
        if messagebox.askyesno("Confirm Rename", "Do you want to proceed with renaming the selected files?"):
            num = 1  # Starting number for sequential numbering
            for item_id in selected_items:
                current_name = self.tree_files.item(item_id, 'text')
                new_name = self.generate_new_name(current_name, pattern, num)
                old_path = os.path.join(self.active_path, current_name)
                new_path = os.path.join(self.active_path, new_name)
                

                try:
                    os.rename(old_path, new_path)
                    # Update the item in the tree view to reflect the new name
                    self.tree_files.item(item_id, text=new_name)
                    self.rename_history.append((old_path, new_path))
                    num += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename '{current_name}' to '{new_name}': {e}")
                    break  # Stop the renaming process on error
            messagebox.showinfo("Success", "Files have been renamed successfully."  def rename_selected_file(self): 
        selected_items = self.tree_files.selection()
        
        if not selected_items:
            messagebox.showinfo("Info", "No file selected for renaming.")
            return

        # Assuming single selection for simplicity
        item_id = selected_items[0]
       
        old_name = self.tree_files.item(item_id, 'text')
        old_path = os.path.join(self.active_path, old_name)

        new_name = simpledialog.askstring("Rename", "Enter new name for the file:", initialvalue=old_name)
        if not new_name or new_name == old_name:
            # No change made or cancelled
            return

        new_path = os.path.join(self.active_path, new_name)
        try:
            os.rename(old_path, new_path)
            # Update the tree view to reflect the change
            self.tree_files.item(item_id, text=new_name)
            messagebox.showinfo("Success", "File renamed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rename file: {e}")
)
