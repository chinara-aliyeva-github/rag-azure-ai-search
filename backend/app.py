# app.py
from fastapi import FastAPI
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
import logging
from fastapi import FastAPI, UploadFile, File
import shutil
from rag import Query, Indexing, Retrieval

load_dotenv()

MODEL = "azure.gpt-4o"
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(openai_api_key=openai_api_key, model=MODEL, temperature=0.0, max_tokens=1000)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG-based API!"}

@app.post("/upload-data")
def upload_data(file: UploadFile= File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    #Save the uploaded file temporarily to the Temp directory
    temp_dir = "./Temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    with open(temp_file_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
    Indexing(temp_file_path).load_into_vector_db()
    os.remove(temp_file_path)
    return {"message": f"{file.filename} has been indexed and chunked in Vector DB."}


@app.post("/rag-response/")
def rag_response(query: Query):
    try:
        logging.info("Setting up RAG system...")
        response_text = Retrieval(query.query, query.top_k, query.search_type).rag()
        return {"response": response_text}
    except Exception as e:
        logging.error(f"Error in RAG response: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

