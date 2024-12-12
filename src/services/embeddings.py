"""
Module to create and manage FAISS vectorstores using OpenAI embeddings.
"""

import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_vectorstore(text_chunks):
    """
    Creates a FAISS vectorstore from text chunks.

    Args:
        text_chunks (list): List of text chunks to embed.

    Returns:
        vectorstore (FAISS): The created FAISS vectorstore.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # Currently, we are using FAISS, but in the future, we can consider using alternatives
    # such as Pinecone or Weaviate if the dataset grows larger
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    print("Vectorstore is: ", vectorstore)
    return vectorstore
