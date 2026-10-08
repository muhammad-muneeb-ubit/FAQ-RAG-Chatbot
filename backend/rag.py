
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from backend.chat_history import format_chat_history
from backend.reranker import rerank_documents
from backend.pgvector_store import similarity_search
from backend.log import logger
import time
from backend.config import llm, rewrite_llm




# prompt = ChatPromptTemplate.from_template("""
# You are a Python FAQ assistant.

# Answer the current question using only the retrieved FAQ context.

# Rules:
# - Use conversation history only to understand context.
# - Do not use knowledge outside the FAQ context.
# - Do not invent or assume information.
# - If the answer is not supported by the context, reply exactly:
# "I don't know based on the provided FAQs."

# Conversation History:
# {chat_history}

# FAQ Context:
# {context}

# Question:
# {question}

# Answer:
# """)

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
    formatted_docs = []

    for item in docs:
        # Reranker result
        if isinstance(item, dict) and "document" in item:
            doc = item["document"]

        # Normal LangChain Document
        else:
            doc = item

        formatted_docs.append(
            f"Question: {doc.metadata.get('question', '')}\n"
            f"Answer: {doc.metadata.get('answer', '')}"
        )

    return "\n\n".join(formatted_docs)

def ask_question(question: str, chat_history, original_question, k: int = 4):
    logger.info("Calling similarity search for question: %s", question)
    start = time.perf_counter()
    results = similarity_search( question, top_k=k)
    elapsed = time.perf_counter() - start
    logger.info(f"Similarity search completed in {elapsed}s (from rag.py)")
    # print(f"Retrieved {len(results)} documents from the database. (rag.py backend)")
    
    logger.info("Calling reranker function")
    start = time.perf_counter()
    reranked_docs = rerank_documents( query=question, documents=results, top_k=2)
    elapsed = time.perf_counter() - start
    logger.info(f"Reranking completed in {elapsed}s (from rag.py)")
    
    # print(f"Reranked {len(reranked_docs)} documents. (rag.py backend)")
    logger.info("Formatting reranked documents")
    start = time.perf_counter()
    context = format_docs(reranked_docs)
    elapsed = time.perf_counter() - start
    logger.info(f"Context formatting completed in {elapsed}s (from rag.py)")
    # print("\nRetrieved context:(rag.py backend)\n", context)
    history = format_chat_history(chat_history)
    # print("\nHistory: (rag.py backend)\n", history)
    # print("\nRetrieved context:\n", context)
    chain = ( prompt | llm | StrOutputParser())
    logger.info("Calling LLM with formatted context")
    start = time.perf_counter()
    try:
        response = chain.invoke(
            {
                "chat_history": history,
                "context": context,
                "question": question,
                "original_question": original_question
            }
        )
    except Exception as e:
        logger.error(f"Error occurred while invoking LLM: {e}")
        raise
    elapsed = time.perf_counter() - start
    logger.info(f"LLM response generated in {elapsed}s (from rag.py)")
    # print("\nResponse: (rag.py backend)\n", response)
    # print("\nresults: (rag.py backend)\n", results[0])
    # print("\nreranked_docs: (rag.py backend)\n", reranked_docs)
    return response, results, reranked_docs

def ask_question_stream(question: str, chat_history, original_question, k: int = 4):
    logger.info("Calling similarity search for question: %s", question)
    start = time.perf_counter()
    results = similarity_search( question, top_k=k)
    elapsed = time.perf_counter() - start
    logger.info( "Similarity search completed in %ss", elapsed)
    logger.info("Calling reranker function")
    start = time.perf_counter()
    reranked_docs = rerank_documents( query=question, documents=results, top_k=2)
    elapsed = time.perf_counter() - start
    logger.info( "Reranking completed in %ss", elapsed)
    logger.info("Formatting reranked documents")
    start = time.perf_counter()
    context = format_docs(reranked_docs)
    elapsed = time.perf_counter() - start
    logger.info( "Context formatting completed in %ss", elapsed)
    history = format_chat_history(chat_history)

    chain = prompt | llm | StrOutputParser()
    logger.info("Starting LLM streaming")
    llm_start  = time.perf_counter()
    try:
        stream = chain.stream(
            {
                "chat_history": history,
                "context": context,
                "question": question,
                "original_question": original_question
            }
        )

        logger.info(
            "LLM streaming started"
        )

        return stream, results, reranked_docs, llm_start

    except Exception as e:

        logger.exception(
            "Error occurred while starting LLM stream"
        )

        raise

def rewrite_query(user_question, llm):
#     prompt = f"""
#         Rewrite the user's question into a concise search query for a Python FAQ database.

#         Rules:
#         - Preserve the meaning.
#         - Remove greetings and filler.
#         - Keep important technical terms.
#         - Do not answer the question.
#         - Return only the rewritten query. 

#         Question:
#         {user_question}
# """
    prompt = f"""
You are a search query optimizer for a multilingual Python FAQ database.

Rewrite the user's question into a concise search query for document retrieval.

Rules:
- Preserve the exact meaning.
- Do not answer the question.
- Remove greetings and unnecessary filler.
- Keep important technical terms.
- Preserve technical names such as Python, NumPy, Pandas,
  TensorFlow, SQL, API, RAG, LangChain, etc.
- If the user's language is not English, you may translate
  the query into concise English to improve retrieval.
- Do not translate or change technical terms unnecessarily.
- Return ONLY the search query.
- Do not add explanations.
- Do not add labels.

User question:
{user_question}
"""
    
    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(str(text))
        content = "".join(parts)
    if not isinstance(content, str):
        content = str(content)
    # print("Rewritten query: (rag.py backend)", content)
    return content.strip()
