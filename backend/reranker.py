from sentence_transformers import CrossEncoder #type: ignore

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)

def rerank_documents( query, documents, top_k=2, threshold=0.60):
    """
    Rerank retrieved documents based on relevance
    to the user's query.
    """
    if not documents:
        return []
    pairs = []
    for document in documents:
        if hasattr(document, "page_content"):
            document_text = document.page_content
        elif isinstance(document, dict):
            document_text = document.get(
                "page_content",
                ""
            )
        else:
            document_text = str(document)
        pairs.append(
            (query, document_text)
        )

    scores = reranker_model.predict(
        pairs
    )

    scored_documents = list(
        zip(documents, scores)
    )

    scored_documents.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # top_documents = scored_documents[:top_k]

    # return [
    #     {
    #         "document": document,
    #         "rerank_score": float(score)
    #     }
    #     for document, score in top_documents
    # ]
    if threshold is not None:
        scored_documents_with_threshold = [
            (document, score)
            for document, score in scored_documents
            if score >= threshold
        ]

    # Then limit number of documents
    scored_documents = scored_documents_with_threshold[:top_k]

    return [
        {
            "document": document,
            "rerank_score": float(score)
        }
        for document, score in scored_documents_with_threshold
    ]