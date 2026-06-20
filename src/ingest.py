from pypdf import PdfReader
import os

DATA_FOLDER = "../data"


def load_pdfs():
    documents = []

    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_FOLDER, file)

            reader = PdfReader(file_path)

            text = ""

            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()

                if page_text:
                    text += page_text

            documents.append({
                "file_name": file,
                "text": text
            })

    return documents


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


def build_chunks(documents):
    all_chunks = []

    for doc in documents:

        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):

            all_chunks.append({
                "file_name": doc["file_name"],
                "chunk_id": i,
                "text": chunk
            })

    return all_chunks


if __name__ == "__main__":

    docs = load_pdfs()

    chunks = build_chunks(docs)

    print(f"Documents loaded: {len(docs)}")
    print(f"Total chunks: {len(chunks)}")

    print("\nSample chunk:\n")
    print(chunks[0])