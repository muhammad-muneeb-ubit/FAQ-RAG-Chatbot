# from langchain_core.documents import Document
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# from app import GOOGLE_API_KEY
# from config import llm, prompt, format_docs
# import streamlit as st #type: ignore

# load_dotenv()

# st.set_page_config(
#     page_title="Python FAQ Assistant",
#     page_icon="🐍",
#     layout="centered"
# )

# @st.cache_resource
# def load_vectorstore():
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", api_key=GOOGLE_API_KEY)
#     vectorstore = Chroma(
#         persist_directory="./db",
#         embedding_function=embeddings
#     )
#     return vectorstore

# vectorstore = load_vectorstore()

# question = "is it hard to learn python as a begineer?"

# # docs = vectorstore.similarity_search(question, k=3)

# # for i, doc in enumerate(docs):
# #     print("RESULT:", i + 1)
# #     print("Content:", doc.page_content)

# def ask_question(question):

#     docs = vectorstore.similarity_search(question, k=3)

#     context = format_docs(docs)

#     response = (
#         prompt
#         | llm
#         | StrOutputParser()
#     ).invoke({
#         "context": context,
#         "question": question
#     })

#     return response, docs

# # while True:

# #     question = input("\nYou: ")
# #     if question.lower() == "exit":
# #         break
# #     response, docs = ask_question(question)
# #     print("\nAI:", response)
# st.title("🐍 Python FAQ Assistant")

# st.write(
#     "Ask questions about Python and get answers from the FAQ knowledge base."
# )


# # Initialize chat history

# if "messages" not in st.session_state:
#     st.session_state.messages = []


# # Display previous messages

# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):

#         st.markdown(message["content"])


# # Chat input

# question = st.chat_input(
#     "Ask a Python question..."
# )


# if question:

#     # User message

#     st.session_state.messages.append({
#         "role": "user",
#         "content": question
#     })

#     with st.chat_message("user"):
#         st.markdown(question)


#     # Assistant message

#     with st.chat_message("assistant"):
#         with st.spinner("Searching FAQs..."):
#             response, docs = ask_question(question)
#         st.markdown(response)

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": response
#     })


#     # Retrieved documents

#     with st.expander("🔎 Retrieved FAQ Documents"):
#         for i, doc in enumerate(docs):
#             st.markdown(f"### Result {i + 1}")
#             st.markdown(
#                 f"**Question:** "
#                 f"{doc.metadata.get('question', 'N/A')}"
#             )
#             st.markdown(
#                 f"**Answer:** "
#                 f"{doc.metadata.get('answer', 'N/A')}"
#             )
#             st.divider()



import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from config import llm, prompt, format_docs

load_dotenv()

st.set_page_config(
    page_title="Python FAQ Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Main container */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    /* Header */
    .main-header {
        text-align: center;
        padding: 10px 0 25px 0;
    }
    .main-header h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }
    .main-header p {
        font-size: 17px;
        opacity: 0.7;
    }
    /* Welcome card */
    .welcome-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 25px;
    }
    /* FAQ source cards */
    .source-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 12px;
    }
    .source-title {
        font-weight: 600;
        margin-bottom: 8px;
    }
    /* Sidebar */
    .sidebar-title {
        font-size: 22px;
        font-weight: 600;
    }
    /* Chat input */
    [data-testid="stChatInput"] {
        bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def load_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )
    vectorstore = Chroma(
        persist_directory="./db",
        embedding_function=embeddings
    )
    return vectorstore

vectorstore = load_vectorstore()

def ask_question(question):
    docs = vectorstore.similarity_search(
        question,
        k=3
    )
    context = format_docs(docs)
    response = (
        prompt
        | llm
        | StrOutputParser()
    ).invoke(
        {
            "context": context,
            "question": question
        }
    )
    return response, docs

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">🐍 Python FAQ</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        """
        ### About
        This chatbot uses **Retrieval-Augmented Generation (RAG)**
        to answer Python questions from a FAQ knowledge base.
        **Pipeline**
        CSV  
        ↓  
        Documents  
        ↓  
        Embeddings  
        ↓  
        Chroma  
        ↓  
        Semantic Search  
        ↓  
        LLM  
        ↓  
        Answer
        """
    )
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    number_of_results = st.slider(
        "Retrieved FAQs",
        min_value=1,
        max_value=5,
        value=3
    )
    st.markdown("---")
    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption(
        "Powered by LangChain + Chroma + Gemini"
    )

st.markdown(
    """
    <div style="text-align: center;">
    <h1>🐍 Python FAQ Assistant</h1>
    <p>
        Ask anything about Python and get answers
        from the FAQ knowledge base.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
        ### 👋 Welcome!
        I can help you find answers from the Python FAQ dataset.
        Try asking:
        - What is Python?
        - How do I create a list in Python?
        - What is a Python dictionary?
        - How do I install Python?
        - Is Python difficult for beginners?
        </div>
        """,
        unsafe_allow_html=True
    )

for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🐍" if message["role"] == "assistant" else "👤"
    ):
        st.markdown(
            message["content"]
        )
        if (
            message["role"] == "assistant"
            and "docs" in message
        ):
            docs = message["docs"]
            with st.expander(
                f"📚 Retrieved FAQs ({len(docs)})"
            ):
                for i, doc in enumerate(docs):

                    question_text = doc.metadata.get(
                        "question",
                        "Question unavailable"
                    )
                    answer_text = doc.metadata.get(
                        "answer",
                        "Answer unavailable"
                    )
                    st.markdown(
                        f"""
                        <div class="source-card">
                        <div class="source-title">
                        Result {i + 1}
                        </div>

                        <b>Question</b><br>
                        {question_text}
                        <br><br>
                        <b>Answer</b><br>
                        {answer_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
question = st.chat_input(
    "💬 Ask a Python question..."
)

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(question)

    with st.chat_message(
        "assistant",
        avatar="🐍"
    ):
        with st.spinner(
            "🔎 Searching FAQ knowledge base..."
        ):
            try:
                docs = vectorstore.similarity_search(
                    question,
                    k=number_of_results
                )
                context = format_docs(docs)
                response = (
                    prompt
                    | llm
                    | StrOutputParser()
                ).invoke(
                    {
                        "context": context,
                        "question": question
                    }
                )
                st.markdown(response)

                with st.expander(
                    f"📚 Retrieved FAQs ({len(docs)})"
                ):
                    for i, doc in enumerate(docs):
                        question_text = doc.metadata.get(
                            "question",
                            "Question unavailable"
                        )
                        answer_text = doc.metadata.get(
                            "answer",
                            "Answer unavailable"
                        )
                        st.markdown(
                            f"""
                            <div class="source-card">
                            <div class="source-title">
                            Result {i + 1}
                            </div>
                            <b>Question</b><br>
                            {question_text}
                            <br><br>
                            <b>Answer</b><br>
                            {answer_text}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "docs": docs
                    }
                )
            except Exception as e:
                st.error(
                    f"Something went wrong: {e}"
                )