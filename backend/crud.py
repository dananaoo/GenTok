from sqlalchemy.orm import Session
import models, schemas

def get_videos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Video).offset(skip).limit(limit).all()

def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def delete_video(db: Session, video_id: int):
    db_video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if db_video:
        db.delete(db_video)
        db.commit()
        return {"ok": True}
    return {"error": "Not found"}

def update_video(db: Session, video_id: int, video: schemas.VideoCreate):
    db_video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if db_video:
        db_video.title = video.title
        db_video.description = video.description
        db_video.url = video.url
        db.commit()
        db.refresh(db_video)
        return db_video
    raise HTTPException(status_code=404, detail="Video not found")

