import pandas as pd
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
# df = pd.read_csv("data/faq_dataset.csv",  encoding="latin1")
df = pd.read_csv("data/python_ai_ml_faq_dataset.csv",  encoding="latin1")

documents = []
for _, row in df.iterrows():
    content = f"""
        Question: {row['Question']}
        Answer: {row['Answer']}      
    """
    metadata = {
        "source": "python_ai_ml_faq_dataset.csv",
        "question": row['Question'],
        "answer": row['Answer'],
    }
    documents.append(
        Document(
            page_content=content,
            metadata=metadata
        )
    )

# print("Documents created with", len(documents), "documents.")
# print("First document:", documents[0].page_content if documents else "No documents found.")

embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, api_key=GOOGLE_API_KEY)

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./db"
)
print("DB Collection count:", vector_store._collection.count())


