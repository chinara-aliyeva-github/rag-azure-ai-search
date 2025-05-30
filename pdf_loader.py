from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import logging

class DataProcessing:
    def __init__(self):
        pass

    def load_pdfs_from_directory(self, pdf_directory) -> list[Document]:
        logging.info(f"Loading PDFs from directory: {pdf_directory}")
        if not os.path.exists(pdf_directory):
            raise FileNotFoundError(f"Directory does not exist: {pdf_directory}")
        loader = PyPDFDirectoryLoader(pdf_directory)
        return loader.load()
    
    def load_single_pdf(self, pdf_path: str) -> list[Document]:
        logging.info(f"Loading PDF from path: {pdf_path}")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File does not exist: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        return loader.load()
    

    def create_chunks(self, file_path) -> list[Document]:
        if os.path.isfile(file_path):
            documents = self.load_single_pdf(file_path)
        elif os.path.isdir(file_path):
            documents = self.load_pdfs_from_directory(file_path)
        else:
            raise ValueError(f"Invalid file path: {file_path}. It should be a file or a directory.")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True
        )
        chunks = splitter.split_documents(documents)
        return chunks
