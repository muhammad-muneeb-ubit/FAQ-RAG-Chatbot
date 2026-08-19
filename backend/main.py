from fastapi import FastAPI # type: ignore
from backend.crud import chats, create_message, test_database, get_messages, create_chat
from backend.schema import Chat_Create, Message_Create
from backend.rag import ask_question
from backend.chat_history import get_chat_history
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FAQ RAG Chatbot API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {
        "message": "FAQ RAG API is running"
    }

@app.post("/test-rag")
def test_rag(question: str):
    print("Testing RAG with question:", question)

    response, docs = ask_question(question)

    return {
        "question": question,
        "answer": response,
        "retrieved_documents": [
            {
                "question": doc.metadata.get("question"),
                "answer": doc.metadata.get("answer")
            }
            for doc in docs
        ]
    }
    
@app.get("/test-database")
def health():
    return test_database()
    
@app.get("/chats")
def get_chats():
    return chats()
    
@app.post("/chats/{chat_id}/messages")
def create_new_message(message: Message_Create):
    return create_message(message.chat_id, message.role, message.content)
    
@app.get("/chats/{chat_id}/messages")
def chat_history(chat_id: int):
    return get_chat_history(chat_id)


@app.post("/chats")
def create_new_chat(chat: Chat_Create):
    return create_chat(chat.title)

@app.post("/chats/{chat_id}/ask")
def ask_chatbot(chat_id: int, message: Message_Create):

    create_message(
        chat_id,
        "user",
        message.content
    )
    history = get_messages(chat_id)
  
    chat_history = history["messages"]

    response, docs = ask_question(
        message.content,
        chat_history=chat_history
    )
    create_message(
        chat_id,
        "assistant",
        response
    )

    return {
        "chat_id": chat_id,
        "question": message.content,
        "answer": response,
        "retrieved_documents": docs
    }