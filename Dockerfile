# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./frontend.py /app/frontend.py

EXPOSE 8503

CMD ["streamlit", "run", "frontend.py", "--server.port=8503", "--server.address=0.0.0.0"]
