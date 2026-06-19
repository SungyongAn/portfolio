from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    name: str
    phase_name: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: TaskStatus = TaskStatus.TODO
    progress: int = Field(default=0, ge=0, le=100)
    start_date: Optional[date] = None
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    phase_name: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    start_date: Optional[date] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: int
    project_id: int
    name: str
    phase_name: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    assignee_name: Optional[str] = None
    status: TaskStatus
    progress: int
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
