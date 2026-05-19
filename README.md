# 🌐 Language | 语言

[![zh-CN](https://img.shields.io/badge/中文-简体-blue)](README_zh-CN.md)
[![zh-TW](https://img.shields.io/badge/中文-繁體-red)](README_zh-TW.md)
[![en](https://img.shields.io/badge/English-green)](README.md)
[![ja](https://img.shields.io/badge/日本語-orange)](README_ja.md)

---

# 🛠️ PDFForge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-orange.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg" alt="Platform">
</p>

<p align="center">
  <strong>Zero-Dependency Intelligent PDF Document Analysis & Processing Engine</strong>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PDFForge">Documentation</a>
  •
  <a href="https://github.com/gitstq/PDFForge/releases">Releases</a>
  •
  <a href="https://github.com/gitstq/PDFForge/issues">Issues</a>
</p>

---

## 🎉 Project Introduction

**PDFForge** is a powerful, lightweight, and zero-dependency PDF document analysis and processing engine. It provides comprehensive text extraction, table detection, structure analysis, and Markdown conversion capabilities through an intuitive CLI interface.

✨ **Why PDFForge?**

- 🔧 **Zero Dependencies** - Pure Python implementation, no C extensions, no external libraries required
- 📊 **Intelligent Table Detection** - Automatically detects and extracts tabular data
- 🏗️ **Structure Analysis** - Analyzes document structure including headings, paragraphs, lists
- 📝 **Markdown Export** - Converts PDF content to clean Markdown format
- ⚡ **Blazing Fast** - Optimized for speed with minimal memory footprint
- 🌐 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- 🎯 **Developer Friendly** - Clean API for integration into your projects

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📄 **Text Extraction** | Extract text from entire PDF or specific page ranges |
| 📊 **Table Detection** | Automatically detect and extract tables to CSV/JSON |
| 🏗️ **Structure Analysis** | Analyze headings, paragraphs, lists, footers |
| 📝 **Markdown Conversion** | Convert PDF to clean Markdown format |
| 🔑 **Keyword Extraction** | Extract keywords using word frequency analysis |
| 📦 **Batch Processing** | Process multiple PDF files in one command |
| 💾 **JSON Export** | Export PDF data with structure analysis |
| 🎨 **Colorful CLI** | Beautiful, informative command-line output |

---

## 🚀 Quick Start

### 📥 Installation

**Option 1: pip install (Recommended)**
```bash
pip install pdfforge
```

**Option 2: From Source**
```bash
git clone https://github.com/gitstq/PDFForge.git
cd PDFForge
pip install -e .
```

**Option 3: Direct Usage (No Installation)**
```bash
python -m pdfForge <command> <input_file>
```

### 🔰 Basic Usage

```bash
# Show PDF information
pdfforge info document.pdf

# Extract text
pdfforge extract document.pdf -o text.txt

# Extract tables
pdfforge tables document.pdf -f csv -o tables.csv

# Analyze document structure
pdfforge analyze document.pdf -o structure.json

# Convert to Markdown
pdfforge convert document.pdf -o document.md

# Extract keywords
pdfforge keywords document.pdf --top 20

# Batch process
pdfforge batch ./pdf_folder/ --mode all --output ./output/
```

### 💻 Python API

```python
from pdfForge import PDFDocument, TextExtractor, TableExtractor

# Load PDF
doc = PDFDocument("document.pdf")
doc.parse()

# Extract text
text = doc.get_full_text()
print(f"Extracted {len(text)} characters")

# Extract tables
extractor = TableExtractor(doc)
tables = extractor.detect_tables()

for table in tables:
    csv = table.to_csv()
    print(f"Table: {table.rows}x{table.cols}")
```

---

## 📖 Detailed Usage Guide

### CLI Commands

#### 📄 PDF Information
```bash
pdfforge info <input.pdf>
```
Displays detailed PDF metadata including title, author, creation date, page count, and file size.

#### 📝 Text Extraction
```bash
# Extract all text
pdfforge extract <input.pdf> -o output.txt

# Extract plain text (cleaned)
pdfforge extract <input.pdf> --plain -o output.txt
```

#### 📊 Table Extraction
```bash
# Display tables
pdfforge tables <input.pdf>

# Export as CSV
pdfforge tables <input.pdf> -f csv -o tables.csv

# Export as JSON
pdfforge tables <input.pdf> -f json -o tables.json
```

#### 🏗️ Structure Analysis
```bash
pdfforge analyze <input.pdf> -o structure.json
```

#### 📝 Markdown Conversion
```bash
# Basic conversion
pdfforge convert <input.pdf> -o output.md

# Full conversion with structure
pdfforge convert <input.pdf> --full -o output.md
```

#### 🔑 Keyword Extraction
```bash
pdfforge keywords <input.pdf> --top 30 -o keywords.json
```

#### 📦 Batch Processing
```bash
# Process all PDFs in folder
pdfforge batch ./pdf_folder/ --output ./output/

# Specific mode
pdfforge batch ./pdf_folder/ --mode text --output ./text_output/
pdfforge batch ./pdf_folder/ --mode table --output ./table_output/
pdfforge batch ./pdf_folder/ --mode markdown --output ./md_output/
```

#### 💾 JSON Export
```bash
# Basic JSON export
pdfforge json <input.pdf> -o output.json

# With structure analysis
pdfforge json <input.pdf> --structure -o output.json
```

---

## 🛠️ Configuration

PDFForge works out of the box with default settings. No configuration required!

For advanced usage, you can:

1. **Custom Output Paths**: Use `-o/--output` to specify output file locations
2. **Batch Processing Modes**: Choose between `text`, `table`, `markdown`, or `all`
3. **Keyword Count**: Adjust `--top` parameter for keyword extraction

---

## 💡 Design Philosophy

### 🎯 Core Principles

1. **Zero Dependencies** - Pure Python implementation ensures maximum compatibility
2. **Simple by Default** - Sensible defaults that work immediately
3. **Extensible** - Clean architecture for custom extensions
4. **Performance First** - Optimized for speed and memory efficiency

### 🔄 Future Roadmap

- [ ] OCR integration for scanned PDFs
- [ ] Image extraction from PDFs
- [ ] PDF creation capabilities
- [ ] GUI application
- [ ] Web API service
- [ ] Language-specific content detection

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the need for simple, dependency-free PDF processing tools
- Built with ❤️ for developers and data scientists
- Special thanks to all contributors

---

<p align="center">
  <strong>Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a></strong>
  <br>
  <sub>If you find this project useful, please give it a ⭐</sub>
</p>
