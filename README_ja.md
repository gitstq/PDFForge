# 🛠️ PDFForge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/依存関係-ゼロ依存-orange.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/プラットフォーム-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg" alt="Platform">
</p>

<p align="center">
  <strong>ゼロ依存 インテリジェント PDF ドキュメント分析・処理エンジン</strong>
</p>

<p align="center">
  <a href="https://github.com/gitstq/PDFForge">ドキュメント</a>
  •
  <a href="https://github.com/gitstq/PDFForge/releases">リリース</a>
  •
  <a href="https://github.com/gitstq/PDFForge/issues">イシュー</a>
</p>

---

## 🎉 プロジェクト紹介

**PDFForge** は、強力で軽量、ゼロ依存のPDFドキュメント分析・処理エンジンです。テキスト抽出、テーブル検出、構造分析、Markdown変換など総合的にサポートし、直感的なCLIインターフェースでPDF処理を簡単・効率的に行えます。

✨ **なぜPDFForge인가？**

- 🔧 **ゼロ依存** - ピュアPython実装、C拡張なし、外部ライブラリ不要
- 📊 **インテリジェントテーブル検出** - テーブルデータを自動検出・抽出
- 🏗️ **構造分析** - 見出し、段落、リストなどのドキュメント構造を分析
- 📝 **Markdown出力** - PDF内容をクリーンなMarkdown形式に変換
- ⚡ **高速処理** - 最適化された速度、最小限のメモリ使用量
- 🌐 **クロスプラットフォーム** - Windows、macOS、Linuxでシームレスに動作
- 🎯 **開発者向け** - プロジェクトへの統合が容易なクリーンなAPI

---

## ✨ コア機能

| 機能 | 説明 |
|------|------|
| 📄 **テキスト抽出** | PDF全体または指定ページのテキストを抽出 |
| 📊 **テーブル検出** - テーブルを自動検出しCSV/JSON形式に変換 |
| 🏗️ **構造分析** - 見出し、段落、リスト、フッターなどを分析 |
| 📝 **Markdown変換** - PDFをクリーンなMarkdown形式に変換 |
| 🔑 **キーワード抽出** - 頻度分析に基づいてキーワードを抽出 |
| 📦 **バッチ処理** - 複数のPDFファイルを一度に処理 |
| 💾 **JSON出力** - 構造分析付きのPDFデータをエクスポート |
| 🎨 **カラーCLI** - 美しく情報量の多いコマンドライン出力 |

---

## 🚀 クイックスタート

### 📥 インストール

**方法1：pipでインストール（推奨）**
```bash
pip install pdfforge
```

**方法2：ソースからインストール**
```bash
git clone https://github.com/gitstq/PDFForge.git
cd PDFForge
pip install -e .
```

**方法3：直接使用（インストール不要）**
```bash
python -m pdfForge <コマンド> <入力ファイル>
```

### 🔰 基本的な使い方

```bash
# PDF情報を表示
pdfforge info document.pdf

# テキストを抽出
pdfforge extract document.pdf -o text.txt

# テーブルを抽出
pdfforge tables document.pdf -f csv -o tables.csv

# ドキュメント構造を分析
pdfforge analyze document.pdf -o structure.json

# Markdownに変換
pdfforge convert document.pdf -o document.md

# キーワードを抽出
pdfforge keywords document.pdf --top 20

# バッチ処理
pdfforge batch ./pdf_folder/ --mode all --output ./output/
```

### 💻 Python API

```python
from pdfForge import PDFDocument, TextExtractor, TableExtractor

# PDFを読み込む
doc = PDFDocument("document.pdf")
doc.parse()

# テキストを抽出
text = doc.get_full_text()
print(f"{len(text)} 文字を抽出しました")

# テーブルを抽出
extractor = TableExtractor(doc)
tables = extractor.detect_tables()

for table in tables:
    csv = table.to_csv()
    print(f"テーブル: {table.rows}x{table.cols}")
```

---

## 📖 詳細な使い方ガイド

### CLIコマンド詳解

#### 📄 PDF情報
```bash
pdfforge info <input.pdf>
```
タイトル、作者、作成日、ページ数、ファイルサイズなど詳細なPDFメタデータを表示します。

#### 📝 テキスト抽出
```bash
# 全テキストを抽出
pdfforge extract <input.pdf> -o output.txt

# プレーンテキストを抽出（クリーンアップ済み）
pdfforge extract <input.pdf> --plain -o output.txt
```

#### 📊 テーブル抽出
```bash
# テーブルを表示
pdfforge tables <input.pdf>

# CSVでエクスポート
pdfforge tables <input.pdf> -f csv -o tables.csv

# JSONでエクスポート
pdfforge tables <input.pdf> -f json -o tables.json
```

#### 🏗️ 構造分析
```bash
pdfforge analyze <input.pdf> -o structure.json
```

#### 📝 Markdown変換
```bash
# 基本的な変換
pdfforge convert <input.pdf> -o output.md

# 完全な変換（構造を保持）
pdfforge convert <input.pdf> --full -o output.md
```

#### 🔑 キーワード抽出
```bash
pdfforge keywords <input.pdf> --top 30 -o keywords.json
```

#### 📦 バッチ処理
```bash
# フォルダ内の全PDFを処理
pdfforge batch ./pdf_folder/ --output ./output/

# モード指定
pdfforge batch ./pdf_folder/ --mode text --output ./text_output/
pdfforge batch ./pdf_folder/ --mode table --output ./table_output/
pdfforge batch ./pdf_folder/ --mode markdown --output ./md_output/
```

#### 💾 JSONエクスポート
```bash
# 基本的なJSONエクスポート
pdfforge json <input.pdf> -o output.json

# 構造分析を含む
pdfforge json <input.pdf> --structure -o output.json
```

---

## 🛠️ 設定ガイド

PDFForgeは箱から出してすぐに動作し、設定は不要です！

高度な使い方：

1. **カスタム出力パス**: `-o/--output` で出力ファイルの位置を指定
2. **バッチ処理モード**: `text`、`table`、`markdown`、`all` から選択
3. **キーワード数**: `--top` パラメータで抽出数を調整

---

## 💡 設計理念

### 🎯 コア原則

1. **ゼロ依存** - ピュアPython実装で最大限の互換性を確保
2. **シンプルデフォルト** - そのまま動作する合理的なデフォルト
3. **拡張性** - カスタム拡張のためのクリーンなアーキテクチャ
4. **パフォーマンス優先** - 速度とメモリ効率の最適化

### 🔄 今後のロードマップ

- [ ] OCR統合（スキャンPDFサポート）
- [ ] 画像抽出
- [ ] PDF作成機能
- [ ] GUIアプリケーション
- [ ] Web APIサービス
- [ ] 多言語コンテンツ検出

---

## 🤝 コントリビュート

コントリビュートは大歓迎です！Pull Requestをお気軽にお送りください。

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

---

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

## 🙏 謝辞

- シンプルさで依存関係のないPDF処理ツールへの需要からインスピレーションを得る
- 開発者とデータサイエンティストのために心を込めて構築
- すべてのコントリビューターに感謝

---

<p align="center">
  <strong>❤️ <a href="https://github.com/gitstq">gitstq</a> 精心製作</strong>
  <br>
  <sub>このプロジェクトが役立った場合は、⭐ を付けてください</sub>
</p>
