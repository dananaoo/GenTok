from sqlalchemy.orm import Session
from . import models, schemas
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

class ChatbotService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("WARNING: GEMINI_API_KEY not found in environment variables!")
        else:
            print("GEMINI_API_KEY found in environment")
        
        genai.configure(api_key=api_key)
        # Using a more basic model
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
        
    async def get_chat_response(self, message: str) -> str:
        try:
            print(f"Sending message to Gemini: {message}")
            # Add retry logic with delay
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(message)
                    print(f"Received response from Gemini: {response.text}")
                    return response.text
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)  # Progressive delay: 5s, 10s, 15s
                        print(f"Rate limit hit, waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    raise e
        except Exception as e:
            print(f"Error in get_chat_response: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

async def create_chat_message(
    db: Session, 
    user_id: int, 
    chat_message: schemas.ChatMessageCreate,
    chatbot: ChatbotService
) -> models.ChatMessage:
    print(f"Creating chat message for user {user_id}")
    response = await chatbot.get_chat_response(chat_message.message)
    db_message = models.ChatMessage(
        user_id=user_id,
        message=chat_message.message,
        response=response
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_chat_history(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> list[models.ChatMessage]:
    return db.query(models.ChatMessage)\
        .filter(models.ChatMessage.user_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all() 