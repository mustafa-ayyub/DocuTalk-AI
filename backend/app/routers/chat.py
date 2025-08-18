from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.conversation_chain import answer_user_question
from src.services.embeddings import initialize_pinecone, get_pinecone_index, initialize_embeddings
from langchain_pinecone import PineconeVectorStore


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    user_id: str
    question: str
    chat_context: str = ""


class ChatResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=ChatResponse)
def ask(req: ChatRequest):
    try:
        pc = initialize_pinecone()
        index = get_pinecone_index(pc, req.user_id.lower())
        embeddings = initialize_embeddings()
        vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
        answer = answer_user_question(req.question, vectorstore, req.chat_context)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

