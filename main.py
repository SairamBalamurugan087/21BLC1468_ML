import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import redis
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import time
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Initialize database connections
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/document_retrieval")
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_database()
documents_collection = db["documents"]
users_collection = db["users"]

# Initialize Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

class SearchQuery(BaseModel):
    text: str
    top_k: Optional[int] = 5
    threshold: Optional[float] = 0.5

@lru_cache(maxsize=128)
def get_user(user_id: str):
    return users_collection.find_one({"_id": user_id})

def update_user_requests(user_id: str):
    users_collection.update_one(
        {"_id": user_id},
        {"$inc": {"request_count": 1}},
        upsert=True
    )

def check_rate_limit(user_id: str):
    user = get_user(user_id)
    if user and user.get("request_count", 0) >= 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/search")
async def search(query: SearchQuery, user_id: str):
    check_rate_limit(user_id)
    update_user_requests(user_id)

    # Check cache
    cache_key = f"{query.text}:{query.top_k}:{query.threshold}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return JSONResponse(content=eval(cached_result))

    # Perform search
    query_embedding = model.encode(query.text)
    results = documents_collection.aggregate([
        {
            "$search": {
                "index": "default",
                "knnBeta": {
                    "vector": query_embedding.tolist(),
                    "path": "embedding",
                    "k": query.top_k
                }
            }
        },
        {
            "$project": {
                "content": 1,
                "score": {"$meta": "searchScore"}
            }
        },
        {
            "$match": {
                "score": {"$gte": query.threshold}
            }
        }
    ])

    search_results = list(results)
    
    # Cache results
    redis_client.setex(cache_key, 3600, str(search_results))  # Cache for 1 hour

    return JSONResponse(content=search_results)

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get("https://news.ycombinator.com") as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    for item in soup.select(".storylink")[:5]:  # Get top 5 stories
                        title = item.text
                        url = item['href']
                        content = f"{title}\n{url}"
                        embedding = model.encode(content).tolist()
                        documents_collection.insert_one({
                            "content": content,
                            "embedding": embedding
                        })
                print("Scraped and stored news articles")
            except Exception as e:
                print(f"Error scraping news: {e}")
            await asyncio.sleep(3600)  # Sleep for 1 hour

async def initial_scrape_and_insert():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://news.ycombinator.com") as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.select(".titleline > a")[:20]:  # Get top 20 stories
                title = item.text
                url = item['href']
                content = f"{title}\n{url}"
                embedding = model.encode(content).tolist()
                documents_collection.insert_one({
                    "content": content,
                    "embedding": embedding
                })
    print("Initial scraping and insertion completed")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scrape_news())
    await initial_scrape_and_insert()
    
@app.post("/manual_scrape")
async def manual_scrape():
    await initial_scrape_and_insert()
    return {"message": "Manual scrape completed"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
