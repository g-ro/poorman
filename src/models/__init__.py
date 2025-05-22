#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Models Package
~~~~~~~~~~~~

This package contains the data models used throughout the application.
Models represent the core data structures and their behaviors.

Available Models:
    - RequestModel: Represents an HTTP request with all its parameters
    - ResponseModel: Represents an HTTP response with its data

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

from .request_model import RequestModel
from .response_model import ResponseModel

__all__ = ['RequestModel', 'ResponseModel'] 