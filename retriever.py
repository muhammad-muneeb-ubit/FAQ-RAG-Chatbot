# import streamlit as st
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# from config import llm, prompt, format_docs
# import os 

# load_dotenv()
# EMBEDDING_MODEL= os.getenv("EMBEDDING_MODEL")
# st.set_page_config(
#     page_title="Python FAQ Assistant",
#     page_icon="🐍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown(
#     """
#     <style>
#     /* Main container */
#     .block-container {
#         max-width: 1100px;
#         padding-top: 2rem;
#         padding-bottom: 5rem;
#     }
#     /* Header */
#     .main-header {
#         text-align: center;
#         padding: 10px 0 25px 0;
#     }
#     .main-header h1 {
#         font-size: 42px;
#         margin-bottom: 5px;
#     }
#     .main-header p {
#         font-size: 17px;
#         opacity: 0.7;
#     }
#     /* Welcome card */
#     .welcome-card {
#         padding: 25px;
#         border-radius: 15px;
#         border: 1px solid rgba(128, 128, 128, 0.25);
#         margin-bottom: 25px;
#     }
#     /* FAQ source cards */
#     .source-card {
#         padding: 15px;
#         border-radius: 10px;
#         border: 1px solid rgba(128, 128, 128, 0.25);
#         margin-bottom: 12px;
#     }
#     .source-title {
#         font-weight: 600;
#         margin-bottom: 8px;
#     }
#     /* Sidebar */
#     .sidebar-title {
#         font-size: 22px;
#         font-weight: 600;
#     }
#     /* Chat input */
#     [data-testid="stChatInput"] {
#         bottom: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


# @st.cache_resource
# def load_vectorstore():
#     embeddings = GoogleGenerativeAIEmbeddings(
#         model=EMBEDDING_MODEL
#     )
#     vectorstore = Chroma(
#         persist_directory="./db",
#         embedding_function=embeddings
#     )
#     return vectorstore

# vectorstore = load_vectorstore()

# def ask_question(question):
#     docs = vectorstore.similarity_search(
#         question,
#         k=3
#     )
#     context = format_docs(docs)
#     response = ( prompt | llm | StrOutputParser()).invoke(
#         {
#             "context": context,
#             "question": question
#         }
#     )
#     return response, docs

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# with st.sidebar:
#     st.markdown(
#         '<div class="sidebar-title">🐍 Python FAQ</div>',
#         unsafe_allow_html=True
#     )
#     st.markdown("---")
#     st.markdown(
#         """
#         ### About
#         This chatbot uses **Retrieval-Augmented Generation (RAG)**
#         to answer Python questions from a FAQ knowledge base.
#         **Pipeline**
#         CSV  
#         ↓  
#         Documents  
#         ↓  
#         Embeddings  
#         ↓  
#         Chroma  
#         ↓  
#         Semantic Search  
#         ↓  
#         LLM  
#         ↓  
#         Answer
#         """
#     )
#     st.markdown("---")
#     st.markdown("### ⚙️ Settings")
#     number_of_results = st.slider(
#         "Retrieved FAQs",
#         min_value=1,
#         max_value=5,
#         value=3
#     )
#     st.markdown("---")
#     if st.button(
#         "🧹 Clear Chat",
#         use_container_width=True
#     ):
#         st.session_state.messages = []
#         st.rerun()
#     st.markdown("---")
#     st.caption(
#         "Powered by LangChain + Chroma + Gemini"
#     )

# st.markdown(
#     """
#     <div style="text-align: center;">
#     <h1>🐍 Python FAQ Assistant</h1>
#     <p>
#         Ask anything about Python and get answers
#         from the FAQ knowledge base.
#     </p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# if not st.session_state.messages:
#    st.markdown("""
# ### 👋 Welcome!

# I can help you find answers from the **Python FAQ dataset**.

# Try asking:

# - What is Python?
# - How do I create a list in Python?
# - What is a Python dictionary?
# - How do I install Python?
# - Is Python difficult for beginners?
# """)

# for message in st.session_state.messages:
#     with st.chat_message(
#         message["role"],
#         avatar="🐍" if message["role"] == "assistant" else "👤"
#     ):
#         st.markdown(
#             message["content"]
#         )
#         if (
#             message["role"] == "assistant"
#             and "docs" in message
#         ):
#             docs = message["docs"]
#             with st.expander(
#                 f"📚 Retrieved FAQs ({len(docs)})"
#             ):
#                 for i, doc in enumerate(docs):

#                     question_text = doc.metadata.get(
#                         "question",
#                         "Question unavailable"
#                     )
#                     answer_text = doc.metadata.get(
#                         "answer",
#                         "Answer unavailable"
#                     )
#                     st.markdown(
#                         f"""
#                         <div class="source-card">
#                         <div class="source-title">
#                         Result {i + 1}
#                         </div>

#                         <b>Question</b><br>
#                         {question_text}
#                         <br><br>
#                         <b>Answer</b><br>
#                         {answer_text}
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )
# question = st.chat_input(
#     "💬 Ask a Python question..."
# )

# if question:
#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": question
#         }
#     )
#     with st.chat_message(
#         "user",
#         avatar="👤"
#     ):
#         st.markdown(question)

#     with st.chat_message(
#         "assistant",
#         avatar="🐍"
#     ):
#         with st.spinner(
#             "🔎 Searching FAQ knowledge base..."
#         ):
#             try:
#                 docs = vectorstore.similarity_search(
#                     question,
#                     k=number_of_results
#                 )
#                 context = format_docs(docs)
#                 response = (
#                     prompt
#                     | llm
#                     | StrOutputParser()
#                 ).invoke(
#                     {
#                         "context": context,
#                         "question": question
#                     }
#                 )
#                 st.markdown(response)

#                 with st.expander(
#                     f"📚 Retrieved FAQs ({len(docs)})"
#                 ):
#                     for i, doc in enumerate(docs):
#                         question_text = doc.metadata.get(
#                             "question",
#                             "Question unavailable"
#                         )
#                         answer_text = doc.metadata.get(
#                             "answer",
#                             "Answer unavailable"
#                         )
#                         st.markdown(
#                             f"""
#                             <div class="source-card">
#                             <div class="source-title">
#                             Result {i + 1}
#                             </div>
#                             <b>Question</b><br>
#                             {question_text}
#                             <br><br>
#                             <b>Answer</b><br>
#                             {answer_text}
#                             </div>
#                             """,
#                             unsafe_allow_html=True
#                         )
#                 st.session_state.messages.append(
#                     {
#                         "role": "assistant",
#                         "content": response,
#                         "docs": docs
#                     }
#                 )
#             except Exception as e:
#                 st.error(
#                     f"Something went wrong: {e}"
#                 )

# import streamlit as st
# import requests


# # ============================================================
# # CONFIG
# # ============================================================

# API_URL = "http://127.0.0.1:8000"


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Python FAQ Assistant",
#     page_icon="🐍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )


# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown(
#     """
#     <style>

#     .block-container {
#         max-width: 1100px;
#         padding-top: 2rem;
#         padding-bottom: 5rem;
#     }

#     .sidebar-title {
#         font-size: 22px;
#         font-weight: 600;
#     }

#     .source-card {
#         padding: 15px;
#         border-radius: 10px;
#         border: 1px solid rgba(128, 128, 128, 0.25);
#         margin-bottom: 12px;
#     }

#     .source-title {
#         font-weight: 600;
#         margin-bottom: 8px;
#     }

#     [data-testid="stChatInput"] {
#         bottom: 20px;
#     }


#     /* ============================= */
#     /* CHAT MESSAGE ALIGNMENT        */
#     /* ============================= */

#     [data-testid="stChatMessage"] {
#         display: flex;
#         width: 100%;
#     }


#     /* ============================= */
#     /* USER MESSAGE                  */
#     /* ============================= */

#     [data-testid="stChatMessage"]:has(
#         [data-testid="stChatMessageAvatarUser"]
#     ) {
#         width: 80%;
#         margin-left: auto;
#         margin-right: 0;
#         flex-direction: row-reverse;
#     }

#     [data-testid="stChatMessage"]:has(
#         [data-testid="stChatMessageAvatarUser"]
#     ) [data-testid="stChatMessageContent"] {
#         text-align: right;
#     }


#     /* ============================= */
#     /* ASSISTANT MESSAGE             */
#     /* ============================= */

#     [data-testid="stChatMessage"]:has(
#         [data-testid="stChatMessageAvatarAssistant"]
#     ) {
#         width: 80%;
#         margin-left: 0;
#         margin-right: auto;
#         flex-direction: row;
#     }

#     [data-testid="stChatMessage"]:has(
#         [data-testid="stChatMessageAvatarAssistant"]
#     ) [data-testid="stChatMessageContent"] {
#         text-align: left;
#     }

#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ============================================================
# # API FUNCTIONS
# # ============================================================

# def get_chats():

#     response = requests.get(
#         f"{API_URL}/chats"
#     )

#     response.raise_for_status()

#     return response.json()


# def create_chat(title):

#     response = requests.post(
#         f"{API_URL}/chats",
#         json={
#             "title": title
#         }
#     )

#     response.raise_for_status()

#     data = response.json()

#     return data


# def get_messages(chat_id):

#     response = requests.get(
#         f"{API_URL}/chats/{chat_id}/messages"
#     )

#     response.raise_for_status()

#     return response.json()


# def ask_question(chat_id, question):

#     response = requests.post(
#         f"{API_URL}/chats/{chat_id}/ask",
#         json={
#             "chat_id": chat_id,
#             "role": "user",
#             "content": question
#         }
#     )

#     if response.status_code == 422:

#         print("422 RESPONSE:")
#         print(response.text)

#     response.raise_for_status()

#     return response.json()

# # ============================================================
# # SESSION STATE
# # ============================================================

# # ============================================================
# # SESSION STATE
# # ============================================================

# if "chats" not in st.session_state:
#     try:
#         data = get_chats()

#         # Your backend returns:
#         # {
#         #     "chats": [...]
#         # }

#         st.session_state.chats = data.get("chats", [])

#     except Exception as e:
#         st.session_state.chats = []
#         st.error(f"Could not load chats: {e}")


# if "current_chat_id" not in st.session_state:
#     st.session_state.current_chat_id = None


# if "messages" not in st.session_state:
#     st.session_state.messages = []


# if "show_new_chat" not in st.session_state:
#     st.session_state.show_new_chat = False


# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:

#     st.markdown(
#         '<div class="sidebar-title">🐍 Python FAQ</div>',
#         unsafe_allow_html=True
#     )

#     st.markdown("---")


#     # ========================================================
#     # NEW CHAT BUTTON
#     # ========================================================

#     if st.button(
#         "➕ New Chat",
#         use_container_width=True
#     ):

#         st.session_state.show_new_chat = True


#     # ========================================================
#     # NEW CHAT FORM
#     # ========================================================

#     if st.session_state.show_new_chat:

#         chat_title = st.text_input(
#             "Chat name",
#             placeholder="e.g. Python Basics",
#             key="new_chat_title"
#         )

#         col1, col2 = st.columns(2)

#         with col1:

#             if st.button(
#                 "Create",
#                 use_container_width=True
#             ):

#                 if not chat_title.strip():

#                     st.warning(
#                         "Please enter a chat name."
#                     )

#                 else:

#                     try:

#                         result = create_chat(
#                             chat_title.strip()
#                         )

#                         chat = result["chat"]

#                         # Add new chat to sidebar
#                         st.session_state.chats.insert(
#                             0,
#                             chat
#                         )

#                         # Select new chat
#                         st.session_state.current_chat_id = chat["id"]

#                         # Empty conversation
#                         st.session_state.messages = []

#                         # Close form
#                         st.session_state.show_new_chat = False

#                         st.rerun()

#                     except Exception as e:

#                         st.error(
#                             f"Could not create chat: {e}"
#                         )


#         with col2:

#             if st.button(
#                 "Cancel",
#                 use_container_width=True
#             ):

#                 st.session_state.show_new_chat = False

#                 st.rerun()


#     st.markdown("---")


#     # ========================================================
#     # CHAT LIST
#     # ========================================================

#     st.markdown("### 💬 Chats")


#     chats = st.session_state.chats


#     if not chats:

#         st.caption(
#             "No chats found."
#         )

#     else:

#        for chat in st.session_state.chats:

#         chat_id = chat["id"]

#         title = chat.get(
#             "title",
#             "Untitled Chat"
#         )

#         if chat_id == st.session_state.current_chat_id:
#             button_label = f"🟢 {title}"
#         else:
#             button_label = f"💬 {title}"

#         if st.button(
#             button_label,
#             key=f"chat_{chat_id}",
#             use_container_width=True
#         ):

#             try:

#                 data = get_messages(chat_id)

#                 st.session_state.current_chat_id = chat_id

#                 # Handle both possible API responses
#                 if isinstance(data, dict):

#                     st.session_state.messages = data.get(
#                         "messages",
#                         []
#                     )

#                 elif isinstance(data, list):

#                     st.session_state.messages = data

#                 else:

#                     st.session_state.messages = []

#                 st.rerun()

#             except Exception as e:

#                 st.error(
#                     f"Could not load chat: {e}"
#                 )

#     st.markdown("---")


#     # ========================================================
#     # ABOUT
#     # ========================================================

#     st.markdown(
#         """
#         ### About

#         This chatbot uses **Retrieval-Augmented Generation (RAG)**
#         to answer Python questions from a FAQ knowledge base.

#         **Pipeline**

#         User Question  
#         ↓  
#         FastAPI  
#         ↓  
#         Chat History  
#         ↓  
#         Chroma Retrieval  
#         ↓  
#         RAG Context  
#         ↓  
#         Gemini  
#         ↓  
#         PostgreSQL  
#         ↓  
#         Answer
#         """
#     )


#     st.markdown("---")


#     # ========================================================
#     # CLEAR CURRENT CHAT
#     # ========================================================

#     if st.button(
#         "🧹 Clear Current Chat",
#         use_container_width=True
#     ):

#         st.session_state.messages = []

#         st.rerun()


#     st.markdown("---")

#     st.caption(
#         "Powered by FastAPI + PostgreSQL + LangChain + Chroma + Gemini"
#     )


# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     """
#     <div style="text-align: center;">

#     <h1>🐍 Python FAQ Assistant</h1>

#     <p>
#         Ask anything about Python and get answers
#         from the FAQ knowledge base.
#     </p>

#     </div>
#     """,
#     unsafe_allow_html=True
# )


# # ============================================================
# # NO CHAT SELECTED
# # ============================================================

# if st.session_state.current_chat_id is None:

#     st.markdown(
#         """
#         ### 👋 Welcome!

#         I can help you find answers from the
#         **Python FAQ dataset**.

#         Try asking:

#         - What is Python?
#         - How do I create a list in Python?
#         - What is a Python dictionary?
#         - How do I install Python?
#         - Is Python difficult for beginners?

#         👈 Select an existing chat or click
#         **➕ New Chat** to start.
#         """
#     )


# # ============================================================
# # DISPLAY CHAT HISTORY
# # ============================================================

# for message in st.session_state.messages:

#     role = message.get(
#         "role",
#         "assistant"
#     )

#     content = message.get(
#         "content",
#         ""
#     )


#     # PostgreSQL may use "user" / "assistant"
#     # which matches Streamlit chat_message.

#     with st.chat_message(
#         role,
#         avatar="🐍" if role == "assistant" else "👤"
#     ):

#         st.markdown(
#             content
#         )


# # ============================================================
# # CHAT INPUT
# # ============================================================

# question = st.chat_input(
#     "💬 Ask a Python question..."
# )


# if question:

#     # --------------------------------------------------------
#     # MAKE SURE CHAT EXISTS
#     # --------------------------------------------------------

#     if st.session_state.current_chat_id is None:

#         st.warning(
#             "Please create a chat first."
#         )

#         st.stop()


#     chat_id = st.session_state.current_chat_id


#     # --------------------------------------------------------
#     # DISPLAY USER MESSAGE
#     # --------------------------------------------------------

#     with st.chat_message(
#         "user",
#         avatar="👤"
#     ):

#         st.markdown(
#             question
#         )


#     # --------------------------------------------------------
#     # ASK BACKEND
#     # --------------------------------------------------------

#     with st.chat_message(
#         "assistant",
#         avatar="🐍"
#     ):

#         with st.spinner(
#             "🔎 Searching FAQ knowledge base..."
#         ):

#             try:

#                 result = ask_question(
#                     chat_id,
#                     question
#                 )


#                 # ------------------------------------------------
#                 # RESPONSE
#                 # ------------------------------------------------

#                 answer = result.get(
#                     "answer",
#                     "I don't know based on the provided FAQs."
#                 )


#                 st.markdown(
#                     answer
#                 )


#                 # ------------------------------------------------
#                 # RETRIEVED DOCUMENTS
#                 # ------------------------------------------------

#                 docs = result.get(
#                     "retrieved_documents",
#                     []
#                 )


#                 if docs:

#                     with st.expander(
#                         f"📚 Retrieved FAQs ({len(docs)})"
#                     ):

#                         for i, doc in enumerate(docs):

#                             # Depending on your backend response,
#                             # documents may be dictionaries.

#                             if isinstance(
#                                 doc,
#                                 dict
#                             ):

#                                 question_text = doc.get(
#                                     "question",
#                                     "Question unavailable"
#                                 )

#                                 answer_text = doc.get(
#                                     "answer",
#                                     "Answer unavailable"
#                                 )

#                             else:

#                                 question_text = "Question unavailable"

#                                 answer_text = str(doc)


#                             st.markdown(
#                                 f"""
#                                 <div class="source-card">

#                                 <div class="source-title">
#                                 Result {i + 1}
#                                 </div>

#                                 <b>Question</b><br>
#                                 {question_text}

#                                 <br><br>

#                                 <b>Answer</b><br>
#                                 {answer_text}

#                                 </div>
#                                 """,
#                                 unsafe_allow_html=True
#                             )


#                 # ------------------------------------------------
#                 # ADD USER + ASSISTANT TO LOCAL STATE
#                 # ------------------------------------------------

#                 st.session_state.messages.append(
#                     {
#                         "role": "user",
#                         "content": question
#                     }
#                 )


#                 st.session_state.messages.append(
#                     {
#                         "role": "assistant",
#                         "content": answer
#                     }
#                 )


#             except requests.exceptions.ConnectionError:

#                 st.error(
#                     "❌ Could not connect to FastAPI. "
#                     "Make sure your backend is running."
#                 )


#             except requests.exceptions.HTTPError as e:

#                 st.error(
#                     f"❌ Backend error: {e}"
#                 )


#             except Exception as e:

#                 st.error(
#                     f"❌ Something went wrong: {e}"
#                 )

import streamlit as st
import requests


# =========================================================
# CONFIG
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Python FAQ Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "chats" not in st.session_state:
    st.session_state.chats = []

if "selected_chat_id" not in st.session_state:
    st.session_state.selected_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_loaded" not in st.session_state:
    st.session_state.chat_loaded = False


# =========================================================
# BACKEND FUNCTIONS
# =========================================================

def get_chats():
    response = requests.get(
        f"{BACKEND_URL}/chats",
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    # Backend returns:
    # {
    #     "chats": [...]
    # }

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

    print("RAW GET MESSAGES RESPONSE:")
    print(data)

    # If backend returns:
    # {"chat_id": 20, "messages": [...]}

    if isinstance(data, dict):

        messages = data.get("messages", [])

        if isinstance(messages, list):
            return messages

        return []

    # If backend directly returns [...]
    elif isinstance(data, list):

        return data

    return []

def ask_chatbot(chat_id, question):

    response = requests.post(
        f"{BACKEND_URL}/chats/{chat_id}/ask",
        json={
            "chat_id": chat_id,
            "role": "user",
            "content": question
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# LOAD CHATS
# =========================================================

if not st.session_state.chats:

    try:
        st.session_state.chats = get_chats()

    except Exception as e:

        st.error(f"Could not load chats: {e}")

        st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💬 Chats")

    st.divider()

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "🟢 New Chat",
        use_container_width=True
    ):

        st.session_state.selected_chat_id = None
        st.session_state.messages = []
        st.session_state.chat_loaded = False

        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # CHAT LIST
    # -----------------------------------------------------

    for chat in st.session_state.chats:

        # Your backend should return dictionaries like:
        #
        # {
        #     "id": 20,
        #     "title": "Learning Python",
        #     "created_at": "..."
        # }

        chat_id = chat.get("id")
        title = chat.get("title", "Untitled Chat")

        if chat_id is None:
            continue

        is_selected = (
            st.session_state.selected_chat_id == chat_id
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

            st.session_state.selected_chat_id = chat_id
            st.session_state.chat_loaded = False
            st.session_state.messages = []

            st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.title("🐍 Python FAQ Assistant")

st.caption(
    "Ask anything about Python and get answers "
    "from the FAQ knowledge base."
)


# =========================================================
# NO CHAT SELECTED
# =========================================================

if st.session_state.selected_chat_id is None:

    st.info(
        "👈 Select an existing chat or click **New Chat** "
        "to start a conversation."
    )

    # -----------------------------------------------------
    # CREATE CHAT
    # -----------------------------------------------------

    st.subheader("Create a new chat")

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

                result = create_chat(
                    chat_title.strip()
                )

                # Backend:
                #
                # {
                #     "chat": {
                #         "id": ...,
                #         "title": ...,
                #         "created_at": ...
                #     }
                # }

                new_chat = result.get("chat")

                if isinstance(new_chat, dict):

                    st.session_state.chats.insert(
                        0,
                        new_chat
                    )

                    st.session_state.selected_chat_id = (
                        new_chat.get("id")
                    )

                    st.session_state.messages = []

                    st.session_state.chat_loaded = True

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


# =========================================================
# SELECTED CHAT
# =========================================================

chat_id = st.session_state.get("selected_chat_id")


# =========================================================
# LOAD SELECTED CHAT
# =========================================================

if chat_id is not None:

    if not st.session_state.get("chat_loaded", False):

        try:

            loaded_messages = get_messages(chat_id)

            print("TYPE:", type(loaded_messages))
            print("VALUE:", loaded_messages)

            st.session_state.messages = loaded_messages

            st.session_state.chat_loaded = True

        except Exception as e:

            st.error(
                f"❌ Could not load chat: {e}"
            )

            st.session_state.messages = []

            st.session_state.chat_loaded = True


# =========================================================
# DISPLAY MESSAGES
# =========================================================

if chat_id is not None:

    for message in st.session_state.messages:

        if not isinstance(message, dict):
            continue

        # Your backend returns LangChain message format
        message_type = message.get("type")
        content = message.get("content")

        if not content:
            continue

        # Human message
        if message_type == "human":

            with st.chat_message(
                "user",
                avatar="👤"
            ):
                st.write(content)

        # AI message
        elif message_type == "ai":

            with st.chat_message(
                "assistant",
                avatar="🐍"
            ):
                st.write(content)


# =========================================================
# NO CHAT SELECTED
# =========================================================

else:

    st.info(
        "👈 Select a chat from the sidebar or create a new chat."
    )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "💬 Ask a Python question..."
)


# =========================================================
# SEND QUESTION
# =========================================================

if question:

    question = question.strip()

    if not question:
        st.stop()

    if chat_id is None:

        st.error(
            "Please select or create a chat first."
        )

        st.stop()

    # =====================================================
    # SHOW USER MESSAGE IMMEDIATELY
    # =====================================================

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.write(question)

    # =====================================================
    # SHOW ASSISTANT LOADING
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="🐍"
    ):

        with st.spinner(
            "🔎 Searching FAQ knowledge base..."
        ):

            try:

                # =========================================
                # CALL BACKEND
                # =========================================

                result = ask_chatbot(
                    chat_id,
                    question
                )

                print(
                    "CHATBOT RESPONSE:",
                    result
                )

                # =========================================
                # GET ANSWER
                # =========================================

                answer = result.get(
                    "answer",
                    "No answer received."
                )

                retrieved_documents = result.get(
                    "retrieved_documents",
                    []
                )

                # =========================================
                # DISPLAY ANSWER
                # =========================================

                st.write(answer)

                # =========================================
                # DISPLAY RAG SOURCES
                # =========================================

                if retrieved_documents:

                    with st.expander(
                        f"📚 Retrieved FAQs "
                        f"({len(retrieved_documents)})"
                    ):

                        for i, doc in enumerate(
                            retrieved_documents,
                            start=1
                        ):

                            st.markdown(
                                f"### Result {i}"
                            )

                            if isinstance(
                                doc,
                                dict
                            ):

                                doc_question = doc.get(
                                    "question",
                                    "Question unavailable"
                                )

                                doc_answer = doc.get(
                                    "answer",
                                    "Answer unavailable"
                                )

                                st.markdown(
                                    f"**Question**\n\n"
                                    f"{doc_question}"
                                )

                                st.markdown(
                                    f"**Answer**\n\n"
                                    f"{doc_answer}"
                                )

                            else:

                                st.write(doc)

                            if i < len(
                                retrieved_documents
                            ):

                                st.divider()

                else:

                    st.caption(
                        "No FAQ documents were retrieved."
                    )

                # =========================================
                # RELOAD DATABASE MESSAGES
                # =========================================

                st.session_state.messages = (
                    get_messages(chat_id)
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

                st.error(
                    f"❌ Something went wrong: {e}"
                )