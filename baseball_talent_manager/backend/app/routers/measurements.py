from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.models.user import User
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
    confirm_measurement,
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


@router.get("/all")
def get_all_measurements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_measurements(db, current_user, include_all=True)


@router.post("/{measurement_id}/submit", response_model=MeasurementSubmitResponse)
async def submit_measurement_endpoint(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["manager"])),
):
    return await submit_measurement(db, measurement_id, current_user)


@router.patch("/{measurement_id}/member-approve", response_model=ApproveResponse)
async def member_approve_endpoint(
    measurement_id: int,
    request: ApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["member"])),
):
    return await member_approve(
        db,
        measurement_id,
        request.action,
        current_user,
    )


@router.patch("/{measurement_id}/coach-approve", response_model=ApproveResponse)
async def coach_approve_endpoint(
    measurement_id: int,
    request: ApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["coach"])),
):
    return await coach_approve(db, measurement_id, request.action, current_user)


@router.patch("/{measurement_id}/confirm", response_model=ApproveResponse)
def confirm_measurement_endpoint(
    measurement_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["manager"])),
):
    result = confirm_measurement(db, measurement_id, current_user)
    return result
