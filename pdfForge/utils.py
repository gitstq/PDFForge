# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge Utility Module
工具函数模块

提供通用工具函数。
Provides common utility functions.
"""

import re
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符 / Sanitize filename, remove illegal characters
    
    Args:
        filename: 原始文件名 / Original filename
        
    Returns:
        清理后的文件名 / Sanitized filename
    """
    # 移除Windows非法字符
    illegal_chars = r'[<>:"|?*\\/]'
    filename = re.sub(illegal_chars, '_', filename)
    
    # 移除前后空格
    filename = filename.strip()
    
    # 限制长度
    if len(filename) > 200:
        name, ext = Path(filename).stem, Path(filename).suffix
        filename = name[:200-len(ext)] + ext
    
    return filename


def get_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
    """
    计算文件哈希值 / Calculate file hash
    
    Args:
        file_path: 文件路径 / File path
        algorithm: 哈希算法 (md5, sha1, sha256) / Hash algorithm
        
    Returns:
        十六进制哈希字符串 / Hex hash string
    """
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本 / Truncate text
    
    Args:
        text: 原始文本 / Original text
        max_length: 最大长度 / Maximum length
        suffix: 后缀 / Suffix
        
    Returns:
        截断后的文本 / Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def split_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    将文本分割为重叠的块 / Split text into overlapping chunks
    
    Args:
        text: 原始文本 / Original text
        chunk_size: 块大小 / Chunk size
        overlap: 重叠大小 / Overlap size
        
    Returns:
        文本块列表 / List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


def detect_encoding(file_path: str) -> str:
    """
    检测文件编码 / Detect file encoding
    
    Args:
        file_path: 文件路径 / File path
        
    Returns:
        编码名称 / Encoding name
    """
    import chardet
    
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding'] or 'utf-8'


def count_pdf_pages(file_path: str) -> int:
    """
    快速统计PDF页数 / Quick count PDF pages
    
    Args:
        file_path: PDF文件路径 / PDF file path
        
    Returns:
        页数 / Page count
    """
    import re
    
    with open(file_path, 'rb') as f:
        content = f.read().decode('latin-1', errors='ignore')
        
        # 查找页面数
        count_match = re.search(r'/Count\s+(\d+)', content)
        if count_match:
            return int(count_match.group(1))
        
        # 备选：统计/Type/Page
        page_matches = re.findall(r'/Type\s*/Page[^s]', content)
        return max(len(page_matches), 1)


def validate_pdf(file_path: str) -> Tuple[bool, Optional[str]]:
    """
    验证PDF文件 / Validate PDF file
    
    Args:
        file_path: 文件路径 / File path
        
    Returns:
        (是否有效, 错误信息) / (Is valid, Error message)
    """
    path = Path(file_path)
    
    # 检查文件存在
    if not path.exists():
        return False, "File not found"
    
    # 检查文件扩展名
    if path.suffix.lower() != '.pdf':
        return False, "Not a PDF file"
    
    # 检查文件大小
    if path.stat().st_size == 0:
        return False, "File is empty"
    
    # 检查PDF头部
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
            
            if not header.startswith(b'%PDF-'):
                return False, "Invalid PDF header"
            
        return True, None
        
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def get_pdf_preview_text(file_path: str, max_chars: int = 2000) -> str:
    """
    获取PDF预览文本 / Get PDF preview text
    
    Args:
        file_path: PDF文件路径 / PDF file path
        max_chars: 最大字符数 / Maximum characters
        
    Returns:
        预览文本 / Preview text
    """
    from .core import PDFDocument
    
    try:
        doc = PDFDocument(file_path)
        doc.parse()
        
        text = doc.get_full_text()
        
        # 清理文本
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text[:max_chars]
        
    except Exception:
        return ""


def merge_pdf_texts(files: List[str]) -> str:
    """
    合并多个PDF文本 / Merge multiple PDF texts
    
    Args:
        files: PDF文件路径列表 / List of PDF file paths
        
    Returns:
        合并后的文本 / Merged text
    """
    from .core import PDFDocument
    
    texts = []
    
    for file_path in files:
        try:
            doc = PDFDocument(file_path)
            doc.parse()
            texts.append(doc.get_full_text())
        except Exception:
            continue
    
    return '\n\n'.join(texts)


class ProgressBar:
    """简单的进度条 / Simple progress bar"""
    
    def __init__(self, total: int, width: int = 40, desc: str = "Progress"):
        self.total = total
        self.width = width
        self.desc = desc
        self.current = 0
    
    def update(self, n: int = 1) -> None:
        """更新进度 / Update progress"""
        self.current += n
        self._draw()
    
    def _draw(self) -> None:
        """绘制进度条 / Draw progress bar"""
        percent = self.current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        
        print(f'\r{self.desc}: |{bar}| {percent:.1%} ({self.current}/{self.total})', end='')
        
        if self.current >= self.total:
            print()
    
    def close(self) -> None:
        """关闭进度条 / Close progress bar"""
        if self.current < self.total:
            print()


__all__ = [
    'sanitize_filename',
    'get_file_hash',
    'truncate_text',
    'split_into_chunks',
    'detect_encoding',
    'count_pdf_pages',
    'validate_pdf',
    'get_pdf_preview_text',
    'merge_pdf_texts',
    'ProgressBar'
]
