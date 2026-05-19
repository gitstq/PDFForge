# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge Package
零依赖智能PDF文档分析与处理引擎
Zero-Dependency Intelligent PDF Document Analysis & Processing Engine

Usage:
    from pdfForge import PDFDocument, TextExtractor, TableExtractor
    
    # Load PDF
    doc = PDFDocument("document.pdf")
    doc.parse()
    
    # Extract text
    text = doc.get_full_text()
    
    # Extract tables
    extractor = TableExtractor(doc)
    tables = extractor.detect_tables()
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__email__ = "gitstq@github.com"
__license__ = "MIT"
__description__ = "Zero-Dependency Intelligent PDF Document Analysis & Processing Engine"

from .core import (
    PDFDocument,
    PDFMetadata,
    PDFPage,
    TextBlock,
    Table,
    TableCell
)

from .extractor import (
    TextExtractor,
    TableExtractor,
    StructureAnalyzer,
    MarkdownConverter
)

from .utils import (
    sanitize_filename,
    get_file_hash,
    truncate_text,
    split_into_chunks,
    validate_pdf,
    get_pdf_preview_text,
    merge_pdf_texts
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    
    # Core classes
    "PDFDocument",
    "PDFMetadata",
    "PDFPage",
    "TextBlock",
    "Table",
    "TableCell",
    
    # Extractors
    "TextExtractor",
    "TableExtractor",
    "StructureAnalyzer",
    "MarkdownConverter",
    
    # Utilities
    "sanitize_filename",
    "get_file_hash",
    "truncate_text",
    "split_into_chunks",
    "validate_pdf",
    "get_pdf_preview_text",
    "merge_pdf_texts"
]
