import asyncio
import csv

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()

# Initialize vector store with embedding model
vector_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=OpenAIEMInvoker(model_name="text-embedding-3-small")
)

# Load documents from data/imaginary_animals.csv
if __name__ == "__main__":
    with open("data/imaginary_animals.csv", "r") as f:
        reader = csv.DictReader(f)
        chunks = [Chunk(content=row["description"], metadata={"name": row["name"]}) for row in reader]

    asyncio.run(vector_store.add_chunks(chunks))



