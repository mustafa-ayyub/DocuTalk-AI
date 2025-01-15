
"""
Utilities for text processing.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_text_splitter():
    """Create a configured RecursiveCharacterTextSplitter instance."""
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""], chunk_size=1000, chunk_overlap=150, length_function=len
    )

def split_text_with_metadata(data, text_splitter):
    """Split text into chunks and attach metadata to each chunk."""
    chunks = text_splitter.split_text(data["text"])
    return [
        {
            "chunk": chunk,
            "page_num": data.get("page_num"),
            "file_name": data["file_name"],
            "doc_type": data["doc_type"],
            "category": data["category"]
        }
        for chunk in chunks
    ]

def get_text_chunks(extracted_data: list[dict]) -> list[dict]:
    """
    Splits text into chunks while retaining metadata.

    Args:
        extracted_data (list[dict]): List of extracted text with metadata.

    Returns:
        list[dict]: List of text chunks with metadata.
    """
    text_splitter = create_text_splitter()
    all_chunks = []
    for data in extracted_data:
        all_chunks.extend(split_text_with_metadata(data, text_splitter))
    return all_chunks
