import uuid
import json
from pgvector import Vector
from dotenv import load_dotenv
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_huggingface import HuggingFaceEmbeddings #type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
from langchain_core.documents import Document
import os


load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# print("\nEmbeddings initialized:", embeddings.embed_query("hi, do you know about deep learning?"))
def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor,
    )
    register_vector(conn)
    return conn

def save_document(document):
    content = document.page_content
    metadata = document.metadata
    question = metadata.get("question", "")
    answer = metadata.get("answer", "")
    embedding = embeddings.embed_query(content)
    document_id = str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO faq_documents( id, question, answer, content, metadata, embedding)
                VALUES ( %s, %s, %s, %s, %s, %s)""",
                ( document_id, question, answer, content, json.dumps(metadata), embedding,)
            )
        conn.commit()
    finally:
        conn.close()
    return document_id

def save_documents(documents):
    for i, document in enumerate( documents, start=1):
        document_id = save_document(document)
        print(
            f"Saved document {i}/{len(documents)} "
            f"→ {document_id}"
        )
        
def similarity_search(query, top_k=4):

    query_embedding = embeddings.embed_query(query)
    # print("\nQuery embedding (pg vectore store):", query_embedding)
    query_embedding = Vector(query_embedding)
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, question, answer, content, metadata, embedding <=> %s AS distance FROM faq_documents ORDER BY embedding <=> %s LIMIT %s
                """, ( query_embedding, query_embedding, top_k))
            rows = cursor.fetchall()
    finally:
        conn.close()
    documents = []
    for row in rows:
        document = Document(
            id=str(row["id"]),
            page_content=row["content"],
            metadata={
                **row["metadata"],
                "distance": float(row["distance"])
            }
        )
        # print(f"Retrieved document: {document.id}")

        documents.append(document)
    print(f"Retrieved {len(documents)} documents from the database.")
    return documents
