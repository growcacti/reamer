# Example place where prefix_suffix might be called
selected_item = self.tree_files.selection()[0] # Assuming single selection for simplicity
old_name = self.tree_files.item(selected_item, 'text')
new_name = "new_file_name_here" # Determine how new_name is set in your application

self.prefix_suffix(old_name, new_name)
# Example place where prefix_suffix might be called
selected_item = self.tree_files.selection()[0] # Assuming single selection for simplicity
old_name = self.tree_files.item(selected_item, 'text')
new_name = "new_file_name_here" # Determine how new_name is set in your application

self.prefix_suffix(old_name, new_name)




# Example place where prefix_suffix might be called
selected_item = self.tree_files.selection()[0] # Assuming single selection for simplicity
old_name = self.tree_files.item(selected_item, 'text')
new_name = "new_file_name_here" # Determine how new_name is set in your application

self.prefix_suffix(old_name, new_name)







def prefix_suffix(self, old_name, new_name):
    # Ensure both old_name and new_name are passed to this function
    old_path = os.path.join(self.active_path, old_name)
    new_path = os.path.join(self.active_path, new_name)

    try:
        os.rename(old_path, new_path)
        # Update the Treeview and any other UI components as necessary
        # For example, find the Treeview item with old_path and update its name to new_name
        print(f"Successfully renamed {old_name} to {new_name}")
    except Exception as e:
        print(f"Error renaming file: {e}")
