from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import crud, schemas

router = APIRouter(prefix="/chatbot", tags=["chatbot"])
chatbot_service = crud.ChatbotService()

@router.post("/chat", response_model=schemas.ChatMessageResponse)
async def create_chat(
    chat_message: schemas.ChatMessageCreate,
    db: Session = Depends(get_db)
):
    return await crud.create_chat_message(db, chat_message.user_id, chat_message, chatbot_service)

@router.get("/history/{user_id}", response_model=List[schemas.ChatMessageResponse])
def get_chat_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    messages = crud.get_user_chat_history(db, user_id, skip=skip, limit=limit)
    return messages 