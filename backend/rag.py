from pdf_loader import DataProcessing
import warnings
from pydantic import BaseModel
import logging
from utility import llm_call_structured, vector_store
from dotenv import load_dotenv
import os

warnings.filterwarnings("ignore", category=RuntimeWarning)

load_dotenv()

class Query(BaseModel):
    query: str
    top_k: int
    search_type: str

class Indexing:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_and_chunk_documents(self):
        logging.info("Loading and chunking documents...")
        loader = DataProcessing()
        return loader.create_chunks(self.file_path)

    def load_into_vector_db(self):
        logging.info("Loading documents into vector database...")
        docs = self.load_and_chunk_documents()
        vector_store.add_documents(documents=docs)
        logging.info("Documents successfully loaded into vector database.")

class Retrieval:
    def __init__(self, query: str, top_k: int, search_type: str):
        logging.info("Initializing Retrieval class...")
        self.query = query
        self.top_k = top_k
        self.search_type = search_type

    def retrieve_from_vector_db(self):
        logging.info("Retrieving context from vector database...")

        source_citations = []
        results_content = ""

        results = vector_store.similarity_search(
            query=self.query,
            k=self.top_k,
            search_type=self.search_type,
        )

        for result in results:
            results_content += result.page_content
            source_citations.append((result.metadata.get("source", "unknown"), result.metadata.get("page", "unknown")))

        return results_content, source_citations

    def rag(self):
        logging.info("Setting up RAG system...")

        sources, citations = self.retrieve_from_vector_db()

        system_prompt = """You are a helpful assistant and an expert in accounting and auditing annual reports."""

        prompt = f"""Fulfill this query: '{self.query}'.
                    Use only the following sources that include extracted context, tables, and tags:
                    {sources}

                    Answer with the following: Yes or no response to the existence of such inconsistency and the reasoning behind it."""

        response = llm_call_structured(system_prompt, prompt, os.getenv("MODEL"))
        llm_response = response.choices[0].message.content

        return llm_response, citations

# if __name__ == "__main__":
#     file_path = 'Data/EnronAnnualReport2000.pdf'

#     # # Load documents into vector database
#     # indexer = Indexing(file_path)
#     # indexer.load_into_vector_db()

#     # Example query
#     query = "Who is the CEO of Enron in 2000?"
#     retriever = Retrieval(query=query, top_k=3, search_type="hybrid")

#     # Get RAG response
#     response, citations = retriever.rag()
#     print("Response:", response)
#     print("Citations:", citations)
