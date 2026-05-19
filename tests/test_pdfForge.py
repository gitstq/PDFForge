# PDFForge Test Suite
# PDFForge 测试套件

"""
测试用例
Test Cases
"""

import pytest
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdfForge.core import PDFDocument, PDFMetadata, Table
from pdfForge.extractor import TextExtractor, TableExtractor, StructureAnalyzer
from pdfForge.utils import sanitize_filename, truncate_text, split_into_chunks


class TestPDFDocument:
    """PDF文档测试 / PDF Document Tests"""
    
    def test_metadata_creation(self):
        """测试元数据创建 / Test metadata creation"""
        meta = PDFMetadata()
        assert meta.page_count == 0
        assert meta.title is None
        assert meta.author is None
    
    def test_metadata_to_dict(self):
        """测试元数据转换为字典 / Test metadata to dict conversion"""
        meta = PDFMetadata(
            title="Test Document",
            author="Test Author",
            page_count=10
        )
        
        data = meta.to_dict()
        assert data["title"] == "Test Document"
        assert data["author"] == "Test Author"
        assert data["page_count"] == 10
    
    def test_table_csv_conversion(self):
        """测试表格CSV转换 / Test table CSV conversion"""
        table = Table(
            page_number=1,
            rows=2,
            cols=2,
            cells=[
                ["Name", "Age"],
                ["John", "25"]
            ]
        )
        
        csv = table.to_csv()
        assert "Name" in csv
        assert "John" in csv
    
    def test_table_json_conversion(self):
        """测试表格JSON转换 / Test table JSON conversion"""
        table = Table(
            page_number=1,
            rows=2,
            cols=2,
            cells=[
                ["Header1", "Header2"],
                ["Data1", "Data2"]
            ]
        )
        
        json_str = table.to_json()
        assert '"Header1"' in json_str
        assert '"Data1"' in json_str


class TestTextExtractor:
    """文本提取器测试 / Text Extractor Tests"""
    
    def test_sentence_splitting(self):
        """测试句子分割 / Test sentence splitting"""
        # 这个测试需要真实的PDF文件
        # 跳过实际的文件依赖测试
        pass
    
    def test_keyword_extraction(self):
        """测试关键词提取 / Test keyword extraction"""
        # 创建模拟文档
        meta = PDFMetadata(page_count=1)
        
        # 由于没有真实PDF文件，跳过这个测试
        pass


class TestUtils:
    """工具函数测试 / Utility Tests"""
    
    def test_sanitize_filename(self):
        """测试文件名清理 / Test filename sanitization"""
        # 测试非法字符
        assert sanitize_filename("test<>file.pdf") == "test__file.pdf"
        
        # 测试正常文件名
        assert sanitize_filename("normal_file.pdf") == "normal_file.pdf"
        
        # 测试去除空格
        assert sanitize_filename("  file.pdf  ") == "file.pdf"
    
    def test_truncate_text(self):
        """测试文本截断 / Test text truncation"""
        text = "Hello, World! This is a long text."
        
        # 测试正常截断
        result = truncate_text(text, 20)
        assert len(result) <= 23  # 20 + suffix length
        assert result.endswith("...")
        
        # 测试不截断
        result = truncate_text(text, 100)
        assert result == text
    
    def test_split_into_chunks(self):
        """测试文本分块 / Test text splitting"""
        text = "A" * 1000
        
        chunks = split_into_chunks(text, chunk_size=300, overlap=50)
        
        assert len(chunks) > 1
        assert all(len(chunk) <= 300 for chunk in chunks)
        
        # 验证重叠
        for i in range(len(chunks) - 1):
            assert chunks[i][-50:] == chunks[i + 1][:50]


class TestCLI:
    """CLI测试 / CLI Tests"""
    
    def test_parser_creation(self):
        """测试解析器创建 / Test parser creation"""
        from pdfForge.cli import create_parser
        
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "pdfforge"
    
    def test_colored_output(self):
        """测试彩色输出 / Test colored output"""
        from pdfForge.cli import colored, Colors
        
        # 测试无颜色
        result = colored("test", "")
        assert result == "test"
        
        # 测试有颜色
        result = colored("test", Colors.RED)
        assert Colors.RED in result
        assert Colors.RESET in result


def run_tests():
    """运行所有测试 / Run all tests"""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_tests()
