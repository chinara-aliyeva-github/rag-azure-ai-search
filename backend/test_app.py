# test_app.py

import pytest
from fastapi.testclient import TestClient
from app import app  # Assuming your main file is named app.py
import os


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the RAG-based API!"}


def test_upload_data_pdf():
    with open("test_file.pdf", "wb") as f:
        f.write(b"%PDF-1.4 dummy content")  # Dummy PDF content

    with open("/Users/caliyeva001/fs_bot_version_2/fs_bot_version_2/backend/Data/EnronAnnualReport2000.pdf", "rb") as pdf:
        response = client.post("/upload-data", files={"file": ("test_file.pdf", pdf, "application/pdf")})
        assert response.status_code == 200
        assert "has been indexed and chunked in Vector DB." in response.json()["message"]

    os.remove("test_file.pdf")

def test_upload_invalid_file():
    response = client.post("/upload-data", files={"file": ("test.txt", b"dummy content", "text/plain")})
    assert response.status_code == 200  # You might want to adjust this to HTTP 400 in your app
    assert response.json() == {"error": "Only PDF files are supported."}


def test_rag_response():
    response = client.post("/rag-response/", json={
        "query": "What is Enron?",
        "top_k": 3,
        "search_type": "hybrid"
    })
    assert response.status_code == 200
    assert "response" in response.json()

if __name__ == "__main__":
    pytest.main(["-v", __file__])  # Run the tests in this file