import os
import json
import chromadb
from chromadb.utils import embedding_functions

from src.config import CHROMA_DB_PATH, COLLECTION_NAME


def get_chroma_client():
    """
    Returns a persistent ChromaDB client.
    The database is stored inside the chroma_db folder.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_collection():
    """
    Creates or returns the sports collection.
    """
    client = get_chroma_client()

    embedding_function = embedding_functions.DefaultEmbeddingFunction()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    return collection


def setup_and_populate_db(json_file="./data/sports_facts.json"):
    """
    Reads sports_facts.json and inserts all facts into ChromaDB.
    Only inserts once.
    """

    collection = get_collection()

    # Prevent duplicate insertion
    if collection.count() > 0:
        print(f"Database already contains {collection.count()} documents.")
        return collection

    if not os.path.exists(json_file):
        raise FileNotFoundError(
            f"Could not find {json_file}"
        )

    with open(json_file, "r", encoding="utf-8") as file:
        facts = json.load(file)

    documents = []
    metadatas = []
    ids = []

    for index, item in enumerate(facts):
        documents.append(item["fact"])

        metadatas.append({
            "sport": item["sport"]
        })

        ids.append(f"fact_{index}")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Successfully stored {len(documents)} facts.")

    return collection


def query_historic_facts(
    sport,
    query_text,
    n_results=2
):
    """
    Retrieves relevant historic facts for a selected sport.
    """

    collection = get_collection()

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={
            "sport": sport
        }
    )

    documents = results.get("documents", [[]])[0]

    return documents