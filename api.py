import requests

BASE_URL = "http://127.0.0.1:8000"


def get_chats():

    response = requests.get(
        f"{BASE_URL}/chats"
    )

    response.raise_for_status()

    return response.json()


def create_chat(title):

    response = requests.post(
        f"{BASE_URL}/chats",
        json={
            "title": title
        }
    )

    response.raise_for_status()

    return response.json()


def get_messages(chat_id):

    response = requests.get(
        f"{BASE_URL}/chats/{chat_id}/messages"
    )

    response.raise_for_status()

    return response.json()


def ask_question(chat_id, question):

    response = requests.post(
        f"{BASE_URL}/chats/{chat_id}/ask",
        json={
            "content": question
        }
    )

    response.raise_for_status()

    return response.json()