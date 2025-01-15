
"""
Module for extracting text from PDF, DOCX, and TXT files.
"""

from PyPDF2 import PdfReader
from docx import Document

def _extract_single_pdf_page(page, page_num):
    """Extract text from a single PDF page."""
    text = page.extract_text() or ""
    return {"page_num": page_num + 1, "text": text}

def extract_pdf_text(file):
    """Extract text from a PDF file along with page numbers."""
    pdf_reader = PdfReader(file)
    return [_extract_single_pdf_page(page, page_num) for page_num, page in enumerate(pdf_reader.pages)]

def _extract_docx_paragraphs(doc):
    """Extract text from paragraphs in a DOCX file."""
    return [paragraph.text for paragraph in doc.paragraphs]

def extract_docx_text(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    paragraphs = _extract_docx_paragraphs(doc)
    return "\n".join(paragraphs)

def extract_txt_text(file):
    """Extract text from a TXT file."""
    return file.read().decode("utf-8")

def _attach_metadata(extracted_text, file_name, doc_type, category, page_num=None):
    """Attach metadata to extracted text."""
    return {
        "text": extracted_text,
        "page_num": page_num,
        "file_name": file_name,
        "doc_type": doc_type,
        "category": category,
    }

def _process_pdf_file(file, category):
    """Process a PDF file and return metadata-enhanced text."""
    pdf_data = extract_pdf_text(file)
    return [
        _attach_metadata(page["text"], file.name, "PDF", category, page["page_num"])
        for page in pdf_data
    ]

def _process_docx_file(file, category):
    """Process a DOCX file and return metadata-enhanced text."""
    doc_text = extract_docx_text(file)
    return [_attach_metadata(doc_text, file.name, "DOCX", category)]

def _process_txt_file(file, category):
    """Process a TXT file and return metadata-enhanced text."""
    txt_text = extract_txt_text(file)
    return [_attach_metadata(txt_text, file.name, "TXT", category)]

def process_files(files, document_metadata):
    """Process multiple files and combine their extracted text with metadata."""
    all_extracted_data = []
    for file in files:
        category = document_metadata.get(file.name, "Uncategorized")
        if file.name.endswith(".pdf"):
            all_extracted_data.extend(_process_pdf_file(file, category))
        elif file.name.endswith(".docx"):
            all_extracted_data.extend(_process_docx_file(file, category))
        elif file.name.endswith(".txt"):
            all_extracted_data.extend(_process_txt_file(file, category))
        else:
            raise ValueError(f"Unsupported file type: {file.name}")
    return all_extracted_data
