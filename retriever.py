# import streamlit as st #type: ignore
# import requests
# from voices.STT import transcribe_audio_bytes
# from streamlit_mic_recorder import mic_recorder #type: ignore
# from voices.TTS import text_to_speech
# import re
# import time
# from log import logger

# BACKEND_URL = "http://127.0.0.1:8000"

# def generate_tts(text):

#     logger.info("Preparing text for TTS...")

#     start = time.perf_counter()

#     response = requests.post(
#         f"{BACKEND_URL}/tts/prepare",
#         json={"text": text},
#         timeout=120
#     )

#     response.raise_for_status()

#     result = response.json().get("text", "")

#     if not result:
#         raise ValueError("TTS preparation returned empty text.")

#     elapsed = time.perf_counter() - start

#     logger.info(f"Text prepared for TTS in {elapsed:.2f}s")

#     print("\nText prepared for TTS:", result)

#     return result

# st.set_page_config(
#     page_title="Python FAQ Assistant",
#     page_icon="🐍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
# if "chats" not in st.session_state:
#     st.session_state.chats = []

# if "selected_chat_id" not in st.session_state:
#     st.session_state.selected_chat_id = None

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "chat_loaded" not in st.session_state:
#     st.session_state.chat_loaded = False

# # llm = load_llm()

# def get_chats():
#     response = requests.get(
#         f"{BACKEND_URL}/chats",
#         timeout=10
#     )
#     response.raise_for_status()
#     data = response.json()
#     return data.get("chats", [])

# def create_chat(title):
#     response = requests.post(
#         f"{BACKEND_URL}/chats",
#         json={
#             "title": title
#         },
#         timeout=10
#     )
#     response.raise_for_status()
#     return response.json()

# def get_messages(chat_id):
#     response = requests.get(
#         f"{BACKEND_URL}/chats/{chat_id}/messages",
#         timeout=10
#     )
#     response.raise_for_status()
#     data = response.json()
#     if isinstance(data, dict):
#         messages = data.get("messages", [])
#         if isinstance(messages, list):
#             return messages
#         return []
#     elif isinstance(data, list):
#         return data
#     return []

# # def ask_chatbot( chat_id, original_question, role):
# #     response = requests.post(
# #         f"{BACKEND_URL}/chats/{chat_id}/ask",
# #         json={
# #             "chat_id": chat_id,
# #             "content": original_question,
# #             "role": role,
# #         },
# #         timeout=120
# #     )
# #     response.raise_for_status()
# #     return response.json()

# def ask_chatbot_stream(chat_id, original_question, role):
#     response = requests.post(
#         f"{BACKEND_URL}/chats/{chat_id}/ask",
#         json={
#             "chat_id": chat_id,
#             "content": original_question,
#             "role": role,
#         },
#         stream=True,
#         timeout=120
#     )

#     response.raise_for_status()

#     for line in response.iter_lines(decode_unicode=True):
#         if not line:
#             continue

#         if line.startswith("data: "):
#             yield line[6:]
            
# if not st.session_state.chats:
#     try:
#         logger.info("Fetching chats from backend...")
#         start = time.perf_counter()
#         st.session_state.chats = get_chats()
#         elapsed = time.perf_counter() - start
#         logger.info(f"Chats fetched in {elapsed}s")
#     except Exception as e:
#         st.error(f"Could not load chats: {e}")
#         st.stop()
        
# with st.sidebar:
#     st.title("💬 Chats")
#     st.divider()

#     if st.button("🟢 New Chat", use_container_width=True):
#         st.session_state.selected_chat_id = None
#         st.session_state.messages = []
#         st.session_state.chat_loaded = False
#         st.rerun()
#     st.divider()

#     for chat in st.session_state.chats:
#         chat_id = chat.get("id")
#         title = chat.get( "title", "Untitled Chat")
#         if chat_id is None:
#             continue
#         is_selected = ( st.session_state.selected_chat_id == chat_id)

#         button_text = ( f"🟢 {title}" if is_selected else f"💬 {title}")

#         if st.button( button_text, key=f"chat_{chat_id}", use_container_width=True):
#             st.session_state.selected_chat_id = chat_id
#             st.session_state.chat_loaded = False
#             st.session_state.messages = []
#             st.rerun()

# st.title("🐍 Python FAQ Assistant")
# st.caption(
#     "Ask anything about Python and get answers "
#     "from the FAQ knowledge base."
# )

# if st.session_state.selected_chat_id is None:
#     st.info(
#         "👈 Select an existing chat or click "
#         "**New Chat** to start a conversation."
#     )
#     st.subheader("Create a new chat")
#     chat_title = st.text_input(
#         "Chat name",
#         placeholder="e.g. Learning Python"
#     )
#     if st.button(
#         "Create Chat",
#         type="primary"
#     ):
#         if not chat_title.strip():
#             st.warning("Please enter a chat name.")
#         else:
#             try:
#                 logger.info("Creating new chat")
#                 start = time.perf_counter()
#                 result = create_chat(chat_title.strip())
#                 elapsed = time.perf_counter() - start
#                 logger.info(f"New chat created in {elapsed}s")
#                 new_chat = result.get("chat")
#                 if isinstance(new_chat, dict):
#                     st.session_state.chats.insert(0, new_chat)
#                     st.session_state.selected_chat_id = (new_chat.get("id"))
#                     st.session_state.messages = []
#                     st.session_state.chat_loaded = False
#                     st.rerun()
#                 else:
#                     st.error(
#                         "Chat was created but backend "
#                         "returned an unexpected response."
#                     )
#             except Exception as e:
#                 st.error(f"Could not create chat: {e}")
#     st.stop()

# chat_id = st.session_state.get("selected_chat_id")
# if chat_id is not None:
#     if not st.session_state.get( "chat_loaded", False):
#         try:
#             logger.info("Loading chat messages...")
#             start = time.perf_counter()
#             loaded_messages = get_messages(chat_id)
#             elapsed = time.perf_counter() - start
#             logger.info(f"Chat messages loaded in {elapsed}s")
#             st.session_state.messages = (loaded_messages)
#             st.session_state.chat_loaded = True

#         except Exception as e:
#             st.error(f"❌ Could not load chat: {e}")
#             st.session_state.messages = []
#             st.session_state.chat_loaded = True

# if chat_id is not None:
#     for index, message in enumerate(st.session_state.messages):
#         if not isinstance(message, dict):
#             continue

#         message_type = message.get("type")
#         content = message.get("content")

#         if not content:
#             continue

#         if message_type == "human":
#             with st.chat_message( "user", avatar="👤"):
#                 st.write(content)

#         elif message_type == "ai":
#             with st.chat_message( "assistant", avatar="🐍"):
#                 st.write(content)
#                 if st.button("🔊 Listen", key=f"listen_{index}"):
#                     try:
#                         with st.spinner("🔊 Generating audio..."):
#                             logger.info("Generating audio for AI response...")
#                             start = time.perf_counter()
#                             # audio_path = text_to_speech(content)
#                             audio_bytes = generate_tts(content)
#                             elapsed = time.perf_counter() - start
#                             logger.info(f"Audio generated in {elapsed}s")

#                         # with open(audio_path, "rb") as audio_file:
#                         #     audio_bytes = audio_file.read()

#                         st.audio(
#                             audio_bytes,
#                             format="audio/wav"
#                         )

#                     except Exception as e:
#                         st.error(f"❌ TTS error: {e}")

# col1, col2 = st.columns([10, 1])

# with col1:
#     question = st.chat_input("💬 Ask a Python question...")

# with col2:
#     logger.info("Starting voice recorder...")
#     start = time.perf_counter()
#     audio = mic_recorder(
#         start_prompt="🎤",
#         stop_prompt="⏹️",
#         key="voice_recorder"
#     )
#     elapsed = time.perf_counter() - start
#     logger.info(f"Voice recorder session completed in {elapsed}s")

# original_question = None

# if audio:
#     # print("\nRecorder payload:", audio)
#     audio_bytes = audio.get("bytes")
#     if audio_bytes:
#         # print("Recorder bytes length:", len(audio_bytes))
#         with st.spinner("🎙️ Converting voice to text..."):
#             logger.info("Transcribing audio to text...")
#             start = time.perf_counter()
#             original_question = (transcribe_audio_bytes(audio_bytes))
#             elapsed = time.perf_counter() - start
#             logger.info(f"Audio transcribed to text in {elapsed}s")

#         print("\nVoice transcript:",original_question)

# if question:
#     original_question = question.strip()
#     print("\nText input question: (retriever.py)", question)
# if original_question :
#     original_question = original_question.strip()
#     # print("\nOriginal question: (retriever.py)", original_question )

#     if chat_id is None:
#         st.error("Please select or create a chat first.")
#         st.stop()

#     with st.chat_message("user",avatar="👤"):
#         st.write(original_question)

#     # with st.chat_message("assistant",avatar="🐍"):
#     #     with st.spinner("🔎 Searching FAQ knowledge base..."):
#     #         try:
#     #             logger.info("Sending question to backend for RAG processing...")
#     #             start = time.perf_counter()
#     #             result = ask_chatbot( chat_id=chat_id, original_question=original_question, role="user")
#     #             elapsed = time.perf_counter() - start
#     #             logger.info(f"frontend RAG processing completed in {elapsed}s")
#     #             # print("\nResult response: (retriever.py)", result)
#     #             answer = result.get( "answer", "No answer received.")

#     #             retrieved_documents = result.get( "retrieved_documents", [])
#     #             reranked_documents = result.get( "reranked_documents", [])

#     #             # print("\nRetrieved documents:(retriever.py)", retrieved_documents)
#     #             # print("\nReranked documents:(retriever.py)", reranked_documents)
                
#     #             st.write(answer)
#             #     logger.info("Removed * # from answer for TTS and TTS")
#             #     start = time.perf_counter()
#             #     audio_path = text_to_speech(clean_text_for_tts(answer))
#             #     elapsed = time.perf_counter() - start
#             #     logger.info(f"Audio generated for answer in {elapsed}s after text cleaning")

#             #     if audio_path:
#             #         st.audio(audio_path)
#             #     st.session_state.messages = (get_messages(chat_id))

#             # except requests.HTTPError as e:
#             #     st.error(f"❌ Backend error: {e}")

#             #     try:
#             #         st.code(e.response.text)
#             #     except Exception:
#             #         pass

#             # except Exception as e:
#             #     st.error(f"❌ Something went wrong: {e}")
            
#     with st.chat_message("assistant", avatar="🐍"):
#         with st.spinner("🔎 Searching FAQ knowledge base..."):
#             try:
#                 logger.info("Sending question to backend for streaming RAG processing...")
#                 start = time.perf_counter()
#                 answer = ""
#                 message_placeholder = st.empty()
#                 for chunk in ask_chatbot_stream(
#                     chat_id=chat_id,
#                     original_question=original_question,
#                     role="user"
#                 ):
#                     answer += chunk
#                     message_placeholder.markdown(answer)

#                 elapsed = time.perf_counter() - start

#                 logger.info(
#                     f"Streaming response completed in {elapsed}s"
#                 )

#                 # Generate TTS after complete response
#                 # cleaned_answer = clean_text_for_tts(answer)

#                 # audio_path = text_to_speech(cleaned_answer)

#                 # if audio_path:
#                 #     st.audio(audio_path)
#                 audio_bytes = generate_tts(answer)

#                 if audio_bytes:
#                     st.audio(
#                         audio_bytes,
#                         format="audio/wav"
#                     )

#                 # Reload messages from database
#                 st.session_state.messages = get_messages(chat_id)

#             except requests.HTTPError as e:

#                 st.error(f"❌ Backend error: {e}")

#                 try:
#                     st.code(e.response.text)
#                 except Exception:
#                     pass

#             except Exception as e:

#                 st.error(f"❌ Something went wrong: {e}")

import streamlit as st  # type: ignore
import requests
from voices.STT import transcribe_audio_bytes
from streamlit_mic_recorder import mic_recorder  # type: ignore
from voices.TTS import text_to_speech
import time
from log import logger


BACKEND_URL = "http://127.0.0.1:8000"


# ============================================================
# TTS
# ============================================================

def generate_tts(text):
    """
    Prepare text using the backend and then generate
    audio using the local Piper TTS model.

    Flow:
        Original AI response
            ↓
        /tts/prepare
            ↓
        Cleaned / Roman Urdu text
            ↓
        text_to_speech()
            ↓
        WAV bytes
    """

    if not text or not text.strip():
        raise ValueError("TTS text cannot be empty.")

    logger.info("Preparing text for TTS...")

    start = time.perf_counter()

    # --------------------------------------------------------
    # Step 1: Send original response to backend
    # Backend handles:
    # - Markdown cleaning
    # - Urdu script detection
    # - Urdu → Roman Urdu transliteration
    # --------------------------------------------------------

    response = requests.post(
        f"{BACKEND_URL}/tts/prepare",
        json={
            "text": text
        },
        timeout=120
    )

    response.raise_for_status()

    # --------------------------------------------------------
    # Step 2: Get prepared text
    # --------------------------------------------------------

    data = response.json()

    prepared_text = data.get("text", "")

    if not prepared_text:
        raise ValueError(
            "Backend returned empty text for TTS."
        )

    elapsed = time.perf_counter() - start

    logger.info(
        f"Text prepared for TTS in {elapsed}s"
    )

    print(
        "\nText prepared for TTS:",
        prepared_text
    )

    # --------------------------------------------------------
    # Step 3: Generate audio using Piper
    # --------------------------------------------------------

    logger.info("Generating audio with Piper...")

    audio_start = time.perf_counter()

    audio_path = text_to_speech(prepared_text)

    audio_elapsed = time.perf_counter() - audio_start

    logger.info(
        f"Piper audio generated in {audio_elapsed}s"
    )

    if not audio_path:
        raise ValueError(
            "Piper did not return an audio path."
        )

    # --------------------------------------------------------
    # Step 4: Read generated WAV file
    # --------------------------------------------------------

    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    return audio_bytes


# ============================================================
# Streamlit configuration
# ============================================================

st.set_page_config(
    page_title="Python FAQ Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# Session state
# ============================================================

if "chats" not in st.session_state:
    st.session_state.chats = []


if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = None


if "messages" not in st.session_state:
    st.session_state.messages = []


if "chat_loaded" not in st.session_state:
    st.session_state.chat_loaded = False


# ============================================================
# Backend API functions
# ============================================================

def get_chats():

    response = requests.get(
        f"{BACKEND_URL}/chats",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data.get("chats", [])


def create_chat(title):

    response = requests.post(
        f"{BACKEND_URL}/chats",
        json={
            "title": title
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_messages(chat_id):

    response = requests.get(
        f"{BACKEND_URL}/chats/{chat_id}/messages",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):

        messages = data.get(
            "messages",
            []
        )

        if isinstance(messages, list):
            return messages

        return []

    elif isinstance(data, list):

        return data

    return []


# ============================================================
# Streaming chatbot
# ============================================================

def ask_chatbot_stream(
    chat_id,
    original_question,
    role
):

    response = requests.post(
        f"{BACKEND_URL}/chats/{chat_id}/ask",

        json={
            "chat_id": chat_id,
            "content": original_question,
            "role": role,
        },

        stream=True,

        timeout=120
    )

    response.raise_for_status()

    for line in response.iter_lines(
        decode_unicode=True
    ):

        if not line:
            continue

        if line.startswith("data: "):

            yield line[6:]


# ============================================================
# Load chats
# ============================================================

if not st.session_state.chats:

    try:

        logger.info(
            "Fetching chats from backend..."
        )

        start = time.perf_counter()

        st.session_state.chats = get_chats()

        elapsed = time.perf_counter() - start

        logger.info(
            f"Chats fetched in {elapsed}s"
        )

    except Exception as e:

        st.error(
            f"Could not load chats: {e}"
        )

        st.stop()


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("💬 Chats")

    st.divider()

    # --------------------------------------------------------
    # New chat
    # --------------------------------------------------------

    if st.button(
        "🟢 New Chat",
        use_container_width=True
    ):

        st.session_state.selected_chat_id = None

        st.session_state.messages = []

        st.session_state.chat_loaded = False

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # Existing chats
    # --------------------------------------------------------

    for chat in st.session_state.chats:

        chat_id = chat.get("id")

        title = chat.get(
            "title",
            "Untitled Chat"
        )

        if chat_id is None:
            continue

        is_selected = (
            st.session_state.selected_chat_id
            == chat_id
        )

        button_text = (
            f"🟢 {title}"
            if is_selected
            else f"💬 {title}"
        )

        if st.button(
            button_text,
            key=f"chat_{chat_id}",
            use_container_width=True
        ):

            st.session_state.selected_chat_id = (
                chat_id
            )

            st.session_state.chat_loaded = False

            st.session_state.messages = []

            st.rerun()


# ============================================================
# Main title
# ============================================================

st.title(
    "🐍 Python FAQ Assistant"
)

st.caption(
    "Ask anything about Python and get answers "
    "from the FAQ knowledge base."
)


# ============================================================
# Create new chat
# ============================================================

if st.session_state.selected_chat_id is None:

    st.info(
        "👈 Select an existing chat or click "
        "**New Chat** to start a conversation."
    )

    st.subheader(
        "Create a new chat"
    )

    chat_title = st.text_input(
        "Chat name",
        placeholder="e.g. Learning Python"
    )

    if st.button(
        "Create Chat",
        type="primary"
    ):

        if not chat_title.strip():

            st.warning(
                "Please enter a chat name."
            )

        else:

            try:

                logger.info(
                    "Creating new chat"
                )

                start = time.perf_counter()

                result = create_chat(
                    chat_title.strip()
                )

                elapsed = time.perf_counter() - start

                logger.info(
                    f"New chat created in {elapsed}s"
                )

                new_chat = result.get(
                    "chat"
                )

                if isinstance(
                    new_chat,
                    dict
                ):

                    st.session_state.chats.insert(
                        0,
                        new_chat
                    )

                    st.session_state.selected_chat_id = (
                        new_chat.get("id")
                    )

                    st.session_state.messages = []

                    st.session_state.chat_loaded = False

                    st.rerun()

                else:

                    st.error(
                        "Chat was created but backend "
                        "returned an unexpected response."
                    )

            except Exception as e:

                st.error(
                    f"Could not create chat: {e}"
                )

    st.stop()


# ============================================================
# Selected chat
# ============================================================

chat_id = st.session_state.get(
    "selected_chat_id"
)


# ============================================================
# Load messages
# ============================================================

if chat_id is not None:

    if not st.session_state.get(
        "chat_loaded",
        False
    ):

        try:

            logger.info(
                "Loading chat messages..."
            )

            start = time.perf_counter()

            loaded_messages = get_messages(
                chat_id
            )

            elapsed = time.perf_counter() - start

            logger.info(
                f"Chat messages loaded in {elapsed}s"
            )

            st.session_state.messages = (
                loaded_messages
            )

            st.session_state.chat_loaded = True

        except Exception as e:

            st.error(
                f"❌ Could not load chat: {e}"
            )

            st.session_state.messages = []

            st.session_state.chat_loaded = True


# ============================================================
# Display chat history
# ============================================================

if chat_id is not None:

    for index, message in enumerate(
        st.session_state.messages
    ):

        if not isinstance(
            message,
            dict
        ):
            continue

        message_type = message.get(
            "type"
        )

        content = message.get(
            "content"
        )

        if not content:
            continue

        # ----------------------------------------------------
        # User message
        # ----------------------------------------------------

        if message_type == "human":

            with st.chat_message(
                "user",
                avatar="👤"
            ):

                st.write(
                    content
                )

        # ----------------------------------------------------
        # AI message
        # ----------------------------------------------------

        elif message_type == "ai":

            with st.chat_message(
                "assistant",
                avatar="🐍"
            ):

                st.write(
                    content
                )

                # --------------------------------------------
                # Listen button
                # --------------------------------------------

                if st.button(
                    "🔊 Listen",
                    key=f"listen_{index}"
                ):

                    try:

                        with st.spinner(
                            "🔊 Generating audio..."
                        ):

                            logger.info(
                                "Generating audio for AI response..."
                            )

                            start = time.perf_counter()

                            # IMPORTANT:
                            # Do NOT call text_to_speech(content)
                            #
                            # generate_tts() first sends the
                            # text to /tts/prepare.
                            #
                            # Backend cleans Markdown and
                            # converts Urdu → Roman Urdu.
                            #
                            # Then Piper generates audio.

                            audio_bytes = generate_tts(
                                content
                            )

                            elapsed = (
                                time.perf_counter()
                                - start
                            )

                            logger.info(
                                f"Audio generated in {elapsed}s"
                            )

                        st.audio(
                            audio_bytes,
                            format="audio/wav"
                        )

                    except Exception as e:

                        logger.exception(
                            "TTS generation failed"
                        )

                        st.error(
                            f"❌ TTS error: {e}"
                        )


# ============================================================
# Input area
# ============================================================

col1, col2 = st.columns(
    [10, 1]
)


# ============================================================
# Text input
# ============================================================

with col1:

    question = st.chat_input(
        "💬 Ask a Python question..."
    )


# ============================================================
# Voice recorder
# ============================================================

with col2:

    logger.info(
        "Starting voice recorder..."
    )

    start = time.perf_counter()

    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="⏹️",
        key="voice_recorder"
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    logger.info(
        f"Voice recorder session completed in {elapsed}s"
    )


# ============================================================
# Process voice input
# ============================================================

original_question = None


if audio:

    audio_bytes = audio.get(
        "bytes"
    )

    if audio_bytes:

        with st.spinner(
            "🎙️ Converting voice to text..."
        ):

            logger.info(
                "Transcribing audio to text..."
            )

            start = time.perf_counter()

            original_question = (
                transcribe_audio_bytes(
                    audio_bytes
                )
            )

            elapsed = (
                time.perf_counter()
                - start
            )

            logger.info(
                f"Audio transcribed to text in {elapsed}s"
            )

        print(
            "\nVoice transcript:",
            original_question
        )


# ============================================================
# Process text input
# ============================================================

if question:

    original_question = (
        question.strip()
    )

    print(
        "\nText input question: (retriever.py)",
        question
    )


# ============================================================
# Process question
# ============================================================

if original_question:

    original_question = (
        original_question.strip()
    )

    if chat_id is None:

        st.error(
            "Please select or create a chat first."
        )

        st.stop()


    # ========================================================
    # Display user question
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.write(
            original_question
        )


    # ========================================================
    # Get AI response
    # ========================================================

    with st.chat_message(
        "assistant",
        avatar="🐍"
    ):

        with st.spinner(
            "🔎 Searching FAQ knowledge base..."
        ):

            try:

                logger.info(
                    "Sending question to backend "
                    "for streaming RAG processing..."
                )

                start = time.perf_counter()

                answer = ""

                message_placeholder = st.empty()


                # ------------------------------------------------
                # Stream answer
                # ------------------------------------------------

                for chunk in ask_chatbot_stream(
                    chat_id=chat_id,
                    original_question=original_question,
                    role="user"
                ):

                    answer += chunk

                    message_placeholder.markdown(
                        answer
                    )


                elapsed = (
                    time.perf_counter()
                    - start
                )

                logger.info(
                    f"Streaming response completed in {elapsed}s"
                )


                # =================================================
                # Generate TTS after complete response
                # =================================================

                logger.info(
                    "Preparing AI response for TTS..."
                )

                audio_bytes = generate_tts(
                    answer
                )


                if audio_bytes:

                    st.audio(
                        audio_bytes,
                        format="audio/wav"
                    )


                # =================================================
                # Reload messages from database
                # =================================================

                st.session_state.messages = (
                    get_messages(
                        chat_id
                    )
                )


            except requests.HTTPError as e:

                st.error(
                    f"❌ Backend error: {e}"
                )

                try:

                    st.code(
                        e.response.text
                    )

                except Exception:

                    pass


            except Exception as e:

                logger.exception(
                    "Something went wrong"
                )

                st.error(
                    f"❌ Something went wrong: {e}"
                )