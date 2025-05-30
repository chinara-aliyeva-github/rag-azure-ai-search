# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./app.py /app/app.py
COPY ./.env /app/.env
COPY ./rag.py /app/rag.py
COPY ./pdf_loader.py /app/pdf_loader.py
COPY ./utility.py /app/utility.py



EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
