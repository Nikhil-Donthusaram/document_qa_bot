import os
from dotenv import load_dotenv
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(BASE_DIR, "..", "db")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(name="documents")


def load_pdfs():

    docs = []

    if not os.path.exists(DATA_FOLDER):
        print(f"Data folder not found: {DATA_FOLDER}")
        return docs

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(DATA_FOLDER, file)

            try:
                reader = PdfReader(pdf_path)

                for page_num, page in enumerate(reader.pages):

                    text = page.extract_text()

                    if text and text.strip():

                        docs.append({
                            "text": text,
                            "source": file,
                            "page": page_num + 1
                        })

            except Exception as e:
                print(f"Error reading {file}: {e}")

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

    if collection.count() > 0:
        print("Documents already indexed.")
        return

    docs = load_pdfs()

    if len(docs) == 0:
        print("No PDF documents found.")
        return

    all_chunks = []
    all_ids = []
    all_metadatas = []

    chunk_id = 0

    for doc in docs:

        chunks = chunk_text(doc["text"])

        for chunk in chunks:

            all_chunks.append(chunk)

            all_ids.append(str(chunk_id))

            all_metadatas.append({
                "source": doc["source"],
                "page": doc["page"]
            })

            chunk_id += 1

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


if __name__ == "__main__":
    build_index()