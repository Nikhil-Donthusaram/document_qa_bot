import os
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(BASE_DIR, "db")

print("Using DB:", DB_PATH)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="documents"
)


def load_pdfs():

    documents = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(DATA_FOLDER, file)

            reader = PdfReader(pdf_path)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                if text and text.strip():

                    documents.append(
                        {
                            "text": text,
                            "source": file,
                            "page": page_num + 1
                        }
                    )

    return documents


def chunk_text(text, chunk_size=1000, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start = end - overlap

    return chunks


def build_index():

    if collection.count() > 0:

        print("Database already indexed.")
        print("Stored chunks:", collection.count())
        return

    docs = load_pdfs()

    all_chunks = []
    all_ids = []
    all_metadatas = []

    idx = 0

    for doc in docs:

        chunks = chunk_text(doc["text"])

        for chunk in chunks:

            all_chunks.append(chunk)

            all_ids.append(str(idx))

            all_metadatas.append(
                {
                    "source": doc["source"],
                    "page": doc["page"]
                }
            )

            idx += 1

    print("Total chunks:", len(all_chunks))

    embeddings = embedding_model.encode(
        all_chunks,
        show_progress_bar=True
    ).tolist()

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings,
        metadatas=all_metadatas
    )

    print("Indexing complete!")
    print("Stored chunks:", collection.count())


if __name__ == "__main__":
    build_index()
