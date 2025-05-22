#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Panel Module
~~~~~~~~~~~~~~~~~

This module implements the response panel that displays HTTP response data
with proper formatting and syntax highlighting.

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import json

from models.response_model import ResponseModel
from views.components import SyntaxText
from utils.logging_config import logger

class ResponsePanel:
    """
    Panel for displaying HTTP response data with formatting.
    
    This panel shows:
        - Response status and metadata
        - Formatted response content with syntax highlighting
        - Horizontal and vertical scrolling for large responses
    
    Attributes:
        frame (ttk.Frame): The main container frame
        status_label (ttk.Label): Label showing response status
        time_label (ttk.Label): Label showing response time
        size_label (ttk.Label): Label showing response size
        response_text (SyntaxText): Text widget for response content
    """
    
    def __init__(self, parent: ttk.Frame):
        """
        Initialize the response panel.
        
        Args:
            parent (ttk.Frame): Parent frame to contain this panel
        """
        self.frame = ttk.LabelFrame(parent, text="Response", padding="5")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        # Response info frame
        info_frame = ttk.Frame(self.frame)
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(info_frame, text="Status: -")
        self.status_label.grid(row=0, column=0, padx=(0, 20))
        
        # Time label
        self.time_label = ttk.Label(info_frame, text="Time: -")
        self.time_label.grid(row=0, column=1, padx=(0, 20))
        
        # Size label
        self.size_label = ttk.Label(info_frame, text="Size: -")
        self.size_label.grid(row=0, column=2)
        
        # Create text widget with both scrollbars
        text_frame = ttk.Frame(self.frame)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Response text with syntax highlighting
        self.response_text = SyntaxText(
            text_frame,
            wrap=tk.NONE,
            width=40,
            height=20,
            font=("Consolas", 10)
        )
        self.response_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Vertical scrollbar
        vert_scroll = ttk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=self.response_text.yview
        )
        vert_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Horizontal scrollbar
        horz_scroll = ttk.Scrollbar(
            text_frame,
            orient=tk.HORIZONTAL,
            command=self.response_text.xview
        )
        horz_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure text widget scrolling
        self.response_text.configure(
            yscrollcommand=vert_scroll.set,
            xscrollcommand=horz_scroll.set
        )
    
    def display_response(self, response: ResponseModel):
        """
        Display the response data with appropriate formatting.
        
        Args:
            response (ResponseModel): The response to display
        """
        logger.debug(f"Displaying response: {response}")
        
        # Update status with color
        status_code = response.status_code
        status_color = (
            "green" if 200 <= status_code < 300
            else "red" if status_code >= 400
            else "orange"
        )
        self.status_label.config(
            text=f"Status: {status_code} {response.reason}",
            foreground=status_color
        )
        
        # Update time
        self.time_label.config(text=f"Time: {response.elapsed_time} ms")
        
        # Update size
        content_length = len(response.content) if response.content else 0
        size_text = (
            f"{round(content_length / 1024, 2)} KB"
            if content_length > 1024
            else f"{content_length} bytes"
        )
        self.size_label.config(text=f"Size: {size_text}")
        
        # Display content with formatting
        content_type = response.headers.get('content-type', '')
        
        try:
            # Decode content from bytes
            content = response.content.decode('utf-8') if response.content else ''
            
            # If it's JSON content, try to parse and format it
            if 'json' in content_type.lower():
                try:
                    parsed_json = json.loads(content)
                    formatted_content = json.dumps(parsed_json, indent=2)
                    self.response_text.set_content(formatted_content, content_type)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing error: {e}")
                    self.response_text.set_content(content, None)
            else:
                self.response_text.set_content(content, content_type)
        except UnicodeDecodeError as e:
            logger.error(f"Content decoding error: {e}")
            self.response_text.set_content("Binary content (cannot display)", None)
        
        # Scroll to top
        self.response_text.see("1.0") 