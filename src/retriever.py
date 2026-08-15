from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# ---------------------------------------------------------
# EMBEDDING MODEL
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)


# ---------------------------------------------------------
# CREATE VECTOR STORE
# ---------------------------------------------------------

def create_vector_store(chunks):
    """
    Convert document chunks into embeddings
    and store them in a FAISS vector index.

    Args:
        chunks: List of dictionaries produced by
                document_processor.process_documents()

    Returns:
        index: FAISS vector index
        chunks: Original chunks with metadata
    """

    if not chunks:
        raise ValueError("No chunks were provided.")

    # Extract only the text from each chunk
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # Convert text into embedding vectors
    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # FAISS expects float32
    embeddings = embeddings.astype("float32")

    # Get vector dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    # Inner Product + normalized vectors ≈ cosine similarity
    index = faiss.IndexFlatIP(dimension)

    # Store embeddings in FAISS
    index.add(embeddings)

    return index, chunks


# ---------------------------------------------------------
# RETRIEVE RELEVANT CHUNKS
# ---------------------------------------------------------

def retrieve_documents(index, chunks, query, k=5):
    """
    Retrieve the most relevant chunks for a query.

    Args:
        index: FAISS vector index
        chunks: Original document chunks
        query: User's question
        k: Number of results to return

    Returns:
        List of relevant chunks with similarity scores
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not chunks:
        return []

    # Convert user's question into an embedding
    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = query_embedding.astype("float32")

    # Don't request more results than available chunks
    k = min(k, len(chunks))

    # Search the FAISS index
    scores, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        # Recover the original chunk and its metadata
        chunk = chunks[index_position].copy()

        # Add similarity score
        chunk["score"] = float(score)

        results.append(chunk)

    return results