#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Views Package
~~~~~~~~~~~

This package contains all the UI components and views of the application.
Views are responsible for displaying data and capturing user input.

Available Views:
    - MainWindow: The main application window
    - RequestPanel: Panel for configuring HTTP requests
    - ResponsePanel: Panel for displaying HTTP responses
    - Components: Reusable UI components

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

from .main_window import MainWindow
from .request_panel import RequestPanel
from .response_panel import ResponsePanel

__all__ = ['MainWindow', 'RequestPanel', 'ResponsePanel'] 