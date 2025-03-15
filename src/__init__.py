"""
pfainance package: Tools for document processing and financial analysis.

This package provides utilities for loading and processing documents,
particularly focusing on financial data extraction and analysis.
"""

# Import and expose key functionality
from .document_loader import convert_pdf_to_markdown
from .local_llm import OllamaLLM
from .models import Institution, Account, Transaction, AccountType, TransactionType, InstitutionType
# Define what gets imported with "from src import *"
__all__ = ['convert_pdf_to_markdown', 'OllamaLLM']

# Package metadata
__version__ = '0.1.0'
