from src.document_processor import process_documents
from src.retriever import (
    create_vector_store,
    retrieve_documents
)
from src.rag import answer_question


def main():

    print("=" * 60)
    print("RAG SYSTEM TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # STEP 1: Get documents
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
        # STEP 2: Process documents
        # -------------------------------------------------

        print("\nProcessing documents...")

        chunks = process_documents(paths)

        print(
            f"Created {len(chunks)} chunks."
        )

        # -------------------------------------------------
        # STEP 3: Create vector store
        # -------------------------------------------------

        print(
            "\nCreating vector store..."
        )

        index, stored_chunks = create_vector_store(
            chunks
        )

        print(
            "Vector store created successfully."
        )

        # -------------------------------------------------
        # STEP 4: Ask question
        # -------------------------------------------------

        query = input(
            "\nEnter your question:\n"
        )

        # -------------------------------------------------
        # STEP 5: Retrieve relevant chunks
        # -------------------------------------------------

        print(
            "\nRetrieving relevant information..."
        )

        results = retrieve_documents(
            index,
            stored_chunks,
            query,
            k=5
        )

        print(
            f"Retrieved {len(results)} relevant chunks."
        )

        # -------------------------------------------------
        # STEP 6: Generate answer
        # -------------------------------------------------

        print(
            "\nGenerating answer..."
        )

        answer = answer_question(
            query,
            results
        )

        # -------------------------------------------------
        # STEP 7: Display answer
        # -------------------------------------------------

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(answer)

        print("=" * 60)

    except Exception as error:

        print("\nERROR:")
        print(error)


if __name__ == "__main__":
    main()