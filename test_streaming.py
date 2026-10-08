import requests
import time

url = "http://127.0.0.1:8000/chats/33/ask"

payload = {
    "chat_id": 33,
    "role": "user",
    "content": "Explain deep learning in simple terms."
}

start = time.perf_counter()

print("Sending request...\n")

with requests.post(
    url,
    json=payload,
    stream=True
) as response:

    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("content-type"))

    start = time.perf_counter()

    for chunk in response.iter_content(
        chunk_size=None,
        decode_unicode=True
    ):
        if chunk:
            elapsed = time.perf_counter() - start

            print(
                f"[{elapsed:.2f}s] {repr(chunk)}",
                flush=True
            )