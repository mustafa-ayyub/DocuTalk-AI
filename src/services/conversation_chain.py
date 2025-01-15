"""
Module for answering questions using OpenAI GPT and vectorstore context.
"""

import os
from openai import OpenAI
from .context import get_assistant_role, get_mixed_categories_role

def initialize_openai_client():
    """
    Initialize OpenAI client with API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key for OpenAI is not provided.")
    return OpenAI(api_key=api_key)

def generate_answer(prompt, client, model="gpt-3.5-turbo", max_tokens=500, temperature=0.1):
    """
    Generate an answer using OpenAI.
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content

def prepare_context(user_question, vectorstore, top_k=3):
    """
    Fetch relevant context from the vectorstore.
    """
    if not user_question.strip():
        raise ValueError("User question cannot be empty.")

    results = vectorstore.similarity_search(query=user_question, k=top_k)
    print("Results are: ", results)

    if not results:
        return ""
    context_with_metadata = []
    categories = []
    for doc in results:
        metadata = doc.metadata
        file_name = metadata.get("file_name", "Unknown file")
        page_num = metadata.get("page_num", "Unknown page")
        category = metadata.get("category", "Uncategorized")
        categories.append(category)
        context_with_metadata.append(
            f"Document: {file_name}, Page: {page_num}, Category: {category}\nContent: {doc.page_content}"
        )
    print("categories are: ", categories)
    return "\n\n".join(context_with_metadata), categories

def generate_prompt(context, question, chat_context, categories):
    """
    Create a highly specific prompt using context, chat history, and the current question.
    Tailor the assistant's behavior for each category and ensure references are included.
    """
    if not context.strip():
        return "No relevant content found to answer your question."
    print("Lenth of categories is: ", len(set(categories)))

    if len(set(categories)) == 1:
        category = categories[0]
        print("Single category detected: ", category)
        assistant_role = get_assistant_role(category)
    else:
        print("Mixed categories detected.")
        assistant_role = get_mixed_categories_role()
        
    prompt = (
        f"{assistant_role}\n\n"
        f"Here is the ongoing conversation for context:\n{chat_context}\n\n"
        f"Below is the extracted context from the documents relevant to your query:\n{context}\n\n"
        f"Using the information above, answer the following question:\n\n"
        f"User's Question:\n{question}\n\n"
        f"Be specific, provide examples where necessary, and include references (e.g., 'Reference: Document_Name, Page X') at the end of your answer."
    )
    return prompt


def answer_user_question(user_question, vectorstore, chat_context):
    """
    Answer a question using vectorstore and OpenAI.
    """
    client = initialize_openai_client()
    
    context, categories = prepare_context(user_question, vectorstore)
    if not context:
        return "No relevant information found in your uploaded documents."
    

    prompt = generate_prompt(context, user_question, chat_context, categories)
    return generate_answer(prompt, client)





















# from langchain.chains import ConversationalRetrievalChain
# from langchain_community.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# import os


# def get_conversation_chain(vectorstore):
#     """
#     Create a ConversationalRetrievalChain with memory and explicit output key.

#     Args:
#         vectorstore: The vectorstore retriever object.

#     Returns:
#         ConversationalRetrievalChain: A chain that supports conversational QA.
#     """
#     llm = ChatOpenAI(
#         temperature=0,
#         model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" or "gpt-4"
#         openai_api_key=os.getenv("OPENAI_API_KEY")
#     )
    
#     # Explicitly configure memory
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",  # Store chat history in this key
#         input_key="question",      # Specify the input key for memory
#         output_key="answer",       # Ensure memory stores only the 'answer' key
#         return_messages=True       # Ensures the memory returns in message format
#     )
    
#     # Create the conversational retrieval chain
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory,
#         return_source_documents=True,
#         output_key="answer"  # Explicitly set the key to use in memory
#     )
    
#     return conversation_chain






# from langchain_openai import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# import os

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2,model="gpt-3.5-turbo")
#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever( search_type="similarity",  search_kwargs={"k": 3}),
#         memory=memory
#     )
#     return conversation_chain
