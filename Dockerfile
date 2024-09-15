FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=mongodb://mongodb:27017/document_retrieval
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
