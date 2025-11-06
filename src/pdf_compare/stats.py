"""
Statistics module - Calculates detailed statistics about PDF differences
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import json


@dataclass
class PageStats:
    """Statistics for a single page comparison"""
    page_number: int
    is_identical: bool
    total_pixels: int
    different_pixels: int
    difference_percentage: float
    similarity_percentage: float
    num_difference_regions: int
    difference_regions: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "page_number": int(self.page_number),
            "is_identical": bool(self.is_identical),
            "total_pixels": int(self.total_pixels),
            "different_pixels": int(self.different_pixels),
            "difference_percentage": round(float(self.difference_percentage), 2),
            "similarity_percentage": round(float(self.similarity_percentage), 2),
            "num_difference_regions": int(self.num_difference_regions),
            "difference_regions": self.difference_regions,
        }


@dataclass
class DiffStats:
    """Overall statistics for PDF comparison"""
    pdf1_path: str
    pdf2_path: str
    pdf1_pages: int
    pdf2_pages: int
    pages_compared: int
    identical_pages: int
    different_pages: int
    overall_similarity: float
    page_stats: List[PageStats] = field(default_factory=list)

    @property
    def are_identical(self) -> bool:
        """Check if PDFs are completely identical"""
        return (
            self.pdf1_pages == self.pdf2_pages and
            self.different_pages == 0
        )

    def add_page_stats(self, page_stats: PageStats):
        """Add statistics for a page"""
        self.page_stats.append(page_stats)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "pdf1_path": str(self.pdf1_path),
            "pdf2_path": str(self.pdf2_path),
            "pdf1_pages": int(self.pdf1_pages),
            "pdf2_pages": int(self.pdf2_pages),
            "pages_compared": int(self.pages_compared),
            "identical_pages": int(self.identical_pages),
            "different_pages": int(self.different_pages),
            "overall_similarity": round(float(self.overall_similarity), 2),
            "are_identical": bool(self.are_identical),
            "page_stats": [ps.to_dict() for ps in self.page_stats],
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)

    def get_summary(self) -> str:
        """Get a human-readable summary"""
        lines = []
        lines.append(f"PDF Comparison Summary")
        lines.append(f"=" * 50)
        lines.append(f"PDF 1: {self.pdf1_path} ({self.pdf1_pages} pages)")
        lines.append(f"PDF 2: {self.pdf2_path} ({self.pdf2_pages} pages)")
        lines.append(f"")
        lines.append(f"Result: {'IDENTICAL' if self.are_identical else 'DIFFERENT'}")
        lines.append(f"")
        lines.append(f"Overall Similarity: {self.overall_similarity:.2f}%")
        lines.append(f"Pages Compared: {self.pages_compared}")
        lines.append(f"Identical Pages: {self.identical_pages}")
        lines.append(f"Different Pages: {self.different_pages}")

        if self.page_stats:
            lines.append(f"")
            lines.append(f"Per-Page Details:")
            lines.append(f"-" * 50)

            for ps in self.page_stats:
                status = "IDENTICAL" if ps.is_identical else "DIFFERENT"
                lines.append(f"  Page {ps.page_number + 1}: {status}")

                if not ps.is_identical:
                    lines.append(f"    Similarity: {ps.similarity_percentage:.2f}%")
                    lines.append(f"    Different Pixels: {ps.different_pixels:,} / {ps.total_pixels:,}")
                    lines.append(f"    Difference Regions: {ps.num_difference_regions}")

        return "\n".join(lines)

    def get_different_pages(self) -> List[int]:
        """Get list of page numbers that are different (0-indexed)"""
        return [ps.page_number for ps in self.page_stats if not ps.is_identical]

    def get_page_stats(self, page_number: int) -> PageStats:
        """Get statistics for a specific page (0-indexed)"""
        for ps in self.page_stats:
            if ps.page_number == page_number:
                return ps
        raise ValueError(f"No statistics found for page {page_number}")


class StatsCalculator:
    """Helper class to calculate comparison statistics"""

    @staticmethod
    def calculate_page_stats(
        page_number: int,
        is_identical: bool,
        total_pixels: int,
        different_pixels: int,
        difference_regions: List[Any]
    ) -> PageStats:
        """
        Calculate statistics for a single page

        Args:
            page_number: Page number (0-indexed)
            is_identical: Whether the page is identical
            total_pixels: Total number of pixels
            different_pixels: Number of different pixels
            difference_regions: List of difference regions (BoundingBox objects)

        Returns:
            PageStats object
        """
        if total_pixels == 0:
            difference_percentage = 0.0
            similarity_percentage = 100.0
        else:
            difference_percentage = (different_pixels / total_pixels) * 100
            similarity_percentage = 100.0 - difference_percentage

        # Convert regions to dict format
        regions_dict = []
        for region in difference_regions:
            regions_dict.append({
                "x": region.x1,
                "y": region.y1,
                "width": region.width,
                "height": region.height,
                "area": region.area,
            })

        return PageStats(
            page_number=page_number,
            is_identical=is_identical,
            total_pixels=total_pixels,
            different_pixels=different_pixels,
            difference_percentage=difference_percentage,
            similarity_percentage=similarity_percentage,
            num_difference_regions=len(difference_regions),
            difference_regions=regions_dict,
        )

    @staticmethod
    def calculate_overall_stats(
        pdf1_path: str,
        pdf2_path: str,
        pdf1_pages: int,
        pdf2_pages: int,
        page_stats_list: List[PageStats]
    ) -> DiffStats:
        """
        Calculate overall statistics from individual page statistics

        Args:
            pdf1_path: Path to first PDF
            pdf2_path: Path to second PDF
            pdf1_pages: Number of pages in first PDF
            pdf2_pages: Number of pages in second PDF
            page_stats_list: List of PageStats for compared pages

        Returns:
            DiffStats object
        """
        pages_compared = len(page_stats_list)
        identical_pages = sum(1 for ps in page_stats_list if ps.is_identical)
        different_pages = pages_compared - identical_pages

        # Calculate overall similarity as weighted average
        if page_stats_list:
            total_similarity = sum(ps.similarity_percentage for ps in page_stats_list)
            overall_similarity = total_similarity / pages_compared
        else:
            overall_similarity = 0.0

        stats = DiffStats(
            pdf1_path=pdf1_path,
            pdf2_path=pdf2_path,
            pdf1_pages=pdf1_pages,
            pdf2_pages=pdf2_pages,
            pages_compared=pages_compared,
            identical_pages=identical_pages,
            different_pages=different_pages,
            overall_similarity=overall_similarity,
            page_stats=page_stats_list,
        )

        return stats
