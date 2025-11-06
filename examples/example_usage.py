"""
Example usage of pdf-compare as a Python library
"""

from pdf_compare import PDFComparator

# Example 1: Simple comparison
print("Example 1: Simple comparison")
print("-" * 50)

comparator = PDFComparator(dpi=150, threshold=0)
are_identical = comparator.compare_simple("document1.pdf", "document2.pdf")

if are_identical:
    print("PDFs are identical!")
else:
    print("PDFs are different!")

print()

# Example 2: Detailed comparison with statistics
print("Example 2: Detailed comparison with statistics")
print("-" * 50)

comparator = PDFComparator(dpi=150, threshold=0)
stats = comparator.compare("document1.pdf", "document2.pdf")

print(f"Overall Similarity: {stats.overall_similarity:.2f}%")
print(f"Pages Compared: {stats.pages_compared}")
print(f"Identical Pages: {stats.identical_pages}")
print(f"Different Pages: {stats.different_pages}")

# Print per-page details
for page_stat in stats.page_stats:
    if not page_stat.is_identical:
        print(f"\nPage {page_stat.page_number + 1}:")
        print(f"  Similarity: {page_stat.similarity_percentage:.2f}%")
        print(f"  Different Pixels: {page_stat.different_pixels:,}")
        print(f"  Difference Regions: {page_stat.num_difference_regions}")

print()

# Example 3: Generate multiple output formats
print("Example 3: Generate multiple output formats")
print("-" * 50)

comparator = PDFComparator(dpi=150, threshold=0)
stats = comparator.compare("document1.pdf", "document2.pdf")

# Save reports in different formats
comparator.save_diff_pdf("output/diff_report.pdf")
comparator.save_json_report("output/stats.json")
comparator.save_html_report("output/report.html")
comparator.save_diff_images("output/images/")

print("Reports saved:")
print("  - PDF: output/diff_report.pdf")
print("  - JSON: output/stats.json")
print("  - HTML: output/report.html")
print("  - Images: output/images/")

print()

# Example 4: High-resolution comparison with tolerance
print("Example 4: High-resolution comparison with tolerance")
print("-" * 50)

# Higher DPI for better quality, threshold to ignore minor rendering differences
comparator = PDFComparator(dpi=300, threshold=10)
stats = comparator.compare("document1.pdf", "document2.pdf")

print(f"Overall Similarity: {stats.overall_similarity:.2f}%")
print(f"Using DPI: 300")
print(f"Using Threshold: 10")

print()

# Example 5: Custom progress callback
print("Example 5: Custom progress callback")
print("-" * 50)

def progress_callback(current, total):
    """Custom progress callback"""
    percent = (current / total) * 100
    print(f"Progress: {current}/{total} pages ({percent:.1f}%)")

comparator = PDFComparator(dpi=150, threshold=0, progress_callback=progress_callback)
stats = comparator.compare("document1.pdf", "document2.pdf")

print(f"\nComparison complete! Similarity: {stats.overall_similarity:.2f}%")

print()

# Example 6: Access individual components
print("Example 6: Access individual components")
print("-" * 50)

from pdf_compare import PDFRenderer, PDFDiffer

# Render PDF pages
renderer = PDFRenderer(dpi=150)
img1 = renderer.render_page("document1.pdf", 0)  # First page
img2 = renderer.render_page("document2.pdf", 0)

print(f"Page 1 rendered: {img1.size}")
print(f"Page 2 rendered: {img2.size}")

# Compare images
differ = PDFDiffer(threshold=0)
are_identical, diff_img, diff_pixels = differ.compare_images(img1, img2)

print(f"Images identical: {are_identical}")
print(f"Different pixels: {diff_pixels:,}")

# Find difference regions
regions = differ.find_difference_regions(img1, img2)
print(f"Difference regions found: {len(regions)}")

for i, region in enumerate(regions[:5]):  # Show first 5 regions
    print(f"  Region {i+1}: x={region.x1}, y={region.y1}, w={region.width}, h={region.height}")

# Calculate similarity percentage
similarity = differ.calculate_similarity_percentage(img1, img2)
print(f"Similarity: {similarity:.2f}%")

print()

# Example 7: Batch processing
print("Example 7: Batch processing multiple PDFs")
print("-" * 50)

import os
from pathlib import Path

reference_pdf = "reference.pdf"
test_pdfs = [
    "test1.pdf",
    "test2.pdf",
    "test3.pdf",
]

results = []

for test_pdf in test_pdfs:
    if os.path.exists(test_pdf):
        comparator = PDFComparator(dpi=150, threshold=5)
        stats = comparator.compare(reference_pdf, test_pdf)

        results.append({
            "file": test_pdf,
            "similarity": stats.overall_similarity,
            "identical": stats.are_identical,
            "different_pages": stats.different_pages,
        })

        print(f"Compared {test_pdf}:")
        print(f"  Similarity: {stats.overall_similarity:.2f}%")
        print(f"  Different pages: {stats.different_pages}")

# Save batch results as JSON
import json
with open("output/batch_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nBatch results saved to output/batch_results.json")

print()

# Example 8: Error handling
print("Example 8: Error handling")
print("-" * 50)

try:
    comparator = PDFComparator()
    stats = comparator.compare("nonexistent1.pdf", "nonexistent2.pdf")
except FileNotFoundError as e:
    print(f"Error: {e}")

try:
    comparator = PDFComparator()
    stats = comparator.compare("document1.pdf", "document2.pdf")
    # Try to save without comparing first
    comparator2 = PDFComparator()
    comparator2.save_diff_pdf("output/error.pdf")
except RuntimeError as e:
    print(f"Error: {e}")

print()
print("All examples completed!")
