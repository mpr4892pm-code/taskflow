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

import time

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status
)

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine
from .models import User, Project, Task
from .schemas import (
    UserCreate,
    UserResponse,
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    QuickAddRequest
)
from .dependency import get_db
from .algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)
from .ai_parser import parse_quick_add


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
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


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=422,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()

@app.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=201
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = (
        db.query(User)
        .filter(User.id == project.owner_id)
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = Project(
        project_name=project.project_name,
        description=project.description,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects")
def get_projects(
    db: Session = Depends(get_db)
):
    return db.query(Project).all()

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.project_id == task.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date,
            "project_id": task.project_id
        }
        for task in tasks
    ]

    if sort == "priority":

        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        for record in records:
            record["priority_rank"] = priority_rank[
                record["priority"]
            ]

        insertion_sort(records, "priority_rank")

        for record in records:
            del record["priority_rank"]

    return records

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    data = task_data.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    index = [
        {
            "id": task.id,
            "title": task.title
        }
        for task in tasks
    ]

    if algo == "binary":

        insertion_sort(index, "title")

        position = binary_search(
            index,
            title,
            "title"
        )

    elif algo == "linear":

        position = linear_search(
            index,
            title,
            "title"
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be binary or linear"
        )

    if position == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_id = index[position]["id"]

    return get_task(task_id, db)

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.get("/projects/stats")
def project_stats(
    db: Session = Depends(get_db)
):

    rows = (
        db.query(
            Project.project_id,
            Project.project_name,
            func.count(Task.id).label("task_count")
        )
        .outerjoin(
            Task,
            Project.project_id == Task.project_id
        )
        .group_by(
            Project.project_id,
            Project.project_name
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count
        }
        for row in rows
    ]

@app.post(
    "/tasks/quick-add",
    response_model=TaskResponse,
    status_code=201
)
def quick_add(
    data: QuickAddRequest,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(
            Project.project_id == data.project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=422,
            detail="Project not found"
        )

    parsed = parse_quick_add(
        data.description
    )

    new_task = Task(
        title=parsed["title"],
        description=data.description,
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        status="pending",
        project_id=data.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task