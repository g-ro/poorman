#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Components Package
~~~~~~~~~~~~~~~~~~

This package contains reusable UI components used across different views.
These components provide consistent behavior and appearance throughout the application.

Available Components:
    - EditableTreeView: A tree view widget that supports in-place editing
    - SyntaxText: A text widget that supports syntax highlighting

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

from .tree_view import EditableTreeView
from .syntax_text import SyntaxText

__all__ = ['EditableTreeView', 'SyntaxText'] 