from backend.model import TransliterationRequest
from fastapi import FastAPI # type: ignore
from backend.config import llm, rewrite_llm
from backend.crud import chats, clean_text_for_tts, contains_urdu_script, create_message, test_database, get_messages, create_chat, transliterate_to_roman_urdu
from backend.schema import Chat_Create, Message_Create
from backend.rag import ask_question, ask_question_stream
from backend.chat_history import get_chat_history
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from backend.rag import rewrite_query 
from backend.log import logger
import time
from fastapi.responses import StreamingResponse # type: ignore

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
    logger.info("Root endpoint accessed")
    return {
        "message": "FAQ RAG API is running"
    }

@app.post("/test-rag")
def test_rag(question: str):
    start = time.perf_counter()
    # print("\nTesting RAG with question:", question)
    logger.info("call to test_rag")
    response, docs, reranked_docs = ask_question(question, [])
    elapsed = time.perf_counter() - start
    logger.info(f"RAG query completed in {elapsed}s")

    return {
        "question": question,
        "answer": response,
        "reranked_documents": reranked_docs,
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
    logger.info("Testing database connection...")
    return test_database()
    
@app.get("/chats")
def get_chats():
    logger.info("Fetching all chats...")
    start = time.perf_counter()
    res = chats()
    elapsed = time.perf_counter() - start
    logger.info(f"Chats fetched in {elapsed}s")
    return res
    
@app.post("/chats/{chat_id}/messages")
def create_new_message(message: Message_Create):
    logger.info("Creating new message for chat ID: %d", message.chat_id)
    start = time.perf_counter()
    res =  create_message(message.chat_id, message.role, message.content)
    elapsed = time.perf_counter() - start
    logger.info(f"Message created in {elapsed}s")
    return res
    
@app.get("/chats/{chat_id}/messages")
def chat_history(chat_id: int):
    logger.info("Fetching chat history for chat ID: %d", chat_id)
    start = time.perf_counter()
    res = get_chat_history(chat_id)
    elapsed = time.perf_counter() - start
    logger.info(f"Chat history fetched in {elapsed}s")
    return res

@app.post("/chats")
def create_new_chat(chat: Chat_Create):
    logger.info("Creating new chat with title: %s", chat.title)
    start = time.perf_counter()
    res = create_chat(chat.title)
    elapsed = time.perf_counter() - start
    logger.info(f"Chat created in {elapsed}s")
    return res

@app.post("/chats/{chat_id}/ask")
def ask_chatbot(chat_id: int, message: Message_Create):
    logger.info("Asking chatbot for chat ID: %d  from /chats/{chat_id}/ask", chat_id)
    start = time.perf_counter()
    create_message( chat_id, message.role, message.content)
    elapsed = time.perf_counter() - start
    logger.info(f"Message logged in db in {elapsed}s")
    # print("\nMessage content (main):", message.content)
    
    start = time.perf_counter()
    history = get_messages(chat_id)
    elapsed = time.perf_counter() - start
    logger.info(f"Chat history retrieved in {elapsed}s")
    
    # print("\nChat history (main):", history)
    start = time.perf_counter()
    logger.info(f"Using rewrite LLM: {rewrite_llm.model}")
    rewritten_question = rewrite_query(message.content, rewrite_llm)
    elapsed = time.perf_counter() - start
    logger.info(f"Question rewritten in {elapsed}s")
    print("\nRewritten question (main):", rewritten_question)

    chat_history = history["messages"]
    # print("\nChat history (main):", chat_history)
    
    # start = time.perf_counter()
    # response, docs, reranked_docs = ask_question(
    #     question=rewritten_question,
    #     # question= message.content,
    #     chat_history=chat_history
    # )
    def generate_response():

        stream, results, reranked_docs, llm_start = ask_question_stream(question=rewritten_question, chat_history=chat_history, original_question=message.content)
        print("\nRetrieved docs (main):", results)
        print("\nReranked docs (main):", reranked_docs)
        
        full_response = ""
        for chunk in stream:

            logger.info(
                "RAW STREAM CHUNK: %r",
                chunk
            )

            if not chunk:
                continue

            full_response += chunk

            yield f"data: {chunk}\n\n"

        elapsed = time.perf_counter() - llm_start
        logger.info(f"Full LLM response received in {elapsed}s")
                
        db_message_start = time.perf_counter()
        create_message( chat_id, "assistant", full_response)
        elapsed = time.perf_counter() - db_message_start
        logger.info(f"Response logged in db in {elapsed}s")
        
    return StreamingResponse(
    generate_response(),
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",
    }
)

    # elapsed = time.perf_counter() - start
    # logger.info(f"Question answered by LLm in {elapsed}s")
    # # print("\nResponse (main):", response)
    # # print("\ndocs (main):", docs)
    # # print("\nreranked_docs  (main):", reranked_docs )
    
    # start = time.perf_counter()
    # # create_message( chat_id, "assistant", response)
    # create_message( chat_id, "assistant", full_response)
    # elapsed = time.perf_counter() - start
    # logger.info(f"Response logged in db in {elapsed}s")
    
    # return {
    #     "chat_id": chat_id,
    #     "question": message.content,
    #     "answer": full_response,
    #     # "answer": response,
    #     # "retrieved_documents": docs,
    #     "retrieved_documents": results,
    #     "reranked_documents": reranked_docs
    # }
     
@app.post("/tts/prepare")
async def prepare_tts(request: TransliterationRequest):

    text = clean_text_for_tts(request.text)

    if contains_urdu_script(text):
        text = transliterate_to_roman_urdu(text)

    return {
        "text": text
    }

  