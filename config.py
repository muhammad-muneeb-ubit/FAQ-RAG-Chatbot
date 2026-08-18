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
# """
# You are a Python FAQ assistant.

# Answer the user's question ONLY using the provided FAQ context. Use this context to answer the question in your wordings in good way. 

# If the answer cannot be found in the context, say:

# "I don't know based on the provided FAQs."

# Do not make up information.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
"""
You are a Python FAQ assistant.

Answer the user's question ONLY using the provided FAQ context. Use this context to answer the question in your wordings in good way.

Rules:
1. Use only information present in the provided context.
2. Do not use your own knowledge or make up information.
3. If the question contains multiple topics, answer each topic separately.
4. If the context supports one topic but does not support another:
   - Answer the supported topic.
   - For the unsupported topic, say:
     "I don't know based on the provided FAQs."
5. If none of the requested topics are supported, say:
   "I don't know based on the provided FAQs."
6. If the answer found for all topics is too long, summarize it in a concise manner and provide the summary as the answer.
7. Do not assume that a vaguely related document answers the question.
8. Keep answers concise and clear.

Context:
{context}

Question:
{question}"""
)
def format_docs(docs):

    return "\n\n".join(
        f"Question: {doc.metadata.get('question', '')}\n"
        f"Answer: {doc.metadata.get('answer', '')}"
        for doc in docs
    )
