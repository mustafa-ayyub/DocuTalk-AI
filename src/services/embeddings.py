"""
Module to create and manage FAISS vectorstores using sentence transformers.
"""

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def get_vectorstore(text_chunks):
    """
    Vectorstore.

    Args:
        text_chunks (List[str]): Chunks

    Returns:
        FAISS: Store
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    print("Vectorstore is: ", vectorstore)
    return vectorstore
