# Usage Examples

Complete examples of using pdf-compare in various scenarios.

## Table of Contents

- [Basic Comparison](#basic-comparison)
- [Generating Reports](#generating-reports)
- [Advanced Options](#advanced-options)
- [Scripting Integration](#scripting-integration)
- [Batch Processing](#batch-processing)
- [CI/CD Integration](#cicd-integration)

## Basic Comparison

### Simple Comparison

Compare two PDFs and see if they're identical:

```bash
pdf-compare document1.pdf document2.pdf
```

### Verbose Output

Get detailed statistics with per-page breakdown:

```bash
pdf-compare document1.pdf document2.pdf --verbose
```

Output:
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

### Quiet Mode

For scripts - only returns exit code:

```bash
pdf-compare document1.pdf document2.pdf --quiet
echo $?  # 0 = identical, 1 = different
```

## Generating Reports

### PDF Report with Differences

Generate a PDF highlighting differences in red:

```bash
pdf-compare doc1.pdf doc2.pdf --output-diff differences.pdf
```

### HTML Interactive Report

Create a beautiful HTML report with embedded images:

```bash
pdf-compare doc1.pdf doc2.pdf --output-html report.html
```

Then open it:
```bash
start report.html  # Windows
open report.html   # macOS
xdg-open report.html  # Linux
```

### JSON Statistics

Export structured data for automation:

```bash
pdf-compare doc1.pdf doc2.pdf --output-json stats.json
```

JSON structure:
```json
{
  "pdf1_path": "document1.pdf",
  "pdf2_path": "document2.pdf",
  "overall_similarity": 98.5,
  "are_identical": false,
  "total_pages_compared": 5,
  "pages_identical": 2,
  "pages_different": 3,
  "page_stats": [...]
}
```

### Text Summary

Simple text file with comparison summary:

```bash
pdf-compare doc1.pdf doc2.pdf --output-text summary.txt
```

### Difference Images

Export individual PNG files for each page:

```bash
pdf-compare doc1.pdf doc2.pdf --output-images ./diff_images/
```

Output:
```
diff_images/
  ├── diff_page_001.png
  ├── diff_page_002.png
  └── diff_page_003.png
```

### All Formats at Once

Generate all report types in one command:

```bash
pdf-compare document1.pdf document2.pdf \
  --output-diff report.pdf \
  --output-json stats.json \
  --output-html report.html \
  --output-images images/ \
  --output-text summary.txt \
  --verbose
```

## Advanced Options

### High Resolution Comparison

Use higher DPI for better quality (slower):

```bash
pdf-compare doc1.pdf doc2.pdf --dpi 300 --output-diff high_res.pdf
```

DPI recommendations:
- `72` - Fast, low quality
- `150` - Default, good balance
- `300` - High quality, slower
- `600` - Very high quality, very slow

### Tolerance Threshold

Ignore minor differences (anti-aliasing, compression artifacts):

```bash
pdf-compare doc1.pdf doc2.pdf --threshold 10 --output-diff result.pdf
```

Threshold values:
- `0` - Exact match (default)
- `5-10` - Ignore minor rendering differences
- `10-20` - Ignore compression artifacts
- `20-50` - Ignore significant differences (use carefully)

### Disable Progress Bar

Useful for automated scripts:

```bash
pdf-compare doc1.pdf doc2.pdf --no-progress
```

## Scripting Integration

### Bash Script

```bash
#!/bin/bash

pdf-compare file1.pdf file2.pdf --quiet

if [ $? -eq 0 ]; then
  echo "✅ Files are identical"
else
  echo "❌ Files differ - generating report"
  pdf-compare file1.pdf file2.pdf --output-html diff-report.html
fi
```

### PowerShell Script

```powershell
pdf-compare file1.pdf file2.pdf --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "Files are identical" -ForegroundColor Green
} else {
    Write-Host "Files differ" -ForegroundColor Red
    pdf-compare file1.pdf file2.pdf --output-html diff-report.html
}
```

### Python Script

```python
import subprocess
import sys

result = subprocess.run(
    ["pdf-compare", "file1.pdf", "file2.pdf", "--quiet"],
    capture_output=True
)

if result.returncode == 0:
    print("✅ Files are identical")
else:
    print("❌ Files differ")
    # Generate report
    subprocess.run([
        "pdf-compare", "file1.pdf", "file2.pdf",
        "--output-html", "report.html"
    ])
```

## Batch Processing

### Compare Multiple Files Against Reference

PowerShell:
```powershell
Get-ChildItem -Filter "*.pdf" | ForEach-Object {
    $result = pdf-compare $_.FullName "reference.pdf" --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "$($_.Name) differs from reference" -ForegroundColor Yellow
        pdf-compare $_.FullName "reference.pdf" `
            --output-json "results\$($_.BaseName).json"
    }
}
```

Bash:
```bash
for file in *.pdf; do
    if ! pdf-compare "$file" "reference.pdf" --quiet; then
        echo "$file differs from reference"
        pdf-compare "$file" "reference.pdf" \
            --output-json "results/$(basename "$file" .pdf).json"
    fi
done
```

### Compare Pairs of Files

```bash
# Compare version1 vs version2 files
for file in *_v1.pdf; do
    base=$(basename "$file" _v1.pdf)
    v2_file="${base}_v2.pdf"

    if [ -f "$v2_file" ]; then
        echo "Comparing $file vs $v2_file"
        pdf-compare "$file" "$v2_file" \
            --output-html "reports/${base}_comparison.html" \
            --verbose
    fi
done
```

## CI/CD Integration

### GitHub Actions

```yaml
name: PDF Comparison Test

on: [push, pull_request]

jobs:
  compare-pdfs:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install pdf-compare
      run: |
        pip install -r requirements.txt
        pip install -e .

    - name: Compare PDFs
      run: |
        pdf-compare expected.pdf generated.pdf --quiet
        if [ $? -ne 0 ]; then
          echo "PDFs differ - generating report"
          pdf-compare expected.pdf generated.pdf \
            --output-html diff-report.html
          exit 1
        fi

    - name: Upload report if failed
      if: failure()
      uses: actions/upload-artifact@v2
      with:
        name: diff-report
        path: diff-report.html
```

### GitLab CI

```yaml
pdf_comparison:
  stage: test
  image: python:3.9

  script:
    - pip install -r requirements.txt
    - pip install -e .
    - |
      if ! pdf-compare expected.pdf generated.pdf --quiet; then
        echo "PDFs differ"
        pdf-compare expected.pdf generated.pdf --output-html diff-report.html
        exit 1
      fi

  artifacts:
    when: on_failure
    paths:
      - diff-report.html
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Compare PDFs') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pip install -e .

                    if ! pdf-compare expected.pdf generated.pdf --quiet; then
                        echo "PDFs differ"
                        pdf-compare expected.pdf generated.pdf \
                            --output-html diff-report.html
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        failure {
            archiveArtifacts artifacts: 'diff-report.html'
        }
    }
}
```

## Use Cases

### Document Version Control

Track changes between document versions:

```bash
# Compare contract versions
pdf-compare contract_v1.pdf contract_v2.pdf \
  --output-html changes.html \
  --output-json changes.json \
  --verbose

# Review changes in browser
start changes.html
```

### Quality Assurance

Verify PDF generation consistency:

```bash
# Generate PDF from source
generate_pdf.py input.txt output.pdf

# Compare with expected output
pdf-compare expected_output.pdf output.pdf \
  --threshold 5 \
  --quiet || echo "QA Failed"
```

### Print Production Verification

Ensure print-ready PDFs haven't changed:

```bash
pdf-compare approved_print.pdf final_print.pdf \
  --dpi 300 \
  --output-diff print_verification.pdf
```

### Regression Testing

Automated visual regression testing:

```bash
# Generate test PDF
python generate_report.py > test_report.pdf

# Compare with baseline
if pdf-compare baseline.pdf test_report.pdf --quiet; then
  echo "✅ Visual regression test passed"
else
  echo "❌ Visual regression detected"
  pdf-compare baseline.pdf test_report.pdf \
    --output-html regression_report.html
  exit 1
fi
```

## Exit Codes

Understanding pdf-compare exit codes:

| Exit Code | Meaning | Use Case |
|-----------|---------|----------|
| `0` | PDFs are identical | Success in tests |
| `1` | PDFs are different | Normal difference detection |
| `2` | Error occurred | File not found, invalid PDF, etc. |
| `130` | Interrupted by user | Ctrl+C during execution |

Example error handling:

```bash
pdf-compare doc1.pdf doc2.pdf --quiet
EXIT_CODE=$?

case $EXIT_CODE in
  0)
    echo "Identical"
    ;;
  1)
    echo "Different"
    ;;
  2)
    echo "Error occurred"
    exit 1
    ;;
  130)
    echo "Interrupted"
    exit 130
    ;;
esac
```

## Performance Tips

### For Large PDFs

```bash
# Use lower DPI for faster comparison
pdf-compare large1.pdf large2.pdf --dpi 72

# Disable progress bar for slightly better performance
pdf-compare large1.pdf large2.pdf --no-progress --quiet
```

### For High-Quality Comparisons

```bash
# Maximum quality
pdf-compare doc1.pdf doc2.pdf \
  --dpi 600 \
  --threshold 0 \
  --output-diff ultra_high_quality.pdf
```

### For Automation

```bash
# Minimal output, maximum speed
pdf-compare doc1.pdf doc2.pdf --quiet --no-progress
```
