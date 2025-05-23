#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Script for PoorMan
~~~~~~~~~~~~~~~~~~~~~

This script creates a Windows executable using PyInstaller.
Run this script to generate the executable in the dist/ directory.

Usage:
    python build_exe.py

Requirements:
    pip install pyinstaller
"""

import PyInstaller.__main__
import os
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    # Get the absolute path of the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path to the main script
    main_script = os.path.join(script_dir, 'src', 'main.py')
    
    # Define icon path
    icon_path = os.path.join(script_dir, 'resources', 'poorman.ico')
    
    # Ensure icon exists
    if not os.path.exists(icon_path):
        print(f"Warning: Icon file not found at {icon_path}")
        sys.exit(1)
    
    # Define data files to include
    resources_path = os.path.join(script_dir, 'resources')
    
    # PyInstaller command line arguments
    args = [
        main_script,  
        '--name=PoorMan',  
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window when running the executable
        '--icon=' + icon_path,  
        '--add-data=src;src',  # Include the src directory
        f'--add-data={resources_path};resources',  # Include the resources directory
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace existing dist directory without confirmation
    ]
    
    # Add hidden imports for tkinter
    hidden_imports = [
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=requests',
        '--hidden-import=requests_oauthlib',
        '--hidden-import=urllib3',
    ]
    
    args.extend(hidden_imports)
    
    print(f"Building executable from: {main_script}")
    print(f"Working directory: {script_dir}")
    print(f"Including resources from: {resources_path}")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_exe() 