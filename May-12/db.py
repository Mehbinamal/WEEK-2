import chromadb

def create_and_query_collection(collection_name, documents, ids, query_texts, n_results=2):
    # Initialize ChromaDB client
    chromaClient = chromadb.Client()

    # Create or get collection
    collection = chromaClient.create_collection(name=collection_name)

    # Add documents to collection
    collection.add(
        documents=documents,
        ids=ids
    )

    # Query the collection
    results = collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
    
    return results

# Example usage
results = create_and_query_collection(
    collection_name="My_Collection",
    documents=[
        "This is a document",
        "it is a small document"
    ],
    ids=['id1', 'id2'],
    query_texts=["This is a query document about db"],
    n_results=2
)

print(results)
