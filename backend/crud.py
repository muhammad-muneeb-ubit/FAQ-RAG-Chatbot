import re
from backend.config import  load_llm
from backend.database import get_connection
llm, rewrite_llm = load_llm()

def test_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "message": "database connected successfully",
       
    }
    
def chats():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM chats ORDER BY created_at DESC;")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        cursor.close()
        conn.close()
        raise e
    return {
        "chats": result
    }
    
def create_message(chat_id: int, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()
    # print("\nCreating message with chat_id:", chat_id, "role:", role, "content:", content)
    try:
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (%s, %s, %s)  RETURNING id, chat_id, role, content, created_at",
            (chat_id, role, content),
        )      
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:    
        cursor.close()
        conn.close()
    
    return {
            "chat_id": chat_id,
            "role": role,
            "content": content,
            "assistant_response": "Message created successfully",
        }
    
def get_messages(chat_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM messages WHERE chat_id = %s ORDER BY created_at ASC", (chat_id,))
        messages = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        cursor.close()
        conn.close()
        raise e
    return {
        "chat_id": chat_id,
        "messages": messages
    }
    
def create_chat(title: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO chats (title) VALUES (%s) RETURNING id, title, created_at""", (title,))
        chat = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise e
    return {
        "chat": chat
    }
    
    

def contains_urdu_script(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF]", text))

def clean_text_for_tts(text: str) -> str:

    if not text:
        return ""

    # Remove bold / italic markdown
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Remove inline code
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # Remove headings
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Markdown links → link text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove bullet markers
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)

    # Remove numbered-list markers
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()

def transliterate_to_roman_urdu(text: str) -> str:

    prompt = f"""
        Convert the following Urdu-script text into simple Roman Urdu
        for English text-to-speech.

        Rules:
        - Preserve the meaning exactly.
        - Only convert Urdu script to Roman Urdu.
        - Preserve English technical terms such as Python, NumPy, API, AI.
        - Do not add explanations.
        - Return only the Roman Urdu text.

        Text:
        {text}
"""

    response = llm.invoke(prompt)

    if isinstance(response.content, list):
        return response.content[0]["text"].strip()

    return response.content.strip()
    