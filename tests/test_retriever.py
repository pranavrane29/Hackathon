from src.document_processor import process_documents
from src.retriever import (
    create_vector_store,
    retrieve_documents
)


def main():

    print("=" * 60)
    print("EMBEDDING + RETRIEVAL TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # STEP 1: Get document paths
    # -----------------------------------------------------

    paths = input(
        "\nEnter document paths separated by commas:\n"
    ).split(",")

    paths = [
        path.strip()
        for path in paths
        if path.strip()
    ]

    if not paths:
        print("No documents provided.")
        return

    try:

        # -------------------------------------------------
        # STEP 2: Process multiple documents
        # -------------------------------------------------

        print("\nProcessing documents...")

        chunks = process_documents(paths)

        print(
            f"Created {len(chunks)} chunks."
        )

        # -------------------------------------------------
        # STEP 3: Create embeddings + FAISS store
        # -------------------------------------------------

        print(
            "\nCreating embeddings and vector store..."
        )

        index, stored_chunks = create_vector_store(
            chunks
        )

        print(
            "Vector store created successfully."
        )

        # -------------------------------------------------
        # STEP 4: Ask a question
        # -------------------------------------------------

        query = input(
            "\nEnter your question:\n"
        )

        # -------------------------------------------------
        # STEP 5: Retrieve relevant chunks
        # -------------------------------------------------

        results = retrieve_documents(
            index,
            stored_chunks,
            query,
            k=5
        )

        # -------------------------------------------------
        # STEP 6: Display results
        # -------------------------------------------------

        print("\n" + "=" * 60)
        print("RETRIEVAL RESULTS")
        print("=" * 60)

        if not results:
            print("No relevant results found.")
            return

        for number, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\nResult {number}"
            )

            print(
                f"Source: {result.get('source')}"
            )

            print(
                f"Page: {result.get('page')}"
            )

            print(
                f"Slide: {result.get('slide')}"
            )

            print(
                f"Similarity: "
                f"{result.get('score', 0):.4f}"
            )

            print("\nText:")

            print(
                result["text"][:500]
            )

            print("-" * 60)

    except Exception as error:

        print("\nERROR:")
        print(error)


if __name__ == "__main__":
    main()