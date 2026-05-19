# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge Extractor Module
PDF文档内容提取模块

提供文本提取、表格检测、结构分析等功能。
Provides text extraction, table detection, and structure analysis.
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .core import PDFDocument, PDFPage, TextBlock, Table, TableCell


class TextExtractor:
    """文本提取器 / Text Extractor"""
    
    def __init__(self, document: PDFDocument):
        """
        初始化文本提取器 / Initialize Text Extractor
        
        Args:
            document: PDFDocument实例 / PDFDocument instance
        """
        self.document = document
    
    def extract_by_page(self, page_numbers: Optional[List[int]] = None) -> Dict[int, str]:
        """
        按页面提取文本 / Extract text by page
        
        Args:
            page_numbers: 页面编号列表，None表示所有页面
            
        Returns:
            页面号到文本的映射 / Mapping of page number to text
        """
        if page_numbers is None:
            page_numbers = list(range(1, len(self.document) + 1))
        
        result = {}
        for page_num in page_numbers:
            if 1 <= page_num <= len(self.document):
                result[page_num] = self.document.pages[page_num - 1].text_content
        
        return result
    
    def extract_plain_text(self, min_length: int = 10) -> str:
        """
        提取纯文本（清理后）/ Extract plain text (cleaned)
        
        Args:
            min_length: 最小文本长度 / Minimum text length
            
        Returns:
            清理后的纯文本 / Cleaned plain text
        """
        full_text = self.document.get_full_text()
        
        # 移除多余空白
        text = re.sub(r'\n{3,}', '\n\n', full_text)
        text = re.sub(r' {2,}', ' ', text)
        
        # 移除过短的行
        lines = text.split('\n')
        lines = [line for line in lines if len(line.strip()) >= min_length]
        
        return '\n'.join(lines)
    
    def extract_sentences(self) -> List[str]:
        """
        提取句子列表 / Extract sentences
        
        Returns:
            句子列表 / List of sentences
        """
        text = self.extract_plain_text()
        
        # 按句子分割
        sentences = re.split(r'[.!?。！？]+', text)
        
        # 清理和过滤
        result = []
        for s in sentences:
            s = s.strip()
            if len(s) >= 10:  # 过滤过短的句子
                result.append(s)
        
        return result
    
    def extract_keywords(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """
        提取关键词（基于词频）/ Extract keywords (based on word frequency)
        
        Args:
            top_n: 返回前N个关键词 / Return top N keywords
            
        Returns:
            (关键词, 频率)元组列表 / List of (keyword, frequency) tuples
        """
        text = self.extract_plain_text().lower()
        
        # 简单分词
        words = re.findall(r'[a-z\u4e00-\u9fff]{3,}', text)
        
        # 停用词
        stopwords = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
            'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two',
            'who', 'boy', 'did', 'she', 'use', 'way', 'will', 'with', 'this',
            'that', 'from', 'they', 'been', 'have', 'more', 'than', 'into',
            '的', '是', '在', '了', '和', '与', '对', '为', '有', '我',
            '也', '就', '不', '都', '要', '这', '那', '上', '下', '中',
            '可以', '一个', '我们', '你们', '他们', '她们', '什么', '这个',
            '那个', '因为', '所以', '如果', '虽然', '但是', '而且', '或者'
        }
        
        # 统计词频
        word_freq = {}
        for word in words:
            if word not in stopwords:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_words[:top_n]


class TableExtractor:
    """表格提取器 / Table Extractor"""
    
    def __init__(self, document: PDFDocument):
        """
        初始化表格提取器 / Initialize Table Extractor
        
        Args:
            document: PDFDocument实例 / PDFDocument instance
        """
        self.document = document
    
    def detect_tables(self, page_number: Optional[int] = None) -> List[Table]:
        """
        检测表格 / Detect tables
        
        Args:
            page_number: 指定页面，None表示所有页面
            
        Returns:
            检测到的表格列表 / List of detected tables
        """
        tables = []
        
        pages_to_check = (
            [self.document.pages[page_number - 1]] 
            if page_number else self.document.pages
        )
        
        for page in pages_to_check:
            page_tables = self._detect_tables_in_page(page)
            tables.extend(page_tables)
        
        return tables
    
    def _detect_tables_in_page(self, page: PDFPage) -> List[Table]:
        """检测页面中的表格 / Detect tables in a page"""
        tables = []
        text = page.text_content
        
        # 简单的表格检测：基于对齐的文本模式
        lines = text.split('\n')
        
        # 寻找表格模式：用空格或特殊字符分隔的列
        potential_tables = self._find_table_patterns(lines)
        
        for pattern in potential_tables:
            table = Table(
                page_number=page.page_number,
                rows=len(pattern),
                cols=max(len(row) for row in pattern) if pattern else 0,
                cells=pattern,
                confidence=0.7  # 基础置信度
            )
            tables.append(table)
        
        return tables
    
    def _find_table_patterns(self, lines: List[str]) -> List[List[str]]:
        """寻找表格模式 / Find table patterns"""
        tables = []
        
        i = 0
        while i < len(lines):
            # 检测分隔线
            if self._is_delimiter_line(lines[i]):
                table_rows = []
                
                # 向前查找表头
                header_start = i - 1
                while header_start >= 0 and not lines[header_start].strip():
                    header_start -= 1
                
                if header_start >= 0:
                    header = self._split_by_separator(lines[header_start])
                    if len(header) >= 2:
                        table_rows.append(header)
                        
                        # 向下查找数据行
                        j = i + 1
                        while j < len(lines) and len(table_rows) < 50:
                            if lines[j].strip():
                                row = self._split_by_separator(lines[j])
                                if len(row) >= 2:
                                    table_rows.append(row)
                                else:
                                    break
                            j += 1
                        
                        if len(table_rows) >= 2:
                            tables.append(table_rows)
                
                i = j
            else:
                i += 1
        
        return tables
    
    def _is_delimiter_line(self, line: str) -> bool:
        """判断是否为分隔线 / Check if it's a delimiter line"""
        line = line.strip()
        
        # 检查是否全为分隔符
        if re.match(r'^[-|+=]+$', line):
            return True
        
        # 检查是否包含多个空格对齐的文本
        if '  ' in line and len(line) > 10:
            return True
        
        return False
    
    def _split_by_separator(self, line: str) -> List[str]:
        """按分隔符分割 / Split by separator"""
        line = line.strip()
        
        # 尝试用空格分割
        if '  ' in line:
            parts = re.split(r'\s{2,}', line)
        elif '|' in line:
            parts = [p.strip() for p in line.split('|')]
        elif '\t' in line:
            parts = [p.strip() for p in line.split('\t')]
        else:
            parts = [line]
        
        # 过滤空列
        return [p for p in parts if p.strip()]
    
    def extract_to_csv(self, page_number: Optional[int] = None) -> Dict[int, str]:
        """
        提取表格并转换为CSV / Extract tables and convert to CSV
        
        Args:
            page_number: 指定页面，None表示所有页面
            
        Returns:
            页面号到CSV内容的映射 / Mapping of page number to CSV content
        """
        tables = self.detect_tables(page_number)
        result = {}
        
        for table in tables:
            csv_content = table.to_csv()
            if page_number:
                result[page_number] = csv_content
            else:
                result[table.page_number] = csv_content
        
        return result


class StructureAnalyzer:
    """结构分析器 / Structure Analyzer"""
    
    def __init__(self, document: PDFDocument):
        """
        初始化结构分析器 / Initialize Structure Analyzer
        
        Args:
            document: PDFDocument实例 / PDFDocument instance
        """
        self.document = document
        self.text_extractor = TextExtractor(document)
    
    def analyze_structure(self) -> Dict[str, Any]:
        """
        分析文档结构 / Analyze document structure
        
        Returns:
            结构分析结果 / Structure analysis result
        """
        full_text = self.document.get_full_text()
        lines = full_text.split('\n')
        
        # 分析标题
        headings = self._detect_headings(lines)
        
        # 分析段落
        paragraphs = self._detect_paragraphs(lines)
        
        # 分析列表
        lists = self._detect_lists(lines)
        
        # 分析脚注/页脚
        footers = self._detect_footers(lines)
        
        return {
            "headings": headings,
            "paragraphs": paragraphs,
            "lists": lists,
            "footers": footers,
            "statistics": {
                "total_lines": len(lines),
                "total_headings": len(headings),
                "total_paragraphs": len(paragraphs),
                "total_lists": len(lists)
            }
        }
    
    def _detect_headings(self, lines: List[str]) -> List[Dict[str, Any]]:
        """检测标题 / Detect headings"""
        headings = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 标题特征：大写开头、较短、不以标点结尾
            if (len(line) < 100 and len(line) > 3 and
                line[0].isupper() and
                not line.endswith(('.', ',', ':', ';')) and
                not line.startswith(('-', '*', '•', '·'))):
                
                # 检查是否像标题
                is_likely_heading = (
                    len(line.split()) <= 15 or  # 短句
                    bool(re.match(r'^[IVX\d]+\.?\s+\w', line)) or  # 编号标题
                    bool(re.match(r'^\w+\s+\w+:\s*$', line))  # 冒号结尾
                )
                
                if is_likely_heading:
                    headings.append({
                        "text": line,
                        "line_number": i + 1,
                        "level": self._estimate_heading_level(line)
                    })
        
        return headings
    
    def _estimate_heading_level(self, text: str) -> int:
        """估算标题级别 / Estimate heading level"""
        text = text.strip()
        
        # 一级标题：全大写或短标题
        if text.isupper() or len(text) < 20:
            return 1
        
        # 二级标题：数字编号
        if re.match(r'^[IVX\d]+\.?\s+', text):
            return 2
        
        # 三级标题：字母编号
        if re.match(r'^[a-z]\.?\s+', text, re.IGNORECASE):
            return 3
        
        return 4
    
    def _detect_paragraphs(self, lines: List[str]) -> List[Dict[str, Any]]:
        """检测段落 / Detect paragraphs"""
        paragraphs = []
        current_para = []
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            if line:
                if not current_para:
                    current_start = i
                current_para.append(line)
            else:
                if current_para:
                    para_text = ' '.join(current_para)
                    if len(para_text) > 50:  # 过滤短段落
                        paragraphs.append({
                            "text": para_text,
                            "start_line": current_start + 1,
                            "end_line": i,
                            "length": len(para_text)
                        })
                    current_para = []
        
        # 处理最后一个段落
        if current_para:
            para_text = ' '.join(current_para)
            if len(para_text) > 50:
                paragraphs.append({
                    "text": para_text,
                    "start_line": current_start + 1,
                    "end_line": len(lines),
                    "length": len(para_text)
                })
        
        return paragraphs
    
    def _detect_lists(self, lines: List[str]) -> List[Dict[str, Any]]:
        """检测列表 / Detect lists"""
        lists = []
        current_list = []
        current_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 检测列表项
            is_list_item = bool(re.match(r'^[-*•·]\s+\w', line)) or \
                          bool(re.match(r'^\d+[.)]\s+\w', line))
            
            if is_list_item:
                if not current_list:
                    current_start = i
                current_list.append(re.sub(r'^[-*•·\d.)]+\s*', '', line))
            else:
                if current_list:
                    lists.append({
                        "items": current_list,
                        "start_line": current_start + 1,
                        "end_line": i,
                        "count": len(current_list)
                    })
                    current_list = []
        
        # 处理最后一个列表
        if current_list:
            lists.append({
                "items": current_list,
                "start_line": current_start + 1,
                "end_line": len(lines),
                "count": len(current_list)
            })
        
        return lists
    
    def _detect_footers(self, lines: List[str]) -> List[str]:
        """检测页脚 / Detect footers"""
        footers = []
        
        # 假设页脚在文档末尾
        last_lines = lines[-20:] if len(lines) > 20 else lines
        
        for line in last_lines:
            line = line.strip()
            
            # 页脚特征：包含页码、日期、版权信息
            if (re.search(r'page\s*\d+', line, re.IGNORECASE) or
                re.search(r'\d{4}[-/]\d{2}[-/]\d{2}', line) or
                re.search(r'©?\s*\d{4}', line) or
                re.search(r'copyright', line, re.IGNORECASE)):
                footers.append(line)
        
        return list(set(footers))  # 去重
    
    def to_markdown(self) -> str:
        """转换为Markdown格式 / Convert to Markdown format"""
        structure = self.analyze_structure()
        md_lines = []
        
        # 添加标题
        md_lines.append("# Document Structure\n")
        
        # 添加章节
        if structure['headings']:
            md_lines.append("## Headings\n")
            for h in structure['headings'][:20]:  # 限制显示数量
                level = h['level']
                md_lines.append(f"{'#' * level} {h['text']}\n")
            md_lines.append("\n")
        
        # 添加段落统计
        md_lines.append("## Statistics\n")
        stats = structure['statistics']
        md_lines.append(f"- Total Lines: {stats['total_lines']}\n")
        md_lines.append(f"- Headings: {stats['total_headings']}\n")
        md_lines.append(f"- Paragraphs: {stats['total_paragraphs']}\n")
        md_lines.append(f"- Lists: {stats['total_lists']}\n")
        
        return ''.join(md_lines)


class MarkdownConverter:
    """Markdown转换器 / Markdown Converter"""
    
    def __init__(self, document: PDFDocument):
        """
        初始化Markdown转换器 / Initialize Markdown Converter
        
        Args:
            document: PDFDocument实例 / PDFDocument instance
        """
        self.document = document
        self.structure_analyzer = StructureAnalyzer(document)
    
    def convert(self, preserve_layout: bool = True) -> str:
        """
        转换为Markdown / Convert to Markdown
        
        Args:
            preserve_layout: 是否保持布局 / Whether to preserve layout
            
        Returns:
            Markdown格式内容 / Markdown formatted content
        """
        if preserve_layout:
            return self._convert_with_layout()
        else:
            return self._convert_simple()
    
    def _convert_simple(self) -> str:
        """简单转换 / Simple conversion"""
        text = self.document.get_full_text()
        
        # 清理文本
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 处理标题
        lines = text.split('\n')
        converted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # 检测标题模式
                if (len(line) < 80 and 
                    line[0].isupper() and 
                    not line.endswith(('.', ',', ':'))):
                    converted_lines.append(f"## {line}\n")
                else:
                    converted_lines.append(f"{line}\n")
        
        return '\n'.join(converted_lines)
    
    def _convert_with_layout(self) -> str:
        """保持布局的转换 / Conversion with layout preservation"""
        structure = self.structure_analyzer.analyze_structure()
        md_parts = []
        
        # 标题
        md_parts.append("# PDF Document\n")
        md_parts.append(f"*Extracted from {self.document.metadata.title or self.document.file_path.name}*\n\n")
        
        # 结构化内容
        if structure['headings']:
            md_parts.append("## Sections\n\n")
            for h in structure['headings'][:30]:
                level = min(h['level'], 4)
                md_parts.append(f"{'#' * level} {h['text']}\n")
            md_parts.append("\n")
        
        # 段落
        if structure['paragraphs']:
            md_parts.append("## Content\n\n")
            for p in structure['paragraphs'][:10]:
                md_parts.append(f"{p['text']}\n\n")
        
        # 列表
        if structure['lists']:
            md_parts.append("## Lists\n\n")
            for lst in structure['lists'][:10]:
                for item in lst['items']:
                    md_parts.append(f"- {item}\n")
                md_parts.append("\n")
        
        return ''.join(md_parts)
    
    def save(self, output_path: str) -> None:
        """
        保存为Markdown文件 / Save as Markdown file
        
        Args:
            output_path: 输出文件路径 / Output file path
        """
        content = self.convert()
        Path(output_path).write_text(content, encoding='utf-8')
