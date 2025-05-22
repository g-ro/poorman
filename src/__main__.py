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

import tkinter as tk
from views.main_window import MainWindow

def main():
    """Main entry point of the application"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main() 