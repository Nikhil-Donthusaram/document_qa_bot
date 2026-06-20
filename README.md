# 🤖 RAG Document Question Answering Bot

## 📌 Live Demo

🚀 **Try the Application:**
https://documentappbot.streamlit.app/

---

## 📖 Project Description

The RAG (Retrieval-Augmented Generation) Document Question Answering Bot is an AI-powered application that allows users to ask questions about PDF documents and receive context-aware answers grounded in the document content.

The system uses semantic search to retrieve the most relevant document chunks from a vector database and then leverages Google's Gemini model to generate accurate responses. Each answer includes source references with file names and page numbers for transparency and traceability.

---

## ✨ Features

* Ask questions about PDF documents
* Semantic document search
* Source citations with file names and page numbers
* Gemini-powered answer generation
* Interactive Streamlit web interface
* Multi-document support
* Retrieval-Augmented Generation (RAG) architecture

---

# 🛠️ Tech Stack

| Technology              | Version | Purpose                         |
| ----------------------- | ------- | ------------------------------- |
| Python                  | 3.11+   | Programming Language            |
| Streamlit               | 1.45.1  | Frontend Web UI                 |
| ChromaDB                | Latest  | Vector Database                 |
| Sentence Transformers   | Latest  | Embedding Generation            |
| all-MiniLM-L6-v2        | Latest  | Embedding Model                 |
| Google Gemini 2.5 Flash | Latest  | Large Language Model            |
| python-dotenv           | Latest  | Environment Variable Management |
| pypdf                   | Latest  | PDF Text Extraction             |

---

# 🏗️ Architecture Overview

## RAG Pipeline

```text
PDF Documents
      │
      ▼
PDF Text Extraction
   (PyPDF)
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
(all-MiniLM-L6-v2)
      │
      ▼
Store Embeddings
   (ChromaDB)
      │
      ▼
User Question
      │
      ▼
Question Embedding
      │
      ▼
Similarity Search
      │
      ▼
Top Relevant Chunks
      │
      ▼
Gemini 2.5 Flash
      │
      ▼
Answer + Sources
```

---

# ✂️ Chunking Strategy

## Strategy Used

Fixed-size chunking with overlap.

### Configuration

```python
chunk_size = 500
overlap = 100
```

### Why This Strategy?

* Preserves context between chunks
* Improves retrieval accuracy
* Reduces information loss
* Lightweight and easy to implement
* Works well for PDF-based RAG systems

---

# 🧠 Embedding Model and Vector Database

## Embedding Model

### all-MiniLM-L6-v2

Used through:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

### Why This Model?

* Fast inference speed
* Lightweight architecture
* Strong semantic understanding
* Popular in production RAG systems
* Suitable for CPU deployment

---

## Vector Database

### ChromaDB

### Why ChromaDB?

* Open source
* Easy Python integration
* Persistent storage support
* Efficient similarity search
* Excellent choice for beginner-to-intermediate RAG projects

---

# 📂 Project Structure

```text
document_qa_bot/
│
├── data/
│   ├── python.pdf
│   ├── artificial_intelligence_tutorial.pdf
│   └── The Alchemist eBook.pdf
│
├── src/
│   ├── app.py
│   ├── query_bot.py
│   ├── index_documents.py
│   ├── ingest.py
│   └── test_gemini.py
│
├── db/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/Nikhil-Donthusaram/document_qa_bot.git
```

```bash
cd document_qa_bot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## 5. Build the Vector Database

```bash
python src/index_documents.py
```

This step:

* Reads PDFs
* Extracts text
* Chunks content
* Creates embeddings
* Stores vectors in ChromaDB

---

## 6. Run the Application

```bash
streamlit run src/app.py
```

---

## 7. Open the Browser

```text
http://localhost:8501
```

---

# 🔑 Environment Variables

| Variable       | Description           |
| -------------- | --------------------- |
| GOOGLE_API_KEY | Google Gemini API Key |

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```

⚠️ Never commit API keys to GitHub.

---

# 💡 Example Queries

### Query 1

```text
What is Artificial Intelligence?
```

Expected Theme:

* Definition of AI
* Purpose of AI
* Core concepts

---

### Query 2

```text
Who is the father of Artificial Intelligence?
```

Expected Theme:

* John McCarthy
* Contributions to AI

---

### Query 3

```text
What are the types of Artificial Intelligence?
```

Expected Theme:

* Narrow AI
* General AI
* Super AI

---

### Query 4

```text
Explain Machine Learning from the document.
```

Expected Theme:

* Machine Learning overview
* Applications
* Learning methods

---

### Query 5

```text
Summarize the first chapter.
```

Expected Theme:

* Key concepts from Chapter 1
* Main ideas and explanations

---

# ⚠️ Known Limitations

### 1. PDF Quality Dependency

The system relies on text-based PDFs. Scanned PDFs without selectable text may not work correctly.

### 2. Fixed Chunking

Information may occasionally be split across chunk boundaries.

### 3. No Conversation Memory

Questions are answered independently without remembering previous interactions.

### 4. Retrieval Limitations

Answer quality depends on retrieving the correct chunks.

### 5. Limited Context Window

Only the most relevant chunks are provided to Gemini.

### 6. No OCR Support

Image-only PDFs are not currently supported.

---

# 🚀 Future Improvements

* PDF Upload from UI
* OCR Support
* LangChain Integration
* Hybrid Search (BM25 + Vector Search)
* Chat History & Memory
* Authentication System
* Cloud Vector Database
* Advanced Citations
* Multi-user Support

---

# 👨‍💻 Author

**Nikhil Donthusaram**

GitHub:
https://github.com/Nikhil-Donthusaram

Project Repository:
https://github.com/Nikhil-Donthusaram/document_qa_bot

Live Demo:
https://documentappbot.streamlit.app/
