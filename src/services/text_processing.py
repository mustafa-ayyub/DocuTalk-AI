"""
Utilities for text processing.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_text_chunks(text: str) -> list[str]:
    """
    Splits text into chunks.

    Args:
        text (str): Input text.

    Returns:
        list[str]: Text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n", " ", ""], chunk_size=1000, chunk_overlap=150, length_function=len
    )
    return text_splitter.split_text(text)
