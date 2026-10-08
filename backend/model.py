from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    

class TransliterationRequest(BaseModel):
    text: str