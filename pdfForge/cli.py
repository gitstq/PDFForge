# PDFForge - Intelligent PDF Document Analysis & Processing Engine
# 智能PDF文档分析与处理引擎

"""
PDFForge CLI Module
命令行界面模块

提供友好的命令行交互界面。
Provides user-friendly command-line interface.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List
from dataclasses import asdict

# ANSI颜色码
class Colors:
    """ANSI颜色码 / ANSI Color Codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


def colored(text: str, color: str = "") -> str:
    """为文本添加颜色 / Add color to text"""
    if not color:
        return text
    return f"{color}{text}{Colors.RESET}"


def print_header(text: str) -> None:
    """打印标题 / Print header"""
    print()
    print(colored(f"  {text}", Colors.CYAN + Colors.BOLD))
    print(colored("  " + "─" * 60, Colors.DIM))
    print()


def print_success(text: str) -> None:
    """打印成功消息 / Print success message"""
    print(colored(f"  ✅ {text}", Colors.GREEN))


def print_error(text: str) -> None:
    """打印错误消息 / Print error message"""
    print(colored(f"  ❌ {text}", Colors.RED), file=sys.stderr)


def print_info(text: str) -> None:
    """打印信息消息 / Print info message"""
    print(colored(f"  ℹ️  {text}", Colors.BLUE))


def print_warning(text: str) -> None:
    """打印警告消息 / Print warning message"""
    print(colored(f"  ⚠️  {text}", Colors.YELLOW))


def format_size(size: int) -> str:
    """格式化文件大小 / Format file size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def format_keyword(kw: tuple) -> str:
    """格式化关键词 / Format keyword"""
    word, freq = kw
    bar = "█" * min(freq, 20)
    return f"  {word:20s} {bar:20s} ({freq})"


def cmd_info(args) -> int:
    """显示PDF信息命令 / Show PDF info command"""
    from .core import PDFDocument
    
    try:
        print_header("PDF Document Information")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        meta = doc.metadata
        
        # 基本信息
        print(colored("  📄 File Information", Colors.BOLD + Colors.CYAN))
        print(f"  {'  Path:':<15} {colored(meta.file_path, Colors.WHITE)}")
        print(f"  {'  Size:':<15} {colored(format_size(meta.file_size), Colors.WHITE)}")
        print(f"  {'  Pages:':<15} {colored(str(meta.page_count), Colors.WHITE)}")
        print()
        
        # 元数据
        print(colored("  📋 Metadata", Colors.BOLD + Colors.CYAN))
        
        metadata_items = [
            ("Title", meta.title),
            ("Author", meta.author),
            ("Subject", meta.subject),
            ("Creator", meta.creator),
            ("Producer", meta.producer),
            ("Created", meta.creation_date),
            ("Modified", meta.modification_date),
        ]
        
        for key, value in metadata_items:
            if value:
                print(f"  {key + ':':<15} {colored(str(value), Colors.WHITE)}")
            else:
                print(f"  {key + ':':<15} {colored('N/A', Colors.DIM)}")
        
        print()
        print_success(f"Successfully loaded PDF: {doc.file_path.name}")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_extract_text(args) -> int:
    """提取文本命令 / Extract text command"""
    from .core import PDFDocument
    from .extractor import TextExtractor
    
    try:
        print_header("Text Extraction")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        extractor = TextExtractor(doc)
        
        if args.plain:
            text = extractor.extract_plain_text()
        else:
            text = doc.get_full_text()
        
        # 输出
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(text, encoding='utf-8')
            print_success(f"Text extracted to: {output_path}")
        else:
            # 分页显示
            print()
            print(colored(text[:5000], Colors.WHITE))  # 限制显示
            if len(text) > 5000:
                print()
                print_info(f"Text truncated. Full text has {len(text)} characters.")
                print_info("Use --output to save full text to file.")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_extract_tables(args) -> int:
    """提取表格命令 / Extract tables command"""
    from .core import PDFDocument
    from .extractor import TableExtractor
    
    try:
        print_header("Table Extraction")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        extractor = TableExtractor(doc)
        tables = extractor.detect_tables()
        
        if not tables:
            print_warning("No tables detected in the PDF.")
            return 0
        
        print_info(f"Found {len(tables)} table(s)")
        print()
        
        # 处理表格
        for i, table in enumerate(tables):
            print(colored(f"  Table {i + 1} (Page {table.page_number})", Colors.BOLD + Colors.YELLOW))
            print(f"  Rows: {table.rows}, Columns: {table.cols}")
            print(f"  Confidence: {table.confidence:.2f}")
            print()
            
            if args.format == 'csv':
                csv_content = table.to_csv()
                if args.output:
                    output_path = Path(args.output)
                    if len(tables) > 1:
                        output_path = output_path.with_stem(f"{output_path.stem}_{i+1}")
                    output_path.write_text(csv_content, encoding='utf-8')
                    print_success(f"Saved to: {output_path}")
                else:
                    print(csv_content)
            elif args.format == 'json':
                json_content = table.to_json()
                if args.output:
                    output_path = Path(args.output)
                    if len(tables) > 1:
                        output_path = output_path.with_stem(f"{output_path.stem}_{i+1}")
                    output_path.write_text(json_content, encoding='utf-8')
                    print_success(f"Saved to: {output_path}")
                else:
                    print(json_content)
            else:
                # 表格格式显示
                for row in table.cells[:10]:  # 限制显示行数
                    print("  | " + " | ".join(str(cell)[:30] for cell in row) + " |")
                if table.rows > 10:
                    print(f"  ... ({table.rows - 10} more rows)")
            
            print()
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_analyze_structure(args) -> int:
    """分析结构命令 / Analyze structure command"""
    from .core import PDFDocument
    from .extractor import StructureAnalyzer
    
    try:
        print_header("Document Structure Analysis")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        analyzer = StructureAnalyzer(doc)
        structure = analyzer.analyze_structure()
        
        # 统计信息
        print(colored("  📊 Statistics", Colors.BOLD + Colors.CYAN))
        stats = structure['statistics']
        print(f"  Total Lines:     {stats['total_lines']}")
        print(f"  Headings:        {stats['total_headings']}")
        print(f"  Paragraphs:      {stats['total_paragraphs']}")
        print(f"  Lists:           {stats['total_lists']}")
        print()
        
        # 标题
        if structure['headings']:
            print(colored("  📑 Headings", Colors.BOLD + Colors.CYAN))
            for h in structure['headings'][:15]:
                level = min(h['level'], 4)
                prefix = "  " * (level - 1)
                print(f"  {prefix}• {h['text'][:60]}")
            if len(structure['headings']) > 15:
                print(f"  ... and {len(structure['headings']) - 15} more")
            print()
        
        # 列表
        if structure['lists']:
            print(colored("  📝 Lists", Colors.BOLD + Colors.CYAN))
            for i, lst in enumerate(structure['lists'][:5]):
                print(f"  List {i + 1} ({lst['count']} items):")
                for item in lst['items'][:3]:
                    print(f"    - {item[:50]}")
                if lst['count'] > 3:
                    print(f"    ... and {lst['count'] - 3} more")
            print()
        
        # 保存JSON
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(
                json.dumps(structure, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print_success(f"Analysis saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_convert_markdown(args) -> int:
    """转换为Markdown命令 / Convert to Markdown command"""
    from .core import PDFDocument
    from .extractor import MarkdownConverter
    
    try:
        print_header("Markdown Conversion")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        converter = MarkdownConverter(doc)
        
        if args.full:
            md_content = converter.convert(preserve_layout=True)
        else:
            md_content = converter.convert(preserve_layout=False)
        
        # 输出
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(md_content, encoding='utf-8')
            print_success(f"Markdown saved to: {output_path}")
        else:
            # 输出到stdout
            output_path = Path(args.input).with_suffix('.md')
            output_path.write_text(md_content, encoding='utf-8')
            print_success(f"Markdown saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_keywords(args) -> int:
    """提取关键词命令 / Extract keywords command"""
    from .core import PDFDocument
    from .extractor import TextExtractor
    
    try:
        print_header("Keyword Extraction")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        extractor = TextExtractor(doc)
        keywords = extractor.extract_keywords(top_n=args.top)
        
        if not keywords:
            print_warning("No keywords found.")
            return 0
        
        print_info(f"Top {len(keywords)} keywords:")
        print()
        
        for kw in keywords:
            print(format_keyword(kw))
        
        # 保存
        if args.output:
            output_path = Path(args.output)
            kw_list = [{"word": k, "frequency": v} for k, v in keywords]
            output_path.write_text(
                json.dumps(kw_list, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            print()
            print_success(f"Keywords saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_batch(args) -> int:
    """批量处理命令 / Batch processing command"""
    from .core import PDFDocument
    from .extractor import TextExtractor, TableExtractor, MarkdownConverter
    
    try:
        print_header("Batch Processing")
        
        input_path = Path(args.input)
        
        # 获取PDF文件
        if input_path.is_file():
            pdf_files = [input_path]
        elif input_path.is_dir():
            pdf_files = list(input_path.glob("*.pdf"))
        else:
            pdf_files = list(Path(".").glob(f"*{input_path}*.pdf"))
        
        if not pdf_files:
            print_error(f"No PDF files found in: {args.input}")
            return 1
        
        print_info(f"Found {len(pdf_files)} PDF file(s)")
        print()
        
        output_dir = Path(args.output) if args.output else Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # 处理每个文件
        results = []
        for pdf_file in pdf_files:
            try:
                doc = PDFDocument(str(pdf_file))
                doc.parse()
                
                base_name = pdf_file.stem
                
                # 根据模式处理
                if args.mode == 'text':
                    extractor = TextExtractor(doc)
                    output_file = output_dir / f"{base_name}.txt"
                    output_file.write_text(extractor.extract_plain_text(), encoding='utf-8')
                    
                elif args.mode == 'table':
                    extractor = TableExtractor(doc)
                    tables = extractor.detect_tables()
                    output_file = output_dir / f"{base_name}_tables.csv"
                    
                    if tables:
                        csv_content = '\n\n'.join(t.to_csv() for t in tables)
                        output_file.write_text(csv_content, encoding='utf-8')
                    else:
                        output_file.write_text("No tables found", encoding='utf-8')
                        
                elif args.mode == 'markdown':
                    converter = MarkdownConverter(doc)
                    output_file = output_dir / f"{base_name}.md"
                    converter.save(str(output_file))
                    
                else:  # all
                    # 提取文本
                    extractor = TextExtractor(doc)
                    (output_dir / f"{base_name}.txt").write_text(
                        extractor.extract_plain_text(), encoding='utf-8'
                    )
                    
                    # 提取表格
                    table_extractor = TableExtractor(doc)
                    tables = table_extractor.detect_tables()
                    if tables:
                        csv_content = '\n\n'.join(t.to_csv() for t in tables)
                        (output_dir / f"{base_name}_tables.csv").write_text(
                            csv_content, encoding='utf-8'
                        )
                    
                    # 转换为Markdown
                    md_converter = MarkdownConverter(doc)
                    (output_dir / f"{base_name}.md").write_text(
                        md_converter.convert(), encoding='utf-8'
                    )
                    
                    output_file = output_dir / base_name
                
                results.append((pdf_file.name, "success", str(output_file)))
                
            except Exception as e:
                results.append((pdf_file.name, "error", str(e)))
        
        # 显示结果
        print()
        print(colored("  Results", Colors.BOLD + Colors.CYAN))
        for name, status, info in results:
            if status == "success":
                print(colored(f"  ✅ {name}", Colors.GREEN))
                print(f"     → {info}")
            else:
                print(colored(f"  ❌ {name}", Colors.RED))
                print(f"     {info}")
        
        print()
        print_success(f"Batch processing completed. Output directory: {output_dir}")
        
        return 0
        
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def cmd_json(args) -> int:
    """导出JSON命令 / Export JSON command"""
    from .core import PDFDocument
    from .extractor import StructureAnalyzer
    
    try:
        print_header("JSON Export")
        
        doc = PDFDocument(args.input)
        doc.parse()
        
        # 构建JSON数据
        data = {
            "metadata": doc.metadata.to_dict(),
            "pages": [
                {
                    "page_number": p.page_number,
                    "text_content": p.text_content,
                    "char_count": len(p.text_content)
                }
                for p in doc.pages
            ]
        }
        
        # 添加结构分析
        if args.structure:
            analyzer = StructureAnalyzer(doc)
            data["structure"] = analyzer.analyze_structure()
        
        # 输出
        json_content = json.dumps(data, indent=2, ensure_ascii=False)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(json_content, encoding='utf-8')
            print_success(f"JSON saved to: {output_path}")
        else:
            output_path = Path(args.input).with_suffix('.json')
            output_path.write_text(json_content, encoding='utf-8')
            print_success(f"JSON saved to: {output_path}")
        
        return 0
        
    except FileNotFoundError:
        print_error(f"File not found: {args.input}")
        return 1
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器 / Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="pdfforge",
        description=colored("PDFForge", Colors.CYAN) + 
                    " - " +
                    colored("Intelligent PDF Document Analysis & Processing Engine", Colors.DIM),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdfforge info document.pdf
  pdfforge extract document.pdf -o text.txt
  pdfforge tables document.pdf --format csv -o tables.csv
  pdfforge analyze document.pdf -o structure.json
  pdfforge convert document.pdf -o document.md
  pdfforge keywords document.pdf --top 30
  pdfforge batch ./pdf_folder/ --mode all --output ./output/

License: MIT
        """
    )
    
    # 全局选项
    parser.add_argument(
        "--version",
        action="version",
        version="PDFForge 1.0.0"
    )
    
    # 子命令
    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        required=True
    )
    
    # info命令
    info_parser = subparsers.add_parser(
        "info",
        help="Show PDF document information"
    )
    info_parser.add_argument("input", help="Input PDF file")
    info_parser.set_defaults(func=cmd_info)
    
    # extract命令
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extract text from PDF"
    )
    extract_parser.add_argument("input", help="Input PDF file")
    extract_parser.add_argument("-o", "--output", help="Output file path")
    extract_parser.add_argument(
        "--plain",
        action="store_true",
        help="Extract plain text (cleaned)"
    )
    extract_parser.set_defaults(func=cmd_extract_text)
    
    # tables命令
    tables_parser = subparsers.add_parser(
        "tables",
        help="Extract tables from PDF"
    )
    tables_parser.add_argument("input", help="Input PDF file")
    tables_parser.add_argument("-o", "--output", help="Output file path")
    tables_parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "display"],
        default="display",
        help="Output format (default: display)"
    )
    tables_parser.set_defaults(func=cmd_extract_tables)
    
    # analyze命令
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze document structure"
    )
    analyze_parser.add_argument("input", help="Input PDF file")
    analyze_parser.add_argument("-o", "--output", help="Output JSON file path")
    analyze_parser.set_defaults(func=cmd_analyze_structure)
    
    # convert命令
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert PDF to Markdown"
    )
    convert_parser.add_argument("input", help="Input PDF file")
    convert_parser.add_argument("-o", "--output", help="Output Markdown file path")
    convert_parser.add_argument(
        "--full",
        action="store_true",
        help="Full conversion with structure preservation"
    )
    convert_parser.set_defaults(func=cmd_convert_markdown)
    
    # keywords命令
    keywords_parser = subparsers.add_parser(
        "keywords",
        help="Extract keywords from PDF"
    )
    keywords_parser.add_argument("input", help="Input PDF file")
    keywords_parser.add_argument("-o", "--output", help="Output JSON file path")
    keywords_parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of top keywords to extract (default: 20)"
    )
    keywords_parser.set_defaults(func=cmd_keywords)
    
    # batch命令
    batch_parser = subparsers.add_parser(
        "batch",
        help="Batch process multiple PDF files"
    )
    batch_parser.add_argument("input", help="Input PDF file or folder")
    batch_parser.add_argument("-o", "--output", help="Output directory")
    batch_parser.add_argument(
        "-m", "--mode",
        choices=["text", "table", "markdown", "all"],
        default="all",
        help="Processing mode (default: all)"
    )
    batch_parser.set_defaults(func=cmd_batch)
    
    # json命令
    json_parser = subparsers.add_parser(
        "json",
        help="Export PDF to JSON format"
    )
    json_parser.add_argument("input", help="Input PDF file")
    json_parser.add_argument("-o", "--output", help="Output JSON file path")
    json_parser.add_argument(
        "--structure",
        action="store_true",
        help="Include structure analysis"
    )
    json_parser.set_defaults(func=cmd_json)
    
    return parser


def main() -> int:
    """主入口函数 / Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
