import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db")

print("Using DB:", DB_PATH)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path=DB_PATH
)

collection = client.get_or_create_collection(
    name="documents"
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)


def ask_question(question):

    if collection.count() == 0:
        return (
            "Database is empty. Run index_documents.py first.",
            []
        )

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=7,
        include=["documents", "metadatas", "distances"]
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # If no relevant chunks found
    if not docs or min(distances) > 1.2:
        return (
            "I am sorry, but the uploaded documents do not contain information about this question.",
            []
        )

    context = ""

    sources = []
    seen = set()

    for doc, meta in zip(docs, metas):

        context += f"""
Source: {meta['source']}
Page: {meta['page']}

Content:
{doc}

--------------------
"""

        key = f"{meta['source']}|{meta['page']}"

        if key not in seen:
            sources.append(key)
            seen.add(key)

    prompt = f"""
You are a strict document QA assistant.

Rules:

1. Answer ONLY from the provided context.
2. Do NOT use outside knowledge.
3. Do NOT make up information.
4. Mention source file and page number.
5. If answer is not found in context, reply exactly:

I am sorry, but the uploaded documents do not contain information about this question.

Context:

{context}

Question:

{question}
"""

    response = model.generate_content(prompt)

    return response.text, sources