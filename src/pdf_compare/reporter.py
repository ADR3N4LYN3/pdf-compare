"""
Reporter module - Generates reports in various formats (PDF, JSON, HTML, Images)
"""

from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import List, Optional
import os
import json
import html
from datetime import datetime

from .stats import DiffStats


class Reporter:
    """Generates comparison reports in various formats"""

    def __init__(self, stats: DiffStats):
        """
        Initialize reporter with comparison statistics

        Args:
            stats: DiffStats object containing comparison results
        """
        self.stats = stats

    def save_json_report(self, output_path: str):
        """
        Save statistics as JSON file

        Args:
            output_path: Path to save JSON report
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.stats.to_json())

    def save_text_report(self, output_path: str):
        """
        Save statistics as text file

        Args:
            output_path: Path to save text report
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.stats.get_summary())

    def save_diff_images(self, diff_images: List[Image.Image], output_dir: str,
                        format: str = 'PNG', prefix: str = 'diff_page'):
        """
        Save difference images to a directory

        Args:
            diff_images: List of difference images
            output_dir: Directory to save images
            format: Image format (PNG, JPEG, etc.)
            prefix: Filename prefix
        """
        os.makedirs(output_dir, exist_ok=True)

        for i, img in enumerate(diff_images):
            filename = f"{prefix}_{i + 1:03d}.{format.lower()}"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, format=format)

    def create_pdf_report(self, diff_images: List[Image.Image], output_path: str,
                         page_size=A4, title: str = "PDF Comparison Report"):
        """
        Create a PDF report with difference images and statistics

        Args:
            diff_images: List of difference images
            output_path: Path to save PDF report
            page_size: Page size tuple (width, height)
            title: Report title
        """
        c = canvas.Canvas(output_path, pagesize=page_size)
        page_width, page_height = page_size

        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(page_width / 2, page_height - inch, title)

        c.setFont("Helvetica", 12)
        y_pos = page_height - 2 * inch

        # Summary statistics
        summary_lines = [
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"PDF 1: {os.path.basename(self.stats.pdf1_path)} ({self.stats.pdf1_pages} pages)",
            f"PDF 2: {os.path.basename(self.stats.pdf2_path)} ({self.stats.pdf2_pages} pages)",
            "",
            f"Result: {'IDENTICAL' if self.stats.are_identical else 'DIFFERENT'}",
            f"Overall Similarity: {self.stats.overall_similarity:.2f}%",
            f"Pages Compared: {self.stats.pages_compared}",
            f"Identical Pages: {self.stats.identical_pages}",
            f"Different Pages: {self.stats.different_pages}",
        ]

        for line in summary_lines:
            c.drawString(inch, y_pos, line)
            y_pos -= 20

        c.showPage()

        # Add difference images
        for i, img in enumerate(diff_images):
            page_stats = self.stats.page_stats[i] if i < len(self.stats.page_stats) else None

            # Add page header
            c.setFont("Helvetica-Bold", 16)
            c.drawString(inch, page_height - inch, f"Page {i + 1}")

            if page_stats:
                c.setFont("Helvetica", 10)
                y_pos = page_height - inch - 20
                info_lines = [
                    f"Status: {'IDENTICAL' if page_stats.is_identical else 'DIFFERENT'}",
                    f"Similarity: {page_stats.similarity_percentage:.2f}%",
                    f"Different Pixels: {page_stats.different_pixels:,} / {page_stats.total_pixels:,}",
                    f"Difference Regions: {page_stats.num_difference_regions}",
                ]

                for line in info_lines:
                    c.drawString(inch, y_pos, line)
                    y_pos -= 15

            # Calculate image dimensions to fit on page
            max_width = page_width - 2 * inch
            max_height = page_height - 3 * inch

            img_width, img_height = img.size
            scale = min(max_width / img_width, max_height / img_height, 1.0)

            scaled_width = img_width * scale
            scaled_height = img_height * scale

            # Draw image
            img_reader = ImageReader(img)
            c.drawImage(
                img_reader,
                inch,
                page_height - 2.5 * inch - scaled_height,
                width=scaled_width,
                height=scaled_height,
                preserveAspectRatio=True
            )

            c.showPage()

        c.save()

    def create_html_report(self, diff_images: List[Image.Image], output_path: str,
                          image_format: str = 'PNG'):
        """
        Create an HTML report with embedded images

        Args:
            diff_images: List of difference images
            output_path: Path to save HTML report
            image_format: Format for embedded images
        """
        import base64
        from io import BytesIO

        html_parts = []
        html_parts.append("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Comparison Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #333;
            margin-top: 0;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 28px;
            font-weight: bold;
        }
        .status {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .status.identical {
            background-color: #10b981;
            color: white;
        }
        .status.different {
            background-color: #ef4444;
            color: white;
        }
        .page-section {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e5e5e5;
        }
        .page-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .page-stat {
            background-color: #f9fafb;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        .page-stat-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .page-stat-value {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .diff-image {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>PDF Comparison Report</h1>
        <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>

        <div>
            <strong>PDF 1:</strong> """ + html.escape(os.path.basename(self.stats.pdf1_path)) + f""" ({self.stats.pdf1_pages} pages)<br>
            <strong>PDF 2:</strong> """ + html.escape(os.path.basename(self.stats.pdf2_path)) + f""" ({self.stats.pdf2_pages} pages)
        </div>

        <div class="status """ + ("identical" if self.stats.are_identical else "different") + """">
            """ + ("IDENTICAL" if self.stats.are_identical else "DIFFERENT") + """
        </div>

        <div class="summary">
            <div class="stat-card">
                <div class="stat-label">Overall Similarity</div>
                <div class="stat-value">""" + f"{self.stats.overall_similarity:.1f}%" + """</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pages Compared</div>
                <div class="stat-value">""" + str(self.stats.pages_compared) + """</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Identical Pages</div>
                <div class="stat-value">""" + str(self.stats.identical_pages) + """</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Different Pages</div>
                <div class="stat-value">""" + str(self.stats.different_pages) + """</div>
            </div>
        </div>
    </div>
""")

        # Add each page
        for i, (img, page_stat) in enumerate(zip(diff_images, self.stats.page_stats)):
            # Convert image to base64
            buffered = BytesIO()
            img.save(buffered, format=image_format)
            img_str = base64.b64encode(buffered.getvalue()).decode()

            html_parts.append(f"""
    <div class="page-section">
        <div class="page-header">
            <h2>Page {i + 1}</h2>
            <span class="status {"identical" if page_stat.is_identical else "different"}">
                {"IDENTICAL" if page_stat.is_identical else "DIFFERENT"}
            </span>
        </div>

        <div class="page-stats">
            <div class="page-stat">
                <div class="page-stat-label">Similarity</div>
                <div class="page-stat-value">{page_stat.similarity_percentage:.2f}%</div>
            </div>
            <div class="page-stat">
                <div class="page-stat-label">Different Pixels</div>
                <div class="page-stat-value">{page_stat.different_pixels:,}</div>
            </div>
            <div class="page-stat">
                <div class="page-stat-label">Total Pixels</div>
                <div class="page-stat-value">{page_stat.total_pixels:,}</div>
            </div>
            <div class="page-stat">
                <div class="page-stat-label">Difference Regions</div>
                <div class="page-stat-value">{page_stat.num_difference_regions}</div>
            </div>
        </div>

        <img src="data:image/{image_format.lower()};base64,{img_str}" alt="Page {i + 1} Diff" class="diff-image">
    </div>
""")

        html_parts.append("""
    <div class="footer">
        <p>Generated by pdf-compare - Modern PDF Comparison Tool</p>
    </div>
</body>
</html>
""")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(html_parts))
