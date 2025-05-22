#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PoorMan - A lightweight REST API testing tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A cross-platform desktop application for testing REST APIs, similar to Postman.
Built with Python and Tkinter, it provides a user-friendly interface for making
HTTP requests, handling authentication, and managing API testing workflows.

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = "PoorMan"
__description__ = "A lightweight, cross-platform desktop application for testing REST APIs, similar to Postman. Built with Python and Tkinter."
__version__ = "0.1"
__author__ = "Rohit Gupta"
__author_email__ = "grohit11@gmail.com"
__license__ = "Apache License 2.0"
__copyright__ = "Copyright 2024 Rohit Gupta"
__website__ = "https://github.com/g-ro/poorman"
__status__ = "Beta"

# Additional metadata that can be useful
__keywords__ = ["rest", "api", "testing", "http", "client", "postman"]
__requires__ = [
    "requests>=2.31.0",
    "requests-oauthlib>=1.3.1",
    "urllib3>=2.0.7"
]

__all__ = [
    '__title__', '__description__', '__version__', '__author__',
    '__author_email__', '__license__', '__copyright__', '__website__',
    '__status__', '__keywords__', '__requires__'
] 