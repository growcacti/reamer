self.insert_node(parent, entry, values=(entry.name,))




self.tree_files["columns"] = ("new_name",)
self.tree_files.heading("new_name", text="New Name", anchor="w")

self.insert_node(parent, entry, values=(entry.name,))
# single column


self.insert_node(parent, entry, values=(entry.name, entry.name))

#both columns



selected_item = self.tree_files.selection()[0]  # Assuming single selection
current_values = list(self.tree_files.item(selected_item, 'values'))
new_name = 'New Value'  # The new name you want to set
current_values[0] = new_name  # Assuming 'new_name' is the first column after the main one
self.tree_files.item(selected_item, values=tuple(current_values))
