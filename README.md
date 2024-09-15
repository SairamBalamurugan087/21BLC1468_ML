# Document Retrieval System for Chat Applications

## Project Overview

This project is part of the **Trademarkia assignment**, aimed at building a **Document Retrieval Backend** for chat applications. The system is designed to store and retrieve documents efficiently using **MongoDB** for document storage and **Redis** for caching. It also includes a background thread to scrape news articles when the server starts.

### Key Features:
1. **Document Storage in MongoDB**: Documents are manually scraped and stored with scores to facilitate efficient search and retrieval.
2. **Caching with Redis**: Implements caching for faster searches and retrieval of frequently accessed documents.
3. **Background Scraper**: A background thread scrapes news articles at server startup, storing relevant data in the database.
4. **Rate Limiting**: Limits each user to 5 API requests within a given time frame and returns HTTP 429 if the limit is exceeded.
5. **API Endpoints**:
   - `/health`: A simple health check endpoint to verify if the API is running.
   - `/search`: Search documents using parameters like text, top_k (number of results), and threshold (similarity score).
6. **Web-based Output**: Provides a webpage to search and view document scores.
7. **Dockerized Application**: The application is fully dockerized for easy deployment.

## Technologies Used
- **Python** (Backend Development)
- **MongoDB** (Document Storage)
- **Redis** (Caching)
- **Flask** (Web framework for API)
- **Docker** (Containerization)
- **Threading** (For background tasks)
- **Rate-limiting** (To control user requests)

## File Structure
- `main.py`: Backend API logic.
- `scraper.py`: Script for scraping and storing documents in MongoDB.
- `Dockerfile`: Configuration file for building the Docker image.
- `requirements.txt`: Python dependencies required for the project.

## OUTPUT:
![image](https://github.com/user-attachments/assets/d89284ba-5d6a-41b5-b05b-db701c4ace84)

Result 1
Content: "DeepMind's new AI model can predict the structure of almost every known protein
https://www.nature.com/articles/d41586-022-02083-2"
Score: 0.8234

Result 2
Content: "Google's AI Test Kitchen lets you demo its latest language model
https://techcrunch.com/2022/08/02/googles-ai-test-kitchen-lets-you-demo-its-latest-language-model/"
Score: 0.7856

Result 3
Content: "Meta's new AI can turn text prompts into videos
https://about.fb.com/news/2022/09/metas-ai-powered-text-to-video-generator/"
Score: 0.7321


## How to Deploy

### Prerequisites:
- Install **Docker** and **Docker Compose** on your machine.
- Install **MongoDB** and **Redis** (or use Docker containers for both).

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SairamBalamurugan087/21BLC1468_ML.git
   cd 21BLC1468_ML

2. **Set Up Environment**:
   - (Optional) Create a `.env` file in the root directory to configure environment variables like MongoDB and Redis connection strings. This step is only required if you're using custom connection URLs.
   
   - Example `.env` file:
     ```bash
     MONGO_URI=mongodb://localhost:27017
     REDIS_URL=redis://localhost:6379
     ```

   - Ensure you have Python dependencies installed if running locally (without Docker). To install dependencies, run:
     ```bash
     pip install -r requirements.txt
     ```

3. **Build and Run the Application with Docker**:
   - If you're using Docker, you can build and run the project using **Docker Compose**. This command will build the Flask API backend, MongoDB, and Redis in separate containers:
     ```bash
     docker-compose up --build
     ```

   - This will start the API at `http://localhost:5000`. Make sure that both MongoDB and Redis services are running. If MongoDB or Redis are running on different ports, update your `.env` file accordingly.

4. **Access the API**:
   - The application will expose the following API endpoints:
     - `/health`: To verify that the API is running.
     - `/search`: To search for documents based on input text.

5. **Verify API Health**:
   - Once the application is running, check if the API is active by visiting the `/health` endpoint:
     ```bash
     curl http://localhost:5000/health
     ```
     You should see a response similar to:
     ```json
     {
       "status": "API is active"
     }
     ```

6. **Search for Documents**:
   - Use the `/search` endpoint to query the stored documents. For example, using `curl`:
     ```bash
     curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "user123",
       "text": "sample query",
       "top_k": 5,
       "threshold": 0.8
     }'
     ```

   - Expected response:
     ```json
     {
       "documents": [
         {
           "title": "Document Title 1",
           "content": "Relevant document content...",
           "score": 0.85
         },
         {
           "title": "Document Title 2",
           "content": "Another document content...",
           "score": 0.78
         }
       ]
     }
     ```

7. **Rate Limiting**:
   - The API has built-in rate limiting, allowing each user to make a maximum of **5 requests** in a given timeframe.
   - If the rate limit is exceeded, the API will return an **HTTP 429 (Too Many Requests)** error. Example error response:
     ```json
     {
       "error": "Rate limit exceeded"
     }
     ```

8. **Monitor Logs**:
   - View real-time logs from the Docker containers to track API requests, processing times, and error handling:
     ```bash
     docker logs <container_id>
     ```

## Dockerfile

Here’s the **Dockerfile** that builds the Python Flask API:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for production
ENV FLASK_ENV=production

# Run the application
CMD ["python", "main.py"]
