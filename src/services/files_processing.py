"""
Module for extracting text from PDF, DOCX, and TXT files.

Functions:
- extract_pdf_text: Extracts text from a PDF file.
- extract_docx_text: Extracts text from a DOCX file.
- extract_txt_text: Extracts text from a TXT file.
- process_files: Processes multiple files and combines their extracted text.
"""

from PyPDF2 import PdfReader
from docx import Document

def extract_pdf_text(file):
    """Extract text from a PDF file."""
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""  # Handle None return from extract_text
    return text

def extract_docx_text(file):
    """Extract text from a DOCX file."""
    text = ""
    doc = Document(file)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_txt_text(file):
    """Extract text from a TXT file."""
    return file.read().decode("utf-8")

def process_files(files):
    """Process files and return the combined extracted text."""
    all_text = ""
    for file in files:
        if file.name.endswith(".pdf"):
            all_text += extract_pdf_text(file)
        elif file.name.endswith(".docx"):
            all_text += extract_docx_text(file)
        elif file.name.endswith(".txt"):
            all_text += extract_txt_text(file)
        else:
            raise ValueError(f"Unsupported file type: {file.name}")
    return all_text
