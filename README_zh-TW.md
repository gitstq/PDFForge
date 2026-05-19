# 🛠️ PDFForge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/依賴-零依賴-orange.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg" alt="Platform">
</p>

<p align="center">
  <strong>零依賴智能PDF文檔分析與處理引擎</strong>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PDFForge">文檔</a>
  •
  <a href="https://github.com/gitstq/PDFForge/releases">版本發布</a>
  •
  <a href="https://github.com/gitstq/PDFForge/issues">問題回饋</a>
</p>

---

## 🎉 專案介紹

**PDFForge** 是一款強大、輕量級、零依賴的PDF文檔分析與處理引擎。它提供全面的文本提取、表格檢測、結构分析和Markdown轉換功能，透過直觀的CLI介面讓PDF處理變得簡單高效。

✨ **為什麼選擇PDFForge？**

- 🔧 **零依賴** - 純Python實现，無需C擴展，無需安裝任何外部庫
- 📊 **智能表格檢測** - 自動檢測並提取表格數據
- 🏗️ **結構分析** - 分析文檔結構，包括標題、段落、列表等
- 📝 **Markdown導出** - 將PDF內容轉換為整潔的Markdown格式
- ⚡ **極速高效** - 優化速度，最小記憶體佔用
- 🌐 **跨平台** - 在Windows、macOS、Linux上無縫運行
- 🎯 **開發者友好** - 簡潔的API，易於整合到你的專案中

---

## ✨ 核心特性

| 功能 | 描述 |
|------|------|
| 📄 **文本提取** | 從整個PDF或指定頁面範圍提取文本 |
| 📊 **表格檢測** | 自動檢測並將表格提取為CSV/JSON格式 |
| 🏗️ **結构分析** | 分析標題、段落、列表、頁腳等結構 |
| 📝 **Markdown轉換** | 將PDF轉換為整潔的Markdown格式 |
| 🔑 **關鍵詞提取** | 基於詞頻分析提取關鍵詞 |
| 📦 **批量處理** | 一條命令處理多個PDF檔案 |
| 💾 **JSON導出** | 導出帶結构分析的PDF數據 |
| 🎨 **彩色CLI** - 精美、有資訊的命令列輸出 |

---

## 🚀 快速開始

### 📥 安裝

**方式一：pip安裝（推薦）**
```bash
pip install pdfforge
```

**方式二：從原始碼安裝**
```bash
git clone https://github.com/gitstq/PDFForge.git
cd PDFForge
pip install -e .
```

**方式三：直接使用（免安裝）**
```bash
python -m pdfForge <命令> <輸入檔案>
```

### 🔰 基本用法

```bash
# 查看PDF資訊
pdfforge info document.pdf

# 提取文本
pdfforge extract document.pdf -o text.txt

# 提取表格
pdfforge tables document.pdf -f csv -o tables.csv

# 分析文檔結構
pdfforge analyze document.pdf -o structure.json

# 轉換為Markdown
pdfforge convert document.pdf -o document.md

# 提取關鍵詞
pdfforge keywords document.pdf --top 20

# 批量處理
pdfforge batch ./pdf_folder/ --mode all --output ./output/
```

### 💻 Python API

```python
from pdfForge import PDFDocument, TextExtractor, TableExtractor

# 載入PDF
doc = PDFDocument("document.pdf")
doc.parse()

# 提取文本
text = doc.get_full_text()
print(f"提取了 {len(text)} 個字元")

# 提取表格
extractor = TableExtractor(doc)
tables = extractor.detect_tables()

for table in tables:
    csv = table.to_csv()
    print(f"表格: {table.rows}x{table.cols}")
```

---

## 📖 詳細使用指南

### CLI命令詳解

#### 📄 PDF資訊
```bash
pdfforge info <input.pdf>
```
顯示詳細的PDF元數據，包括標題、作者、建立日期、頁數和檔案大小。

#### 📝 文本提取
```bash
# 提取所有文本
pdfforge extract <input.pdf> -o output.txt

# 提取純文本（清理後）
pdfforge extract <input.pdf> --plain -o output.txt
```

#### 📊 表格提取
```bash
# 顯示表格
pdfforge tables <input.pdf>

# 導出為CSV
pdfforge tables <input.pdf> -f csv -o tables.csv

# 導出為JSON
pdfforge tables <input.pdf> -f json -o tables.json
```

#### 🏗️ 結构分析
```bash
pdfforge analyze <input.pdf> -o structure.json
```

#### 📝 Markdown轉換
```bash
# 基本轉換
pdfforge convert <input.pdf> -o output.md

# 完整轉換（保留結構）
pdfforge convert <input.pdf> --full -o output.md
```

#### 🔑 關鍵詞提取
```bash
pdfforge keywords <input.pdf> --top 30 -o keywords.json
```

#### 📦 批量處理
```bash
# 處理資料夾中的所有PDF
pdfforge batch ./pdf_folder/ --output ./output/

# 指定模式
pdfforge batch ./pdf_folder/ --mode text --output ./text_output/
pdfforge batch ./pdf_folder/ --mode table --output ./table_output/
pdfforge batch ./pdf_folder/ --mode markdown --output ./md_output/
```

#### 💾 JSON導出
```bash
# 基本JSON導出
pdfforge json <input.pdf> -o output.json

# 包含結构分析
pdfforge json <input.pdf> --structure -o output.json
```

---

## 🛠️ 配置說明

PDFForge開箱即用，無需任何配置！

高級用法：

1. **自訂輸出路徑**：使用 `-o/--output` 指定輸出檔案位置
2. **批量處理模式**：選擇 `text`、`table`、`markdown` 或 `all`
3. **關鍵詞數量**：調整 `--top` 參數控制提取數量

---

## 💡 設計理念

### 🎯 核心原則

1. **零依賴** - 純Python實现確保最大相容性
2. **簡單預設** - 開箱即用的合理預設值
3. **可擴展** - 清晰的架構便於擴展
4. **效能優先** - 優化速度和記憶體效率

### 🔄 未來規劃

- [ ] OCR整合（掃描PDF支援）
- [ ] 圖片提取
- [ ] PDF建立功能
- [ ] GUI圖形介面
- [ ] Web API服務
- [ ] 多語言內容檢測

---

## 🤝 貢獻指南

歡迎貢獻！請隨時提交Pull Request。

1. Fork本倉庫
2. 建立你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 建立Pull Request

詳情請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 開源協議

本專案採用MIT協議 - 詳見 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- 靈感來源於對簡單、無依賴PDF處理工具的需求
- 為開發者和數據科學家用心打造
- 感謝所有貢獻者

---

<p align="center">
  <strong>❤️ 由 <a href="https://github.com/gitstq">gitstq</a> 精心製作</strong>
  <br>
  <sub>如果這個專案對你有幫助，請給個 ⭐</sub>
</p>
