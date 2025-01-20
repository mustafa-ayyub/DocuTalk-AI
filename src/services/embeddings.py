"""
Module to create and manage Pinecone vectorstores using HuggingFace embeddings.
"""

import os
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

def initialize_pinecone():
    """Initialize the Pinecone client."""
    return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def create_index_if_not_exists(pc, index_name):
    """Create a Pinecone index if it doesn't exist."""
    if index_name not in [index.name for index in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

def get_pinecone_index(pc, index_name):
    """Retrieve a Pinecone index."""
    return pc.Index(index_name)

def initialize_embeddings():
    """Initialize HuggingFace embeddings."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def prepare_documents(text_chunks):
    """Convert text chunks into Document objects."""
    return [
        Document(
            page_content=chunk["chunk"],
            metadata={
                "file_name": chunk["file_name"],
                "page_num": chunk.get("page_num"),
                "doc_type": chunk["doc_type"],
                "category": chunk["category"],
            },
        )
        for chunk in text_chunks
    ]

def get_user_vectorstore(text_chunks, user_id):
    """Create a user-specific Pinecone vectorstore."""
    index_name = f"{user_id.lower()}"

    pc = initialize_pinecone()

    create_index_if_not_exists(pc, index_name)

    index = get_pinecone_index(pc, index_name)

    embeddings = initialize_embeddings()

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    if text_chunks:
        documents = prepare_documents(text_chunks)
        vector_store.add_documents(documents=documents)

    return vector_store
