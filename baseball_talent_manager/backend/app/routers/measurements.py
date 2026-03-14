from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.schemas.measurement import (
    ApproveRequest,
    ApproveResponse,
    MeasurementCreateRequest,
    MeasurementCreateResponse,
    MeasurementListResponse,
    MeasurementSubmitResponse,
)
from app.services.measurement_service import (
    coach_approve,
    create_measurement,
    get_measurements,
    member_approve,
    submit_measurement,
)

router = APIRouter(prefix="/api/measurements", tags=["測定記録管理"])


@router.post("/", response_model=MeasurementCreateResponse)
def regist_measurement(
    measurement_data: MeasurementCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["manager"])),
):
    result = create_measurement(db, measurement_data)

    return result


@router.get("/", response_model=MeasurementListResponse)
def get_measurements_endpoint(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    result = get_measurements(db, current_user)

    return result


@router.post("/{measurement_id}/submit", response_model=MeasurementSubmitResponse)
def submit_measurement_endpoint(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["manager"])),
):

    result = submit_measurement(db, measurement_id, current_user)

    return result


@router.patch("/{measurement_id}/member-approve", response_model=ApproveResponse)
def member_approve_endpoint(
    measurement_id: int,
    request: ApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["member"])),
):

    result = member_approve(
        db,
        measurement_id,
        request.action,
        current_user,
    )

    return result


@router.patch("/{measurement_id}/coach-approve", response_model=ApproveResponse)
def coach_approve_endpoint(
    measurement_id: int,
    request: ApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["coach"])),
):

    result = coach_approve(db, measurement_id, request.action, current_user)

    return result
