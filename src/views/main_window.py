#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window Module
~~~~~~~~~~~~~~~~

This module implements the main application window for the PoorMan REST API testing tool.
It serves as the primary container for all UI components and coordinates the interaction
between different parts of the application.

Key Components:
    - Request Panel: For configuring and sending HTTP requests
    - Response Panel: For displaying response data
    - Menu System: File operations and application information
    - Status Bar: For showing current application state

Example:
    To use this module, create a tkinter root window and initialize MainWindow:

    >>> import tkinter as tk
    >>> from views.main_window import MainWindow
    >>> root = tk.Tk()
    >>> app = MainWindow(root)
    >>> root.mainloop()

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import webbrowser

from models.request_model import RequestModel
from models.response_model import ResponseModel
from controllers.request_controller import RequestController
from views.request_panel import RequestPanel
from views.response_panel import ResponsePanel
from utils.logging_config import logger, redact_headers
from version import (
    __title__, __description__, __version__, __author__,
    __license__, __copyright__, __website__, __status__
)

class MainWindow:
    """
    Main application window class that manages the overall UI layout and interactions.
    
    This class is responsible for:
        - Creating and managing the main application window
        - Setting up the menu system
        - Coordinating between request and response panels
        - Managing the application lifecycle
        - Handling file operations (save/load requests)
    
    Attributes:
        root (tk.Tk): The root window instance
        request_controller (RequestController): Controller for handling request operations
        request_panel (RequestPanel): Panel for configuring requests
        response_panel (ResponsePanel): Panel for displaying responses
        status_bar (ttk.Label): Status bar for showing application state
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window with all its components.
        
        Args:
            root (tk.Tk): The root window instance for the application
        """
        logger.info("Initializing main window")
        self.root = root
        
        # Configure window
        self.root.title(f"{__title__} v{__version__}")
        self.root.minsize(800, 600)  # Set minimum window size
        self.root.geometry("1200x800")  # Set default size
        
        # Configure grid weights for proper resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main container with proper padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Initialize controller
        logger.debug("Initializing request controller")
        self.request_controller = RequestController(self.on_response_received)
        
        # Create request panel
        logger.debug("Creating request panel")
        self.request_panel = RequestPanel(main_frame, self.on_send_request)
        self.request_panel.request_controller = self.request_controller
        self.request_panel.frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create response panel
        logger.debug("Creating response panel")
        self.response_panel = ResponsePanel(main_frame)
        self.response_panel.frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Set up menu
        self.create_menu()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        logger.info("Main window initialization completed")
    
    def create_menu(self):
        """Create and configure the application menu system."""
        logger.debug("Creating application menu")
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Request", command=self.save_request)
        file_menu.add_command(label="Load Request", command=self.load_request)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        help_menu.add_command(label="Visit Website", command=lambda: webbrowser.open(__website__))
        logger.debug("Application menu created")
    
    def show_about_dialog(self):
        """Display the About dialog with application information."""
        logger.debug("Showing About dialog")
        about_window = tk.Toplevel(self.root)
        about_window.title(f"About {__title__}")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center the window
        about_window.geometry(f"+{self.root.winfo_x() + 150}+{self.root.winfo_y() + 150}")
        
        # Create a frame with padding
        frame = ttk.Frame(about_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Application name and version (larger font)
        name_label = ttk.Label(
            frame,
            text=f"{__title__} v{__version__}",
            font=("Helvetica", 16, "bold")
        )
        name_label.pack(pady=(0, 10))
        
        # Status label
        status_label = ttk.Label(
            frame,
            text=f"Status: {__status__}",
            font=("Helvetica", 10, "italic")
        )
        status_label.pack()
        
        # Description
        desc_label = ttk.Label(
            frame,
            text=__description__,
            wraplength=400,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(10, 20))
        
        # Developer info
        dev_label = ttk.Label(
            frame,
            text=f"Developer: {__author__}",
            font=("Helvetica", 10)
        )
        dev_label.pack()
        
        # License info
        license_label = ttk.Label(
            frame,
            text=__copyright__ + "\n" + f"Licensed under {__license__}",
            justify=tk.CENTER
        )
        license_label.pack(pady=(20, 0))
        
        # Website link (clickable)
        website_label = ttk.Label(
            frame,
            text=__website__,
            foreground="blue",
            cursor="hand2"
        )
        website_label.pack(pady=(10, 20))
        website_label.bind("<Button-1>", lambda e: webbrowser.open(__website__))
        
        # Close button
        ttk.Button(
            frame,
            text="Close",
            command=about_window.destroy
        ).pack(pady=(20, 0))
    
    def on_send_request(self, request: RequestModel):
        """
        Handle the send request action.
        
        Args:
            request (RequestModel): The request to be sent
        """
        logger.info(f"Sending {request.method} request to {request.url}")
        try:
            safe_details = {
                'method': request.method,
                'url': request.url,
                'params': list(request.params.keys()),
                'headers': list(redact_headers(request.headers).items()),
                'body_type': request.body_type,
                'body_size': len(request.body_content or '') if request.body_type in ['raw', 'json'] else len(request.form_data or {}),
                'auth_type': request.auth_type,
            }
            logger.debug(f"Request details: {safe_details}")
        except Exception:
            logger.debug("Failed to log request details safely", exc_info=True)
        self.status_bar.config(text="Sending request...")
        self.request_controller.send_request(request)
    
    def on_response_received(self, response: ResponseModel):
        """
        Handle the received response.
        
        Args:
            response (ResponseModel): The response received from the request
        """
        logger.info(f"Received response with status code: {response.status_code}")
        logger.debug(f"Response details: {response}")
        self.response_panel.display_response(response)
        if response.is_success:
            self.status_bar.config(text="Request completed")
        else:
            if response.status_code == 0 and response.error:
                self.status_bar.config(text=f"Error: {response.error}")
            else:
                self.status_bar.config(text="Request failed")
    
    def save_request(self):
        """Save the current request configuration to a file."""
        logger.debug("Opening save request dialog")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Request"
        )
        if file_path:
            logger.info(f"Saving request to file: {file_path}")
            request = self.request_panel.get_request()
            self.request_controller.save_request(request, file_path)
            self.status_bar.config(text=f"Request saved to {file_path}")
    
    def load_request(self):
        """Load a request configuration from a file."""
        logger.debug("Opening load request dialog")
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load Request"
        )
        if file_path:
            logger.info(f"Loading request from file: {file_path}")
            request = self.request_controller.load_request(file_path)
            if request:
                self.request_panel.set_request(request)
                self.status_bar.config(text=f"Request loaded from {file_path}")
    
    def on_closing(self):
        """Handle the application closing event."""
        logger.debug("Application closing requested")
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            logger.info("Application shutting down")
            self.root.destroy() 