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

to run the frontend:

```bash
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

## Git Workflow

This project was developed using feature branches and merged into main.

## Running the App

Start the FastAPI backend and frontend locally using the commands documented above.

### 1.Backend

Open PowerShell in the project folder:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload