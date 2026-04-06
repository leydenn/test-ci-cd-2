from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db, Base
from .models import Message
from pydantic import BaseModel
from datetime import datetime

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My WebApp API")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageCreate(BaseModel):
    username: str
    content: str

class MessageResponse(BaseModel):
    id: int
    username: str
    content: str
    created_at: datetime

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/messages", response_model=list[MessageResponse])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).order_by(Message.created_at.desc()).limit(50).all()
    return messages

@app.post("/messages", response_model=MessageResponse)
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    db_msg = Message(username=msg.username, content=msg.content)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg