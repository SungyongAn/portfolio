from datetime import date

from pydantic import BaseModel


class MeasurementCreateRequest(BaseModel):
    user_id: int
    measurement_date: date
    sprint_50m: float
    base_running: float
    throwing_distance: float
    pitch_speed: float
    batting_speed: float
    swing_speed: float
    bench_press: float
    squat: float


class MeasurementCreateResponse(BaseModel):
    measurement_id: int
    message: str


class MeasurementItem(BaseModel):
    measurement_id: int
    user_id: int
    name: str
    grade: int | None = None
    measurement_date: date
    sprint_50m: float
    base_running: float
    throwing_distance: float
    pitch_speed: float
    batting_speed: float
    swing_speed: float
    bench_press: float
    squat: float
    status: str


class MeasurementListResponse(BaseModel):
    measurements: list[MeasurementItem]


class MeasurementSubmitResponse(BaseModel):
    measurement_id: int
    message: str


class ApproveRequest(BaseModel):
    action: str


class ApproveResponse(BaseModel):
    message: str
    status: str
