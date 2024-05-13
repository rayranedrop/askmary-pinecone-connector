import json
import os
import uuid

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

import cohere
from dotenv import load_dotenv

load_dotenv()


def process_text(file_name: str):
    with open(file_name, "r") as f:
        knowledge = f.read()
        text_splitter = SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="interquartile")
        return text_splitter.create_documents([knowledge])


if __name__ == "__main__":
    documents = []

    file_path = "chapter17_new.txt"
    chunks = process_text(file_path)

    for chunk in chunks:
        doc = chunk.page_content

        documents.append(
            {
                "id": str(uuid.uuid4()),
                "text": doc
            }
        )

    co = cohere.Client(os.environ["PINECONE_COHERE_API_KEY"])
    embedded_docs = {}
    batch_size = 50
    limit = len(documents)

    for i in range(0, limit, batch_size):
        texts = []
        if i + batch_size > limit:
            texts = [doc["text"] for doc in documents[i:]]
        else:
            texts = [doc["text"] for doc in documents[i : i + batch_size]]

        response = co.embed(
            texts,
            model=os.environ["PINECONE_COHERE_EMBED_MODEL"],
            input_type="search_document",
        )

        for e, _ in enumerate(response.embeddings):
            embedded_docs[documents[i + e]["id"]] = {
                **documents[i + e],
                "embedding": response.embeddings[e],
                "metadata": {
                    "author": "Dr. Pepper Schwartz",
                    "title": "Chapter 17",
                    "text": documents[i + e]["text"]
                }
            }

    with open("chapter17_embeddings.json", "w") as json_file:
        json.dump(embedded_docs, json_file)
