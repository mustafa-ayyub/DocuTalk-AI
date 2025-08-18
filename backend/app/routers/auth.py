from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from src.firebase_utils.auth_utils import authenticate_user, register_user
from src.firebase_utils.db_utils import get_user_data


router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user_id: str
    email: EmailStr


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    result = authenticate_user(payload.email, payload.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"]) 
    user = result["user"]

    user_id = user.get("localId") or user.get("uid")
    if not user_id:
        raise HTTPException(status_code=500, detail="Missing user id from auth provider")

    data = get_user_data(user_id) or {}
    return LoginResponse(user_id=user_id, email=payload.email)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register", response_model=LoginResponse)
def register(payload: RegisterRequest):
    result = register_user(payload.email, payload.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"]) 
    user = result["user"]
    user_id = user.get("localId") or user.get("uid")
    return LoginResponse(user_id=user_id, email=payload.email)

