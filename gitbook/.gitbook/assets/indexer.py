"""Defines a script to index first quest data into a local Elasticsearch container.

Authors:
    Henry Wicaksono (henry.wicaksono@gdplabs.id)
    Delfia Nur Anrianti Putri (delfia.n.a.putri@gdplabs.id)

References:
    NONE
"""

import asyncio
import os

import pandas as pd
from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_core.utils import LoggerManager
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from tqdm import tqdm

logger_manager = LoggerManager()
logger = logger_manager.get_logger(__name__)


def init_vector_db() -> ElasticsearchVectorDataStore:
    """Initializes the vector database using Elasticsearch and an embedding model.

    This function initializes a vector database by creating an embedding model and returning an
    ElasticsearchVectorDataStore instance. The embedding model is created using OpenAI's embedding model
    with a specified API key, and it is connected to the ElasticsearchVectorDataStore instance with the
    provided index name and Elasticsearch URL from environment variables.

    Returns:
        ElasticsearchVectorDataStore: An instance of ElasticsearchVectorDataStore.
    """
    logger.info("Initializing vector database...")
    embedding_model = OpenAIEMInvoker(
        model_name=os.getenv("EMBEDDING_MODEL"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    return ElasticsearchVectorDataStore(
        index_name=os.getenv("INDEX_NAME"),
        embedding=embedding_model,
        url=os.getenv("ELASTICSEARCH_URL"),
    )


def delete_index_if_exists(data_store: ElasticsearchVectorDataStore, index_name: str) -> None:
    """Deletes an index if it exists in the vector data store, without using the elasticsearch module directly.

    Args:
        data_store: An instance of ElasticsearchVectorDataStore, which has a .vector_store attribute.
        index_name (str): The name of the index to check and delete.
    """
    client = getattr(getattr(data_store, "vector_store", None), "client", None)
    if client is not None and hasattr(client, "indices"):
        if client.indices.exists(index=index_name):
            client.indices.delete(index=index_name)


def load_chunk_list() -> list[Chunk]:
    """Loads a list of document chunks from a CSV file.

    This function reads a CSV file specified by the environment variable `CSV_DATA_PATH` and converts each row
    into a `Chunk` object. Each `Chunk` contains an ID, content, and metadata, with an optional score field.

    Returns:
        list[Chunk]: A list of `Chunk` objects created from the CSV data.
    """
    logger.info("Loading chunk list from CSV...")
    df = pd.read_csv(os.getenv("CSV_DATA_PATH"))
    return [
        Chunk(
            id=str(row.no),
            content=row.description,
            metadata={"name": row["name"]},
            score=row.get("score", None),  # Optional field, may not exist in all rows
        )
        for _, row in df.iterrows()
    ]


async def index_data(vector_db: ElasticsearchVectorDataStore, chunk_list: list[Chunk]) -> None:
    """Indexes document chunks into the vector database.

    This function takes a list of document chunks and indexes them into the provided vector database instance.

    Args:
        vector_db (ElasticsearchVectorDataStore): The vector database instance.
        chunk_list (list[Chunk]): The list of document chunks to index.
    """
    logger.info(f"Indexing {len(chunk_list)} chunks into Elasticsearch...")
    await vector_db.add_chunks(chunk_list)
    logger.info(f"Successfully indexed {len(chunk_list)} chunks into Elasticsearch.")


def main() -> None:
    """Main function to run the indexing process.

    This function loads environment variables, initializes the vector database, deletes an existing index if it exists,
    loads a list of document chunks from a CSV file, and indexes the data into the vector database.
    It uses asynchronous execution to handle the indexing process efficiently.

    Returns:
        None
    """
    load_dotenv()
    vector_db = init_vector_db()
    delete_index_if_exists(vector_db, os.getenv("INDEX_NAME"))
    chunk_list = load_chunk_list()
    asyncio.run(index_data(vector_db, chunk_list))


if __name__ == "__main__":
    """Entry point for the script to execute the main function.

    This block ensures that the main function is called when the script is run directly.

    Returns:
        None
    """
    main()
