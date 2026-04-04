from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import require_roles
from app.services.advice_service import get_advice

router = APIRouter(prefix="/api/advice", tags=["AIアドバイス"])


@router.post("/{user_id}")
def get_advice_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["coach", "director"])),
):
    return get_advice(db, user_id)