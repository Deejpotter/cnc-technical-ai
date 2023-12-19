import os
from typing import Dict
import pinecone
from IDataManager import IDataManager


class PineconeDataManager(IDataManager):
    def __init__(self, index_name):
        """
        The PineconeDataManager class handles the interaction with a Pinecone index.
        It just handles interactions with the index and not the vector embeddings or structure of the data.
        """
        self.index_name = index_name
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                self.index_name, dimension=768
            )  # Assuming 768 dimensions
        self.index = pinecone.Index(self.index_name)

    def create(self, data: Dict[str, any]):
        """
        Upsert a vector into Pinecone index.

        data: A dictionary with 'id', 'vector', and optional 'metadata'.
        """
        self.index.upsert(
            vectors=[(data["id"], data["vector"], data.get("metadata", {}))]
        )

    def get(self, id):
        """
        Fetch a vector by its ID.
        id: The unique ID of the vector.
        """
        return self.index.fetch(ids=[id])

    def update(self, id, data):
        """
        Update a vector. Pinecone handles updates via upserts.
        id: The unique ID of the vector.
        data: Updated data for the vector.
        """
        self.index.upsert(vectors=[(id, data["vector"], data.get("metadata", {}))])

    def delete(self, id):
        """
        Delete a vector by its ID.
        id: The unique ID of the vector.
        """
        self.index.delete(ids=[id])

    def find(self, query_vector, top_k=10):
        """
        Query the index with a vector to find the most similar vectors.
        query_vector: The query vector.
        top_k: Number of top similar results to return.
        """
        return self.index.query(vector=query_vector, top_k=top_k)
