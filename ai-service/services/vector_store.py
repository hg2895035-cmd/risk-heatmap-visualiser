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

def search_similar(text, n_results=3):
    results = collection.query(
        query_texts=[text],
        n_results=n_results
    )

    output = []

    if results["documents"]:
        for i in range(len(results["documents"][0])):
            output.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })

    return output    