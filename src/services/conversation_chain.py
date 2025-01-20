import os
from openai import OpenAI
from .context import get_assistant_role, get_mixed_categories_role

BASE_URL_OF_NVIDA = "https://integrate.api.nvidia.com/v1"

def initialize_nvidia_client():
    """
    Initialize NVIDIA client with API key and base URL.
    """
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("API key for NVIDIA is not provided.")
    return OpenAI(
        base_url=BASE_URL_OF_NVIDA,
        api_key=api_key
    )

def generate_answer(prompt, client, model="nvidia/llama-3.1-nemotron-70b-instruct", max_tokens=500, temperature=0.5):
    """
    Generate an answer using NVIDIA model.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=1,
        stream=True
    )

    answer = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            answer += chunk.choices[0].delta.content

    return answer

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
    print("Length of categories is: ", len(set(categories)))

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
    Answer a question using vectorstore and NVIDIA's OpenAI integration.
    """
    client = initialize_nvidia_client()

    context, categories = prepare_context(user_question, vectorstore)
    if not context:
        return "No relevant information found in your uploaded documents."

    prompt = generate_prompt(context, user_question, chat_context, categories)
    return generate_answer(prompt, client)

