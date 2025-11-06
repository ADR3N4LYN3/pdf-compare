# 📄 pdf-compare

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

> Modern command-line tool for comparing PDF files with advanced visual diff capabilities, detailed statistics, and multiple output formats.

## ✨ Features

- 🔍 **Visual Comparison**: Pixel-by-pixel comparison of PDF pages rendered as high-resolution images
- 📊 **Multiple Output Formats**: Generate reports as PDF, HTML, JSON, or individual images
- 📈 **Detailed Statistics**: Per-page and overall similarity percentages, difference counts, and region detection
- 📑 **Advanced Multi-Page Support**: Compare PDFs with different page counts, with clear reporting of differences
- ⚙️ **Configurable Tolerance**: Set pixel difference threshold to ignore minor rendering variations
- 🚀 **High Performance**: Optimized rendering with PyMuPDF and progress tracking
- 🔢 **Exit Codes**: Script-friendly with exit code 0 for identical PDFs, 1 for differences
- 🎨 **Beautiful Reports**: Color-coded HTML reports and annotated PDF outputs with difference highlighting

---

## 📦 Installation

### Option 1: Install from PyPI (when published)

```bash
pip install pdf-compare
```

### Option 2: Install from source

```bash
# Clone the repository
git clone https://github.com/ADR3N4LYN3/pdf-compare.git
cd pdf-compare

# Install dependencies and the tool
pip install -r requirements.txt
pip install -e .
```

### Option 3: Windows One-Click Installation

```powershell
# Extract the ZIP and run:
.\install.bat
```

The installation script automatically:
- ✅ Verifies Python installation
- ✅ Updates pip to latest version
- ✅ Installs all dependencies
- ✅ Makes `pdf-compare` available globally

---

## 🚀 Quick Start

### Basic Comparison

Compare two PDFs and see if they're identical:

```bash
pdf-compare document1.pdf document2.pdf
```

**Output:**
```
[INFO] Comparing PDFs...
[INFO] Rendering pages...
[INFO] Comparing 5 pages...
[OK] PDFs are identical (100.0% similar)
```

### Generate Difference Report

Create a PDF showing differences highlighted in red:

```bash
pdf-compare document1.pdf document2.pdf --output-diff differences.pdf
```

### Detailed Statistics

Get verbose statistics with per-page details:

```bash
pdf-compare document1.pdf document2.pdf --verbose
```

**Sample Output:**
```
[INFO] Comparing PDFs...
[INFO] PDF 1: document1.pdf (5 pages)
[INFO] PDF 2: document2.pdf (5 pages)

Page 1: 98.5% similar (different)
Page 2: 100.0% similar (identical)
Page 3: 97.2% similar (different)
Page 4: 100.0% similar (identical)
Page 5: 99.1% similar (different)

Overall similarity: 98.96%
[WARNING] PDFs are different
```

### Multiple Output Formats

Generate all report types at once:

```bash
pdf-compare document1.pdf document2.pdf \
  --output-diff diff.pdf \
  --output-json stats.json \
  --output-html report.html \
  --output-images diff_images/
```

---

## 📚 Command-Line Reference

### Basic Syntax

```bash
pdf-compare [OPTIONS] PDF1 PDF2
```

### Arguments

| Argument | Description |
|----------|-------------|
| `PDF1` | First PDF file to compare |
| `PDF2` | Second PDF file to compare |

### Output Options

| Option | Description | Example |
|--------|-------------|---------|
| `--output-diff PATH` | Output PDF file with highlighted differences | `--output-diff result.pdf` |
| `--output-json PATH` | Output JSON file with detailed statistics | `--output-json stats.json` |
| `--output-html PATH` | Output HTML report with visual comparison | `--output-html report.html` |
| `--output-images DIR` | Output directory for difference images | `--output-images diffs/` |
| `--output-text PATH` | Output text file with comparison summary | `--output-text summary.txt` |

### Rendering Options

| Option | Default | Description | Example |
|--------|---------|-------------|---------|
| `--dpi INTEGER` | 150 | Resolution for PDF rendering (higher = better quality) | `--dpi 300` |
| `--threshold INTEGER` | 0 | Pixel difference threshold 0-255 (ignore minor differences) | `--threshold 10` |

### Display Options

| Option | Description |
|--------|-------------|
| `--quiet, -q` | Quiet mode - only output exit code (no messages) |
| `--verbose, -v` | Verbose mode - show detailed per-page statistics |
| `--no-progress` | Disable progress bar during comparison |

### Information

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `--help` | Show help message and exit |

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | PDFs are identical |
| `1` | PDFs are different |
| `2` | Error occurred (file not found, invalid PDF, etc.) |

---

## 💡 Usage Examples

### 1. Script Integration (Bash)

Use in scripts with exit codes:

```bash
pdf-compare file1.pdf file2.pdf --quiet

if [ $? -eq 0 ]; then
  echo "✅ Files are identical"
else
  echo "❌ Files differ"
fi
```

### 2. Script Integration (PowerShell)

```powershell
pdf-compare file1.pdf file2.pdf --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "Files are identical" -ForegroundColor Green
} else {
    Write-Host "Files differ" -ForegroundColor Red
}
```

### 3. Custom DPI and Threshold

Higher DPI for better quality, threshold to ignore minor differences:

```bash
pdf-compare document1.pdf document2.pdf \
  --dpi 300 \
  --threshold 10 \
  --output-diff high_res_diff.pdf
```

**Use case**: Ignore anti-aliasing or minor rendering differences

### 4. Batch Processing (PowerShell)

Compare multiple files against a reference:

```powershell
Get-ChildItem -Filter "*.pdf" | ForEach-Object {
    pdf-compare $_.FullName "reference.pdf" `
      --output-json "results\$($_.BaseName).json" `
      --quiet
}
```

### 5. CI/CD Integration

Integrate into automated testing pipelines:

```yaml
# GitHub Actions example
- name: Compare PDFs
  run: |
    pdf-compare expected.pdf generated.pdf --quiet
    if [ $? -ne 0 ]; then
      pdf-compare expected.pdf generated.pdf --output-html diff-report.html
      exit 1
    fi
```

### 6. Generate Complete Report Package

Create all outputs for comprehensive analysis:

```bash
pdf-compare contract_v1.pdf contract_v2.pdf \
  --output-diff "reports/differences.pdf" \
  --output-html "reports/comparison.html" \
  --output-json "reports/stats.json" \
  --output-images "reports/images/" \
  --output-text "reports/summary.txt" \
  --verbose
```

---

## 📋 Output Formats

### 📄 PDF Report (`--output-diff`)

Generates a multi-page PDF with:
- **Summary page** with overall statistics and comparison overview
- **One page per compared page** showing differences highlighted in red
- **Per-page similarity statistics** displayed on each page
- **Visual diff highlighting** with configurable colors

**Perfect for**: Document reviews, version control, print verification

### 📊 JSON Report (`--output-json`)

Structured data including:

```json
{
  "pdf1_path": "document1.pdf",
  "pdf2_path": "document2.pdf",
  "overall_similarity": 98.5,
  "are_identical": false,
  "total_pages_compared": 5,
  "pages_identical": 2,
  "pages_different": 3,
  "page_stats": [
    {
      "page_number": 0,
      "is_identical": false,
      "similarity_percentage": 97.3,
      "different_pixels": 12450,
      "total_pixels": 480000,
      "difference_regions": [
        {
          "x": 120,
          "y": 340,
          "width": 200,
          "height": 50
        }
      ]
    }
  ]
}
```

**Perfect for**: Automated testing, data analysis, custom reporting

### 🌐 HTML Report (`--output-html`)

Beautiful, interactive HTML page with:
- 🎨 **Responsive design** with gradient cards and modern styling
- 📊 **Overall statistics dashboard** with color-coded indicators
- 🖼️ **Per-page comparison** with embedded base64 images
- ✅ **Visual status indicators** (identical/different badges)
- 📱 **Mobile-friendly** layout

**Perfect for**: Sharing with non-technical users, presentations

### 🖼️ Image Output (`--output-images`)

Individual PNG files for each page's difference visualization:
- `diff_page_001.png`
- `diff_page_002.png`
- `diff_page_003.png`
- etc.

**Perfect for**: Manual review, embedding in other documents

### 📝 Text Report (`--output-text`)

Simple text summary:

```
PDF Comparison Summary
====================
PDF 1: document1.pdf (5 pages)
PDF 2: document2.pdf (5 pages)

Overall Similarity: 98.5%
Status: DIFFERENT

Page-by-Page Results:
  Page 1: 97.3% similar (DIFFERENT)
  Page 2: 100.0% similar (IDENTICAL)
  Page 3: 99.1% similar (DIFFERENT)
  Page 4: 100.0% similar (IDENTICAL)
  Page 5: 98.7% similar (DIFFERENT)
```

**Perfect for**: Quick reviews, log files, email reports

---

## 🎯 Use Cases

### 📑 Document Version Control

Compare different versions of contracts, proposals, or technical documents:

```bash
pdf-compare contract_v1.pdf contract_v2.pdf \
  --output-html changes.html \
  --verbose
```

### ✅ Quality Assurance

Verify PDF generation consistency in automated workflows:

```bash
pdf-compare expected_output.pdf actual_output.pdf \
  --threshold 5 \
  --quiet
```

### 🤖 Automated Testing

Integrate into CI/CD pipelines for regression testing:

```bash
# Test that PDF generation hasn't changed
pdf-compare reference.pdf generated.pdf --quiet || exit 1
```

### 🖨️ Print Production

Verify print-ready PDFs haven't changed unexpectedly:

```bash
pdf-compare approved_print.pdf final_print.pdf \
  --dpi 300 \
  --output-diff print_verification.pdf
```

### 📧 Email Campaign Verification

Compare rendered email PDFs across different email clients:

```bash
pdf-compare email_outlook.pdf email_gmail.pdf \
  --threshold 15 \
  --output-html client_differences.html
```

---

## ⚙️ Requirements

- **Python 3.8 or higher**
- **PyMuPDF (fitz)** - PDF rendering and manipulation
- **Pillow** - Image processing and comparison
- **Click** - Command-line interface framework
- **reportlab** - PDF report generation
- **tqdm** - Progress bars and status display
- **colorama** - Colored terminal output (Windows compatible)
- **numpy** - Numerical operations for pixel comparison

All dependencies are automatically installed via `pip install -r requirements.txt`

---

## 🆚 Comparison with diff-pdf

This tool improves upon [vslavik/diff-pdf](https://github.com/vslavik/diff-pdf):

| Feature | diff-pdf | pdf-compare |
|---------|----------|-------------|
| **Language** | C++ | Python |
| **Maintenance** | Inactive since 2024 | ✅ Active |
| **Dependencies** | wxWidgets, Cairo, Poppler | PyMuPDF, Pillow |
| **Installation** | Build from source | `pip install` |
| **Multi-page Support** | Basic | ✅ Advanced with statistics |
| **Output Formats** | PDF only | ✅ PDF, HTML, JSON, Images, Text |
| **Statistics** | None | ✅ Detailed per-page and overall |
| **Progress Display** | None | ✅ Progress bar with tqdm |
| **Windows Binary** | Limited | ✅ One-click installer (.bat) |
| **Threshold Support** | No | ✅ Yes (configurable 0-255) |
| **Exit Codes** | Basic | ✅ 0/1/2 for scripting |
| **HTML Reports** | No | ✅ Beautiful responsive design |
| **JSON Export** | No | ✅ Full structured data |

---

## 🛠️ Building from Source

### User Installation

```bash
# Clone the repository
git clone https://github.com/ADR3N4LYN3/pdf-compare.git
cd pdf-compare

# Install directly (no virtual environment needed)
pip install -r requirements.txt
pip install -e .

# Verify installation
pdf-compare --version

# Run tests
pytest
```

### Development Setup (for contributors)

If you want to develop and modify the code:

```bash
# Optional: Create virtual environment for isolated development
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev tools
pip install -r requirements-dev.txt
pip install -e .

# Run tests with coverage
pytest --cov=pdf_compare
```

### Windows Distribution

For Windows users, simply distribute the repository with `install.bat`:

```bash
# Create a ZIP with the project
# Users can extract and run install.bat for one-click installation
```

---

## 📚 Documentation

For detailed guides and examples, check out the [docs/](docs/) folder:

- **[Installation Guide](docs/installation.md)** - Detailed installation instructions and troubleshooting
- **[Usage Examples](docs/examples.md)** - Comprehensive examples for all use cases
- **[Testing Guide](docs/testing.md)** - How to test and validate the tool
- **[Contributing Guide](CONTRIBUTING.md)** - Development guidelines
- **[Changelog](CHANGELOG.md)** - Version history and updates

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features.

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/ADR3N4LYN3/pdf-compare.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes** and add tests

4. **Run the test suite**
   ```bash
   pytest
   ```

5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request** on GitHub

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guidelines
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [PyMuPDF](https://pymupdf.readthedocs.io/) for excellent PDF rendering
- Inspired by [diff-pdf](https://github.com/vslavik/diff-pdf) but modernized and extended
- Uses [Click](https://click.palletsprojects.com/) for the CLI interface
- Image processing powered by [Pillow](https://pillow.readthedocs.io/)

---

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/ADR3N4LYN3/pdf-compare/issues)
- 📖 **Documentation**: [docs/](docs/) folder
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ADR3N4LYN3/pdf-compare/discussions)

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Text-based comparison mode** - Compare extracted text instead of pixels
- [ ] **Side-by-side comparison view** - Interactive HTML viewer with slider
- [ ] **Annotation detection** - Compare annotations and form fields separately
- [ ] **Parallel processing** - Multi-threaded rendering for large PDFs
- [ ] **Docker container** - Cross-platform containerized version
- [ ] **Web interface** - Optional web UI for drag-and-drop comparison
- [ ] **CI/CD integrations** - GitHub Actions, GitLab CI, Jenkins plugins
- [ ] **Fuzzy matching** - Detect moved content even if position changed
- [ ] **Metadata comparison** - Compare PDF properties, bookmarks, links
- [ ] **Batch reporting** - Compare multiple file pairs and generate summary report

---

<p align="center">
  <strong>Made with ❤️ and Python by developers who need better PDF comparison tools</strong>
</p>

<p align="center">
  <a href="https://github.com/ADR3N4LYN3/pdf-compare">⭐ Star this repo if you find it useful!</a>
</p>
