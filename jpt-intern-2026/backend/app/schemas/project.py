from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.project import ProjectStatus, DevelopmentMethod


# 作成
class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    budget_amount: Optional[int] = Field(None, ge=0)
    planned_months: Optional[int] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    development_method: Optional[DevelopmentMethod] = None


# 更新
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    budget_amount: Optional[int] = Field(None, ge=0)
    planned_months: Optional[int] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    development_method: Optional[DevelopmentMethod] = None


# 承認 / 却下
class ApprovalRequest(BaseModel):
    reject_reason: Optional[str] = None


# レスポンス
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    development_method: Optional[DevelopmentMethod] = None
    applicant_id: int
    department_id: int

    # 追加
    department_name: Optional[str] = None
    applicant_name: Optional[str] = None

    budget_amount: Optional[int] = None
    planned_months: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reject_reason: Optional[str] = None

    progress: int = 0
    alert_level: Optional[str] = None
    alert_reason: Optional[str] = None

    actual_amount: Optional[int] = None
    consumption_rate: Optional[int] = None

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[ProjectResponse]


class BudgetSummaryResponse(BaseModel):
    total_projects: int
    total_budget: int
    total_actual: int
    avg_consumption_rate: int
