"""
Module to create and manage FAISS vectorstores using OpenAI embeddings.
"""

import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
Hugging_face_api_key=os.getenv("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")




def get_vectorstore(text_chunks, use_huggingface=True):
    """
    Creates a Chroma vectorstore from text chunks, using either OpenAI or Hugging Face embeddings.

    Args:
        text_chunks (list[str]): List of text chunks to embed.
        use_huggingface (bool): If True, use Hugging Face embeddings. Otherwise, use OpenAI.

    Returns:
        vectorstore (Chroma): The created Chroma vectorstore.
    """

    if use_huggingface:
        # Example: using the MiniLM-L6-v2 model from sentence-transformers
        embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
        print("Using Hugging Face Embeddings...")
    else:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        print("No Api KEy...")

    # Chroma can be in-memory (default) or you can specify a persist_directory
    # vectorstore = Chroma.from_texts(text_chunks, embeddings)
    # print("Chroma Vectorstore created:", vectorstore)

    # return vectorstore
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    print("Vectorstore is: ", vectorstore)
    return vectorstore

# def get_vectorstore(text_chunks):
#     """
#     Creates a FAISS vectorstore from text chunks.

#     Args:
#         text_chunks (list): List of text chunks to embed.

#     Returns:
#         vectorstore (FAISS): The created FAISS vectorstore.
#     """
#     embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    
#     # Currently, we are using FAISS, but in the future, we can consider using alternatives
#     # such as Pinecone or Weaviate if the dataset grows larger
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     print("Vectorstore is: ", vectorstore)
#     return vectorstore
