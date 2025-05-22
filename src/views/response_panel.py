import tkinter as tk
from tkinter import ttk, scrolledtext
import json

from models.response_model import ResponseModel

class ResponsePanel:
    def __init__(self, parent: ttk.Frame):
        self.parent = parent
        
        # Create main frame
        self.frame = ttk.LabelFrame(parent, text="Response", padding="5")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Response info frame
        info_frame = ttk.Frame(self.frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status code label
        self.status_label = ttk.Label(info_frame, text="Status: -", foreground="blue")
        self.status_label.grid(row=0, column=0, padx=(0, 20))
        
        # Time label
        self.time_label = ttk.Label(info_frame, text="Time: -")
        self.time_label.grid(row=0, column=1, padx=(0, 20))
        
        # Size label
        self.size_label = ttk.Label(info_frame, text="Size: -")
        self.size_label.grid(row=0, column=2)
        
        # Response text area
        self.response_text = scrolledtext.ScrolledText(self.frame, height=15, wrap=tk.WORD)
        self.response_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def display_response(self, response: ResponseModel):
        """Display response data"""
        # Update status with color
        status_color = "green" if response.is_success else "red"
        self.status_label.config(
            text=f"Status: {response.status_code} {response.reason}",
            foreground=status_color
        )
        
        # Update time and size
        self.time_label.config(text=f"Time: {round(response.elapsed_time, 2)} ms")
        self.size_label.config(text=f"Size: {response.size_formatted}")
        
        # Display response content
        self.response_text.delete("1.0", tk.END)
        
        if response.error:
            self.response_text.insert("1.0", f"Error: {response.error}")
            return
        
        try:
            # Try to format as JSON
            if response.is_json:
                content = json.loads(response.content)
                formatted_content = json.dumps(content, indent=2)
            else:
                formatted_content = response.content.decode('utf-8')
            
            self.response_text.insert("1.0", formatted_content)
            
        except Exception as e:
            # If formatting fails, display raw content
            self.response_text.insert("1.0", response.content.decode('utf-8', errors='replace')) 