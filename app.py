import pandas as pd
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings #type: ignore
import os
load_dotenv()
from backend.pgvector_store import save_documents


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

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print(f"Total documents: {len(documents)}")

# uncomment this line to save documents to the database
# if runs multiple times, it will create duplicates in the database
# save_documents(documents)  

print("\nAll documents saved.")

# vector_store = Chroma.from_documents(
#     documents=documents,
#     embedding=embeddings,
#     persist_directory="./vector_store2"
# )
# print("\nDB Collection count:", vector_store._collection.count())


