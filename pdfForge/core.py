# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge Core Module
核心PDF处理模块

提供PDF文档的基础读取、解析和元数据提取功能。
Provides basic PDF document reading, parsing, and metadata extraction.
"""

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime


@dataclass
class PDFMetadata:
    """PDF元数据结构 / PDF Metadata Structure"""
    
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[str] = None
    modification_date: Optional[str] = None
    page_count: int = 0
    file_size: int = 0
    file_path: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 / Convert to dictionary"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为JSON字符串 / Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class PDFPage:
    """PDF页面结构 / PDF Page Structure"""
    
    page_number: int
    width: float = 0.0
    height: float = 0.0
    rotation: int = 0
    text_content: str = ""
    raw_content: str = ""
    
    def __str__(self) -> str:
        return f"Page {self.page_number}: {len(self.text_content)} chars"


@dataclass
class TextBlock:
    """文本块结构 / Text Block Structure"""
    
    text: str
    page_number: int
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    font_name: Optional[str] = None
    font_size: float = 0.0
    is_bold: bool = False
    is_italic: bool = False
    
    def is_heading(self, threshold: float = 14.0) -> bool:
        """判断是否为标题 / Check if it's a heading"""
        return self.font_size >= threshold
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "page_number": self.page_number,
            "position": {"x": self.x, "y": self.y},
            "size": {"width": self.width, "height": self.height},
            "font": {
                "name": self.font_name,
                "size": self.font_size,
                "bold": self.is_bold,
                "italic": self.is_italic
            }
        }


@dataclass 
class TableCell:
    """表格单元格 / Table Cell"""
    
    text: str
    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1
    x: float = 0.0
    y: float = 0.0
    
    def __str__(self) -> str:
        return self.text.strip()


@dataclass
class Table:
    """表格结构 / Table Structure"""
    
    page_number: int
    rows: int
    cols: int
    cells: List[List[str]] = field(default_factory=list)
    bbox: Tuple[float, float, float, float] = (0, 0, 0, 0)
    confidence: float = 0.0
    
    def to_csv(self) -> str:
        """转换为CSV格式 / Convert to CSV format"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        for row in self.cells:
            # 转义CSV特殊字符
            escaped_row = []
            for cell in row:
                cell = cell.replace('"', '""')
                if ',' in cell or '"' in cell or '\n' in cell:
                    cell = f'"{cell}"'
                escaped_row.append(cell)
            writer.writerow(escaped_row)
        
        return output.getvalue()
    
    def to_html(self) -> str:
        """转换为HTML表格 / Convert to HTML table"""
        html = ['<table border="1">']
        
        for row in self.cells:
            html.append('  <tr>')
            for cell in row:
                cell_text = cell.replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
                html.append(f'    <td>{cell_text}</td>')
            html.append('  </tr>')
        
        html.append('</table>')
        return '\n'.join(html)
    
    def to_json(self) -> str:
        """转换为JSON格式 / Convert to JSON format"""
        return json.dumps({
            "page_number": self.page_number,
            "rows": self.rows,
            "cols": self.cols,
            "bbox": list(self.bbox),
            "confidence": self.confidence,
            "cells": self.cells
        }, indent=2, ensure_ascii=False)


class PDFDocument:
    """PDF文档类 / PDF Document Class"""
    
    def __init__(self, file_path: str):
        """
        初始化PDF文档 / Initialize PDF Document
        
        Args:
            file_path: PDF文件路径 / PDF file path
        """
        self.file_path = Path(file_path)
        self.metadata = PDFMetadata(file_path=str(self.file_path))
        self.pages: List[PDFPage] = []
        self._text_extractor = None
        self._page_cache = {}
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        self.metadata.file_size = self.file_path.stat().st_size
    
    def parse(self, use_basic: bool = True) -> 'PDFDocument':
        """
        解析PDF文档 / Parse PDF Document
        
        Args:
            use_basic: 是否使用基础解析模式（零依赖）/ Use basic parsing mode (zero dependency)
        """
        self._parse_basic()
        self.metadata.page_count = len(self.pages)
        return self
    
    def _parse_basic(self) -> None:
        """基础PDF解析 - 零依赖实现 / Basic PDF parsing - Zero dependency implementation"""
        with open(self.file_path, 'rb') as f:
            content = f.read()
        
        # 提取元数据
        self._extract_metadata_basic(content)
        
        # 提取页面数
        page_count = self._extract_page_count(content)
        
        # 提取文本内容
        text_content = self._extract_text_basic(content)
        
        # 创建页面对象
        for i in range(page_count):
            page = PDFPage(
                page_number=i + 1,
                text_content=text_content,
                raw_content=content.decode('latin-1', errors='ignore')[:5000]  # 只保存部分原始内容
            )
            self.pages.append(page)
    
    def _extract_metadata_basic(self, content: bytes) -> None:
        """基础元数据提取 / Basic metadata extraction"""
        try:
            content_str = content.decode('latin-1', errors='ignore')
            
            # 提取Title
            title_match = re.search(r'/Title\s*\(([^)]+)\)', content_str)
            if title_match:
                self.metadata.title = self._decode_pdf_string(title_match.group(1))
            
            # 提取Author
            author_match = re.search(r'/Author\s*\(([^)]+)\)', content_str)
            if author_match:
                self.metadata.author = self._decode_pdf_string(author_match.group(1))
            
            # 提取Subject
            subject_match = re.search(r'/Subject\s*\(([^)]+)\)', content_str)
            if subject_match:
                self.metadata.subject = self._decode_pdf_string(subject_match.group(1))
            
            # 提取Creator
            creator_match = re.search(r'/Creator\s*\(([^)]+)\)', content_str)
            if creator_match:
                self.metadata.creator = self._decode_pdf_string(creator_match.group(1))
            
            # 提取Producer
            producer_match = re.search(r'/Producer\s*\(([^)]+)\)', content_str)
            if producer_match:
                self.metadata.producer = self._decode_pdf_string(producer_match.group(1))
            
            # 提取CreationDate
            date_match = re.search(r'/CreationDate\s*\(([^)]+)\)', content_str)
            if date_match:
                self.metadata.creation_date = date_match.group(1)
            
            # 提取ModDate
            mod_match = re.search(r'/ModDate\s*\(([^)]+)\)', content_str)
            if mod_match:
                self.metadata.modification_date = mod_match.group(1)
                
        except Exception:
            pass
    
    def _extract_page_count(self, content: bytes) -> int:
        """提取页面数量 / Extract page count"""
        content_str = content.decode('latin-1', errors='ignore')
        
        # 查找 /Type /Page 出现次数
        page_matches = re.findall(r'/Type\s*/Page[^s]', content_str)
        count = len(page_matches)
        
        if count == 0:
            # 备选方案：查找 /Count
            count_match = re.search(r'/Count\s+(\d+)', content_str)
            if count_match:
                count = int(count_match.group(1))
        
        return max(count, 1)
    
    def _extract_text_basic(self, content: bytes) -> str:
        """基础文本提取 - 提取可读的文本内容 / Basic text extraction"""
        text_parts = []
        
        try:
            content_str = content.decode('latin-1', errors='ignore')
            
            # 提取BT...ET块中的文本
            text_blocks = re.findall(r'BT\s*(.*?)\s*ET', content_str, re.DOTALL)
            
            for block in text_blocks:
                # 提取Tj和TJ操作符中的文本
                tj_matches = re.findall(r'\(([^)]+)\)\s*Tj', block)
                for match in tj_matches:
                    decoded = self._decode_pdf_string(match)
                    if decoded.strip():
                        text_parts.append(decoded)
                
                # 提取TJ数组中的文本
                tj_arrays = re.findall(r'\[(.*?)\]\s*TJ', block, re.DOTALL)
                for arr in tj_arrays:
                    inner_texts = re.findall(r'\(([^)]+)\)', arr)
                    combined = ''.join([self._decode_pdf_string(t) for t in inner_texts])
                    if combined.strip():
                        text_parts.append(combined)
                        
        except Exception:
            pass
        
        return '\n'.join(text_parts)
    
    def _decode_pdf_string(self, s: str) -> str:
        """解码PDF字符串 / Decode PDF string"""
        if not s:
            return ""
        
        # 处理转义序列
        result = []
        i = 0
        while i < len(s):
            if s[i] == '\\':
                i += 1
                if i < len(s):
                    c = s[i]
                    if c == 'n':
                        result.append('\n')
                    elif c == 'r':
                        result.append('\r')
                    elif c == 't':
                        result.append('\t')
                    elif c == '\\':
                        result.append('\\')
                    elif c == '(':
                        result.append('(')
                    elif c == ')':
                        result.append(')')
                    elif c.isdigit():
                        # 八进制转义
                        oct_str = c
                        for _ in range(2):
                            if i + 1 < len(s) and s[i + 1].isdigit():
                                oct_str += s[i + 1]
                                i += 1
                        try:
                            result.append(chr(int(oct_str, 8)))
                        except ValueError:
                            result.append(c)
                    else:
                        result.append(c)
            else:
                result.append(s[i])
            i += 1
        
        return ''.join(result)
    
    def get_text(self, pages: Optional[List[int]] = None) -> str:
        """
        获取文本内容 / Get text content
        
        Args:
            pages: 指定页面列表，None表示所有页面 / Specified page list, None for all pages
        """
        if pages is None:
            return '\n\n'.join([p.text_content for p in self.pages])
        
        selected_pages = [p for p in self.pages if p.page_number in pages]
        return '\n\n'.join([p.text_content for p in selected_pages])
    
    def get_full_text(self) -> str:
        """获取完整文本内容 / Get full text content"""
        return self.get_text()
    
    def to_json(self, include_pages: bool = True) -> str:
        """
        转换为JSON格式 / Convert to JSON format
        
        Args:
            include_pages: 是否包含页面内容 / Include page content
        """
        data = {
            "metadata": self.metadata.to_dict(),
        }
        
        if include_pages:
            data["pages"] = [
                {
                    "page_number": p.page_number,
                    "text_content": p.text_content,
                    "width": p.width,
                    "height": p.height
                }
                for p in self.pages
            ]
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def __len__(self) -> int:
        """返回页面数量 / Return page count"""
        return len(self.pages)
    
    def __repr__(self) -> str:
        return f"PDFDocument(pages={len(self.pages)}, file={self.file_path.name})"
