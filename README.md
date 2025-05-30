# Retrieval-Augmented Generation (RAG) System with FastAPI and Streamlit

This repository provides an advanced implementation of a Retrieval-Augmented Generation (RAG) system leveraging modern software engineering practices. The backend uses FastAPI for robust API management, and the frontend uses Streamlit for dynamic user interaction. The project includes structured PDF processing, intelligent document indexing with Azure AI, and seamless Docker-based deployment with orchestration via Docker Compose.

---

## Key Features

### 🛠 Backend

* **FastAPI-based REST API** providing efficient handling of PDF documents.
* **PDF processing** for document ingestion and chunking.
* **Azure AI Search integration** for semantic retrieval using vector embeddings.
* **Structured RAG endpoint** for intelligent question-answering with context.
* **Secure and configurable environment** using environment variables.

### 🎨 Frontend

* **Interactive Streamlit interface** enabling users to effortlessly upload PDF files.
* **Real-time question-answering interface** integrated directly with backend APIs.
* **Responsive and intuitive UI** ensuring smooth user experience.

### 🚀 Dockerized Deployment

* **Docker containers** for easy deployment and consistent environments.
* **Docker Compose orchestration** for efficient multi-container management.
* **Isolated network environments** to maintain secure communication between services.

---

## Project Structure

```
fs_bot_version_2/
├── backend/
│   ├── app.py                  # FastAPI backend application
│   ├── requirements.txt        # Backend dependencies
│   ├── Dockerfile              # Containerizes the backend
│   ├── .env                    # Backend environment configuration
│   ├── tests/
│   │   └── test_app.py         # Backend unit tests
├── frontend/
│   ├── frontend.py             # Streamlit frontend application
│   ├── requirements.txt        # Frontend dependencies
│   ├── Dockerfile              # Containerizes the frontend
├── docker-compose.yml          # Docker Compose orchestration file
└── README.md                   # Project documentation
```

---

## Prerequisites

* **Docker & Docker Compose** (recommended)
* **Python 3.11+** (if running locally without Docker)

---

## Setup & Deployment

### 🖥️ Clone the Repository

```bash
git clone <repository-url>
cd fs_bot_version_2
```

### 🐳 Docker-Based Setup

Build and launch both backend and frontend services:

```bash
docker-compose up --build
```

* **Backend available at**: [http://localhost:8000](http://localhost:8000)
* **Frontend available at**: [http://localhost:8503](http://localhost:8503)

To stop and remove containers:

```bash
docker-compose down
```

---

### 💻 Local Setup (Without Docker)

#### **Backend Setup**

Navigate and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Start FastAPI server:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

* **Swagger UI**: [http://127.0.0.1:8000/]

#### **Frontend Setup**

Navigate and install dependencies:

```bash
cd frontend
pip install -r requirements.txt
```

Run Streamlit app:

```bash
streamlit run frontend.py --server.port 8503
```

* **Frontend UI**: [http://127.0.0.1:8503](http://127.0.0.1:8503)

---

## API Endpoints

### 📁 **Upload PDF File**

* **URL**: `POST /upload-data`
* **Description**: Uploads and indexes PDF into the vector database.
* **Payload**: `multipart/form-data` with file field.

### 🔍 **Query RAG System**

* **URL**: `POST /rag-response/`
* **Description**: Performs retrieval and returns answers.
* **Payload**:

  ```json
  {
    "query": "Your question here",
    "top_k": 3,
    "search_type": "hybrid"
  }
  ```

---

## Environment Configuration

### ⚙️ Backend (`backend/.env`)

```env
OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL_NAME=text-embedding-ada-002
MODEL=your_openai_model
```

### ⚙️ Frontend

Configure backend API connection via environment:

```env
API_URL=http://backend:8000
```

---

## Docker Compose Configuration

The provided `docker-compose.yml` orchestrates the backend and frontend services seamlessly, managing networks and dependencies:

```yaml
version: "3.8"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend
    ports:
      - "8000:8000"
    environment:
      - API_URL=http://backend:8000
    networks:
      - app-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend
    ports:
      - "8503:8503"
    environment:
      - API_URL=http://backend:8000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

---

## 🧪 Testing

### **Backend**

Run backend unit tests:

```bash
pytest backend/tests
```

API functional tests via Swagger UI or Postman are recommended.

### **Frontend**

Test frontend functionality:

1. Navigate to [http://127.0.0.1:8503](http://127.0.0.1:8503)
2. Upload PDFs and validate interactions by querying the system.

---

## 🚦 Best Practices and Standards

* **Code Quality**: Adherence to clean code standards, modularization, and PEP 8.
* **CI/CD**: Docker-based deployment ensures consistent environments.
* **Testing**: Unit tests and API validation ensure system robustness.
* **Logging & Monitoring**: Clear logging within backend services enhances traceability and debugging.

---

## 📌 Contributing

We welcome contributions to improve the project. Please submit pull requests adhering to project standards and best practices.
