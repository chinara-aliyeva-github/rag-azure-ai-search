# frontend.py
import streamlit as st
import requests
import os
API_URL = os.getenv("API_URL", "http://backend:8000")

st.title("  Q&A Retrieval-Augmented Generation (RAG) with Azure OpenAI and Azure Search")

st.header("Upload PDF File")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Uploading and Indexing ..."):
        files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/upload-data", files=files)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.json()['error']}")

query = st.text_input("Enter your question:")
top_k = st.text_input("Enter top number of retrivals:")
search_type = st.selectbox("Select search type:", ["hybrid", "vector", "keyword"])

if st.button("Get Response") and query:
    with st.spinner("Fetching response..."):
        response = requests.post(f"{API_URL}/rag-response/", json={"query": query, "top_k": int(top_k), "search_type": search_type})

        if response.status_code == 200:
            result = response.json()["response"]
            st.write("### Response:")
            st.write(result)
        else:
            st.error("Failed to fetch response. Check backend.")
