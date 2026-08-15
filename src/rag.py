import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set."
    )


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


# ---------------------------------------------------------
# BUILD CONTEXT
# ---------------------------------------------------------

def build_context(chunks):
    """
    Convert retrieved chunks into a context string
    for the language model.
    """

    if not chunks:
        return "No relevant document information was found."

    context_parts = []

    for number, chunk in enumerate(
        chunks,
        start=1
    ):

        source = chunk.get(
            "source",
            "Unknown"
        )

        page = chunk.get(
            "page"
        )

        slide = chunk.get(
            "slide"
        )

        text = chunk.get(
            "text",
            ""
        )

        location = ""

        if page is not None:
            location = f", page {page}"

        elif slide is not None:
            location = f", slide {slide}"

        context_parts.append(
            f"[Source {number}: "
            f"{source}{location}]\n"
            f"{text}"
        )

    return "\n\n".join(context_parts)


# ---------------------------------------------------------
# GENERATE ANSWER
# ---------------------------------------------------------

def answer_question(query, chunks):
    """
    Generate an answer using only the retrieved
    document chunks.
    """

    if not query or not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    context = build_context(chunks)

    prompt = f"""
You are a research assistant.

Answer the user's question using ONLY the
information provided in the document context.

Do not invent information that is not present
in the context.

If the context does not contain enough information
to answer the question, clearly say that the
provided documents do not contain enough information.

When possible, mention the source document and
page number used for the answer.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    response = llm.invoke(prompt)

    return response.content