import os
from dotenv import load_dotenv
from langchain_google_genai import ( GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI)
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typer.cli import docs
from pathlib import Path

from backend.chat_history import format_chat_history

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db"

# print("Chroma DB:", DB_PATH)
load_dotenv()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LLM_MODEL = os.getenv("LLM_MODEL")

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    persist_directory= DB_PATH,
    embedding_function=embeddings
)
llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful Python FAQ assistant.

Use the retrieved FAQ context and conversation history
to answer the user's question.

If the answer is available in the retrieved context,
answer using that information.

If the answer is not available in the retrieved context,
say:

"I don't know based on the provided FAQs."

Do not make up information.

Conversation History:
{chat_history}

Retrieved FAQ Context:
{context}

Current Question:
{question}
""")

def format_docs(docs):
    return "\n\n".join(
        [
            f"Question: {doc.metadata.get('question', '')}\n"
            f"Answer: {doc.metadata.get('answer', '')}"
            for doc in docs
        ]
    )
def ask_question(question: str, chat_history, k: int = 3):
    docs = vectorstore.similarity_search(
        question,
        k=k
    )
    context = format_docs(docs)
    history = format_chat_history(chat_history)
    # print("Retrieved context:\n", context)
    chain = ( prompt | llm | StrOutputParser())
    response = chain.invoke(
        {
            "chat_history": history,
            "context": context,
            "question": question
        }
    )
    return response, docs