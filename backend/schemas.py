from typing import Optional, Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class TaskCreate(BaseModel):

    title: str

    description: Optional[str] = None

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

    description: Optional[str] = None

    priority: Optional[
        Literal["low", "medium", "high"]
    ] = None

    due_date: Optional[str] = None


class TaskResponse(BaseModel):

    id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[str]
    project_id: int

    class Config:
        from_attributes = True