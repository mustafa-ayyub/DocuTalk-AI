from typing import List, Dict
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from src.services.files_processing import process_files
from src.services.text_processing import get_text_chunks
from src.services.embeddings import get_user_vectorstore


router = APIRouter(prefix="/files", tags=["files"])


class ProcessResponse(BaseModel):
    chunks: int


@router.post("/process", response_model=ProcessResponse)
async def process(
    user_id: str = Form(...),
    files: List[UploadFile] = File(...),
    metadata_json: str = Form("{}"),
):
    try:
        # NOTE: Streamlit uploaded file API differs from FastAPI's UploadFile
        # process_files expects file-like objects with .name and .read()
        # FastAPI UploadFile has .filename and .file
        wrapped_files = []
        for f in files:
            class FWrap:
                def __init__(self, uf):
                    self.uf = uf
                    self.name = uf.filename
                def read(self):
                    return self.uf.file.read()
            wrapped_files.append(FWrap(f))

        import json
        document_metadata: Dict[str, str] = json.loads(metadata_json)

        extracted = process_files(wrapped_files, document_metadata)
        chunks = get_text_chunks(extracted)
        _ = get_user_vectorstore(chunks, user_id)
        return ProcessResponse(chunks=len(chunks))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

