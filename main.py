from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch

# Initialize FastAPI app
app = FastAPI()

# Initialize Elasticsearch client
es = Elasticsearch(hosts=["http://localhost:9200"])

# Define the index name
INDEX_NAME = "courses"

# Pydantic model for course info
class Course(BaseModel):
    title: str
    description: str

@app.post("/course/", response_model=dict)
async def store_course(course: Course):
    """Endpoint to store a course document in Elasticsearch."""
    try:
        # Create a document for Elasticsearch
        doc = {
            "title": course.title,
            "description": course.description,
        }
        # Index the document in Elasticsearch
        response = es.index(index=INDEX_NAME, document=doc)
        return {"id": response["_id"], "result": response["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/course/{course_id}", response_model=Course)
async def get_course(course_id: str):
    """Endpoint to retrieve a course document from Elasticsearch by its ID."""
    try:
        # Retrieve the document from Elasticsearch
        response = es.get(index=INDEX_NAME, id=course_id)
        if not response["found"]:
            raise HTTPException(status_code=404, detail="Course not found")
        source = response["_source"]
        return Course(title=source["title"], description=source["description"])
    except Exception as e:
        if "NotFoundError" in str(e):
            raise HTTPException(status_code=404, detail="Course not found")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/", response_model=list)
async def search_courses(keyword: str):
    """Endpoint to search courses by keyword in title or description."""
    try:
        # Perform a search query in Elasticsearch
        query = {
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["title", "description"]
                }
            }
        }
        response = es.search(index=INDEX_NAME, body=query)
        results = [
            {
                "id": hit["_id"],
                "title": hit["_source"]["title"],
                "description": hit["_source"]["description"]
            }
            for hit in response["hits"]["hits"]
        ]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))