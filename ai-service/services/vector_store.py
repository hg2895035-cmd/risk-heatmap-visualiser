import chromadb
from sentence_transformers import SentenceTransformer
import logging
import os

logger = logging.getLogger(__name__)

class VectorStore:
    client = None
    collection = None
    embedding_model = None

    @staticmethod
    def init():
        if VectorStore.client is None:
            try:
                persist_dir = os.getenv("CHROMADB_PATH", "./chroma_data")
                VectorStore.client = chromadb.PersistentClient(path=persist_dir)
                VectorStore.collection = VectorStore.client.get_or_create_collection(
                    name="risk_documents",
                    metadata={"hnsw:space": "cosine"}
                )
                VectorStore.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                logger.error(f"Vector store init error: {e}")

    @staticmethod
    def chunk_documents(text, chunk_size=500, overlap=50):
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if len(chunk.strip()) > 10:
                chunks.append(chunk)
        return chunks

    @staticmethod
    def add_document(doc_id, text, metadata=None):
        try:
            VectorStore.init()
            chunks = VectorStore.chunk_documents(text)

            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            embeddings = VectorStore.embedding_model.encode(chunks).tolist()

            metadatas = [
                {**(metadata or {}), "chunk": i, "original_length": len(text)}
                for i in range(len(chunks))
            ]

            VectorStore.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            return True
        except Exception as e:
            logger.error(f"Add document error: {e}")
            return False

    @staticmethod
    def search(query, limit=3):
        try:
            VectorStore.init()
            query_embedding = VectorStore.embedding_model.encode([query])[0].tolist()

            results = VectorStore.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit
            )

            if results and results['documents']:
                return {
                    "documents": results['documents'][0],
                    "distances": results['distances'][0],
                    "metadatas": results['metadatas'][0]
                }
            return {"documents": [], "distances": [], "metadatas": []}
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {"documents": [], "distances": [], "metadatas": []}

def init_vector_store():
    VectorStore.init()

def add_to_vector_store(doc_id, text, metadata=None):
    return VectorStore.add_document(doc_id, text, metadata)

def search_vector_store(query, limit=3):
    return VectorStore.search(query, limit)
