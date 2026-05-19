# 🛠️ PDFForge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/依赖-零依赖-orange.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg" alt="Platform">
</p>

<p align="center">
  <strong>零依赖智能PDF文档分析与处理引擎</strong>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PDFForge">文档</a>
  •
  <a href="https://github.com/gitstq/PDFForge/releases">版本发布</a>
  •
  <a href="https://github.com/gitstq/PDFForge/issues">问题反馈</a>
</p>

---

## 🎉 项目介绍

**PDFForge** 是一款强大、轻量级、零依赖的PDF文档分析与处理引擎。它提供全面的文本提取、表格检测、结构分析和Markdown转换功能，通过直观的CLI界面让PDF处理变得简单高效。

✨ **为什么选择PDFForge？**

- 🔧 **零依赖** - 纯Python实现，无需C扩展，无需安装任何外部库
- 📊 **智能表格检测** - 自动检测并提取表格数据
- 🏗️ **结构分析** - 分析文档结构，包括标题、段落、列表等
- 📝 **Markdown导出** - 将PDF内容转换为整洁的Markdown格式
- ⚡ **极速高效** - 优化速度，最小内存占用
- 🌐 **跨平台** - 在Windows、macOS、Linux上无缝运行
- 🎯 **开发者友好** - 简洁的API，易于集成到你的项目中

---

## ✨ 核心特性

| 功能 | 描述 |
|------|------|
| 📄 **文本提取** | 从整个PDF或指定页面范围提取文本 |
| 📊 **表格检测** | 自动检测并将表格提取为CSV/JSON格式 |
| 🏗️ **结构分析** | 分析标题、段落、列表、脚注等结构 |
| 📝 **Markdown转换** | 将PDF转换为整洁的Markdown格式 |
| 🔑 **关键词提取** | 基于词频分析提取关键词 |
| 📦 **批量处理** | 一条命令处理多个PDF文件 |
| 💾 **JSON导出** | 导出带结构分析的PDF数据 |
| 🎨 **彩色CLI** - 精美、有信息的命令行输出 |

---

## 🚀 快速开始

### 📥 安装

**方式一：pip安装（推荐）**
```bash
pip install pdfforge
```

**方式二：从源码安装**
```bash
git clone https://github.com/gitstq/PDFForge.git
cd PDFForge
pip install -e .
```

**方式三：直接使用（免安装）**
```bash
python -m pdfForge <命令> <输入文件>
```

### 🔰 基本用法

```bash
# 查看PDF信息
pdfforge info document.pdf

# 提取文本
pdfforge extract document.pdf -o text.txt

# 提取表格
pdfforge tables document.pdf -f csv -o tables.csv

# 分析文档结构
pdfforge analyze document.pdf -o structure.json

# 转换为Markdown
pdfforge convert document.pdf -o document.md

# 提取关键词
pdfforge keywords document.pdf --top 20

# 批量处理
pdfforge batch ./pdf_folder/ --mode all --output ./output/
```

### 💻 Python API

```python
from pdfForge import PDFDocument, TextExtractor, TableExtractor

# 加载PDF
doc = PDFDocument("document.pdf")
doc.parse()

# 提取文本
text = doc.get_full_text()
print(f"提取了 {len(text)} 个字符")

# 提取表格
extractor = TableExtractor(doc)
tables = extractor.detect_tables()

for table in tables:
    csv = table.to_csv()
    print(f"表格: {table.rows}x{table.cols}")
```

---

## 📖 详细使用指南

### CLI命令详解

#### 📄 PDF信息
```bash
pdfforge info <input.pdf>
```
显示详细的PDF元数据，包括标题、作者、创建日期、页数和文件大小。

#### 📝 文本提取
```bash
# 提取所有文本
pdfforge extract <input.pdf> -o output.txt

# 提取纯文本（清理后）
pdfforge extract <input.pdf> --plain -o output.txt
```

#### 📊 表格提取
```bash
# 显示表格
pdfforge tables <input.pdf>

# 导出为CSV
pdfforge tables <input.pdf> -f csv -o tables.csv

# 导出为JSON
pdfforge tables <input.pdf> -f json -o tables.json
```

#### 🏗️ 结构分析
```bash
pdfforge analyze <input.pdf> -o structure.json
```

#### 📝 Markdown转换
```bash
# 基本转换
pdfforge convert <input.pdf> -o output.md

# 完整转换（保留结构）
pdfforge convert <input.pdf> --full -o output.md
```

#### 🔑 关键词提取
```bash
pdfforge keywords <input.pdf> --top 30 -o keywords.json
```

#### 📦 批量处理
```bash
# 处理文件夹中的所有PDF
pdfforge batch ./pdf_folder/ --output ./output/

# 指定模式
pdfforge batch ./pdf_folder/ --mode text --output ./text_output/
pdfforge batch ./pdf_folder/ --mode table --output ./table_output/
pdfforge batch ./pdf_folder/ --mode markdown --output ./md_output/
```

#### 💾 JSON导出
```bash
# 基本JSON导出
pdfforge json <input.pdf> -o output.json

# 包含结构分析
pdfforge json <input.pdf> --structure -o output.json
```

---

## 🛠️ 配置说明

PDFForge开箱即用，无需任何配置！

高级用法：

1. **自定义输出路径**：使用 `-o/--output` 指定输出文件位置
2. **批量处理模式**：选择 `text`、`table`、`markdown` 或 `all`
3. **关键词数量**：调整 `--top` 参数控制提取数量

---

## 💡 设计理念

### 🎯 核心原则

1. **零依赖** - 纯Python实现确保最大兼容性
2. **简单默认** - 开箱即用的合理默认值
3. **可扩展** - 清晰的架构便于扩展
4. **性能优先** - 优化速度和内存效率

### 🔄 未来规划

- [ ] OCR集成（扫描PDF支持）
- [ ] 图片提取
- [ ] PDF创建功能
- [ ] GUI图形界面
- [ ] Web API服务
- [ ] 多语言内容检测

---

## 🤝 贡献指南

欢迎贡献！请随时提交Pull Request。

1. Fork本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

详情请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 开源协议

本项目采用MIT协议 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 灵感来源于对简单、无依赖PDF处理工具的需求
- 为开发者和数据科学家用心打造
- 感谢所有贡献者

---

<p align="center">
  <strong>❤️ 由 <a href="https://github.com/gitstq">gitstq</a> 精心制作</strong>
  <br>
  <sub>如果这个项目对你有用，请给个 ⭐</sub>
</p>
