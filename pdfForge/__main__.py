# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge CLI Entry Point
命令行入口点

允许直接使用 python -m pdfForge 运行
Allows running with: python -m pdfForge
"""

from .cli import main

if __name__ == "__main__":
    exit(main())
