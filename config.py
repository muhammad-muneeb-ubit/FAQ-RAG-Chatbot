from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st # type: ignore

@st.cache_resource
def load_llm():

    return ChatGoogleGenerativeAI(
        model="models/gemma-4-31b-it",
        temperature=0
    )
llm = load_llm()
prompt = ChatPromptTemplate.from_template(
"""
You are a Python FAQ assistant.

Answer the user's question ONLY using the provided FAQ context. Use this context to answer the question in your wordings in good way. 

If the answer cannot be found in the context, say:

"I don't know based on the provided FAQs."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""
)
def format_docs(docs):

    return "\n\n".join(
        f"Question: {doc.metadata.get('question', '')}\n"
        f"Answer: {doc.metadata.get('answer', '')}"
        for doc in docs
    )
