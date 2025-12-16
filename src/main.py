#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PoorMan REST API Testing Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~

Main entry point for the PoorMan application.
This file is used both for running the application directly
and for creating the executable.

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk
from views.main_window import MainWindow
from utils.logging_config import logger, install_global_exception_hooks

def main():
    """Main function to run the application"""
    # Create root window but don't show it yet
    root = tk.Tk()
    root.withdraw()

    # Install global exception hooks to capture all errors
    install_global_exception_hooks(root)
    
    # Set application icon
    try:
        # Get the directory containing the script/executable
        if getattr(sys, 'frozen', False):
            # If running as compiled executable
            base_dir = os.path.dirname(sys.executable)
            icon_path = os.path.join(base_dir, 'resources', 'poorman.ico')
            if not os.path.exists(icon_path):
                # Try looking in temp directory where PyInstaller extracts files
                base_dir = sys._MEIPASS
                icon_path = os.path.join(base_dir, 'resources', 'poorman.ico')
        else:
            # If running as script
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, 'resources', 'poorman.ico')
        
        # Load and set the icon
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            logger.warning("Could not find icon at %s", icon_path)
    except Exception as e:
        logger.exception("Could not load application icon")
    
    # Configure style
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass
    
    # Create the application (this will configure the window)
    app = MainWindow(root)
    
    # Center the window on screen
    root.eval('tk::PlaceWindow . center')
    
    # Show the window now that it's fully configured
    root.deiconify()
    
    # Start the application
    root.mainloop()

if __name__ == '__main__':
    main() 