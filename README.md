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

## How to Deploy

### Prerequisites:
- Install **Docker** and **Docker Compose** on your machine.
- Install **MongoDB** and **Redis** (or use Docker containers for both).

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SairamBalamurugan087/21BLC1468_ML.git
   cd 21BLC1468_ML
