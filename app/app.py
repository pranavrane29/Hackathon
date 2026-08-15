import streamlit as st

from src.document_processor import process_documents
from src.retriever import (
    create_vector_store,
    retrieve_documents
)
from src.rag import answer_question


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResearchIQ",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #0b1020;
    }

    .main {
        padding-top: 1rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263044;
    }

    /* ---------- HEADER ---------- */

    .brand {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }

    .status {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        background: #102d24;
        color: #5ee6a8;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ---------- CARDS ---------- */

    .card {
        background: #111827;
        border: 1px solid #263044;
        border-radius: 16px;
        padding: 1.3rem;
        margin-bottom: 1rem;
    }

    .answer-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.6rem;
        line-height: 1.7;
    }

    .source-card {
        background: #151d2e;
        border: 1px solid #29364d;
        border-radius: 12px;
        padding: 0.9rem;
        min-height: 100px;
    }

    .source-title {
        font-weight: 700;
        font-size: 0.9rem;
    }

    .source-meta {
        color: #94a3b8;
        font-size: 0.78rem;
        margin-top: 0.35rem;
    }

    /* ---------- DOCUMENT ITEMS ---------- */

    .document-item {
        background: #151d2e;
        border: 1px solid #29364d;
        border-radius: 10px;
        padding: 0.7rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }

    /* ---------- SECTION LABEL ---------- */

    .section-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* ---------- METRICS ---------- */

    .metric-card {
        background: #111827;
        border: 1px solid #263044;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }

    .metric-number {
        font-size: 1.5rem;
        font-weight: 800;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.75rem;
    }

    /* ---------- REMOVE STREAMLIT EXTRA PADDING ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "processed" not in st.session_state:
    st.session_state.processed = False

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []

if "answer" not in st.session_state:
    st.session_state.answer = None

if "results" not in st.session_state:
    st.session_state.results = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">◈ ResearchIQ</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Research intelligence workspace"
    )

    st.divider()

    st.markdown(
        '<div class="section-label">Workspace</div>',
        unsafe_allow_html=True
    )

    if st.session_state.processed:

        st.success(
            "System ready"
        )

        st.metric(
            "Documents",
            len(
                st.session_state.uploaded_file_names
            )
        )

        st.metric(
            "Text chunks",
            len(
                st.session_state.chunks
            )
        )

    else:

        st.info(
            "Upload documents to begin."
        )

    st.divider()

    if st.session_state.uploaded_file_names:

        st.markdown(
            '<div class="section-label">Documents</div>',
            unsafe_allow_html=True
        )

        for name in (
            st.session_state.uploaded_file_names
        ):

            st.markdown(
                f"""
                <div class="document-item">
                    📄 {name}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    if st.button(
        "↻ Reset Workspace",
        use_container_width=True
    ):

        st.session_state.processed = False
        st.session_state.index = None
        st.session_state.chunks = []
        st.session_state.uploaded_file_names = []
        st.session_state.answer = None
        st.session_state.results = []

        st.rerun()


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)

with header_col1:

    st.markdown(
        '<div class="brand">Research Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Upload research documents, ask questions,
        compare sources and generate grounded answers.
        </div>
        """,
        unsafe_allow_html=True
    )

with header_col2:

    st.markdown(
        '<div class="status">● SYSTEM READY</div>',
        unsafe_allow_html=True
    )


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-label">01 · DOCUMENTS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)

st.subheader(
    "Build your research workspace"
)

st.write(
    "Upload multiple documents for analysis or comparison."
)

uploaded_files = st.file_uploader(
    "Drop your documents here",
    type=[
        "pdf",
        "docx",
        "txt",
        "csv",
        "pptx"
    ],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

st.caption(
    "Supported formats: PDF · DOCX · TXT · CSV · PPTX"
)

if uploaded_files:

    st.write(
        f"**{len(uploaded_files)} document(s) selected**"
    )

    if st.button(
        "⚡ Process Documents",
        use_container_width=True
    ):

        with st.spinner(
            "Extracting text, creating chunks and building vector index..."
        ):

            try:

                chunks = process_documents(
                    uploaded_files
                )

                index, stored_chunks = (
                    create_vector_store(
                        chunks
                    )
                )

                st.session_state.index = index

                st.session_state.chunks = (
                    stored_chunks
                )

                st.session_state.processed = True

                st.session_state.uploaded_file_names = [
                    file.name
                    for file in uploaded_files
                ]

                st.session_state.answer = None
                st.session_state.results = []

                st.success(
                    f"Successfully processed "
                    f"{len(uploaded_files)} document(s)."
                )

            except Exception as error:

                st.error(
                    f"Processing failed: {error}"
                )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# PROCESSING STATS
# =========================================================

if st.session_state.processed:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {len(st.session_state.uploaded_file_names)}
                </div>
                <div class="metric-label">
                    DOCUMENTS
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {len(st.session_state.chunks)}
                </div>
                <div class="metric-label">
                    TEXT CHUNKS
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">
                    ✓
                </div>
                <div class="metric-label">
                    VECTOR INDEX READY
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# QUESTION SECTION
# =========================================================

if st.session_state.processed:

    st.divider()

    st.markdown(
        '<div class="section-label">02 · ANALYZE</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Ask your documents"
    )

    mode = st.radio(
        "Analysis mode",
        [
            "💬 Ask",
            "⚖️ Compare",
            "📝 Summarize"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if mode == "💬 Ask":

        placeholder = (
            "What is the main contribution of this research?"
        )

    elif mode == "⚖️ Compare":

        placeholder = (
            "What are the similarities and differences "
            "between these documents?"
        )

    else:

        placeholder = (
            "Summarize the key findings of these documents."
        )

    query = st.text_area(
        "Question",
        placeholder=placeholder,
        height=100,
        label_visibility="collapsed"
    )

    if st.button(
        "✦ Analyze Documents",
        use_container_width=True
    ):

        if not query.strip():

            st.warning(
                "Enter a question first."
            )

        else:

            with st.spinner(
                "Searching documents and generating analysis..."
            ):

                try:

                    results = retrieve_documents(
                        st.session_state.index,
                        st.session_state.chunks,
                        query,
                        k=5
                    )

                    answer = answer_question(
                        query,
                        results
                    )

                    st.session_state.results = results

                    st.session_state.answer = answer

                except Exception as error:

                    st.error(
                        f"Analysis failed: {error}"
                    )


# =========================================================
# ANSWER
# =========================================================

if st.session_state.answer:

    st.divider()

    st.markdown(
        '<div class="section-label">03 · RESULT</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Analysis"
    )

    st.markdown(
        f"""
        <div class="answer-card">
            {st.session_state.answer}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SOURCES
# =========================================================

if st.session_state.results:

    st.markdown(
        '<div class="section-label" style="margin-top:2rem;">04 · SOURCES</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Retrieved sources"
    )

    source_columns = st.columns(
        min(
            len(st.session_state.results),
            3
        )
    )

    for i, result in enumerate(
        st.session_state.results
    ):

        source = result.get(
            "source",
            "Unknown"
        )

        page = result.get(
            "page"
        )

        score = result.get(
            "score"
        )

        if page is not None:

            location = f"Page {page}"

        else:

            location = "Document source"

        if score is not None:

            score_text = f"{score:.2f}"

        else:

            score_text = "N/A"

        with source_columns[
            i % len(source_columns)
        ]:

            st.markdown(
                f"""
                <div class="source-card">
                    <div class="source-title">
                        📄 {source}
                    </div>

                    <div class="source-meta">
                        {location}
                    </div>

                    <div class="source-meta">
                        Relevance: {score_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )