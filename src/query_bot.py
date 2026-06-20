import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from index_documents import build_index

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection("documents")

if collection.count() == 0:
    print("No collection found. Building index...")
    build_index()
    collection = client.get_collection("documents")

model = genai.GenerativeModel("models/gemini-2.5-flash")


def ask_question(question):

    query_embedding = embedding_model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""
    sources = []

    seen = set()

    for doc, meta in zip(docs, metas):

        context += f"""
Source: {meta['source']} | Page: {meta['page']}
Content: {doc}
-----------------------
"""

        key = f"{meta['source']}|{meta['page']}"

        if key not in seen:
            sources.append(key)
            seen.add(key)

    prompt = f"""
You are a strict document QA assistant.

Answer ONLY from the context.

Always mention file and page number.

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text, sources