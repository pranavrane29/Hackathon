# 📚 ResearchIQ

> **An intelligent multi-document research assistant powered by Retrieval-Augmented Generation (RAG)**

ResearchIQ is a document intelligence platform designed to help users **upload, process, retrieve, compare, and question multiple documents through a unified AI-powered interface**.

Instead of treating every uploaded document as an isolated file, ResearchIQ builds a searchable knowledge base from the uploaded content and uses semantic retrieval to identify the most relevant information before generating an answer.

The result is a complete pipeline connecting **document processing → text chunking → embeddings → vector retrieval → RAG-based answer generation → source-aware presentation** in one application.

---

## ✨ Why ResearchIQ?

Modern research often means dealing with multiple PDFs, presentations, text files, reports, and datasets at the same time. Finding relationships between them manually is slow, repetitive, and prone to missing important information.

ResearchIQ addresses this by allowing users to:

- 📄 Upload multiple documents at once
- 🔍 Search documents using semantic similarity rather than simple keyword matching
- 🧠 Ask questions about the uploaded knowledge base
- ⚖️ Compare information across multiple documents
- 📝 Generate document-based summaries
- 📚 View the retrieved sources behind an answer
- 🚫 Reduce unsupported answers by grounding generation in retrieved document content

The project was designed as a modular pipeline so that each major component can be developed, tested, and improved independently.

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                ┌─────────────────────┐
                │   Streamlit UI      │
                │     app/app.py      │
                └──────────┬──────────┘
                           │
                    Upload Documents
                           │
                           ▼
                ┌─────────────────────┐
                │ Document Processor  │
                │ src/                │
                │ document_processor  │
                └──────────┬──────────┘
                           │
                     Extracted Text
                           │
                           ▼
                ┌─────────────────────┐
                │ Text Chunking       │
                │ Recursive Splitter  │
                └──────────┬──────────┘
                           │
                         Chunks
                           │
                           ▼
                ┌─────────────────────┐
                │ Embedding Model     │
                │ SentenceTransformers│
                └──────────┬──────────┘
                           │
                       Embeddings
                           │
                           ▼
                ┌─────────────────────┐
                │ FAISS Vector Store  │
                │ Semantic Retrieval  │
                └──────────┬──────────┘
                           │
                  Relevant Chunks
                           │
                           ▼
                ┌─────────────────────┐
                │ RAG Pipeline        │
                │ src/rag.py          │
                └──────────┬──────────┘
                           │
                     Context + Query
                           │
                           ▼
                ┌─────────────────────┐
                │ Groq LLM            │
                │ Answer Generation   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Answer + Sources    │
                │      UI             │
                └─────────────────────┘
```

---

# 🔄 End-to-End Workflow

## 1. Document Upload

The user uploads one or multiple supported files through the Streamlit interface.

### Supported formats

| Format | Supported |
|---|---|
| PDF | ✅ |
| DOCX | ✅ |
| TXT | ✅ |
| CSV | ✅ |
| PPTX | ✅ |

Multiple documents can be uploaded simultaneously, enabling cross-document analysis.

---

## 2. Document Processing

The document processor identifies the file type and extracts its textual content.

The processor accepts both uploaded-file objects and normal file paths, making it useful for both the Streamlit application and local testing.

The extracted text is normalized into a common representation before being passed to the chunking stage.

### Main module

```text
src/document_processor.py
```

### Main entry point

```python
process_documents(files)
```

---

## 3. Text Chunking

Large documents are divided into smaller overlapping chunks.

The project uses:

```text
RecursiveCharacterTextSplitter
```

with an overlapping-window strategy so that relevant context is less likely to be lost at chunk boundaries.

This produces manageable units of text for semantic embedding and retrieval.

---

## 4. Embedding Generation

Each chunk is converted into a numerical vector representation using a Sentence Transformers embedding model.

Conceptually:

```text
Document text
     ↓
Text chunk
     ↓
Embedding model
     ↓
Numerical vector
```

Semantically similar pieces of information produce vectors that are close to one another in embedding space.

---

## 5. Vector Retrieval

The generated embeddings are indexed using **FAISS**.

When a user asks a question:

```text
User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Top Relevant Chunks
```

This allows the system to retrieve relevant information even when the wording of the question differs from the wording used inside the documents.

### Main module

```text
src/retriever.py
```

---

## 6. Retrieval-Augmented Generation

The retrieved chunks are passed to the RAG layer along with the user's question.

The system therefore does not simply ask the language model to answer from its general knowledge.

Instead:

```text
Question
   +
Retrieved Document Context
   ↓
RAG Prompt
   ↓
LLM
   ↓
Grounded Answer
```

The project uses **Groq** through the `langchain-groq` integration for answer generation.

### Main module

```text
src/rag.py
```

---

## 7. Streamlit Interface

The final interaction happens through a Streamlit-based web interface.

The interface provides:

- 🎨 Modern research workspace
- 📤 Multi-file upload
- ⚙️ Processing feedback
- 📊 Document statistics
- 💬 Ask mode
- ⚖️ Compare mode
- 📝 Summarize mode
- 🧠 Generated answer display
- 📚 Retrieved source display
- 🔄 Workspace reset functionality

### Main application

```text
app/app.py
```

---

# 🧩 Project Structure

```text
Hackathon/
│
├── app/
│   └── app.py
│
├── src/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── retriever.py
│   └── rag.py
│
├── tests/
│   ├── __init__.py
│   ├── test_document_processor.py
│   ├── test_retriever.py
│   └── test_rag.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The project follows a modular structure so that the application layer, processing layer, retrieval layer, and generation layer remain separated.

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Programming Language | Python |
| PDF Processing | pypdf |
| DOCX Processing | python-docx |
| Spreadsheet/Data Processing | pandas |
| PPTX Processing | python-pptx |
| Text Chunking | LangChain Text Splitters |
| Embeddings | Sentence Transformers |
| Vector Database / Index | FAISS |
| RAG / LLM Integration | LangChain + Groq |
| Configuration | python-dotenv |
| Version Control | Git + GitHub |

---

# 🚀 Running the Project Locally

## Prerequisites

Make sure the following are installed:

- Python 3.12 recommended
- Git
- `uv` package manager
- A Groq API key

---

## 1. Clone the repository

```bash
git clone https://github.com/pranavrane29/Hackathon.git
cd Hackathon
```

---

## 2. Create a virtual environment

Using `uv`:

```bash
uv venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
uv pip install -r requirements.txt --link-mode=copy
```

---

## 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=Did you really thought?
```

**Never commit `.env` or API keys to GitHub.**

---

## 5. Run the application

From the repository root:

```bash
python -m streamlit run app/app.py
```

The application will normally be available at:

```text
https://hackathon-rqqwtrtyw9ltqc6ho3xn5z.streamlit.app/
```

---

# 🧪 Testing

The project includes separate test scripts for the major pipeline components.

### Document processing

```bash
python -m tests.test_document_processor
```

### Retrieval

```bash
python -m tests.test_retriever
```

### RAG pipeline

```bash
python -m tests.test_rag
```

The RAG test supports multiple document paths and allows a question to be asked against the generated vector store.

---

# 🔐 Security

Sensitive credentials should never be stored in source code or committed to GitHub.

For local development:

```text
.env
```

For Streamlit deployment, configure the secret using Streamlit's Secrets management.

Example:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

# ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

Recommended deployment configuration:

```text
Repository:
pranavrane29/Hackathon

Branch:
main

Main file:
app/app.py
```

The Groq API key should be configured through the deployment platform's secret-management system rather than being committed to the repository.

---

# 🎯 Key Design Decisions

## Modular Architecture

Each major responsibility is separated:

```text
Document Processing
        ↓
Retrieval
        ↓
RAG
        ↓
UI
```

This makes the project easier to debug, test, extend, and maintain.

## Multi-Document Support

The system is not restricted to a single document. Multiple files can be processed together, allowing the retrieval and RAG layers to reason over a shared document collection.

## Semantic Retrieval

Traditional keyword search can fail when a user asks a question using different terminology from the source document.

Embedding-based retrieval instead focuses on semantic similarity.

## Grounded Generation

The RAG layer provides retrieved document context to the language model before generating an answer. This is intended to keep responses tied to the available source material and reduce unsupported responses.

---

# 💡 Example Use Cases

ResearchIQ can be adapted for:

- 📑 Academic paper comparison
- 🧪 Research literature review
- 🏢 Business report analysis
- 📚 Study material querying
- 📊 Multi-report comparison
- 📝 Project documentation analysis
- 📋 Technical document exploration
- 🗂️ Multi-file knowledge bases

---

# 👥 Team

This project was developed collaboratively as a four-person team.

| Person | Team Member | GitHub |
|---|---|---|
| Person 1 | **Pritam Tadase** | `pritamDT1` |
| Person 2 | **Sarthak Sapkal** | `sapkalsarthak72` |
| Person 3 | **Pranav Rane** | `pranavrane29` |
| Person 4 | **Arpit Wankhade** | `wandkhadearpit21-pixel` |

---

# 👨‍💻 Contribution Breakdown

### 👤 Member 1 — Pritam Tadase

**Document Processing Module**

Responsible for the document ingestion and preprocessing pipeline, including:

- Multi-format document support
- PDF text extraction
- DOCX processing
- TXT processing
- CSV processing
- PPTX processing
- Text chunking
- Multi-document processing
- Document processor testing

Primary module:

```text
src/document_processor.py
```

---

### 👤 Member 2 — Sarthak Sapkal

**Semantic Retrieval Module**

Responsible for the retrieval layer, including:

- Embedding generation
- Vector representation
- FAISS-based similarity search
- Retrieval of relevant document chunks
- Retrieval testing

Primary module:

```text
src/retriever.py
```

---

### 👤 Member 3 — Pranav Rane

**RAG / Answer Generation Module**

Responsible for integrating retrieval with the language model and building the RAG answer-generation pipeline.

Responsibilities included:

- RAG pipeline design
- Context construction
- LLM integration
- Groq integration
- Grounded answer generation
- RAG testing

Primary module:

```text
src/rag.py
```

---

### 👤 Member 4 — Arpit Wankhade

**User Interface Module**

Responsible for the Streamlit application layer, including:

- Research-focused dashboard
- Multi-document upload interface
- Document workspace
- Ask / Compare / Summarize modes
- Processing indicators
- Answer presentation
- Retrieved-source presentation
- Workspace controls
- UI integration with the processing, retrieval, and RAG layers

Primary module:

```text
app/app.py
```

---

# 🔗 How the Four Contributions Connect

The project was intentionally divided into four major modules:

```text
       PERSON 1
  Document Processing
          │
          ▼
       PERSON 2
      Retrieval
          │
          ▼
       PERSON 3
         RAG
          │
          ▼
       PERSON 4
          UI
```

This separation allowed the team to work on independent components while maintaining a single end-to-end pipeline.

---

# 📈 Future Improvements

ResearchIQ can be extended with:

- Persistent vector databases
- Conversation memory
- Document-level filtering
- Citation highlighting
- More embedding models
- OCR for scanned documents
- Table-aware document extraction
- Authentication and user workspaces
- Document preview
- Advanced comparison tables
- Streaming LLM responses
- Evaluation metrics for retrieval quality
- Retrieval and answer-quality benchmarking

---

# 🏆 Project Objective

The primary objective of ResearchIQ is to demonstrate how **document intelligence, semantic search, vector databases, and Retrieval-Augmented Generation can be combined into a practical multi-document AI application**.

Rather than building a chatbot that simply generates text, the project focuses on a complete information pipeline:

```text
INGEST
  ↓
UNDERSTAND
  ↓
INDEX
  ↓
RETRIEVE
  ↓
GENERATE
  ↓
PRESENT
```

This architecture provides a foundation that can be adapted to many real-world document analysis and knowledge-retrieval applications.

---

# 📌 Final Summary

**ResearchIQ** transforms a collection of heterogeneous documents into an interactive, searchable knowledge base.

The complete system combines:

> **Multi-format Processing + Semantic Embeddings + FAISS Retrieval + RAG + Groq + Streamlit**

into a single application designed for practical document research and comparison.

---

## 👥 Built with collaboration, modular engineering, and a mildly unreasonable amount of debugging.

### Team RulerX

- **Pritam Tadase**
- **Sarthak Sapkal**
- **Pranav Rane**
- **Arpit Wankhade**
