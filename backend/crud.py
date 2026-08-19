from database import get_connection

def test_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1;")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "database": "connected",
        "result": result
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
    # print("Creating message with chat_id:", chat_id, "role:", role, "content:", content)
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
    
    