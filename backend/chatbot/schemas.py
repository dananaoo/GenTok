from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatMessageBase(BaseModel):
    message: str
    user_id: int

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    response: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 