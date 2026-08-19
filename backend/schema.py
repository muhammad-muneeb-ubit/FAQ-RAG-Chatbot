from pydantic import BaseModel

class Chat_Create(BaseModel):
    title: str
        
class Message_Create(BaseModel):

    chat_id: int
    role: str
    content: str