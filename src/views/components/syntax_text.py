#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syntax Highlighting Text Widget
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A custom text widget that supports syntax highlighting for different formats.
Currently supports JSON formatting with color highlighting.

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

import json
import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any
import re

from utils.logging_config import logger

class SyntaxText(tk.Text):
    """
    A text widget that supports syntax highlighting.
    Currently supports JSON formatting with color highlighting.
    
    Attributes:
        json_colors (dict): Color configuration for JSON syntax highlighting
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize the syntax highlighting text widget."""
        super().__init__(*args, **kwargs)
        
        # Configure tags for syntax highlighting
        self.json_colors = {
            'string': '#008000',  # Green
            'number': '#0000FF',  # Blue
            'boolean': '#FF00FF', # Magenta
            'null': '#808080',    # Gray
            'key': '#000080',     # Navy
            'error': '#FF0000'    # Red
        }
        
        # Create tags with their colors
        for tag, color in self.json_colors.items():
            self.tag_configure(tag, foreground=color)
        
        # Make the widget read-only
        self.bind("<Key>", self._readonly)
        
        # Enable horizontal scrolling
        self.config(wrap=tk.NONE)
        
        # Configure tab size (8 spaces)
        self.config(tabs=('8c'))
    
    def _readonly(self, event):
        """Make the widget read-only except for copy operations."""
        return "break" if event.keysym not in ("c", "C", "Copy") else None
    
    def clear(self):
        """Clear all text from the widget."""
        self.delete("1.0", tk.END)
    
    def highlight_json(self, text: str) -> None:
        """
        Display and highlight JSON text.
        
        Args:
            text (str): The JSON text to highlight
        """
        self.clear()
        
        try:
            # Parse and reformat the JSON
            if isinstance(text, (str, bytes)):
                if isinstance(text, bytes):
                    text = text.decode('utf-8')
                parsed = json.loads(text)
            else:
                parsed = text
                
            # Format with proper indentation
            formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
            
            # Insert the formatted text
            self.insert("1.0", formatted)
            
            # Apply syntax highlighting
            self._highlight_json_syntax()
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            # Show raw text with error message
            self.insert("1.0", f"Error parsing JSON: {e}\n\nRaw content:\n{text}")
            self.tag_add("error", "1.0", "2.0")
        except Exception as e:
            logger.error(f"Error formatting JSON: {e}")
            self.insert("1.0", str(text))
    
    def _highlight_json_syntax(self):
        """Apply JSON syntax highlighting to the current content."""
        # Remove any existing tags
        for tag in self.json_colors:
            self.tag_remove(tag, "1.0", tk.END)
        
        content = self.get("1.0", tk.END)
        
        # Define regex patterns for JSON elements
        patterns = {
            'string': r'"(?:[^"\\]|\\.)*"(?=:)',  # Keys
            'value_string': r':\s*"(?:[^"\\]|\\.)*"',  # String values
            'number': r':\s*-?\d+\.?\d*',  # Numbers
            'boolean': r':\s*(true|false)\b',  # Booleans
            'null': r':\s*null\b'  # Null values
        }
        
        # Apply highlighting
        for tag, pattern in patterns.items():
            self._highlight_pattern(pattern, tag if tag != 'value_string' else 'string')
    
    def _highlight_pattern(self, pattern: str, tag: str):
        """
        Apply a tag to all text that matches the pattern.
        
        Args:
            pattern (str): Regular expression pattern to match
            tag (str): Tag to apply to matched text
        """
        content = self.get("1.0", tk.END)
        
        for match in re.finditer(pattern, content):
            start = match.start()
            end = match.end()
            
            # For value patterns, adjust start to skip the colon and whitespace
            if pattern.startswith(':\\s*'):
                start = start + len(re.match(r':\s*', match.group()).group())
            
            # Convert character positions to text widget indices
            start_line = content.count('\n', 0, start) + 1
            start_char = start - content.rfind('\n', 0, start) - 1
            end_line = content.count('\n', 0, end) + 1
            end_char = end - content.rfind('\n', 0, end) - 1
            
            self.tag_add(tag, f"{start_line}.{start_char}", f"{end_line}.{end_char}")
    
    def set_content(self, content: str, content_type: Optional[str] = None):
        """
        Set the widget content with appropriate formatting.
        
        Args:
            content (str): The content to display
            content_type (str, optional): Content type for formatting selection
        """
        self.clear()
        
        if content_type and 'json' in content_type.lower():
            self.highlight_json(content)
        else:
            try:
                # Try to parse as JSON even if content-type is not specified
                json.loads(content if isinstance(content, str) else content.decode('utf-8'))
                self.highlight_json(content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # If not JSON, display as plain text
                if isinstance(content, bytes):
                    try:
                        content = content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = str(content)
                self.insert("1.0", content)
        
        # Reset view to top
        self.see("1.0") 