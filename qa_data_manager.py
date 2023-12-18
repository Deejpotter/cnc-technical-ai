import os
import openai
import pymongo
from typing import Any, Dict, List
from pymongo.collection import Collection
from bson.objectid import ObjectId
from IDataManager import IDataManager


class QADataManager(IDataManager):
    """
    DataManager class handles the interaction with a MongoDB collection for storing and retrieving QA pairs.
    It also manages the creation of vector embeddings and vector search functionality.
    Implements the IDataManager interface.
    """

    def __init__(self):
        """
        Initialize the DataManager with the MongoDB URI and get a reference to the QA collection.
        """
        self.mongo_client = pymongo.MongoClient(os.environ["MONGO_URI"])
        self.qa_collection: Collection = self.mongo_client["cncTechnicalAi"]["qa"]

    def create(self, data: Dict[str, Any]) -> None:
        """
        Add a QA pair to the database. Convert the question to a vector and store it in the database to be used for vector search.
        Args:
            data (Dict[str, Any]): The data containing the question and answer.
        """
        embeddings = self.create_vector_embeddings(data["question"])
        self.qa_collection.insert_one(
            {
                "question": data["question"],
                "answer": data["answer"],
                "vector": embeddings,
            }
        )

    def get(self, id: Any) -> Dict[str, Any]:
        """
        Retrieve a QA pair from the database by its ID.
        Args:
            id (Any): The MongoDB ObjectId of the QA pair.
        Returns:
            Dict[str, Any]: The retrieved QA pair.
        """
        return self.qa_collection.find_one({"_id": ObjectId(id)})

    def find(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Perform a vector search in the MongoDB collection based on a query.
        Args:
            query (Dict[str, Any]): The query for the vector search.
        Returns:
            List[Dict[str, Any]]: The search results.
        """
        query_vector = self.create_vector_embeddings(query["question"])
        search_query = {
            "$vectorSearch": {"index": "qa_vector_index", "query": query_vector}
        }
        return list(self.qa_collection.aggregate([search_query]))

    def update(self, id: Any, data: Dict[str, Any]) -> None:
        """
        Update a QA pair in the database, including regenerating vector embeddings for the new question.
        Args:
            id (Any): The MongoDB ObjectId of the QA pair.
            data (Dict[str, Any]): The updated data containing the question and answer.
        """
        embeddings = self.create_vector_embeddings(data["question"])
        self.qa_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "question": data["question"],
                    "answer": data["answer"],
                    "vector": embeddings,
                }
            },
        )

    def delete(self, id: Any) -> None:
        """
        Delete a QA pair from the database by its ID.
        Args:
            id (Any): The MongoDB ObjectId of the QA pair to be deleted.
        """
        self.qa_collection.delete_one({"_id": ObjectId(id)})

    def create_vector_embeddings(self, text: str) -> List[float]:
        """
        Generate vector embeddings for a given text using an ML model or API.
        Args:
            text (str): The text to generate embeddings for.
        Returns:
            List[float]: The generated vector embeddings.
        """
        response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
        return response["data"][0]["embedding"]
