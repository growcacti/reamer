  def apply_conditional_rename(self, pattern, start_num=1):
        selected_items = self.tree_files.selection()
        if not selected_items:
            messagebox.showinfo("Info", "No files selected for renaming.")
            return

        condition_pattern = re.compile(r'\{if:ext=(\.\w+)\}(.+?)\{else\}(.+?)\{endif\}')
        num = start_num
        for item_id in selected_items:
            old_name = self.tree_files.item(item_id, 'text')
            extension = os.path.splitext(old_name)[1]
            base_name = os.path.splitext(old_name)[0]

            # Check if the pattern includes a conditional statement
            match = condition_pattern.search(pattern)
            if match:
                condition_ext, if_true, if_false = match.groups()
                # Apply the conditional renaming
                if extension == condition_ext:
                    new_name = if_true.replace('{num}', str(num)).replace('{name}', base_name)
                else:
                    new_name = if_false.replace('{num}', str(num)).replace('{name}', base_name)
            else:
                # Fallback to a simple pattern replacement if no condition is found
                new_name = pattern.replace('{num}', str(num)).replace('{name}', base_name)

            new_path = os.path.join(self.active_path, new_name + extension)
            old_path = os.path.join(self.active_path, old_name)

            try:
                os.rename(old_path, new_path)
                self.tree_files.item(item_id, text=new_name + extension)
                num += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename file {old_name} to {new_name}: {e}")
                break  # Stop the renaming process on error
 def generate_new_name(self, current_name, pattern, num):
        base, ext = os.path.splitext(current_name)
        # Basic conditional pattern matching (simplified for example purposes)
        condition_match = re.search(r'\{ifext:(\w+)\}(.+?)\{else\}(.+?)\{endif\}', pattern)
        if condition_match:
            condition_ext, if_pattern, else_pattern = condition_match.groups()
            # Check if the extension matches the condition
            if ext[1:].lower() == condition_ext.lower():  # Removing the dot from the extension and case-insensitive comparison
                pattern = if_pattern
            else:
                pattern = else_pattern

        # Replace placeholders in the chosen pattern
        new_name = pattern.replace("{name}", base).replace("{num}", f"{num:02d}").replace("{ext}", ext)
        return new_name
  
        messagebox.showinfo("Success", "Conditional rename completed successfully.")
 def update_new_name_preview(self, suffix):
        for item_id in self.tree_files.get_children():
            original_name = self.tree_files.item(item_id, 'text')
            new_name = f"{original_name}{suffix}"
            self.tree_files.item(item_id, values=(new_name,))
