from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------------------------
# Project Schemas
# -------------------------

class ProjectCreate(BaseModel):
    project_name: str
    text: Optional[str] = None
    owner_id: int


class ProjectResponse(BaseModel):
    project_id: int
    project_name: str
    text: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True


# -------------------------
# Task Schemas
# -------------------------

class TaskCreate(BaseModel):

    title: str

    text: Optional[str] = None

    priority: Literal[
        "low",
        "medium",
        "high"
    ] = Field(default="medium")

    due_date: Optional[str] = None

    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskUpdate(BaseModel):

    title: Optional[str] = None

    text: Optional[str] = None

    priority: Optional[
        Literal["low", "medium", "high"]
    ] = None

    due_date: Optional[str] = None


class TaskResponse(BaseModel):

    id: int
    title: str
    text: Optional[str]
    priority: str
    due_date: Optional[str]
    project_id: int

    class Config:
        from_attributes = True


# -------------------------
# AI Quick Add
# -------------------------

class QuickAddRequest(BaseModel):
    text: str
    project_id: int

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("text cannot be blank")

        return value