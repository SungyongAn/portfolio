from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.measurement import 

from app.schemas.measurement import MeasurementCreateRequest

def create_measurement(db: Session, measurement_data: MeasurementCreateRequest) -> User:

    # user_idのユーザーが存在するか確認
    existing_user = db.query(User).filter(User.id == measurement_data.user_id).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="指定されたユーザーが存在しません",
        )


def get_user_by_user_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
