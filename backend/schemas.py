from pydantic import BaseModel

# Для получения данных при создании/обновлении видео
class VideoCreate(BaseModel):
    title: str
    description: str
    url: str

# Для ответа с ID
class Video(VideoCreate):
    id: int

    class Config:
        orm_mode = True

# Для Gemini
class Prompt(BaseModel):
    message: str
