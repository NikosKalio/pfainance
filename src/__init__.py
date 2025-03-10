"""
pfainance package: Tools for document processing and financial analysis.

This package provides utilities for loading and processing documents,
particularly focusing on financial data extraction and analysis.
"""

# Import and expose key functionality
from .document_loader import docs, loader

# Define what gets imported with "from src import *"
__all__ = ['docs', 'loader']

# Package metadata
__version__ = '0.1.0'
