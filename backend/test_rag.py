from rag import ask_question, vectorstore

print("Collection count:")
print(vectorstore._collection.count())

question = "What is a Python dictionary?"

response, docs = ask_question(question, k=3)

print("\nAI RESPONSE:")
print(response)

print("\nRETRIEVED DOCUMENTS:")

for i, doc in enumerate(docs):
    print(f"\n--- Result {i + 1} ---")
    print("Question:", doc.metadata.get("question"))
    print("Answer:", doc.metadata.get("answer"))