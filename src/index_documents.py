import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

DATA_FOLDER = "../data"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="../db")

collection = client.get_or_create_collection(name="documents")


def load_pdfs():
    docs = []

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_FOLDER, file)
            reader = PdfReader(path)

            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()

                if text:
                    docs.append({
                        "text": text,
                        "source": file,
                        "page": page_num + 1
                    })

    return docs


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def build_index():
    docs = load_pdfs()

    all_chunks = []
    all_ids = []
    all_metadatas = []

    i = 0

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for chunk in chunks:
            all_chunks.append(chunk)
            all_ids.append(str(i))

            all_metadatas.append({
                "source": doc["source"],
                "page": doc["page"]
            })

            i += 1

    print(f"Total chunks: {len(all_chunks)}")

    embeddings = embedding_model.encode(all_chunks).tolist()

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas
    )

    print("Indexing complete!")


if __name__ == "__main__":
    build_index()