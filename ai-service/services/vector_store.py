import chromadb
from chromadb.utils import embedding_functions

# Create client (local DB)
client = chromadb.Client()

# Use default embedding model
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Create collection
collection = client.get_or_create_collection(
    name="risks",
    embedding_function=embedding_function
)

def store_risk(text, result):
    """
    Store risk text + AI output in vector DB
    """

    collection.add(
        documents=[text],
        metadatas=[result],
        ids=[str(hash(text))]
    )