#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging Configuration Module
~~~~~~~~~~~~~~~~~~~~~~~~~

This module configures the application-wide logging system with best practices:
- Logs to both file and console with different levels
- Rotates log files to manage storage
- Provides formatted output with timestamp, level, and context
- Supports different log levels for different environments

Example:
    To use this logger in any module:
    >>> from utils.logging_config import logger
    >>> logger.debug("Debug message")
    >>> logger.info("Info message")
    >>> logger.error("Error message")

:copyright: (c) 2024 by Rohit Gupta.
:license: Apache 2.0, see LICENSE for more details.
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional

from version import __title__

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file path
LOG_FILE = LOGS_DIR / f"{__title__.lower()}.log"

# Log format with all necessary information
LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - "
    "%(funcName)s() - %(message)s"
)

# Date format for logs
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(
    logger_name: str = __title__,
    log_file: Path = LOG_FILE,
    level: int = logging.INFO,
    console_level: Optional[int] = None
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        logger_name: Name of the logger (default: application name)
        log_file: Path to the log file (default: logs/poorman.log)
        level: Logging level for file handler (default: INFO)
        console_level: Logging level for console handler (default: same as level)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        DATE_FORMAT
    )
    
    # File handler (with rotation)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level or level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

# Create the default logger
logger = setup_logger()

def set_log_level(level: int) -> None:
    """
    Set the log level for both file and console handlers.
    
    Args:
        level: The logging level to set (e.g., logging.DEBUG)
    """
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

# Set debug level if environment variable is set
if os.environ.get("POORMAN_DEBUG"):
    set_log_level(logging.DEBUG)

__all__ = ['logger', 'set_log_level', 'setup_logger'] 