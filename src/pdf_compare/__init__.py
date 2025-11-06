"""
pdf-compare: Modern CLI tool for comparing PDF files
"""

__version__ = "1.0.0"
__author__ = "ADR3N4LYN3"
__license__ = "MIT"

from .comparator import PDFComparator
from .differ import PDFDiffer
from .renderer import PDFRenderer
from .reporter import Reporter
from .stats import DiffStats

__all__ = [
    "PDFComparator",
    "PDFDiffer",
    "PDFRenderer",
    "Reporter",
    "DiffStats",
]
