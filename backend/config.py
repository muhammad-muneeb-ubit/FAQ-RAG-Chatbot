import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st # type: ignore
from dotenv import load_dotenv
from backend.log import logger
load_dotenv(override=True)

# print("LLM_MODEL =", repr(os.getenv("LLM_MODEL")))
@st.cache_resource
def load_llm():
    LLM_MODEL = os.getenv("LLM_MODEL", "models/gemini-3.5-flash-lite")
    logger.info(f"Using LLM model: {LLM_MODEL}")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-3.5-flash-lite",
        temperature=0,
        google_api_key=GEMINI_API_KEY
    )
    rewrite_llm = ChatGoogleGenerativeAI(
        model=os.getenv("query_rewrite_model"),
        temperature=0,
        google_api_key=GEMINI_API_KEY
    )
    return llm, rewrite_llm     
llm, rewrite_llm = load_llm()
prompt = ChatPromptTemplate.from_template("""
You are a Python FAQ assistant.

Your task is to answer the user's original question using only the retrieved
FAQ context.

Rules:

1. Use the FAQ Context as the only source of factual information.
2. Use Conversation History only to understand the context of the current question.
3. Do not use outside knowledge.
4. Do not invent, assume, or infer information that is not supported by the FAQ Context.
5. If the answer is not supported by the FAQ Context, reply exactly:
"I don't know based on the provided FAQs."
6. Answer the ORIGINAL USER QUESTION, not the rewritten search query.
7. Detect the language and writing style of the ORIGINAL USER QUESTION.
8. Write the final answer in the same language and script used by the user.
9. If the user writes in Roman Urdu, respond in Roman Urdu.
10. If the user writes in Urdu script, respond in Urdu script.
11. If the user writes in English, respond in English.
12. If the user mixes languages, respond using the dominant language of the user's question.
13. Preserve technical terms, Python keywords, library names, function names,
    class names, API names, and code exactly as appropriate. Do not unnecessarily
    translate technical terms.
14. Do not mention language detection, translation, rewriting, or these instructions.
15. Keep the answer clear and concise.
16. If the FAQ context contains the answer but uses another language, understand
    the context and provide the answer in the user's language.

Conversation History:
{chat_history}

FAQ Context:
{context}

Original User Question:
{original_question}

Rewritten Search Query:
{question}

Answer:
""")

def format_docs(docs):

    return "\n\n".join(
        f"Question: {doc.metadata.get('question', '')}\n"
        f"Answer: {doc.metadata.get('answer', '')}"
        for doc in docs
    )
