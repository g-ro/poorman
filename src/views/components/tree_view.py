import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Optional, Callable

class EditableTreeView:
    def __init__(self, parent: ttk.Frame, columns: List[str], title: str = ""):
        """Initialize an editable tree view with add/remove buttons"""
        self.parent = parent
        
        # Create container frame
        self.frame = ttk.LabelFrame(parent, text=title, padding="5")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tree view
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=8)
        
        # Set up columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create buttons frame
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text=f"Add {title}", command=self.add_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text=f"Remove {title}", command=self.remove_item).pack(side=tk.LEFT)
    
    def add_item(self):
        """Show dialog to add a new item"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Item")
        dialog.geometry("400x150")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry(f"+{self.parent.winfo_rootx() + 50}+{self.parent.winfo_rooty() + 50}")
        
        # Create entry fields
        entries = []
        for i, col in enumerate(self.tree["columns"]):
            ttk.Label(dialog, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            var = tk.StringVar()
            ttk.Entry(dialog, textvariable=var, width=30).grid(row=i, column=1, padx=10, pady=5)
            entries.append(var)
        
        def save_item():
            values = [var.get() for var in entries]
            if values[0].strip():  # Check if key is not empty
                self.tree.insert("", tk.END, values=values)
                dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=save_item).grid(row=len(entries), column=0, padx=10, pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=len(entries), column=1, padx=10, pady=10)
    
    def remove_item(self):
        """Remove selected item"""
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected[0])
    
    def get_items(self) -> List[Tuple[str, ...]]:
        """Get all items in the tree view"""
        return [self.tree.item(item)["values"] for item in self.tree.get_children()]
    
    def clear(self):
        """Remove all items"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def add_items(self, items: List[Tuple[str, ...]]):
        """Add multiple items to the tree view"""
        for item in items:
            self.tree.insert("", tk.END, values=item) 