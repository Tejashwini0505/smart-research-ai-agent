import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

INDEX_FILE = os.path.join(DATA_DIR, "faiss.index")
DOCS_FILE = os.path.join(DATA_DIR, "docs.npy")

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = model.get_sentence_embedding_dimension()

# Load or create index
if os.path.exists(INDEX_FILE):
    index = faiss.read_index(INDEX_FILE)
    docs = list(np.load(DOCS_FILE, allow_pickle=True))
else:
    index = faiss.IndexFlatL2(dimension)
    docs = []

CHUNK_SIZE = 500


def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i+size] for i in range(0, len(text), size)]


def add_doc_to_index(text):
    global index, docs
    chunks = chunk_text(text)
    vectors = model.encode(chunks)

    index.add(np.array(vectors))
    docs.extend(chunks)

    faiss.write_index(index, INDEX_FILE)
    np.save(DOCS_FILE, np.array(docs, dtype=object))


def retrieve(query, k=3):
    global index, docs

    if len(docs) == 0:
        return []

    vector = model.encode([query])
    D, I = index.search(np.array(vector), k)

    return [docs[i] for i in I[0] if i < len(docs)]