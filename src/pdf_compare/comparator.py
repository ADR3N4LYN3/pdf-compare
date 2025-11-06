"""
PDF Comparator - Main orchestration module for PDF comparison
"""

from typing import List, Tuple, Optional, Callable
from PIL import Image
import os

from .renderer import PDFRenderer
from .differ import PDFDiffer
from .stats import DiffStats, PageStats, StatsCalculator
from .reporter import Reporter


class PDFComparator:
    """Main class for comparing PDFs"""

    def __init__(
        self,
        dpi: int = 150,
        threshold: int = 0,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ):
        """
        Initialize PDF comparator

        Args:
            dpi: Resolution for rendering PDFs (default: 150)
            threshold: Pixel difference threshold (default: 0 for exact match)
            progress_callback: Optional callback function(current, total) for progress updates
        """
        self.renderer = PDFRenderer(dpi=dpi)
        self.differ = PDFDiffer(threshold=threshold)
        self.progress_callback = progress_callback

        self.pdf1_path: Optional[str] = None
        self.pdf2_path: Optional[str] = None
        self.stats: Optional[DiffStats] = None
        self.diff_images: List[Image.Image] = []

    def compare(self, pdf1_path: str, pdf2_path: str) -> DiffStats:
        """
        Compare two PDF files

        Args:
            pdf1_path: Path to first PDF
            pdf2_path: Path to second PDF

        Returns:
            DiffStats object with comparison results
        """
        # Validate inputs
        if not os.path.exists(pdf1_path):
            raise FileNotFoundError(f"PDF file not found: {pdf1_path}")
        if not os.path.exists(pdf2_path):
            raise FileNotFoundError(f"PDF file not found: {pdf2_path}")

        self.pdf1_path = pdf1_path
        self.pdf2_path = pdf2_path

        # Get page counts
        pdf1_pages = self.renderer.get_page_count(pdf1_path)
        pdf2_pages = self.renderer.get_page_count(pdf2_path)

        # Determine how many pages to compare
        pages_to_compare = min(pdf1_pages, pdf2_pages)

        # Compare each page
        page_stats_list = []
        self.diff_images = []

        for page_num in range(pages_to_compare):
            if self.progress_callback:
                self.progress_callback(page_num + 1, pages_to_compare)

            # Render pages
            img1 = self.renderer.render_page(pdf1_path, page_num)
            img2 = self.renderer.render_page(pdf2_path, page_num)

            # Normalize sizes
            img1, img2 = self.renderer.normalize_images(img1, img2)

            # Compare
            is_identical, diff_img, diff_pixels = self.differ.compare_images(img1, img2)

            # Find difference regions
            diff_regions = self.differ.find_difference_regions(img1, img2)

            # Calculate stats
            total_pixels = img1.width * img1.height * 3  # RGB channels
            page_stats = StatsCalculator.calculate_page_stats(
                page_num, is_identical, total_pixels, diff_pixels, diff_regions
            )
            page_stats_list.append(page_stats)

            # Store diff image
            self.diff_images.append(diff_img)

        # Calculate overall stats
        self.stats = StatsCalculator.calculate_overall_stats(
            pdf1_path, pdf2_path, pdf1_pages, pdf2_pages, page_stats_list
        )

        return self.stats

    def compare_simple(self, pdf1_path: str, pdf2_path: str) -> bool:
        """
        Simple comparison that returns True if PDFs are identical, False otherwise

        Args:
            pdf1_path: Path to first PDF
            pdf2_path: Path to second PDF

        Returns:
            True if PDFs are identical, False otherwise
        """
        stats = self.compare(pdf1_path, pdf2_path)
        return stats.are_identical

    def get_diff_images(self) -> List[Image.Image]:
        """
        Get the difference images from the last comparison

        Returns:
            List of difference images
        """
        return self.diff_images

    def get_stats(self) -> Optional[DiffStats]:
        """
        Get the statistics from the last comparison

        Returns:
            DiffStats object or None if no comparison has been done
        """
        return self.stats

    def save_diff_pdf(self, output_path: str):
        """
        Save difference images as a PDF report

        Args:
            output_path: Path to save the PDF report
        """
        if not self.stats or not self.diff_images:
            raise RuntimeError("No comparison results available. Run compare() first.")

        reporter = Reporter(self.stats)
        reporter.create_pdf_report(self.diff_images, output_path)

    def save_diff_images(self, output_dir: str, format: str = 'PNG'):
        """
        Save difference images as individual image files

        Args:
            output_dir: Directory to save images
            format: Image format (PNG, JPEG, etc.)
        """
        if not self.diff_images:
            raise RuntimeError("No comparison results available. Run compare() first.")

        reporter = Reporter(self.stats)
        reporter.save_diff_images(self.diff_images, output_dir, format=format)

    def save_json_report(self, output_path: str):
        """
        Save comparison statistics as JSON

        Args:
            output_path: Path to save JSON file
        """
        if not self.stats:
            raise RuntimeError("No comparison results available. Run compare() first.")

        reporter = Reporter(self.stats)
        reporter.save_json_report(output_path)

    def save_html_report(self, output_path: str):
        """
        Save comparison report as HTML with embedded images

        Args:
            output_path: Path to save HTML file
        """
        if not self.stats or not self.diff_images:
            raise RuntimeError("No comparison results available. Run compare() first.")

        reporter = Reporter(self.stats)
        reporter.create_html_report(self.diff_images, output_path)

    def save_text_report(self, output_path: str):
        """
        Save comparison summary as text file

        Args:
            output_path: Path to save text file
        """
        if not self.stats:
            raise RuntimeError("No comparison results available. Run compare() first.")

        reporter = Reporter(self.stats)
        reporter.save_text_report(output_path)

    def print_summary(self) -> str:
        """
        Get a human-readable summary of the comparison

        Returns:
            Summary string
        """
        if not self.stats:
            return "No comparison results available."

        return self.stats.get_summary()

    def get_exit_code(self) -> int:
        """
        Get exit code for CLI (0 = identical, 1 = different)

        Returns:
            0 if PDFs are identical, 1 if different
        """
        if not self.stats:
            return 1

        return 0 if self.stats.are_identical else 1
