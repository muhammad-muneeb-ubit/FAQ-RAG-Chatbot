from backend.database import get_connection
from langchain_core.messages import HumanMessage, AIMessage

def get_chat_history(chat_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT role, content
            FROM messages
            WHERE chat_id = %s
            ORDER BY created_at ASC
            """,
            (chat_id,)
        )
        messages = cursor.fetchall()
        history = []
        for message in messages:
            if message["role"] == "user":
                history.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )
            elif message["role"] == "assistant":
                history.append(
                    AIMessage(
                        content=message["content"]
                    )
                )
        return history
    finally:
        cursor.close()
        conn.close()
        
def format_chat_history(messages):

    if not messages:
        return "No previous conversation."

    history = []

    for message in messages:
        role = message["role"].upper()
        content = message["content"]

        history.append(
            f"{role}: {content}"
        )

    return "\n".join(history)