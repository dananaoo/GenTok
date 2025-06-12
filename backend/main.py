from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
import os
import redis
from assistant.client import GeminiAssistant
from dotenv import load_dotenv
from chatbot.router import router as chatbot_router

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # для vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chatbot router
app.include_router(chatbot_router)

load_dotenv()

assistant = GeminiAssistant()

@app.post("/chat/")
def chat(prompt: schemas.Prompt):
    response = assistant.generate(prompt.message)
    return {"response": response}

# --- Redis инициализация ---
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, db=0)

# Пример: проверка соединения
try:
    r.set("startup_check", "OK")
    print("✅ Redis connected:", r.get("startup_check"))
except Exception as e:
    print("❌ Redis connection failed:", e)

# Dependency для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoints
@app.post("/videos/", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)

@app.get("/videos/", response_model=list[schemas.Video])
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_videos(db=db, skip=skip, limit=limit)

@app.get("/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.delete("/videos/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: int, db: Session = Depends(get_db)):
    video = crud.get_video(db, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    db.delete(video)
    db.commit()
    return

@app.put("/videos/{video_id}", response_model=schemas.Video)
def update_video(video_id: int, updated_data: schemas.VideoCreate, db: Session = Depends(get_db)):
    video = crud.get_video(db, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    video.title = updated_data.title
    video.description = updated_data.description
    video.url = updated_data.url
    db.commit()
    db.refresh(video)
    return video
