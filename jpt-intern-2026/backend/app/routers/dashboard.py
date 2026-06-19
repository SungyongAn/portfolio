from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.services.dashboard.dashboard_service import (
    get_alert_dashboard,
    get_dashboard_summary,
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["ダッシュボード"])


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """ダッシュボードアラート取得（本部・部門管理者用）"""
    return get_alert_dashboard(db, current_user)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_summary(db, current_user)
