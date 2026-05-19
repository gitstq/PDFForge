# PDFForge Examples
# PDFForge 示例

"""
示例代码
Example Code
"""

# ============================================
# Basic Usage Examples
# 基础用法示例
# ============================================

from pdfForge import PDFDocument, TextExtractor, TableExtractor

# Example 1: Basic PDF Loading
# 示例1: 基础PDF加载
def example_basic_loading():
    """基础PDF加载 / Basic PDF Loading"""
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    print(f"Pages: {len(doc)}")
    print(f"Title: {doc.metadata.title}")
    print(f"Author: {doc.metadata.author}")


# Example 2: Text Extraction
# 示例2: 文本提取
def example_text_extraction():
    """文本提取 / Text Extraction"""
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    extractor = TextExtractor(doc)
    
    # Extract plain text
    plain_text = extractor.extract_plain_text()
    print(plain_text[:500])
    
    # Extract by page
    page_text = extractor.extract_by_page(page_numbers=[1, 2])
    print(page_text)


# Example 3: Table Detection
# 示例3: 表格检测
def example_table_detection():
    """表格检测 / Table Detection"""
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    extractor = TableExtractor(doc)
    tables = extractor.detect_tables()
    
    for i, table in enumerate(tables):
        print(f"Table {i+1}: {table.rows}x{table.cols}")
        
        # Export as CSV
        csv = table.to_csv()
        print(csv)


# Example 4: Structure Analysis
# 示例4: 结构分析
def example_structure_analysis():
    """结构分析 / Structure Analysis"""
    from pdfForge import StructureAnalyzer
    
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    analyzer = StructureAnalyzer(doc)
    structure = analyzer.analyze_structure()
    
    print(f"Headings: {len(structure['headings'])}")
    print(f"Paragraphs: {len(structure['paragraphs'])}")
    print(f"Lists: {len(structure['lists'])}")


# Example 5: Markdown Conversion
# 示例5: Markdown转换
def example_markdown_conversion():
    """Markdown转换 / Markdown Conversion"""
    from pdfForge import MarkdownConverter
    
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    converter = MarkdownConverter(doc)
    converter.save("output.md")
    
    print("Converted to Markdown!")


# Example 6: Keyword Extraction
# 示例6: 关键词提取
def example_keyword_extraction():
    """关键词提取 / Keyword Extraction"""
    from pdfForge import TextExtractor
    
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    extractor = TextExtractor(doc)
    keywords = extractor.extract_keywords(top_n=20)
    
    for word, freq in keywords:
        print(f"{word}: {freq}")


# Example 7: JSON Export
# 示例7: JSON导出
def example_json_export():
    """JSON导出 / JSON Export"""
    import json
    
    doc = PDFDocument("example.pdf")
    doc.parse()
    
    json_data = doc.to_json(include_pages=True)
    data = json.loads(json_data)
    
    print(f"Total pages: {len(data['pages'])}")
    print(f"Metadata: {data['metadata']}")


# Example 8: Batch Processing
# 示例8: 批量处理
def example_batch_processing():
    """批量处理 / Batch Processing"""
    from pathlib import Path
    import shutil
    
    # Process multiple PDFs
    pdf_files = list(Path("pdfs/").glob("*.pdf"))
    
    for pdf_file in pdf_files:
        doc = PDFDocument(str(pdf_file))
        doc.parse()
        
        # Extract text
        text = doc.get_full_text()
        
        # Save to output folder
        output_file = Path("output") / f"{pdf_file.stem}.txt"
        output_file.write_text(text, encoding='utf-8')


# Run all examples
if __name__ == "__main__":
    print("PDFForge Examples")
    print("=" * 50)
    print("Run individual functions to see examples.")
