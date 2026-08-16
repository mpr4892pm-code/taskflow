# TaskFlow

TaskFlow is a task management application with a FastAPI backend,
SQLAlchemy database layer, and JavaScript frontend.

## Local Setup

This project uses the two-process local development setup.

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd TaskFlow

## Frontend

The TaskFlow frontend uses HTML, CSS and JavaScript and communicates
with the FastAPI backend using the Fetch API.
python -m http.server 5500

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- HTML
- CSS
- JavaScript


## Database

users
projects
tasks

## Backend

uvicorn backend.main:app --reload


## API

GET /tasks
POST /tasks
GET /tasks/{id}
PUT /tasks/{id}
DELETE /tasks/{id}

GET /tasks?sort=priority

GET /tasks/search?title=...&algo=binary

GET /tasks/search?title=...&algo=linear

GET /projects/stats

POST /tasks/quick-add