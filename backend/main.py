from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import time

from .database import Base, engine
from .models import Task
from .dependency import get_db
from .algorithms import insertion_sort


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow"
    }


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE"
    ],
    allow_headers=[
        "Content-Type",
        "Authorization"
    ]
)


@app.middleware("http")
async def request_logger(request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    end_time = time.perf_counter()

    processing_time = (
        end_time - start_time
    ) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{processing_time:.2f} ms"
    )

    return response


priority_rank = {
    "low": 1,
    "medium": 2,
    "high": 3
}


@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
            "priority": priority_rank[task.priority],
            "due_date": task.due_date
        }
        for task in tasks
    ]

    insertion_sort(records, "priority")

    return records