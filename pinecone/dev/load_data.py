import json
import os

from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()
INDEX_NAME = os.environ["PINECONE_INDEX"]

if __name__ == "__main__":
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    index = pc.Index(INDEX_NAME)

    bbq_embeddings = json.load(open("chapter17_embeddings.json", "r"))
    docs = list(bbq_embeddings.values())
    batch_size = 50
    limit = len(docs)

    for i in range(0, limit, batch_size):
        records = []
        # The last batch may be smaller than the batch size, so we need to handle that
        if i + batch_size > limit:
            records = [
                (doc["id"], doc["embedding"], doc["metadata"]) for doc in docs[i:]
            ]
        else:
            records = [
                (doc["id"], doc["embedding"], doc["metadata"])
                for doc in docs[i: i + batch_size]
            ]

        print(f"Upserting {len(records)} records")
        index.upsert(records)

    print("Finished loading data")
