import pdfplumber
from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_simple(file_path):
    """Basic text extraction using pypdf."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        print(f"Simple extraction error: {e}")
        return ""

def extract_tables(file_path):
    """Extracts tables from PDF and converts them to a readable string format."""
    tables_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for j, table in enumerate(tables):
                    tables_text += f"\n[Table {i+1}:{j+1}]\n"
                    for row in table:
                        # Filter out None values and join with tabs
                        row_str = "\t".join([str(cell) if cell is not None else "" for cell in row])
                        tables_text += row_str + "\n"
    except Exception as e:
        print(f"Table extraction error: {e}")
    return tables_text

def extract_text_ocr(file_path):
    """Performs OCR on PDF pages using pytesseract and pdf2image."""
    ocr_text = ""
    try:
        # Convert PDF pages to images
        # Note: poppler must be installed on the system for this to work
        images = convert_from_path(file_path)
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            ocr_text += f"\n--- Page {i+1} OCR ---\n" + text + "\n"
    except Exception as e:
        print(f"OCR extraction error: {e}")
        print("Hint: Ensure Tesseract-OCR and Poppler are installed and in your system PATH.")
    return ocr_text

def extract_text_from_pdf(file_path, mode="hybrid"):
    """
    Advanced PDF extraction engine.
    Modes:
    - 'simple': Just text.
    - 'ocr': Force OCR on all pages.
    - 'hybrid': Try text first; if too short or tables found, supplement with tables and OCR.
    """
    if mode == "simple":
        return extract_text_simple(file_path)

    if mode == "ocr":
        return extract_text_ocr(file_path)

    # Hybrid Mode (Default)
    print("Performing hybrid extraction (Text + Tables + OCR fallback)...")

    # 1. Get basic text
    text = extract_text_simple(file_path)

    # 2. Get tables to preserve structure
    tables = extract_tables(file_path)

    # 3. Check if text is too sparse (indicates scanned PDF)
    if len(text.strip()) < 100:
        print("Document appears to be scanned. Triggering OCR...")
        ocr_text = extract_text_ocr(file_path)
        return ocr_text if ocr_text else text

    # Combine text and tables
    return f"{text}\n\n--- Extracted Tables ---\n{tables}"
