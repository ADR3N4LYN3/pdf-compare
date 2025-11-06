"""
Script to create test PDFs for testing pdf-compare
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, red, blue

def create_test_pdf1(filename):
    """Create first test PDF"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Page 1
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Document 1")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This is the first test PDF.")
    c.drawString(100, height - 170, "It contains some text and shapes.")

    # Draw a rectangle
    c.setStrokeColor(black)
    c.setFillColor(blue)
    c.rect(100, 300, 200, 100, fill=1)

    c.showPage()

    # Page 2
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, "Page 2")
    c.drawString(100, height - 150, "This is the second page.")

    c.showPage()
    c.save()
    print(f"Created {filename}")

def create_test_pdf2(filename):
    """Create second test PDF (slightly different)"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Page 1
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Document 2")  # Different text

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This is the second test PDF.")  # Different
    c.drawString(100, height - 170, "It contains some text and shapes.")

    # Draw a rectangle (different position)
    c.setStrokeColor(black)
    c.setFillColor(red)  # Different color
    c.rect(150, 300, 200, 100, fill=1)  # Different position

    c.showPage()

    # Page 2
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, "Page 2")
    c.drawString(100, height - 150, "This is the second page.")

    c.showPage()
    c.save()
    print(f"Created {filename}")

def create_identical_pdf(filename):
    """Create a PDF identical to test_pdf1"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Page 1
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, height - 100, "Test Document 1")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, "This is the first test PDF.")
    c.drawString(100, height - 170, "It contains some text and shapes.")

    # Draw a rectangle
    c.setStrokeColor(black)
    c.setFillColor(blue)
    c.rect(100, 300, 200, 100, fill=1)

    c.showPage()

    # Page 2
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 100, "Page 2")
    c.drawString(100, height - 150, "This is the second page.")

    c.showPage()
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_pdf1("test_pdf1.pdf")
    create_test_pdf2("test_pdf2.pdf")
    create_identical_pdf("test_pdf1_copy.pdf")
    print("\nAll test PDFs created successfully!")
