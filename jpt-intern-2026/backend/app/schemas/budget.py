from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.models.expense import ExpenseType


class ProjectBudgetCreate(BaseModel):
    budget_amount: int
    unit_price: Optional[int] = None
    planned_months: Optional[int] = None


class ProjectBudgetUpdate(BaseModel):
    budget_amount: Optional[int] = None
    unit_price: Optional[int] = None
    planned_months: Optional[int] = None


class ProjectBudgetResponse(BaseModel):
    id: int
    project_id: int
    budget_amount: int
    unit_price: Optional[int] = None
    planned_months: Optional[int] = None
    actual_amount: int
    consumption_rate: int = 0  # 追加
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorklogCreate(BaseModel):
    work_month: str  # 例: "2026-04"
    actual_months: Decimal


class WorklogUpdate(BaseModel):
    actual_months: Decimal


class WorklogResponse(BaseModel):
    id: int
    project_id: int
    work_month: str
    actual_months: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExpenseCreate(BaseModel):
    expense_type: ExpenseType
    amount: int
    description: Optional[str] = None
    expense_date: date


class ExpenseUpdate(BaseModel):
    expense_type: Optional[ExpenseType] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    expense_date: Optional[date] = None


class ExpenseResponse(BaseModel):
    id: int
    project_id: int
    expense_type: ExpenseType
    amount: int
    description: Optional[str] = None
    expense_date: date
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
