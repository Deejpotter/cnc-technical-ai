import os
import openai
import pymongo
from typing import Any, Dict, List
from pymongo.collection import Collection
from bson.objectid import ObjectId
from IDataManager import IDataManager

vector_index_name = "vector_search_index"


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
        self.qa_collection: Collection = self.mongo_client["cnctechnicalai"]["qa"]

    def create(self, data: Dict[str, Any]) -> None:
        """
        Add a QA pair to the database with both text and vector representations.

        Args:
            data (Dict[str, Any]): The data containing the question and answer.
        """
        question_text = data["question"]
        embeddings = self.create_vector_embeddings(question_text)
        self.qa_collection.insert_one(
            {
                "question": question_text,
                "answer": data["answer"],
                "question_vector": embeddings,
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

    def find(self, query_text: str) -> List[Dict[str, Any]]:
        """
        Perform a vector search in the MongoDB collection based on a query text.
        Args:
            query_text (str): The text for the vector search.
        Returns:
            List[Dict[str, Any]]: The search results.
        """
        query_vector = self.create_vector_embeddings(query_text)
        return self.vector_search(vector_index_name, query_vector)

    def update(self, id: Any, data: str) -> None:
        """
        Update a QA pair in the database, including regenerating vector embeddings for the new question.

        Args:
            id (Any): The MongoDB ObjectId of the QA pair.
            data (Dict[str, Any]): The updated data containing the question and answer.
        """
        embeddings = self.create_vector_embeddings(data)
        self.qa_collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "question": data,
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

    def create_vector_embeddings(self, text: str) -> list:
        """
        Use the OpenAI API to generate embeddings for the given text.

        Args:
            text (str): The text to generate embeddings for.

        Returns:
            list: The generated embeddings as a list of floats.
        """
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]

    def vector_search(self, query_vector):
        """
        Perform a vector search in the MongoDB collection using the vector search index.
        Uses mongoDB's $vectorSearch aggregation pipeline stage: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/

        Args:
            query_vector (list): The vector representation of the query.

        Returns:
            List[Dict[str, Any]]: The search results.
        """
        search_query = [
            {
                "$vectorSearch": {
                    "index": vector_index_name,
                    "path": "question_vector",
                    "queryVector": query_vector,
                    "numCandidates": 150,
                    "limit": 10,
                }
            },
            {
                "$project": {
                    "question": 1,
                    "answer": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]
        return list(self.qa_collection.aggregate([search_query]))

    def create_vector_search_index(self):
        """
        Create a vector search index in the MongoDB collection.
        This method should be run separately to set up the index initially.
        """
        existing_indexes = self.qa_collection.list_indexes()
        if any(index["name"] == vector_index_name for index in existing_indexes):
            print("Index already exists.")
            return

        index_definition = {
            "name": vector_index_name,
            "type": "vectorSearch",
            "fields": [
                {
                    "type": "vector",
                    "path": "question_vector",
                    "numDimensions": 768,
                    "similarity": "cosine",
                }
            ],
        }
        index_model = pymongo.IndexModel(
            [("question_vector", pymongo.TEXT)], **index_definition
        )

        self.qa_collection.create_indexes([index_model])
        print(f"Index {vector_index_name} created.")

    def reinitialize_collection(self):
        """
        Reinitialize the qa collection by ensuring all documents are valid
        and creating the necessary vector search index.
        """
        # Validate documents
        # (Implement any document validation logic if necessary)

        # Create vector search index
        self.create_vector_search_index()
